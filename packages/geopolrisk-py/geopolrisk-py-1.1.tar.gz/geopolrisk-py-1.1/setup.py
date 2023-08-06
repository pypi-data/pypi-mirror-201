# Copyright (C) 2023 University of Bordeaux, CyVi Group & Anish Koyamparambath
# This file is part of geopolrisk-py library.
#
# geopolrisk-py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# geopolrisk-py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with geopolrisk-py.  If not, see <https://www.gnu.org/licenses/>.
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys
import subprocess


class RunTests(TestCommand):
    """
    Custom test command that runs the tests defined in the 'tests.py' file.
    """
    def run_tests(self):
        # Run the tests using the 'unittest' module
        test_file = 'geopolrisk/tests.py'
        test_result = subprocess.run([sys.executable, test_file], stdout=subprocess.PIPE)
        
        # Display the test results to the user
        print(test_result.stdout.decode('utf-8'))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='geopolrisk-py',
    version='1.1',
    author="Anish Koyamparambath",
    author_email="anish.koyamparambath@u-bordeaux.fr",
    description="A complete library for calculation of the GeoPolRisk method",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/akoyamp/geopolrisk-py",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
        'pandas',
        'matplotlib',
        'scipy',
        'comtradeapicall',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    license="GPL-3.0-or-later",
    cmdclass={
        'test': RunTests,
    },
)



