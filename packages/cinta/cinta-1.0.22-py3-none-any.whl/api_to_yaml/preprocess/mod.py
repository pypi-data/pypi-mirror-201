from collections import defaultdict
from copy import deepcopy
import os
import re
import sys
import oyaml as yaml
from time import sleep
from api_to_yaml.layout.mod import parse as parse_filename
from api_to_yaml.operators.mod import var_replace
from api_to_yaml.preprocess.verify import verify
from api_to_yaml.read.mod import get_arn, get_name, get_resource
from api_to_yaml.operators.mod import apply as apply_operators

# cache
REF_FILE_CACHE = {}
REF_FILE_CONTENT_CACHE = {}


def get_variables(folder, info):
    combined = deepcopy(info)
    variables = []
    while folder:
        filename = os.path.join(folder, "variables.yaml")
        if os.path.isfile(filename):
            with open(filename) as f:
                content = yaml.safe_load(f)
                variables.insert(0, content)
        folder = os.path.dirname(folder)
    for variable in variables:
        combined.update(variable)
    return combined


def resolve_path(folder, ref):
    return os.path.join(folder, ref)


def get_kind(content, info):
    kind = content.get("kind")
    # todo wafv2
    return kind


def _resolve(filename):
    filename = os.path.normpath(filename).replace(os.getcwd() + '/', '')
    info = parse_filename(filename)
    with open(filename) as f:
        content = yaml.safe_load(f)
    kind = get_kind(content, info)
    region = info["region"]
    folder = os.path.dirname(filename)
    variables = get_variables(folder, info)
    content = var_replace(content, variables)
    content = ref_file(folder, content, {}, True)
    kind, info, content = preprocess(content, info, folder)
    name = get_name(content, kind, info)

    return content, info, kind, region, name


def resolve_arn(filename, waiting):
    kind, info, content = preprocess_file(filename, False, True)
    region = info["region"]
    name = get_name(content, kind, info)
    # content, info, kind, region, name = _resolve(filename)
    arn = get_arn(content, info)
    if arn is None:
        if waiting:
            print("wait for resources: {kind}, {region}, {name}".format(
                kind=kind, region=region, name=name))
            sys.stdout.flush()
    else:
        if waiting:
            print("refed resources: {kind}, {region}, {name}".format(
                kind=kind, region=region, name=name))
            sys.stdout.flush()
    # wait till resources created ( by other prowjob )
    while waiting and arn is None:
        sleep(5)  # reduce speed
        arn = get_arn(content, info)
    return arn


def resolve_yaml_ref(yaml_file):
    with open(yaml_file) as f:
        content = yaml.safe_load(f)
        return content


def is_crd_yaml(filename):
    with open(filename) as f:
        content = yaml.safe_load(f)
        return "apiVersion" in content and "kind" in content


def resolve_field(filename, field, waiting):
    """
    Get field value from yaml file
    """
    content, info, kind, region, name = _resolve(filename)
    v = get_field_value(content, info, field)
    if v is None:
        if waiting:
            print("wait for resources: {kind}, {region}, {name}".format(
                kind=kind, region=region, name=name))
            sys.stdout.flush()
    else:
        if waiting:
            print("refed resources: {kind}, {region}, {name}".format(
                kind=kind, region=region, name=name))
            sys.stdout.flush()
    # wait till resources created ( by other prowjob )
    while waiting and v is None:
        sleep(5)  # reduce speed
        v = get_field_value(content, info, field)
    return v


def get_field_value(content, info, field: str):
    """
    Get field value from resource result
    """
    kind = get_kind(content, info)
    current = get_resource(content, kind, info)
    if current is None:
        return None
    field_levels = field.split(".")
    key = field_levels.pop(0)
    if key not in current:
        raise Exception(
            f"The {key} not in {','.join(current.keys())}, please check it.")
    result = current.get(key)
    while len(field_levels) > 0 and result != None:
        key = field_levels.pop(0)
        if key not in current:
            raise Exception(
                f"The {key} not in {','.join(current.keys())}, please check it."
            )
        result = result.get(key)
    return result


def ref_file(folder, content, ref_map, waiting):
    reg = r"\$file\((.+)\)"
    def return_rendered(arn, origin): return re.sub(reg, arn, origin)

    if type(content) == str:

        match = re.match(reg, content)
        if match:
            parms = (match.groups()[0].replace(" ", "")).split(",")
            # get file path
            file_path = parms.pop(0)
            refed_file = resolve_path(folder, file_path)

            # find ref file
            if not os.path.exists(refed_file) and ".trash" in refed_file:
                refed_file = refed_file.replace("/.trash", "")
            if not os.path.exists(refed_file):
                refed_file = resolve_path(os.path.dirname(folder), file_path)
                if not os.path.exists(refed_file):
                    raise Exception(f"File not found: {refed_file}")
            # use cache
            cache_key = f'{refed_file}:{content}'
            if cache_key in REF_FILE_CACHE:
                ref_map[refed_file] = REF_FILE_CACHE[cache_key]
                return REF_FILE_CACHE[cache_key]
            if is_crd_yaml(refed_file):
                if len(parms) == 0:
                    # resolve arn
                    # params string example $file(taskDefinition.yaml)
                    arn = resolve_arn(refed_file, waiting)
                    if arn:
                        ref_map[refed_file] = arn
                        # save cache
                        REF_FILE_CACHE[cache_key] = arn
                        return return_rendered(arn, content)
                    else:
                        ref_map[refed_file] = None
                else:
                    # resolve field
                    # params string example $file(taskDefinition.yaml, name)
                    field = parms.pop(0)
                    value = resolve_field(refed_file, field, waiting)
                    if value:
                        ref_map[refed_file] = value
                        REF_FILE_CACHE[cache_key] = value
                        return return_rendered(value, content)
                    else:
                        ref_map[refed_file] = None
            else:
                return return_rendered(resolve_yaml_ref(os.path.join(folder, file_path)), content)
        return content
    elif type(content) == dict:
        for k, v in content.items():
            content[k] = ref_file(folder, v, ref_map, waiting)
        return content
    elif type(content) == list:
        return [ref_file(folder, one, ref_map, waiting) for one in content]
    return content


def get_content(filepath):
    with open(filepath, 'r') as f:
        return f.read()


def load_yaml(filepath):
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)


def ref_yaml_content(folder, content, ref_map):
    # load yaml obj from another file into current yaml
    reg = r"^\$yaml_content\((.+)\)$"
    if type(content) == str:

        match = re.match(reg, content)
        if match:
            file_path = match.groups()[0].strip()
            referred_file = resolve_path(folder, file_path)

            # find ref file
            if not os.path.exists(referred_file) and ".trash" in referred_file:
                referred_file = referred_file.replace("/.trash", "")
            if not os.path.exists(referred_file):
                referred_file = resolve_path(
                    os.path.dirname(folder), file_path)
                if not os.path.exists(referred_file):
                    raise Exception(f"File not found: {referred_file}")
            file_content = load_yaml(referred_file)
            return file_content
        return content
    elif type(content) == dict:
        for k, v in content.items():
            content[k] = ref_yaml_content(folder, v, ref_map)
        return content
    elif type(content) == list:
        return [ref_yaml_content(folder, one, ref_map) for one in content]
    return content


def ref_file_content(folder, content, ref_map):
    reg = r"\$file_content\((.+)\)"
    def return_rendered(user_data, origin): return re.sub(
        reg, user_data, origin)

    if type(content) == str:

        match = re.match(reg, content)
        if match:
            file_path = match.groups()[0].strip()
            referred_file = resolve_path(folder, file_path)

            # find ref file
            if not os.path.exists(referred_file) and ".trash" in referred_file:
                referred_file = referred_file.replace("/.trash", "")
            if not os.path.exists(referred_file):
                referred_file = resolve_path(
                    os.path.dirname(folder), file_path)
                if not os.path.exists(referred_file):
                    raise Exception(f"File not found: {referred_file}")
            # use cache
            cache_key = f'{referred_file}:{content}'
            if cache_key in REF_FILE_CONTENT_CACHE:
                ref_map[referred_file] = REF_FILE_CONTENT_CACHE[cache_key]
                return REF_FILE_CONTENT_CACHE[cache_key]
            file_content = get_content(referred_file)
            REF_FILE_CONTENT_CACHE[cache_key] = file_content
            return return_rendered(file_content, content)
        return content
    elif type(content) == dict:
        for k, v in content.items():
            content[k] = ref_file_content(folder, v, ref_map)
        return content
    elif type(content) == list:
        return [ref_file_content(folder, one, ref_map) for one in content]
    return content


def ref_all(filename, content, ref_map, waiting):
    folder = os.path.dirname(filename)
    info = parse_filename(filename)
    variables = get_variables(folder, info)
    content = var_replace(content, variables)
    content = preprocess(content, info, folder,
                         enable_ref_file=True, wait_for_ref=waiting)
    content = ref_file(folder, content, ref_map, waiting)
    return content


def build_reverse_ref_map(folders):
    """
        return Dict
        Key: referenced file
        Value: the file which made the reference
    """
    references = defaultdict(list)
    filenames = [
        os.path.join(path, filename) for folder in folders
        for path, _, filenames in os.walk(folder) for filename in filenames
        if (filename.endswith('.yaml') or filename.endswith('.yml'))
        and os.path.join(path, filename).find("/.trash/") == -1
    ]
    for filename in filenames:
        with open(filename) as f:
            content = yaml.safe_load(f)
        ref_map = {}
        ref_all(filename, content, ref_map, False)
        for ref in ref_map.keys():
            references[ref].append(filename)
    return references


def preprocess(content, info, folder, enable_ref_file=True, wait_for_ref=False):
    kind = verify(content)
    variables = get_variables(folder, info)
    content = var_replace(content, variables)
    ref_map = {}
    if enable_ref_file:
        content = ref_file(folder, content, ref_map, wait_for_ref)
        content = ref_yaml_content(folder, content, ref_map)
        content = ref_file_content(folder, content, ref_map)
    content = apply_operators(content)
    return kind, info, content


def preprocess_file(filename, enable_ref_file=True, wait_for_ref=False):
    info = parse_filename(filename)
    folder = os.path.dirname(filename)
    with open(filename) as f:
        content = yaml.safe_load(f)
    return preprocess(content, info, folder, enable_ref_file, wait_for_ref)
