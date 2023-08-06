import re


class Version:
    _release_expression = re.compile(r"\d+(\.\d+){0,2}")
    _pre_release_expression = re.compile(r"\D+")
    _levels = {"a": 1, "b": 2, "c": 3, "alpha": 1, "beta": 2, "rc": 3, "": 4}

    def __init__(self, version: str):
        exp = self._release_expression
        index = exp.match(version).end()

        release = version[:index]
        pre_release = version[index:]

        self._release_size = 3
        major, minor, micro, *_ = *release.split("."), None, None

        if micro is None:
            micro = "0"
            self._release_size -= 1

        if minor is None:
            minor = "0"
            self._release_size -= 1

        exp = self._pre_release_expression
        if exp.match(pre_release):
            index = exp.match(pre_release).end()

            pre_letter = pre_release[:index]
            pre_number = pre_release[index:]
        else:
            pre_letter = ""
            pre_number = ""

        self.major = int(major)
        self.minor = int(minor)
        self.micro = int(micro)
        self._pre_letter = pre_letter
        self._pre_number = int(pre_number) if pre_number != "" else 0

    def __repr__(self):
        return self.string

    def __str__(self):
        return self.string

    def __eq__(self, other):
        if self.major != other.major:
            return False
        if self.minor != other.minor:
            return False
        if self.micro != other.micro:
            return False
        if not self.pre_release_is_equal(other):
            return False

        return True

    def __lt__(self, other):
        if self.major != other.major:
            return self.major < other.major
        if self.minor != other.minor:
            return self.minor < other.minor
        if self.micro != other.micro:
            return self.micro < other.micro
        if not self.pre_release_is_equal(other):
            return self.pre_release_is_lower(other)

        return False

    def __le__(self, other):
        if self.major != other.major:
            return self.major < other.major
        if self.minor != other.minor:
            return self.minor < other.minor
        if self.micro != other.micro:
            return self.micro < other.micro
        if not self.pre_release_is_equal(other):
            return self.pre_release_is_lower(other)

        return True

    def __gt__(self, other):
        if self.major != other.major:
            return self.major > other.major
        if self.minor != other.minor:
            return self.minor > other.minor
        if self.micro != other.micro:
            return self.micro > other.micro
        if not self.pre_release_is_equal(other):
            return self.pre_release_is_greater(other)

        return False

    def __ge__(self, other):
        if self.major != other.major:
            return self.major > other.major
        if self.minor != other.minor:
            return self.minor > other.minor
        if self.micro != other.micro:
            return self.micro > other.micro
        if not self.pre_release_is_equal(other):
            return self.pre_release_is_greater(other)

        return True

    def split_pre_release(self):
        if self.pre_release == "":
            return "", 0

        exp = self._pre_release_expression
        if exp.match(self.pre_release):
            index = exp.match(self.pre_release).end()

            pre_letter = self.pre_release[:index]
            pre_number = self.pre_release[index:]
            pre_number = int(pre_number) if pre_number != "" else 0
        else:
            pre_letter = ""
            pre_number = 0

        return pre_letter, pre_number

    def pre_release_is_greater(self, other):
        this = self.split_pre_release()
        that = other.split_pre_release()
        levels = self._levels

        if levels[this[0]] != levels[that[0]]:
            return levels[this[0]] > levels[that[0]]
        if this[1] != that[1]:
            return this[1] > that[1]

        return False

    def pre_release_is_lower(self, other):
        this = self.split_pre_release()
        that = other.split_pre_release()
        levels = self._levels

        if levels[this[0]] != levels[that[0]]:
            return levels[this[0]] < levels[that[0]]
        if this[1] != that[1]:
            return this[1] < that[1]

        return False

    def pre_release_is_equal(self, other):
        this = self.split_pre_release()
        that = other.split_pre_release()
        levels = self._levels

        if levels[this[0]] != levels[that[0]]:
            return False
        if this[1] != that[1]:
            return False

        return True

    def bump_major(self):
        self.major += 1
        self.minor = 0
        self.micro = 0
        del self.pre_release

    def bump_minor(self):
        self._release_size = max(self._release_size, 2)
        self.minor += 1
        self.micro = 0
        del self.pre_release

    def bump_micro(self):
        self._release_size = max(self._release_size, 3)
        self.micro += 1
        del self.pre_release

    def add_alpha(self):
        pre_letter, pre_number = self.split_pre_release()
        if pre_letter in ["a", "alpha"]:
            pre_number += 1
        else:
            pre_letter = "a"
            pre_number = 0

        self._pre_letter = pre_letter
        self._pre_number = pre_number

    def add_beta(self):
        pre_letter, pre_number = self.split_pre_release()
        if pre_letter in ["b", "beta"]:
            pre_number += 1
        else:
            pre_letter = "b"
            pre_number = 0

        self._pre_letter = pre_letter
        self._pre_number = pre_number

    def add_rc(self):
        pre_letter, pre_number = self.split_pre_release()
        if pre_letter in ["c", "rc"]:
            pre_number += 1
        else:
            pre_letter = "rc"
            pre_number = 0

        self._pre_letter = pre_letter
        self._pre_number = pre_number

    def add_dev(self):
        if self.string.find(".dev") == -1:
            self.string += ".dev"
        else:
            index = self.string.find(".dev") + 4
            version = self.string[:index]
            dev_number_str = self.string[index:]
            dev_number = int(dev_number_str) if dev_number_str != "" else 0
            dev_number += 1

            self.string = f"{version}{dev_number}"

    def remove_dev(self):
        if self.string.find(".dev") != -1:
            self.string = self.string.replace(".dev", "")

    @property
    def release(self):
        "return version release as a string"
        release_list = [self.major]
        if self.minor != 0 or self._release_size >= 2:
            release_list.append(self.minor)
        if self.micro != 0 or self._release_size == 3:
            release_list.append(self.micro)

        return ".".join(list(map(str, release_list)))

    @property
    def pre_release(self):
        "return version pre-release label"
        pre_letter = self._pre_letter
        pre_number = str(self._pre_number) if self._pre_number != 0 else ""

        return f"{pre_letter}{pre_number}"

    @pre_release.setter
    def pre_release(self, value):
        exp = self._pre_release_expression

        if exp.match(value):
            index = exp.match(value).end()

            pre_letter = value[:index]
            pre_number = value[index:]
        else:
            pre_letter = ""
            pre_number = ""

        self._pre_letter = pre_letter
        self._pre_number = int(pre_number) if pre_number != "" else 0

    @pre_release.deleter
    def pre_release(self):
        self._pre_letter = ""
        self._pre_number = 0

    @property
    def tuple(self):
        "return version in tuple format"
        return self.major, self.minor, self.micro, self.pre_release

    @tuple.setter
    def tuple(self, value):
        major, minor, micro, pre_release = list(value)

        if value[1] is None and value[2] is None:
            self._release_size = 1
            minor = 0
            micro = 0
        elif value[2] is None:
            self._release_size = 2
            micro = 0
        elif None in value:
            raise ValueError("None is only valid for micro or both minor and micro")

        self.major = major
        self.minor = minor
        self.micro = micro
        self.pre_release = pre_release

    @property
    def string(self):
        "return version in string format"
        return f"{self.release}{self.pre_release}"

    @string.setter
    def string(self, value):
        self.__init__(value)
