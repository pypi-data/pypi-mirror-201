from lxml import html
import requests

from rich.progress import Progress
from rich.console import Console
import click

from pathlib import Path

console = Console()

def print_info(message):
    console.log(f":information_source: {message}")

def print_success(message):
    console.log(f":heavy_check_mark: {message}")

def print_error(message):
    console.log(f":x: {message}")



@click.command()
@click.option('--package', required=True, help='Package to check out')
@click.option('--version', required=True, help='Version to be used')
def main(package, version):
    response = requests.get("https://pypi.org/simple/")

    tree = html.fromstring(response.content)

    package_list = [package for package in tree.xpath('//a/text()')]

def run():
    main()


if __name__ == "__main__":
    run()