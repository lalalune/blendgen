import os
import subprocess
import sys
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "--debug", action="store_true", help="Print the command to run each subtest"
)
args = parser.parse_args()

files = os.listdir("simian/tests")
test_files = [file for file in files if file.endswith("_test.py")]

# Flag to track if any test has failed
test_failed = False

for test_file in test_files:
    print(f"Running tests in {test_file}...")
    # get the module name from the file by removing .py
    module_name = test_file[:-3]
    cmd = [sys.executable, "-m", f"simian.tests.{module_name}"]

    if args.debug:
        print(f"Command: {' '.join(cmd)}")

    # Run the test file and capture the output
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Check if there are any errors in the output
    if (
        "FAILED" in result.stderr
        or "ERROR" in result.stderr
        or "ValueError" in result.stderr
        or "Traceback" in result.stderr
    ):
        print(f"Tests in {test_file} failed!")
        print(result.stderr)
        test_failed = True
    else:
        print(f"Tests in {test_file} passed.")

# Exit with appropriate exit code based on test results
if test_failed:
    print("Some tests failed. Exiting with exit code 1.")
    sys.exit(1)
else:
    print("All tests passed. Exiting with exit code 0.")
    sys.exit(0)
