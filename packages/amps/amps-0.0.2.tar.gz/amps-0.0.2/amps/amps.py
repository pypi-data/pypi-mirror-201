#!/usr/bin/env python
import requests
import subprocess
import shlex
import distro
import os
from bs4 import BeautifulSoup
from lxml import etree
from rich.console import Console
from rich.table import Table
from dotenv import load_dotenv

console = Console()
# load_dotenv()

# install_directory = os.getenv('INSTALLATION_DIRECTORY')
table = Table(show_header=True, header_style="bold")
table.add_column("Package", justify="left")
table.add_column("Severity", justify="left")
table.add_column("Status", justify="left")
table.add_column("Issue", justify="left")

'''
def get_system_distribution():
    return subprocess.check_output([install_directory + '/get_distro.sh'])
'''


def get_system_distribution():
    try:
        distribution = subprocess.check_output(["./get_disto.sh"])
    except FileNotFoundError:
        distribution = distro.id()

    return distribution


def intersection(lst1, lst2):
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3


def mainfunction():
    system_distro = get_system_distribution()

    r = requests.get('https://security.archlinux.org/')
    soup = BeautifulSoup(r.content, 'html.parser')
    arch_packages = []

    index = 1
    list = []

    # for x in tqdm(soup.find_all('td', class_='wrap'), desc="finding vulnerable packages", ascii=" ####", bar_format="{desc}: {percentage:.1f}%[{bar}]"):
    for x in soup.find_all('td', class_='wrap'):
        list.append([x.text[1:-1], index])
        index += 1
        arch_packages.append(x.text[1: -1])

    # Python 3.5+
    # cmd for arch based systems pacman -Q
    cmd = 'pacman -Q '
    cmd2 = 'cut -f 1 -d " "'
    args = shlex.split(cmd)
    args2 = shlex.split(cmd2)

    proc = subprocess.Popen(args, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    output = subprocess.check_output(args2, stdin=proc.stdout)
    proc.wait()

    output = output.decode().splitlines()
    vulnerable_packages = set(intersection(arch_packages, output))

    dom = etree.HTML(str(soup))

    for vuln in vulnerable_packages:
        severity = dom.xpath('/ html/body/div[2]/div[3]/table/tbody/tr[' + str(
            arch_packages.index(vuln)+1) + ']/td[6]/span')[0].text

        status = dom.xpath('/ html/body/div[2]/div[3]/table/tbody/tr[' + str(
            arch_packages.index(vuln)+1) + ']/td[7]/span')[0].text

        cve = dom.xpath('/ html/body/div[2]/div[3]/table/tbody/tr[' + str(
            arch_packages.index(vuln)+1) + ']/td[2]/a[1]')[0].text

        issue = cve + " (https://security.archlinux.org/" + str(cve) + ")"

        table.add_row(
            vuln, severity, status, issue
        )

    num_packages = len(output)
    print(str(num_packages) + " packages installed via pacman")
    print("found " + str(len(vulnerable_packages)) +
          " vulnerable packages")
    print("distribution: " + system_distro)

    console.print(table)


if __name__ == "__main__":
    """This runs when you execute '$ python3 mypackage/mymodule.py'"""
    mainfunction()
