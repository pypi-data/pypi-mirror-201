#!/usr/bin/env python3
import sys
import re
import argparse

import toml

try:
    from version import Version
except ImportError:
    from bumpline.version import Version


class Release(argparse.Namespace):
    def __init__(self, args):
        self.file = args.file
        self.release = args.release
        self.pre_release = args.alpha or args.beta or args.rc
        self.dev = args.dev
        self.no_dev = args.no_dev


def read_file(input_file):
    content = []

    with open(input_file, "r") as file:
        for line in file.readlines():
            content.append(line)

    return content


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="the config file to be changed")
    parser.add_argument("release", nargs="?",
                        help="the part of the release to be increased")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-a", "--alpha", action="store_const", const="alpha",
                       help="label the new version as an alpha pre-release")
    group.add_argument("-b", "--beta", action="store_const", const="beta",
                       help="label the new version as a beta pre-release")
    group.add_argument("-c", "--rc", action="store_const", const="rc",
                       help="label the new version as a release candidate")

    parser.add_argument("-d", "--dev", action="store_true",
                        help="label the new version as a development release")
    parser.add_argument("-D", "--no-dev", action="store_true",
                        help="remove development release label")

    args = Release(parser.parse_args())

    input_file = args.file
    content = read_file(input_file)

    get_version = lambda line: line.strip().find("version") == 0
    has_version = list(map(get_version, content))

    version_index = has_version.index(True)
    version_object = toml.loads(content[version_index])
    version = Version(version_object["version"])

    if args.release == "major":
        version.bump_major()
    elif args.release == "minor":
        version.bump_minor()
    elif args.release == "micro":
        version.bump_micro()

    if args.pre_release == "alpha":
        version.add_alpha()
    elif args.pre_release == "beta":
        version.add_beta()
    elif args.pre_release == "rc":
        version.add_rc()

    if args.dev:
        version.add_dev()
    elif args.no_dev:
        version.remove_dev()

    content[version_index] = toml.dumps({"version": str(version)})

    with open(input_file, "w") as file:
        for line in content:
            file.write(line)


if __name__ == "__main__":
    main()
