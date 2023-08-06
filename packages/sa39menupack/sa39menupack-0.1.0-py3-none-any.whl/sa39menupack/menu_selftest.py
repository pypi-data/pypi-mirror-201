import subprocess
import sys
from io import StringIO


def menu(**kwargs):
    while True:
        print(f"Available options: {' / '.join(sorted(kwargs))}")
        user_input = input("Please make a selection: ")
        if user_input in kwargs:
            return kwargs[user_input]()
        print("Command not found, please try again.")


def test_good_input(monkeypatch):
    monkeypatch.setattr(sys, "stdin", StringIO("a\n"))

    def a():
        return "called a"

    returned_value = menu(a=a)

    assert "called a" in returned_value


def test_bad_then_good_input(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", StringIO("q\na\n"))

    def a():
        return "called a"

    returned_value = menu(a=a)
    captured_stdout, captured_stderr = capsys.readouterr()

    assert "Command not found, please try again." in captured_stdout
    assert "called a" in returned_value
    # assert not captured_stderr


if __name__ == "__main__":
    program_name = sys.argv[0]

    subprocess.run(f"pytest -vv {program_name}", shell=True)
