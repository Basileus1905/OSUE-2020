from httptest import HttpTest


def main():
    # base_url = "http://localhost"
    base_url = "http://eu.httpbin.org"
    index_url = f"{base_url}/"
    html_url = f"{base_url}/html"
    pic_url = f"{base_url}/image/png"
    port = 80
    base2_url = f"http://eu.httpbin.org:{port}"
    index2_url = f"{base2_url}/"
    html_url = f"{base2_url}/html"
    cat2_url = f"{base2_url}/image/png"

    # Initialize the testsuite
    h = HttpTest()

    # Working examples
    h.is_returncode(f"./client -p {port} {index_url}", 0) #1
    h.is_returncode(f"./client -p {port} {html_url}", 0)#2
    h.is_returncode(f"./client -p {port} {pic_url}", 0) #3
    h.is_returncode("./client http://coolsoothinginnerjoke.neverssl.com/online", 0) #4
    h.is_returncode("./client http://www.nonhttps.com/", 0) #5
    h.is_returncode(f"./client -p {port} {index_url}", 0) #6

    # Missing http scheme
    h.is_returncode(f"./client -p {port} localhost/", 1) #7

    # Missing arguments for the flags
    h.is_returncode(f"./client -p {index_url}", 1) #8
    h.is_returncode(f"./client -o {index_url}", 1) #9
    h.is_returncode(f"./client -d {index_url}", 1) #10

    # Statuscodes that are not 200 OK
    h.is_returncode(f"./client -p {port} {base_url}/does-not-exist", 3) #11
    h.does_print( #12
        f"./client -p {port} {base_url}/does-not-exist",
        "404 NOT FOUND",
    )

    # Conflicting arguments
    h.is_returncode( #13
        f"./client -p {port} -d __tmp -o __tmp/index.html {index_url}",
        1,
    )
    h.is_returncode( #14
        f"./client -p {port} -d __tmp -d __tmp/ {index_url}",
        1,
    )
    h.is_returncode( #15
        f"./client -p {port} -o __tmp/index.html -o __tmp/index.html {index_url}",
        1,
    )

    # Check if the client creates the right filenames
    h.creates_file( #16
        f"./client -p {port} -o __tmp/index.html {index_url}",
        "__tmp/index.html",
    )
    h.creates_file( #17
        f"./client -p {port} -o __tmp/dog.txt {index_url}",
        "__tmp/dog.txt",
    )
    h.creates_file( #18
        f"./client -p {port} -o __tmp/dog.txt {html_url}",
        "__tmp/dog.txt",
    )
    h.creates_file( #19
        f"./client -p {port} -d __tmp {index_url}",
        "__tmp/index.html",
    )
    h.creates_file( #20
        f"./client -p {port} -d __tmp/ {index_url}",
        "__tmp/index.html",
    )
    h.creates_file( #21
        f"./client -p {port} -d __tmp/ {html_url}",
        "__tmp/html",
    )
    h.creates_file( #22
        f"./client -p {port} -d __tmp/ {pic_url}",
        "__tmp/png",
    )


	# TEST NUMBER: 23-28
    # Compare responses
    h.compare_output( #23
        f"./client -p {port} -o __tmp/index.html {index_url}",
        "__tmp/index.html",
        index2_url,
    )
    h.compare_output( #24
        f"./client -p {port} -o __tmp/dog.txt {index_url}",
        "__tmp/dog.txt",
        index2_url,
    )
    h.compare_output( #25
        f"./client -p {port} -o __tmp/dog.txt {html_url}",
        "__tmp/dog.txt",
        html_url,
    )
    h.compare_output( #26
        f"./client -p {port} -d __tmp/ {index_url}",
        "__tmp/index.html",
        index2_url,
    )
    h.compare_output( #27
        f"./client -p {port} -d __tmp/ {html_url}",
        "__tmp/html",
        html_url,
    )
    if not h.compare_output( #28
        f"./client -p {port} -d __tmp/ {pic_url}",
        "__tmp/png",
        cat2_url,
    ):
        print(
            "NOTE: this test might fail because you didn't implement binary reading in your client which is a bonus exercise."
        )

    # Test for memoryleaks with valgrind
    h.does_leak(f"./client -p {port} {index_url}")
    h.does_leak(f"./client -p {port} {html_url}")
    h.does_leak(f"./client -p {port} {pic_url}")
    h.does_leak(
        "./client http://neverssl.com",
    )
    h.does_leak("./client http://www.nonhttps.com/")
    h.does_leak(f"./client -p {port} {index_url}")
    h.does_leak(f"./client -p {port} localhost/")
    h.does_leak(f"./client -p {index_url}")
    h.does_leak(f"./client -o {index_url}")
    h.does_leak(f"./client -d {index_url}")
    h.does_leak(f"./client -p {port} {base_url}/does-not-exist")
    h.does_leak(f"./client -p {port} -o __tmp/index.html {index_url}")
    h.does_leak(f"./client -p {port} -o __tmp/dog.txt {index_url}")
    h.does_leak(f"./client -p {port} -o __tmp/dog.txt {html_url}")
    h.does_leak(f"./client -p {port} -d __tmp {index_url}")
    h.does_leak(f"./client -p {port} -d __tmp/ {html_url}")
    h.does_leak(f"./client -p {port} -d __tmp/ {pic_url}")

    # Print the statistics at the end
    h.print_result()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(
            """
                      ___  _   _   ___  _  __
                     | __|| | | | / __|| |/ /
                     | _| | |_| || (__ |   < 
                     |_|   \___/  \___||_|\_\\

                    ���� The Testsuite crashed! ����

Okay, this shouldn't have happend and is my (the testsuite dev) fault.
However, there is probably some error in your code that triggered the crash.

Here is what you do:
1) Read the Python Traceback below and double check your code for bugs.
2) Write a Issue on GitHub (include the Traceback):
   https://github.com/flofriday/OSUE-2020/issues/new



--- TRACEBACK BELOW ---
        """
        )
        raise e
