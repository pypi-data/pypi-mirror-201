import dataclasses
import logging
import pathlib
import pprint
import re
import shutil
import string
import subprocess
import tarfile
import urllib.parse
import zipfile

import jinja2
import pkg_resources
import requests

from . import component
from . import product as productmod
from . import versions

_logger = logging.getLogger(__name__)

data = pathlib.Path("data")

keep = (
    string.ascii_lowercase
    + string.ascii_uppercase
    + string.digits
    + string.hexdigits
    + string.octdigits
)

package = __name__.split(".")[0]
templates_dir = pathlib.Path(pkg_resources.resource_filename(package, "templates"))

loader = jinja2.FileSystemLoader(searchpath=templates_dir)
env = jinja2.Environment(loader=loader, keep_trailing_newline=True)


@dataclasses.dataclass
class UrlMeta:
    url: str

    def __post_init__(self):
        pass


component_abbreviations = {
    "Encoder": "Enc",
    "Decoder": "Dec",
    "SCP": "SCP",
}


products = [
    productmod.Product(
        "https://streambox-cdi.s3-us-west-2.amazonaws.com/latest/linux/InstallSbxCDI.tgz",  # noqa: E501
        "Bridge",
        "released",
    ),
    productmod.Product(
        "https://streambox-cdi.s3-us-west-2.amazonaws.com/next-latest/linux/InstallSbxCDI.tgz",  # noqa: E501
        "Bridge",
        "beta",
    ),
    productmod.Product(
        "https://streambox-cdi.s3-us-west-2.amazonaws.com/flame/linux/InstallSbxCDI.tgz",  # noqa: E501
        "Flame",
        "released",
    ),
    productmod.Product(
        "https://streambox-cdi.s3-us-west-2.amazonaws.com/next-flame/linux/InstallSbxCDI.tgz",  # noqa: E501
        "Flame",
        "beta",
    ),
    productmod.Product(
        "https://streambox-spectra.s3-us-west-2.amazonaws.com/latest/linux/spectra.zip",  # noqa: E501
        "Spectra",
        "released",
    ),
]

products_by_url = {product.url: product for product in products}


def view1(data: list[dict]):
    _logger.debug(f"{data=}")
    template = env.get_template("view1.j2")
    out = template.render(data=data)
    print(out)


def unzip(zip_path: str | pathlib.Path, dst: str | pathlib.Path, force: bool = False):
    if not isinstance(zip_path, pathlib.Path):
        zip_path = pathlib.Path(zip_path)

    if not isinstance(dst, pathlib.Path):
        dst = pathlib.Path(dst)

    if dst.exists() and not force:
        _logger.debug(f"{dst.resolve()} already exists, skip unzipping")
        return

    with zipfile.ZipFile(zip_path, "r") as zObject:
        zObject.extractall(path=dst)


def expand_rpm(rpm_path, dest_path):
    dest_path.mkdir(exist_ok=True, parents=True)

    _logger.debug(f"{rpm_path=}")
    # Convert the RPM file to a CPIO archive using rpm2cpio
    rpm2cpio_proc = subprocess.Popen(["rpm2cpio", rpm_path], stdout=subprocess.PIPE)
    cpio_proc = subprocess.Popen(
        ["cpio", "-idmv"], stdin=rpm2cpio_proc.stdout, cwd=dest_path
    )
    cpio_proc.communicate()

    # Check if the extraction was successful
    if cpio_proc.returncode != 0:
        raise Exception("Error expanding RPM file")


def untar(tar_path: pathlib.Path, dst: pathlib.Path):
    suffix = str(tar_path.suffix).lower()
    _logger.debug(f"{suffix=}")

    mode = None
    if suffix in [".tar.gz", ".tgz"]:
        mode = "r:gz"

    elif suffix in [".tar"]:
        mode = "r:"

    _logger.debug(f"expanding {tar_path.resolve()} to {dst.resolve()}")
    tar = tarfile.open(tar_path, mode)
    tar.extractall(dst)
    tar.close()


def url_cache_basedir(url) -> pathlib.Path:
    x1 = "".join(["-" if c not in keep else c for c in str(url)])
    return data / x1


def get_path_matching_substr(paths: list[pathlib.Path], substr: str):
    for path in paths:
        if substr in str(path):
            return path
    return None


def get_installer_script_path(url: str) -> pathlib.Path:
    basedir = get_expandto_path(url)
    p = basedir.glob("**/install*")
    scripts = [
        x for x in p if x.is_file() and x.name.lower() in ["install", "installsbx"]
    ]
    assert len(scripts) <= 1

    msg = (
        f"I can't find installer script for {url}, "
        f"maybe this url is a windows installer, yes?"
    )
    if not scripts:
        # FIXME
        _logger.warning(msg)

    script_path = pathlib.Path(scripts[0])

    _logger.debug(f"installer script for {url} is {script_path.resolve()}")

    return script_path


def get_cache_path(url: str) -> pathlib.Path:
    out = urllib.parse.urlparse(url)
    fname = pathlib.Path(out.path).name
    x1 = url_cache_basedir(url) / fname
    return x1


def get_product_from_url(url: str):
    product = products_by_url[url]
    return product


def get_expandto_path(url: str) -> pathlib.Path:
    x1 = get_cache_path(url)
    return pathlib.Path(f"{x1}-expanded")


def is_rpm_in_installer_script(installer: str, script_path: pathlib.Path) -> bool:
    for line in script_path.read_text().splitlines():
        if installer.lower() in line.lower():
            return True

    return False


def download_file(url: str, dst: pathlib.Path):
    msg = f"{dst.resolve()} exists already, skipping download"

    if dst.exists():
        _logger.debug(msg)
        return

    response = requests.get(url, stream=True)
    with open(dst, "wb") as out_file:
        shutil.copyfileobj(response.raw, out_file)


def expand_compressed(compressed: pathlib.Path, expand_to: pathlib.Path):
    suffix = str(compressed.suffix).lower()

    if suffix in [".zip"]:
        unzip(compressed, expand_to)

    elif suffix in [".tgz"]:
        untar(compressed, expand_to)

    else:
        msg = f"I don't know how to expand file with extension {suffix}"
        raise ValueError(msg)


def handle_rpm_contents(url: str, rpms: list[pathlib.Path]) -> list[dict]:
    installer_script = get_installer_script_path(url)

    ignore_fnames = set(
        [
            "chromactivate.exe",
            "LinuxEncoder.exe",
            "LinuxEncoder3.exe",
            "LinuxEncoder5.exe",
        ]
    )

    version_parser = versions.VersionParser(versions.SubstrTruncateStrategy())

    items = []
    for rpm in rpms:
        expanded_path = pathlib.Path(f"{rpm}-expanded")

        msg = (
            f"skipping {rpm.name} because "
            f"its not listed in {installer_script.resolve()}"
        )

        if not is_rpm_in_installer_script(rpm.name, installer_script):
            _logger.debug(msg)
            continue

        if not expanded_path.exists():
            _logger.debug(f"expanding {rpm} to {expanded_path}")
            expanded_path.mkdir(exist_ok=True, parents=True)
            expand_rpm(rpm, expanded_path)

        p = expanded_path.glob("**/*.exe")
        unique = set(
            [
                x
                for x in p
                if x.is_file() and not x.is_symlink() and x.name not in ignore_fnames
            ]
        )
        x1 = list(unique)
        x1.sort(key=lambda x: x.name.lower())

        product = get_product_from_url(url)
        for item in x1:
            component = versions.get_component_name(item.name)  # Decoder, Encoder, ...
            data = {
                "version": versions.get_version(item.name, version_parser),
                "product_name": product.name,
                "released": product.tag,
                "component_name": component,
                "component_name_abbreviated": component_abbreviations[component],
                "installer_url": product.url,
            }
            items.append(data)

    return items


def handle_rpm_fnames(
    url: str, rpms: list[pathlib.Path]
) -> list[component.Productcomponent]:
    installer_script = get_installer_script_path(url)

    comp_candidates = []

    product = get_product_from_url(url)
    version_parser = versions.VersionParser(versions.RegexStrategy())

    matcher = "streambox_www_for_avenir"
    name = matcher
    comp = component.Productcomponent(name, matcher)
    comp.version_parser = version_parser
    comp.product = product
    comp_candidates.append(comp)

    matcher = "streambox_webui_for_rackmount"
    name = matcher
    comp = component.Productcomponent(name, matcher)
    comp.version_parser = version_parser
    comp.product = product
    comp_candidates.append(comp)

    found_components = []

    for comp in comp_candidates:
        for rpm in rpms:
            msg = (
                f"skipping {rpm.name} because "
                f"its not listed in {installer_script.resolve()}"
            )

            if not is_rpm_in_installer_script(rpm.name, installer_script):
                _logger.debug(msg)
                continue

            regex = f".*{comp.path_matcher}.*"
            mo = re.search(regex, str(rpm), flags=re.IGNORECASE)

            if mo:
                comp.path = pathlib.Path(rpm).resolve()
                comp.version_from_str(rpm.name)
                found_components.append(comp)
                _logger.debug(f"SUCCESS: matching against {str(rpm)}")

    return found_components


def main(args):
    urls = [product.url for product in products]

    for url in urls:
        outdir = url_cache_basedir(url)
        outdir.mkdir(parents=True, exist_ok=True)

        cache_path = get_cache_path(url)
        _logger.debug(f"{cache_path=}")

        download_file(url, dst=cache_path)
        expand_dst = get_expandto_path(url)
        expand_compressed(cache_path, expand_to=expand_dst)

    items = []
    components = []
    for url in urls:
        cache_path = get_cache_path(url)
        basedir = url_cache_basedir(url)
        rpms = list(basedir.glob("**/*.rpm"))
        things = handle_rpm_contents(url, rpms)
        comps = handle_rpm_fnames(url, rpms)
        components.extend(comps)
        items.extend(things)

    view1(items)
    pprint.pprint(components)


if __name__ == "__main__":
    main()
