# Copyright (c) 2022 Anna <cyber@sysrq.in>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the LICENSE file for more details.

import sys

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

from linkgen import linkgen


def main():
    if len(sys.argv) > 1:
        print("Usage: linkgen-web < input.toml > output.html")
        sys.exit(1)

    config = tomllib.load(sys.stdin.buffer)
    print(linkgen(config))


if __name__ == "__main__":
    main()
