# Copyright (c) PyBW
# Distributed under the terms of the MIT License.

import sys
import platform
from setuptools import setup, find_packages

is_win_64 = sys.platform.startswith('win') and platform.machine().endswith('64')
extra_link_args = ['-Wl,--allow-multiple-definition'] if is_win_64 else []

with open('README.md', encoding='utf-8') as f:
    readme = f.read()


setup(
    name='pybw',
    version='23.4.3.2',
    python_requires='>=3.6',
    
    author='Bowei Pu',
    author_email='pubowei@foxmail.com',
    
    description='pybw',
    long_description=readme, 
    long_description_content_type='text/markdown',
    url='https://gitee.com/pubowei/pybw',
    keywords=['pybw', 'tools'],
    license='MIT',
    
    packages=find_packages(), 
    include_package_data=True, 
    
    entry_points={
        'console_scripts': ['ccnbmod = pybw.ccnb_mod.ccnb_mod:main']
    }, 

    project_urls={
        'Docs': 'https://gitee.com/pubowei/pybw',
        'Package': 'https://pypi.org/project/pybw',
        'Repo': 'https://gitee.com/pubowei/pybw',
    },

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
    ],
)


"""
setup(
    name='pybw',
    version='2023.2.28',
    python_requires='>=3.6',
    
    author='Bowei Pu',
    author_email='pubowei@foxmail.com',
    maintainer='Bowei Pu',
    maintainer_email='pubowei@foxmail.com',
    
    description='pybw',
    long_description=readme, 
    long_description_content_type='text/markdown',
    url='https://pubowei.cn',
    keywords=['pybw', 'tools'],
    license='MIT',
    
    packages = find_packages(), 
    
    entry_points={
        'console_scripts': ['ccnbmod = pybw:ccnbmod.ccnbmod.main']
    }, 
    scripts=['pybw/ccnbmod/ccnbmod.py'], 
    
    
    install_requires=[
        'pathlib>=1.0.1',
        'tqdm',
    ],
    extras_require={
        'ase': ['ase>=1.0'],
    },
    project_urls={
        'Docs': 'https://pubowei.cn',
        'Package': 'https://pypi.org/project/pybw',
        'Repo': 'https://gitee.com/pubowei/pybw',
    },

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
"""
