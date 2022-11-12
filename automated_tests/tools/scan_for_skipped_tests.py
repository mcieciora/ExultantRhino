from glob import glob


def main():
    """
    This function is only executed on release branches and looks for all skip marks in test suites.
    :return: None
    """
    for python_file in glob('../*/test_*.py'):
        with open(python_file, 'r', encoding='utf-8') as file:
            file_content = file.read()
            pattern = '@mark.skip'
            if pattern in file_content:
                print(f'[ERR] {file_content.count(pattern)} skip mark(s) found in: {python_file}')


if __name__ == '__main__':
    main()
