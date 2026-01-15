from functions.get_file_content import get_file_content


def test():
    trunc_msg = "truncated at 10000 characters]"

    result = get_file_content("calculator", "lorem.txt")
    print(f"Result for 'lorem.txt' is {len(result)} characters long")
    if trunc_msg in result:
        print("Contents of results were truncated")
    print("")

    result = get_file_content("calculator", "main.py")
    print("Result for 'main.py' file:")
    print(result)

    result = get_file_content("calculator", "pkg/calculator.py")
    print("Result for 'pkg/calculator.py' file:")
    print(result)

    result = get_file_content("calculator", "/bin/cat")
    print("Result for '/bin/cat' file:")
    print(result)

    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print("Result for 'pkg/does_not_exist.py' file:")
    print(result)

if __name__ == "__main__":
    test()