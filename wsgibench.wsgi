#!/usr/bin/env python3

import argparse
import random
import sys
import time

TESTS = (
    "cpubound",
    "bigresponse",
    "bigfile",
    "slow",
    "wedge",
    "segfault",
    "leakmemory",
    "largeupload",
    "slowupload",
    "slowdownload",
)


def application(environ, start_response):
    path = environ["PATH_INFO"]
    if "random" in path and random.randint(1, 100) == 1:
        path = "/wedge"

    status = "200 OK"
    output = "Didn't match any existing test: " + path

    if path.startswith("/cpubound"):
        output = "cpu bound test executed"
        for _ in range(10_000_000):
            pass
    elif path.startswith("/bigresponse"):
        output = "bigresponse test executed " + "x" * 100_000
    elif path.startswith("/bigfile"):
        output = "bigfile test executed " + "x" * 100_000
    elif path.startswith("/slow"):
        output = "slow test executed"
        time.sleep(1)
    elif path.startswith("/wedge"):
        output = "wedge executed"
        while True:
            pass
    elif path.startswith("/segfault"):
        output = "segfault executed"
    elif path.startswith("/leakmemory"):
        output = "leak memory executed"
    elif path.startswith("/largeupload"):
        output = "large upload executed"
    elif path.startswith("/slowupload"):
        output = "slow upload executed"
    elif path.startswith("/slowdownload"):
        output = "slow download executed"

    output_bytes = output.encode("utf-8")
    response_headers = [
        ("Content-Type", "text/plain; charset=utf-8"),
        ("Content-Length", str(len(output_bytes))),
    ]
    start_response(status, response_headers)
    return [output_bytes]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate benchmark URLs for WSGI server testing."
    )
    parser.add_argument("url", help="Base URL to prepend to the tests")
    parser.add_argument(
        "--random",
        action="store_true",
        help="Append /random to each test URL",
    )
    args = parser.parse_args()

    suffix = "/random" if args.random else ""
    for test in TESTS:
        print(args.url + test + suffix)
