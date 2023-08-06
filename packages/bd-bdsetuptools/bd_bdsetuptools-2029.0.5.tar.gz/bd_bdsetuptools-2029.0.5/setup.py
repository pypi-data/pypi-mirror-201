from setuptools import setup, find_packages
import os
import sys
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init()


def amenda():
    print(f'amenda plus bataie!')
    print()
    print(f"{Fore.GREEN}AMENDA!{Style.RESET_ALL}!")
    print()
    print(f"{Fore.YELLOW}BATAIE!{Style.RESET_ALL}!")
    print()
    print(f"{Fore.MAGENTA}GRAV!{Style.RESET_ALL}!")
    print()
    print(f"{Fore.CYAN}TE-AI DUS!{Style.RESET_ALL}!")
    print()
    print(f"{Fore.WHITE}DATA VIITOARE SA DAI CU --index-url!{Style.RESET_ALL}!")

    sys.exit(69)



if not os.getenv('LET_ME_BUILD'):
    amenda()

setup(
    name='bd_bdsetuptools',
    version='2029.0.5',
    author='Malin Jean',
    author_email='malin@example.com',
    description='Dop',
    packages=['bd_bdsetuptools'],
    package_dir={'bd_bdsetuptools': '.'},  
    install_requires=['setuptools', 'wheel', 'colorama'],
)