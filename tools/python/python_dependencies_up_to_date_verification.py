from sys import executable, exit  # pylint: disable=redefined-builtin
from glob import glob
import subprocess
from json import loads


def check_for_outdated_packages():
    """
    Verify if defined packages may be upgraded.

    Script compares list of outdated Python dependencies in current environment and the ones declared in all
    found requirements.txt files. It raises information about possibility to update specific packages, but does not
    require it.

    :return: None
    """
    dependencies_list = []
    non_zero_status_exit = False
    for req_file in glob("./requirements/**/requirements.txt"):
        with open(req_file, mode="r", encoding="utf-8") as req:
            format_dependency_list = [r.split("=")[0] for r in req.readlines()]
            dependencies_list.extend(format_dependency_list)
    outdated_dependencies = subprocess.check_output(
        [executable, "-m", "pip", "list", "-o", "--format", "json"]
    )
    for listed_req in loads(outdated_dependencies):
        if listed_req["name"] in dependencies_list:
            print(
                f"{listed_req['name']} is outdated. Consider upgrading from {listed_req['version']} to "
                f"{listed_req['latest_version']}"
            )
    if non_zero_status_exit:
        exit(1)


if __name__ == "__main__":
    check_for_outdated_packages()
