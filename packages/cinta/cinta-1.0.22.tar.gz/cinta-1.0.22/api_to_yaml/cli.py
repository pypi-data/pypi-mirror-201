# fmt: off
from copy import deepcopy
import os

pkg_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.insert(0, pkg_dir)
import json
import oyaml as yaml
from api_to_yaml.utils.dump import dump as yaml_dump
import api_to_yaml.layout.mod as layout
from api_to_yaml.layout.mod import parse as parse_filename
from api_to_yaml.diff.mod import diff, obj_to_yaml
from api_to_yaml.operators.mod import dict_replace_mapping, remove_fields
from api_to_yaml.preprocess.mod import build_reverse_ref_map, get_variables, preprocess, preprocess_file
from api_to_yaml.read.mod import get_arn_from_resource, get_name, get_resource
from api_to_yaml.export.mod import export, export_ref
from api_to_yaml.create.mod import create
from api_to_yaml.update.mod import update
from api_to_yaml.validate.mod import validate
from api_to_yaml.delete.mod import delete
from api_to_yaml.plugins.wea_notify import release_notify_wea

# fmt: on


def create_wrap(kind, content, info):
    name = get_name(content, kind, info)
    print("not exists {}, {}, {}".format(kind, info.get('region'), name))
    print(f"creating...")
    res = create(kind, content, info)
    print("✅ created")
    return res


def update_wrap(kind, content, info, current, line):
    arn = get_arn_from_resource(current)
    name = get_name(content, kind, info)
    print("exists {}, {}, {}".format(kind, info.get('region'), name))
    print(arn)
    print("updating...")
    res = update(kind, content, info, current, line)
    print("✅ updated")
    return res


def delete_wrap(kind, content, info, current):
    arn = get_arn_from_resource(current)
    name = get_name(content, kind, info)
    print("exists {}, {}, {}".format(kind, info.get('region'), name))
    print(arn)
    print("deleting...")
    res = delete(kind, content, info, current)
    print("✅ deleted")
    return res


def diff_wrap(kind, before, info, after, line):
    name = get_name(before, kind, info)
    drop_fields = ["ETag"]
    for field in drop_fields:
        if field in before:
            del before[field]
        if field in after:
            del after[field]
    diffs = diff(after, before)
    print(line)
    if len(diffs):
        print("<details><summary>See Changes</summary>")
        print()
        print("```diff")
        sys.stdout.writelines(diffs)
        print("```")
        print("</details>")
    else:
        print("⚪ no changes: {}, {}, {}".format(kind, info.get('region'),
                                                name))
    return diffs


def validate_wrap(kind, content, info):
    name = get_name(content, kind, info)
    print("validating {}, {}, {} ...".format(
        kind, info.get("organization", info.get("region")), name))
    res = validate(kind, content, info)
    print("✅ validated")
    return res


def export_wrap(kind, current, info, line):
    name = get_name(current, kind, info)
    print("exporting {}, {}, {} ...".format(
        kind, info.get("organization", info.get("region")), name))
    current = export(kind, current, info)
    os.makedirs(os.path.dirname(line), exist_ok=True)
    with open(line, "w") as f:
        yaml_dump(current, f)
    print(f"✅ exported: {line}")
    return current


def get_relative_path(filename, line):
    return os.path.join(os.path.relpath(os.path.dirname(filename), os.path.dirname(
        os.path.dirname(line))), os.path.basename(filename))


def export_ref_recursive(all_refs, id_to_filename, kind, current, info, root_filename, write_file=True, depth=100):
    info = deepcopy(info)
    refs, root = export_ref(kind, current, info)
    if depth < 1:
        return root
    for id, v in refs.items():
        if id not in all_refs:
            kind, content, info = v
            new_root_id_to_filename = {}
            current = get_resource(content, kind, info)
            name = get_name({"metadata": current}, kind, {})
            refed_filename = info.get("refed_filename")
            if name:
                refed_filename = name
            info["name"] = refed_filename
            info["filename"] = f"{refed_filename}.yaml"
            filename = layout.format(info)
            ref_str = info.get("ref_template", "$file({})").format(
                get_relative_path(filename, root_filename))
            id_to_filename[id] = ref_str
            all_refs[id] = ref_str
            export_ref_recursive(all_refs, new_root_id_to_filename,
                                 kind, current, info, filename, write_file, depth-1)
        else:
            id_to_filename[id] = all_refs[id]
    root = dict_replace_mapping(root, id_to_filename)
    if write_file:
        os.makedirs(os.path.dirname(root_filename), exist_ok=True)
        with open(root_filename, "w") as f:
            yaml_dump(root, f)
            print(f"✅ exported: {root_filename}")
    return root


def export_ref_wrap(kind, current, info, line):
    name = get_name(current, kind, info)
    print("exporting {}, {}, {} ...".format(
        kind, info.get("organization", info.get("region")), name))

    all_refs = {}
    id_to_filename = {}
    root = export_ref_recursive(
        all_refs, id_to_filename, kind, current, info, line, True, 100)
    return root


def add_to_extra(ref_files):
    with open(".extra-files", "a") as f:
        f.writelines(ref_files)
        f.write("\n")
    return ref_files


def ref_hook(kind, refed_by):
    switch = {
        "TaskDefinition": [
            lambda args: list(
                filter(lambda one: one.endswith("service.yaml"), args)),
            add_to_extra
        ]
    }
    if kind not in switch:
        return
    steps = switch[kind]
    args = refed_by
    print(
        f"trigger file refed me: {json.dumps(refed_by, default=str, indent=4)}"
    )
    for step in steps:
        args = step(args)


def get_resource_by_file(filename):
    folder = os.path.dirname(filename)
    wait_for_ref = False
    kind, info, content = preprocess_file(filename, True, wait_for_ref)
    current = get_resource(content, kind, info)
    return current


def main(action, filename):
    if action not in ["create", "delete", "validate", "export", "export-ref", "diff"]:
        raise Exception(
            f'arg {action} not in ["create", "delete", "validate", "export", "export-ref", "diff"]'
        )
    folder = os.path.dirname(filename)
    wait_for_ref = action == "create"
    kind, info, content = preprocess_file(filename, True, wait_for_ref)
    variables = get_variables(folder, info)
    account_name = "-".join([info.get('project', ''), info.get('env', '')])
    current = get_resource(content, kind, info)
    res = None
    need_diff = True
    if action == "validate":
        res = validate_wrap(kind, content, info)
        need_diff = False
    else:
        current = get_resource(content, kind, info)
    if action == "create":
        if content.get("pipelineConfig", {}).get("no-apply"):
            print(f"this file does not allow apply.\n{filename}")
            return
        if current and current.get('status') not in [
                'INACTIVE', 'DRAINING'
        ]:  # 存在, 更新
            # reverse_ref_map = build_reverse_ref_map([folder])
            res = update_wrap(kind, content, info, current, filename)
            if ("TaskDefinition" in kind):
                release_notify_wea(info.get('name'), variables,
                                   account_name, info.get('ecs_cluster'))
            # refed_by = reverse_ref_map.get(line)
            # if refed_by:
            #     ref_hook(kind, refed_by)
        else:  # 不存在，创建
            res = create_wrap(kind, content, info)
            if ("TaskDefinition" in kind):
                release_notify_wea(info.get('name'), variables,
                                   account_name, info.get('ecs_cluster'))
    elif action == "delete":
        if current:  # 存在, 删除
            need_diff = False
            res = delete_wrap(kind, content, info, current)
        else:  # 不存在，反馈
            print("❌ not exists {}, {}, {}".format(kind, info['region'],
                                                   info['name']))
    elif action == "export":
        need_diff = False
        if current:  # 存在，导出为文件
            res = export_wrap(kind, current, info, filename)
    elif action == "export-ref":  # 导出所引用的资源为yaml
        need_diff = False
        res = export_ref_wrap(kind, current, info, filename)
    elif action == "diff":
        need_diff = False
        current_expanded = {}
        if current:
            all_refs = {}
            id_to_filename = {}
            current_crd = export_ref_recursive(
                all_refs, id_to_filename, kind, current, info, filename, False, 1)
            _, _, current_expanded = preprocess(
                current_crd, info, folder, True, wait_for_ref)
        res = diff_wrap(kind, current_expanded, info, content,  filename)
    if need_diff:
        after = get_resource(content, kind, info)
        diff_wrap(kind, current or {}, info, after, filename)

    if res and os.environ.get("DEBUG"):
        print(json.dumps(res, default=str))


emojis = {"create": "🏗️ ",
          "delete": "🗑️ ",
          "validate": "🔍",
          "export": "🖨️ ",
          "export-ref": "🖨️ ",
          "diff": "📝",
          }
if __name__ == "__main__":
    action = sys.argv[1]
    print(f"{emojis.get(action)} {action}:")
    for line in sys.stdin:
        line = line.strip()
        main(action, line)
