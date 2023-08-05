"""
pygnsstoolbox - Python GNSS processing package
Copyright (C) 2014-2023, Jacques Beilin <jacques.beilin@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

from setuptools import setup, find_packages
import os.path as path
import sys

install_reqs = ['gpsdatetime']

if sys.platform.startswith('win'):
    install_reqs.append('pywin32')
    
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gnsstoolbox',
    version="1.2.8",
    description='Python GNSS processing package',
    long_description=long_description,
    author='Jacques Beilin',
    author_email='jacques.beilin@gmail.com',
    packages = find_packages(exclude=["test","docs"]),

    install_requires = install_reqs,
    package_data = {'': ['*.xml', '*.txt']},
    url='https://gitlab.com/jbeilin/pygnsstoolbox',
    download_url = '',
    licence='gpl',
    classifiers=[
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Pick your license as you wish (should match "license" above)
#    'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    ],
    py_modules=['antex','gnsstools','orbits','rinex_o','ubx_util','gnss_process','gnss_corr','gnss_const','skyplot']
)

