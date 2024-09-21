from os import environ
from sys import argv
from argparse import ArgumentParser
from requests import get, post, put


class MergeBotAPI:
    def __init__(self):
        self.api_url = environ["GITHUB_API_URL"]

    def get_branch_pull_number(self, branch_name):
        """
        Check if branch has related pull request.

        :return: Pull request number if exists else False
        """
        get_pull_requests = get(f"{self.api_url}/pulls")
        for pull_request in get_pull_requests.json():
            if pull_request["head"]["ref"] == branch_name:
                return pull_request["number"]
        return False

    def create_pull_request(self, branch_name, base_branch):
        """
        Create pull request via Github API call.

        :return: None
        """
        if not self.get_branch_pull_number(branch_name):
            headers = {"Authorization": f"Bearer {environ['GITHUB_API_TOKEN']}",
                       "Accept": "application/vnd.github+json",
                       "X-GitHub-Api-Version": "2022-11-28"}
            json = {"title": f"Merge {branch_name}",
                    "body": f"Automatically created pull request that merges {branch_name} into {base_branch}.",
                    "head": f"{environ['GITHUB_USER']}:{branch_name}",
                    "base": base_branch}
            post_response = post(f"{self.api_url}/pulls", headers=headers, json=json)
            if post_response.status_code == 201:
                print("Pull request creation succeeded.")
            else:
                print(f"API call failed. {post_response.reason}")

    def _delete_branch(self, branch_name):
        """
        Delete branch via Github API call.

        :return: None
        """
        pass

    def merge_branch(self, branch_name):
        """
        Merge pull request via Github API call.

        :return: None
        """
        pull_number = self.get_branch_pull_number(branch_name)
        if pull_number:
            headers = {"Authorization": f"Bearer {environ['GITHUB_API_TOKEN']}",
                       "Accept": "application/vnd.github+json",
                       "X-GitHub-Api-Version": "2022-11-28"}
            merge_data = {"commit_title": f"Merge #{pull_number}",
                          "commit_message": f"{branch_name} successfully merged by MergeBot.",
                          "merge_method": "squash"}
            merge_response = put(f"{self.api_url}/pulls/{pull_number}/merge", headers=headers, json=merge_data)
            if merge_response.status_code == 200:
                self._delete_branch(branch_name)
                print("Branch merged successfully.")
            else:
                print(f"API call failed. {merge_response.reason}")


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--create", help="Create pull request. Usage: merge_bot.py --create [--branch] branch "
                                         "name\n[--base] base branch", action="store_true")
    parser.add_argument("--merge", help="Merge branch. Usage: merge_bot.py --merge <branch_name>")
    if "--create" in argv:
        parser.add_argument("--branch", dest="branch_name", required=True, help="Branch name")
        parser.add_argument("--base", dest="base_branch", required=True, help="Base branch")
    args = parser.parse_args()

    merge_bot_api = MergeBotAPI()
    merge_bot_api.create_pull_request(args.branch_name, args.base_branch) if args.create else \
        merge_bot_api.merge_branch(args.merge)
