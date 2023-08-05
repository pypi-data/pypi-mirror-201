# -*- coding: utf-8 -*-

from setuptools import setup
from codecs import open
from os import path
import re
from setuptools.command.install import install
from shutil import which
import platform                          

package_name = "vern"

root_dir = path.abspath(path.dirname(__file__))

def _requirements():
    return [name.rstrip() for name in open(path.join(root_dir, 'requirements.txt')).readlines()]


def _test_requirements():
    return [name.rstrip() for name in open(path.join(root_dir, 'requirements.txt')).readlines()]

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        if platform.system() == "Windows":
            import winreg
            for REG_PATH, CLASS, value in [
                [r"Software\Classes\*\shell\vern", winreg.REG_SZ, "process in VERN"],
                [r"Software\Classes\*\shell\vern\command", winreg.REG_EXPAND_SZ, f"\"{which('vern')}\" \"%1\""],
            ]:
                try:
                    winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
                    registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_WRITE)
                    winreg.SetValueEx(registry_key, "", 0, CLASS, value)
                    winreg.CloseKey(registry_key)
                except WindowsError:
                    pass

with open(path.join(root_dir, package_name, '__init__.py')) as f:
    init_text = f.read()
    version = re.search(r'__version__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)
    license = re.search(r'__license__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)
    author = re.search(r'__author__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)
    author_email = re.search(r'__author_email__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)
    url = re.search(r'__url__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)

assert version
assert license
assert author
assert author_email
assert url

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=package_name,
    packages=[package_name],

    version=version,

    license=license,

    install_requires=_requirements(),
    tests_require=_test_requirements(),

    entry_points={
        "console_scripts": [
            "vern=vern.parse_all:vern",
        ]
    },   
    cmdclass={'install': PostInstallCommand},

    author=author,
    author_email=author_email,

    url=url,

    description='templated auto processing/visualization of measured data',
    long_description=long_description,
    keywords='matplotlib, research, plot',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)