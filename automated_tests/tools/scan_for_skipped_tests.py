from glob import glob


def main():
    """
    This function is only executed on release branches and looks for all skip marks in test suites.
    :return: None
    """
    for file in glob('../*/test_*.py'):
        with open(file, 'r') as f:
            file_content = f.read()
            pattern = '@mark.skip'
            if pattern in file_content:
                print(f'[ERR] {file_content.count(pattern)} skip mark(s) found in: {file}')


if __name__ == '__main__':
    main()
