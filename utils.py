import sys

def assert_exit(condition, err_message=""):
    try:
        assert condition
    except AssertionError:
        print("Oops")
        sys.exit(err_message)