from github import Github


class GHE:
    def __init__(self, base_url, login_or_token):
        self.github = Github(base_url=base_url, login_or_token=login_or_token)

    def get_repo(self, org_name, repo_name):
        repo = self.github.get_organization(org_name).get_repo(repo_name)
        cols = list(repo.get_collaborators())
        permissions = {
            col.login: get_collaborator_permission(col)
            for col in cols if col.suspended_at is None
        }
        return {
            "apiVersion": "repo.ghe.binance/v1alpha1",
            "metadata": {
                "Organization": org_name,
                "RepoName": repo_name
            },
            "kind": "Repo",
            "spec": {
                "collaborators": permissions
            }
        }


def get_collaborator_permission(col):
    if col.permissions.admin:
        return "admin"
    if col.permissions.maintain:
        return "maintain"
    if col.permissions.push:
        return "push"
    if col.permissions.triage:
        return "triage"
    if col.permissions.pull:
        return "pull"
    raise "Uknown permission {col.permissions}"
