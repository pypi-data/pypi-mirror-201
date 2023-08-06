# MIT License
#
# Copyright (c) 2023 Dechin CHEN
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


""" Upload this project to pypi
$ python3 setup.py check
$ python3 setup.py sdist bdist_wheel
$ twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
"""

from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="mindspore-quaternion",
    version="0.6",
    description="Quaternion data structure based on MindSpore Framework",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT Licence",

    url="https://gitee.com/dechin/mindspore-quaternion",
    author="Dechin CHEN",
    author_email="dechin.phy@gmail.com",
    packages=find_packages(exclude=["tests", "examples"]),
    install_requires=open('requirements.txt', 'r').readlines(),
    platforms="any",
    scripts=[],
    include_package_data=True
)
