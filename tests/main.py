import glob
import unittest
from termcolor import colored

def run_tests():
    test_suite = unittest.TestSuite()
    test_file_strings = glob.glob('tests/test_*.py', recursive=True)

    module_strings = [file.replace('.py', '').replace('\\', '.') for file in test_file_strings]

    [__import__(module) for module in module_strings]

    suites = [unittest.TestLoader().loadTestsFromName(module) for module in module_strings]
    [test_suite.addTest(suite) for suite in suites]

    result = unittest.TestResult()
    test_suite.run(result)
    return result

def print_title(color, message):
    line = "=" * 40
    print(f"\n{colored(f'{line + message + line}', color)}\n")

def print_results(results):
    color = 'green' if results.wasSuccessful() else 'red'

    print_title(color, "Test Results")
    print(f"Tests run: {results.testsRun}")
    print(f"Tests passed: {results.testsRun - len(results.errors) - len(results.failures)}")
    print(f"Was successful: {results.wasSuccessful()}")

    if results.errors:
        print_title('red', "Errors")
        for error in results.errors:
            print(f"Error in {error[0]}: {error[1]}")
    if results.failures:
        print_title('red', "Failures")
        for failure in results.failures:
            print(f"Failure in {failure[0]}: {failure[1]}")

if __name__ == "__main__":
    res = run_tests()
    print_results(res)
