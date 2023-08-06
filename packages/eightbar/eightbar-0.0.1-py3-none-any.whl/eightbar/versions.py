import logging
import pathlib
import re

import packaging.version

_logger = logging.getLogger(__name__)

data = pathlib.Path("data")

SBX_FILENAME_MATCHERS = {
    "LinuxDecoder64b.": "Decoder",
    "LinuxEncoder64b.": "Encoder",
    "ECP_CPP_linux_": "SCP",
}


test_str = """
https://streambox-cdi.s3-us-west-2.amazonaws.com/latest/linux/InstallSbxCDI.tgz
LinuxDecoder64b.X.52.B06.exe
LinuxEncoder64b.3.202.52.B06.exe
LinuxEncoder64b.5.102.52.B06.exe

https://streambox-cdi.s3-us-west-2.amazonaws.com/next-latest/linux/InstallSbxCDI.tgz
LinuxDecoder64b.X.52.B15D.exe
LinuxEncoder64b.3.203.52.B15D.exe
LinuxEncoder64b.5.104.52.B15D.exe

https://streambox-cdi.s3-us-west-2.amazonaws.com/flame/linux/InstallSbxCDI.tgz
LinuxDecoder64b.X.52.B10B.exe
LinuxEncoder64b.3.202.52.B10B.exe
LinuxEncoder64b.5.103.52.B10B.exe

https://streambox-cdi.s3-us-west-2.amazonaws.com/next-flame/linux/InstallSbxCDI.tgz
LinuxDecoder64b.X.52.B15D.exe
LinuxEncoder64b.3.203.52.B15D.exe
LinuxEncoder64b.5.104.52.B15D.exe

https://streambox-spectra.s3-us-west-2.amazonaws.com/latest/linux/spectra.zip
LinuxEncoder64b.3.202.51.D07.exe
LinuxEncoder64b.5.102.51.D07.exe
ECP_CPP_linux_0.1.53.exe
"""


class VersionParser:
    def __init__(self, strategy):
        self.strategy = strategy

    def parse(self, string):
        return self.strategy.parse(string)


class RegexStragegy2:
    """
    https://codereview.stackexchange.com/a/124697/207924
    """

    VERSION_REGEX = re.compile(
        r"^"  # start of string
        r"v"  # literal v character
        r"(?P<major>[0-9]+)"  # major number
        r"\."  # literal . character
        r"(?:.(?P<minor>[0-9+]))"  # minor number
        r"(?:b(?P<beta>[0-9+]))?"  # literal b character, and beta number
    )

    def parse(self, string):
        match = self.VERSION_REGEX.search(string)
        return match.groupdict()


class MajorMinorStrategy:
    def parse(self, string):
        pattern = r"(\d+)\.(\d+)"
        match = re.search(pattern, string)
        if match:
            return (match.group(1), match.group(2), "0")
        else:
            return None


class MajorStrategy:
    def parse(self, string):
        pattern = r"(\d+)"
        match = re.search(pattern, string)
        if match:
            return (match.group(1), "0", "0")
        else:
            return None


class RegexStrategy:
    pattern = r"(\d+\.)?(\d+\.)?(-|\*|\d+)"

    def parse(self, _str):
        matches = re.findall(self.pattern, _str)
        _logger.debug(f"{matches=}")
        return matches


class PackageStrategy:
    def parse(self, _str):
        v1 = None
        try:
            v1 = packaging.version.parse(_str)
            _logger.debug(f"SUCCESS: {v1}")
        except ValueError:
            msg = f"can't parse version from {_str}"
            _logger.debug(msg)

        return v1


class SubstrTruncateStrategy:
    def parse(self, _str):
        sanitized = sanitize_str(_str)
        return sanitized


def get_component_name(_str):
    for substr, name in SBX_FILENAME_MATCHERS.items():
        if re.search(substr, _str, flags=re.IGNORECASE):
            return name

    return None


def sanitize_str(_str) -> str:
    removals = [
        "LinuxDecoder64b.",
        "LinuxEncoder64b.",
        "ECP_CPP_linux_",
        ".exe",
    ]
    replacement_str = ""
    new_str = _str

    for removal in removals:
        new_str = re.sub(removal, replacement_str, new_str, flags=re.IGNORECASE)

    return new_str


def get_version(_str, version_parser):
    version1 = version_parser.parse(_str)
    return version1


def test():
    parser1 = VersionParser(SubstrTruncateStrategy())

    for _str in test_str.splitlines():
        if not _str:
            continue
        version1 = parser1.parse(_str)
        print(f"{version1}")


if __name__ == "__main__":
    test()
