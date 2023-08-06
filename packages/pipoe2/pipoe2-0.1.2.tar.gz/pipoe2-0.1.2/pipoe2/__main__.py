from lxml import html
import requests

import subprocess

from urllib.parse import urlparse

from collections import defaultdict
from rich.progress import Progress
from rich.console import Console
from pathlib import Path
import tarfile
from io import BytesIO

import hashlib
import click

from pathlib import Path

console = Console()

def print_info(message):
    console.log(f":information_source: {message}")

def print_success(message):
    console.log(f":heavy_check_mark: {message}")

def print_error(message):
    console.log(f":x: {message}")

def get_version(package):
    command = f"pip3 show {package} | grep Version | cut -d ':' -f 2 | tr -d '[:space:]'"
    version = subprocess.check_output(command, shell=True).decode()
    
    return version

def filter_array(arr):
    return list(set(filter(lambda x: x.strip() != '', arr)))

def get_dependencies(package):
    command = f"pip3 show {package} | grep Requires | cut -d ':' -f 2 | tr -d '[:space:]'"
    dependencies = subprocess.check_output(command, shell=True).decode().split(',')

    # Recursively get the dependencies of each direct dependency.
    for dependency in dependencies:
        if dependency:
            dependencies += get_dependencies(dependency)

    dependencies = filter_array(dependencies)
    return dependencies

def ensure_installed(package, version):
    command = f"pip3 install {package}=={version}"
    result = subprocess.check_output(command, shell=True).decode()
    print(result)


def get_package_write_bb(package, version, dependencies=[]):
    package_url = "https://pypi.org/simple/" + package;
    response = requests.get(package_url)

    print_info(f"Getting package list from: {package_url}")

    package_translated = package.replace("-", "_")
    tree = html.fromstring(response.content)

    package_link = [package for package in tree.xpath('//a/@href')]
    package_text = [package for package in tree.xpath('//a/text()')]

    res = defaultdict(list)
    for i, j in zip(package_text, package_link):
        res[i.lower()].append(j)

    final_dict = dict(res)
    identifier = f'{package_translated}-{version}'
    identifier_b = f'{package}-{version}'

    url = f"https://files.pythonhosted.org/packages/source/r/{package}/{package}-{version}.tar.gz"
    file_identifier = identifier + ".tar.gz"
    file_identifier_b = identifier_b + ".tar.gz"
    result = requests.get(url)
    is_pypi = False
    if result.status_code == 404:    
        is_pypi = True
        final_file_identifier = file_identifier
        if file_identifier not in final_dict:
            final_file_identifier = file_identifier_b
            print_error(f"File not found for: {file_identifier}")
            if file_identifier_b not in final_dict:
                print_error(f"File not found for: {file_identifier_b}")
                return
        target = final_dict[f'{final_file_identifier}'][0]
        parsed_url = urlparse(target)
        url = parsed_url.geturl()

    url = url.split("#")[0]

    if file_identifier not in final_dict.keys() and file_identifier_b not in final_dict.keys():
        print_error(f"Package [b]{package}[/b] with version {version} not found using suffix {file_identifier}!")
        return

    with Progress() as progress:
        task = progress.add_task("Init...", total=5)

        with requests.get(url , stream=True) as  rx, tarfile.open(fileobj=rx.raw, mode="r:gz") as  tarobj  :
            is_poetry = False
            package_archive_key = package
            if is_pypi:
                package_archive_key = package_translated
            if f"{package_archive_key}-{version}/pyproject.toml" in tarobj.getnames():
                print_info("Is a poetry project")
                is_poetry = True
            
            progress.update(task, description="Downloading File to calculate HASH")
            progress.advance(task)

            response = requests.get(url)
            data = response.content
            
            progress.update(task, description="Creating MD5 hash")
            progress.advance(task)
            md5_returned = hashlib.md5(data).hexdigest()
            sha_returned = hashlib.sha256(data).hexdigest()

            progress.update(task, description="Creating Folder")
            progress.advance(task)
            Path(f"python3-{package}").mkdir(parents=True, exist_ok=True)

            
            progress.update(task, description="Creating bb File")
            progress.advance(task)

            f = open(f"python3-{package}/python3-{package}_{version}.bb", "w")
            progress.update(task, description="Writing bb File")
            progress.advance(task)

            builder = "setuptools3"
            if is_poetry:
                builder = "python_poetry_core"
            
            rdepends = ["python3-" + package_name for package_name in dependencies]
            lines_to_write = [
                f'SUMMARY = "Python tool {package}"\n',
                f'LICENSE = "CLOSED"\n',
                f'SRC_URI = "{url.split("#")[0]}"\n'
                f'SRC_URI[sha256sum] = "{sha_returned}"\n',
                f'SRC_URI[md5sum] = "{md5_returned}"\n',
                f'inherit {builder}\n',
                f'RDEPENDS:${{PN}} += "{" ".join(rdepends)}"\n'
                f'BBCLASSEXTEND = "native nativesdk"\n'
            ]

            if is_pypi:
                lines_to_write.append("do_compile:prepend() { \n")
                lines_to_write.append(f"\tcp -r ${{WORKDIR}}/{package_translated}-{version}/* ${{WORKDIR}}/{package}-{version}/\n")
                lines_to_write.append("}\n")

            f.writelines(lines_to_write)

@click.command()
@click.argument("package")
@click.option('--version', required=True, help='Version to be used')
@click.option('--recursive', is_flag=True, help='if set will run and try to fetch dependencies')
def main(package, version, recursive):
    ensure_installed(package, version)
    dependencies = get_dependencies(package)
    get_package_write_bb(package, version, dependencies)

    if (recursive):
        for d in dependencies:
            recursive_resolve(d)

def recursive_resolve(package):
    print_info(f"Getting dependencies for {package}")
    version = get_version(package)
    ensure_installed(package, version)
    dependencies = get_dependencies(package)
    get_package_write_bb(package, version, dependencies)
    for d in dependencies:
        recursive_resolve(d)

    

def run():
    main()


if __name__ == "__main__":
    run()