# Copyright (c) 2022, 2023, Panagiotis Tsirigotis

# This file is part of linuxnet-qos.
#
# linuxnet-qos is free software: you can redistribute it and/or
# modify it under the terms of version 3 of the GNU Affero General Public
# License as published by the Free Software Foundation.
#
# linuxnet-qos is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public
# License for more details.
#
# You should have received a copy of the GNU Affero General
# Public License along with linuxnet-qos. If not, see
# <https://www.gnu.org/licenses/>.

import distutils.command.build
import os
import setuptools


from os.path import abspath, dirname

NAME = "linuxnet-qos"

#
# Check if a suitable Sphinx version is available
#
sphinx_is_available = False

try:
    from sphinx import __version__ as sphinx_version
    sphinx_is_available = True
except ImportError:
    print("** WARNING: sphinx is not available; will not build manpages")

if sphinx_is_available:
    vers = sphinx_version.split('.')
    if (int(vers[0]), int(vers[1])) < (4, 4):
        sphinx_is_available = False
        print(f"** WARNING: need sphinx 4.4 or later; found {sphinx_version}")


class LinuxnetQoSBuild(distutils.command.build.build):
    """Custom build command that also builds the Sphinx documentation.
    """

    def have_sphinx(self) -> bool:
        return sphinx_is_available

    distutils.command.build.build.sub_commands.append(
                                        ('build_sphinx', have_sphinx))


class Contents:
    """This class provides is an iterable returning the contents of
    a directory as paths that include the directory path.
    """
    def __init__(self, dirpath):
        self.__dirpath = dirpath

    def __iter__(self):
        if not os.path.exists(self.__dirpath):
            return iter([])
        paths = []
        for entry in os.listdir(self.__dirpath):
            entry_path = os.path.join(self.__dirpath, entry)
            if not os.path.isdir(entry_path):
                paths.append(entry_path)
        return iter(paths)


def read_version():
    """Returns the value of the _version_ variable from the
    metadata.py module
    """
    source_dir = NAME.replace('-', '/')
    path = os.path.join(source_dir, 'metadata.py')
    globs = {'__builtins__':{}}
    mdvars = {}
    with open(path, encoding='utf-8') as f:
        exec(f.read(), globs, mdvars)
    return mdvars['_version_']


delim = "-----------------"

print(f"{delim} BEGIN {NAME} {delim}")

setup_args = {}

if sphinx_is_available:
    from sphinx.setup_command import BuildDoc
    setup_args['cmdclass'] = {
                                'build_sphinx': BuildDoc,
                                'build' : LinuxnetQoSBuild,
                            }
    html_destdir = f'share/doc/{NAME}/html'
    htmldir = 'build/sphinx/html'
    man_destdir = 'share/man/man3'
    mandir = 'build/sphinx/man/man3'
    data_files = [
            (man_destdir, Contents(mandir)),
            (html_destdir, Contents(htmldir)),
        ]
    for subdir in ('_static',
                        '_modules', '_modules/filters', '_modules/qdiscs',
                        '_sources', '_sources/filters', '_sources/qdiscs',
                        ):
        builddir = os.path.join(htmldir, subdir)
        destdir = os.path.join(html_destdir, subdir)
        data_files.append((destdir, Contents(builddir)))
    setup_args['data_files'] = data_files
    setup_args['options'] = { 'build_sphinx' : { 'builder' : 'man html' } }

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name=NAME,
    version=read_version(),
    author="Panagiotis (Panos) Tsirigotis",
    author_email="ptsirigotis01@gmail.com",
    url="https://gitlab.com/panos-tools/linuxnet-qos",
    project_urls={
            'Source': "https://gitlab.com/panos-tools/linuxnet-qos",
            'Documentation': "https://linuxnet-qos.readthedocs.io/en/latest/index.html",
        },
    description="programmatic access to the Linux queuing disciplines",
    license="AGPLv3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[
        'linuxnet',
        'linuxnet.qos',
        'linuxnet.qos.qdiscs',
        'linuxnet.qos.filters',
        ],
    classifiers=[       # From: https://pypi.org/classifiers/
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Networking"
    ],
    python_requires='>=3.6',
    test_suite="tests",
    **setup_args
)

print(f"{delim} END {NAME} {delim}")
