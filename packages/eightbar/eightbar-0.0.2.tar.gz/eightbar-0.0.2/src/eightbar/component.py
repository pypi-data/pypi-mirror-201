import dataclasses
import logging
import pathlib
import typing

from . import product as productmod
from . import versions

_logger = logging.getLogger(__name__)


def get_version_from_string(_str: str, parser) -> str:
    version = parser.parse(_str)
    _logger.debug(f"{version=}")
    x1 = list_tuples_to_str(version)
    x1 = x1.lstrip("-")
    return x1


def list_tuples_to_str(lst: list[typing.Tuple]):
    x1 = ""
    for tup in lst:
        for val in tup:
            x1 = f"{x1}{val}"

    return x1


@dataclasses.dataclass
class Productcomponent:
    name: str
    path_matcher: str
    version: str = dataclasses.field(init=False)
    path: pathlib.Path = dataclasses.field(init=False)
    product: productmod.Product = dataclasses.field(init=False)
    version_parser: versions.VersionParser = dataclasses.field(init=False)

    def version_from_str(self, _str) -> None:
        tmp = remove_strings_that_obfuscate_fetching_version(_str)
        version = get_version_from_string(tmp, parser=self.version_parser)
        self.version = version


def test2():
    _str = "InstallSbxCDI/streambox_webui_for_rackmount-1.1.161-1.noarch.rpm"
    path = pathlib.Path(_str)

    version = get_version_from_string(path)
    print(f"{version=}")


def remove_strings_that_obfuscate_fetching_version(_str: str) -> str:
    filters = ["x86_64"]

    result = _str
    for filter in filters:
        result = result.replace(filter, "")
    return result


def test3():
    tests = [
        {
            "fname": "streambox_www_for_avenir-1.8.189-3.x86_64.rpm",
            "expected": "1.8.189-3",
        },
        {
            "fname": "streambox_webui_for_rackmount-1.1.152-1.noarch.rpm",
            "expected": "1.1.152-1",
        },
        {
            "fname": "streambox_www_for_avenir-1.8.189.x86_64.rpm",
            "expected": "1.8.189",
        },
    ]

    for test in tests:
        tmp = remove_strings_that_obfuscate_fetching_version(test["fname"])
        version = get_version_from_string(tmp)
        assert version == test["expected"]


if __name__ == "__main__":
    test3()
