import subprocess
import os
import shutil
import urllib.request


class HttpTest:
    def __init__(self):
        self._tests = 0
        self._tests_failed = 0
        self._create_dir()
        print("OSUE Exercise 3 Testsuite")
        print(
            "GitHub: https://github.com/flofriday/OSUE-2020/tree/main/http-testsuite\n"
        )

    # Increase the internal testcounter and print a simple message to stdout
    def test_passed(self):
        self._tests += 1
        print(f"✅ Test {self._tests} Passed")

    # Increate the interal testscounter and failed tests counter and print a
    # simple message to stdout
    def test_failed(self):
        self._tests += 1
        self._tests_failed += 1
        print(f"🚨 Test {self._tests} Failed")

    # Create a directory called __tmp to be used save output files the client
    # creates.
    def _create_dir(self):
        # Create a directory to output files
        if os.path.exists("__tmp"):
            shutil.rmtree("__tmp")
        os.makedirs("__tmp")

    # This testcase expects the program to exit with an provided exit code.
    # It is considered failing if the exitcodes are different or if the
    # process does not exit after 0.5 seconds.
    def is_returncode(self, command: str, code: int) -> bool:
        try:
            cp = subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=0.5,
                shell=True,
            )
        except subprocess.TimeoutExpired as e:
            self.test_failed()
            print(
                f'"{command}" ran for more than 0.5s, but was expected to return {code}'
            )
            return False

        if not cp.returncode == code:
            self.test_failed()
            print(
                f'"{command}" returned with {cp.returncode} instead of {code}'
            )
            return False

        self.test_passed()
        return True

    # This test expects the command to run for 0.5 seconds, if the commands
    # exits earlier for what ever reason this test will fail.
    def does_timeout(self, command: str) -> bool:
        try:
            cp = subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=0.5,
                shell=True,
            )
        except subprocess.TimeoutExpired as e:
            self.test_passed()
            return True

        self.test_failed()
        print(
            f'"{command}" should run forever but did exit with {cp.returncode}.'
        )
        return False

    # This test runs the command and checks afterwards if the file at path got
    # created. However, this test does not check if the file has any content
    # whatsoever. Also this test will fail if the command does not return with
    # exit code 0.
    def creates_file(self, command: str, path: str) -> bool:
        self._create_dir()
        try:
            cp = subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=0.5,
                shell=True,
            )
        except subprocess.TimeoutExpired as e:
            self.test_failed()
            print(
                f'"{command}" ran for more than 0.5s, but was expected to execute faster.'
            )
            return False

        if cp.returncode != 0:
            self.test_failed()
            print(f'"{command}" returned with {cp.returncode} instead of 0')
            return False

        if not os.path.exists(path):
            self.test_failed()
            print(f'"{command}" did not create file "{path}"')
            return False

        print(f"✅ Test {self.tests} Passed")
        return True

    # Run the command and afterwards compare the file saved in path with what
    # python receives in the response when requesting the url.
    # This test will also fail if the command runs for more than 0.5 seconds or
    # the command does not return with exit-code 0 or the file path points to
    # does not exist.
    def compare_output(self, command: str, path: str, url: str) -> bool:
        self._create_dir()
        try:
            cp = subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=0.5,
                shell=True,
            )
        except subprocess.TimeoutExpired as e:
            self.test_failed()
            print(
                f'"{command}" ran for more than 0.5s, but was expected to execute faster.'
            )
            return False

        if cp.returncode != 0:
            self.test_failed()
            print(f'"{command}" returned with {cp.returncode} instead of 0')
            return False

        if not os.path.exists(path):
            self.test_failed()
            print(f'"{command}" did not create file "{path}"')
            return False

        body = urllib.request.urlopen(url).read()
        file = open(path, "rb")
        output = file.read()
        if body != output:
            self.test_failed()
            print(f'"{command}" did not create the same output as python.')
            return False

        self.test_passed()
        return True

    # This test creates a request to url. Then it will look if there is a
    # filed in the response headers with the name and value provided to this
    # test.
    def response_header_contains(
        self, url: str, name: str, value: str
    ) -> bool:
        headers = urllib.request.urlopen(url).headers
        if name not in headers or value not in headers[name]:
            self.test_failed()
            print(
                f'Response to "{url}" did not contain "{name}: {value}" in the headers.'
            )
            if name in headers:
                print(f'Closest Header was: "{name}: {headers[name]}"')
            return False

        self.test_passed()
        return True

    # This test creates a request to url and then compares the response body to
    # the content of the file pointed to by path.
    def compare_response_body(self, url: str, path: str) -> bool:
        body = urllib.request.urlopen(url).read()
        content = open(path, "rb").read()
        if not body == content:
            self.test_failed()
            print(
                f'"Response to {url}" was not the same content as in "{path}"'
            )
            print(
                "NOTE: This might be because you haven't yet implemented the bonus task, binary files."
            )
            return False

        self.test_passed()
        return True

    # This test creates a request to url (optiona with the method provided) and
    # checks if the statuscode provided is equal to the status code of the
    # response. This test will fail if they are not equal.
    def is_statuscode(
        self, url: str, status: int, method: str = "GET"
    ) -> bool:
        req = urllib.request.Request(url, method=method)
        try:
            code = urllib.request.urlopen(req).status
        except urllib.error.URLError as e:
            code = e.code
        if status != code:
            self.test_failed()
            print(
                f'"Response to {url}" returned with status {code} instead of {status}'
            )
            return False

        self.test_passed()
        return True

    # Check if the command prints a certain phrase to either stdout or stderr
    def does_print(self, command: str, output: str) -> bool:
        try:
            cp = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=0.5,
            )
        except subprocess.TimeoutExpired as e:
            self.test_failed()
            print(
                f'"{command}" ran for more than 0.5s, but was expected to execute faster.'
            )
            return False

        if not output in cp.stdout.decode():
            self.test_failed()
            print(f'"{command}" did not print "{output}".')
            return False

        self.test_passed()
        return True

    # Print a very simple statistics to stdout
    def print_result(self):
        self._create_dir()
        print(f"{20*'-'} Statistics {20*'-'}")
        if self._tests_failed == 0:
            print(f"🎉 All {self._tests} tests passed 🎉")
        else:
            print(
                f"⚠️  {self._tests_failed} out of {self._tests} tests failed. ⚠️"
            )
