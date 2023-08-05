import os
import sys
from .testing.runner import runner
from .utils.error_msg import ErrorMsg
from .global_variables.global_variables import GlobalVariables

if __name__ == "__main__":
    # Initialise test suite and test result paths as None
    test_suite_path = env_path = test_result_path = test_tags = None
    # Update the values from user command
    for key, value in zip(sys.argv[1::2], sys.argv[2::2]):
        if key == '-t':
            test_suite_path = value
        elif key == '-e':
            env_path = value
        elif key == '-r':
            test_result_path = value
        elif key == '-h':
            test_tags = value
    # Validate test suite path
    if not test_suite_path or not os.path.exists(test_suite_path):
        sys.exit(ErrorMsg.INVALID_TEST_SUITE_PATH)
    # Env path is optional
    if env_path:
        # Raise error if th env path is invalid
        if not os.path.exists(test_suite_path):
            sys.exit(ErrorMsg.INVALID_ENV_PATH)
        # Add env data to global variables as constants
        GlobalVariables._set_env_variables(path=env_path)
    # test result path is optional and by default its test suite path
    if not test_result_path:
        test_result_path = test_suite_path
    # test tags is optional and by default it's an empty list
    test_tags = test_tags.split("#") if test_tags and test_tags.startswith('#') else []
    # Remove empty tags
    test_tags = [test_tag for test_tag in test_tags if test_tag]
    # Run the test suite
    runner.run(test_suite_path=test_suite_path, test_result_path=test_result_path, test_tags=test_tags)
