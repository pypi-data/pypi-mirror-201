import re


RELEASE_EXPRESSION = re.compile(r"\d+(\.\d+){0,2}")
PRE_RELEASE_EXPRESSION = re.compile(r"\D+\d*")
POST_RELEASE_EXPRESSION = re.compile(r"\.post\d*")


def get_epoch(version: str):
    if version.find("!") == -1:
        return "", version
    return tuple(version.split("!"))


def get_release(version: str):
    exp = RELEASE_EXPRESSION
    if not exp.match(version):
        raise ValueError("version format not recognized")
    index = exp.match(version).end()

    release = version[:index]
    rest = version[index:]

    return release, rest


def get_pre_release(version: str):
    exp = PRE_RELEASE_EXPRESSION
    if not exp.match(version):
        return "", version
    index = exp.match(version).end()

    if version.find(".post") != -1:
        index = version.find(".post")
    elif version.find(".dev") != -1:
        index = version.find(".dev")

    pre_release = version[:index]
    rest = version[index:]

    return pre_release, rest


def get_post_release(version: str):
    exp = POST_RELEASE_EXPRESSION
    if not exp.match(version):
        return "", version
    index = exp.match(version).end()

    if version.find(".dev") != -1:
        index = version.find(".dev")

    post_release = version[:index]
    rest = version[index:]

    return post_release, rest


def get_dev_release(version: str):
    index = version.find(".dev")
    if index == -1:
        return ""

    return version[index:]


def split_version_string(version: str):
    epoch, version = get_epoch(version)
    release, version = get_release(version)
    pre_release, version = get_pre_release(version)
    post_release, dev_release = get_post_release(version)
    #dev_release = get_dev_release(version)

    return epoch, release, pre_release, post_release, dev_release
