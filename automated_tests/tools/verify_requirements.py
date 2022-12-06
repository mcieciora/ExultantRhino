from glob import glob
from re import findall


def main():
    """
    This function collects all of Python test suites and parses test cases inside to find corresponding requirements
    declared in the description of the test. More over it verifies if number of requirements is the same as number of
    assert checks.
    :return: dict of test cases names (key) and requirements list (value)
    """
    test_case_requirements_map = {}
    for python_file in glob('../test_*.py'):
        with open(python_file, 'r', encoding='utf-8') as file:
            for test_case_content in file.read().split('@mark'):
                requirements = findall(r'(?<=Verifies: ).*', test_case_content)
                test_suite = findall(r'test__\w+', test_case_content)
                asserts = findall(r'assert|with raises', test_case_content)
                if len(requirements) != len(asserts):
                    print(f'[ERR] {test_suite[0]}: Number of requirements should be equal to number of asserts in test '
                          f'case!')
                if requirements and test_suite:
                    test_case_requirements_map[test_suite[0]] = requirements
    return test_case_requirements_map


if __name__ == '__main__':
    main()
