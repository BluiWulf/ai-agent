from functions.run_python_file import run_python_file

def test():
    result = run_python_file("calculator", "main.py")
    print("Result for 'main.py' run:")
    print(result)

    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print("Result for 'main.py' plus args run:")
    print(result)

    result = run_python_file("calculator", "tests.py")
    print("Result for 'tests.py' run:")
    print(result)

    result = run_python_file("calculator", "../main.py")
    print("Result for '../main.py' run:")
    print(result)

    result = run_python_file("calculator", "nonexistent.py")
    print("Result for 'nonexistent.py' run:")
    print(result)

    result = run_python_file("calculator", "lorem.txt")
    print("Result for 'lorem.txt' run:")
    print(result)

if __name__ == "__main__":
    test()