from os import environ
from sys import argv
from argparse import ArgumentParser
from requests import get, post, put


class MergeBotAPI:
    """Merge Bot API class."""

    def __init__(self):
        self.api_url = environ["GITHUB_API_URL"]
        self.headers = {"Authorization": f"Bearer {environ['GITHUB_API_TOKEN']}",
                        "Accept": "application/vnd.github+json",
                        "X-GitHub-Api-Version": "2022-11-28"}

    def create_pull_request(self, branch_name, base_branch):
        """
        Create pull request via GitHub API call.

        :return: None
        """
        response = get(f"{self.api_url}/pulls", headers=self.headers, timeout=15)
        for pull_request in response.json():
            if pull_request["head"]["ref"] == branch_name:
                print(f"Pull request for {branch_name} already exists.")
                return
        json = {"title": f"Merge {branch_name}",
                "body": f"Automatically created pull request that merges {branch_name} into {base_branch}.",
                "head": f"{environ['GITHUB_USER']}:{branch_name}",
                "base": base_branch}
        response = post(f"{self.api_url}/pulls", headers=self.headers, json=json, timeout=15)
        if response.status_code == 201:
            print("Pull request creation succeeded.")
        else:
            print(f"API call failed. {response.reason}")

    def merge_pull_request(self):
        """
        Get all active pull requests via GitHub API call.

        :return: None
        """
        response = get(f"{self.api_url}/pulls", headers=self.headers, timeout=15)
        response_json = response.json()
        if not response_json:
            print("No pull requests in the queue.")
            return
        for pull_request in response.json():
            pull_number = pull_request['number']
            response = get(f"{self.api_url}/pulls/{pull_number}/reviews", headers=self.headers, timeout=15)
            if response.json()["state"] == "APPROVED":
                merge_data = {"commit_title": f"Merge #{pull_number}",
                              "commit_message": f"#{pull_number} successfully merged by MergeBot.",
                              "merge_method": "squash"}
                merge_response = put(f"{self.api_url}/pulls/{pull_number}/merge", headers=self.headers, json=merge_data,
                                     timeout=15)
                if merge_response.status_code == 200:
                    print(f"Pull request #{pull_number} merged successfully.")


if __name__ == '__main__':
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--create", help="Create pull request. Usage: merge_bot.py --create [--branch] branch "
                                        "name\n[--base] base branch", action="store_true")
    group.add_argument("--merge", action="store_true", help="Merge branch. Usage: merge_bot.py --merge")
    if "--create" in argv:
        parser.add_argument("--branch", dest="branch_name", required=True, help="Branch name")
        parser.add_argument("--base", dest="base_branch", required=True, help="Base branch")
    args = parser.parse_args()

    merge_bot_api = MergeBotAPI()
    if args.create:
        merge_bot_api.create_pull_request(args.branch_name, args.base_branch)
    else:
        merge_bot_api.merge_pull_request()
