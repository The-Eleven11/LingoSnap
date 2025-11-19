#!/usr/bin/env python3
"""
LingoSnap - Instant translation at your fingertips
Setup script for installation and packaging
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='lingosnap',
    version='0.1.0',
    description='Instant translation at your fingertips',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='LingoSnap Team',
    author_email='',
    url='https://github.com/The-Eleven11/LingoSnap',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'PyQt6>=6.4.0',
        'pytesseract>=0.3.10',
        'Pillow>=10.0.0',
        'argostranslate>=1.9.0',
        'googletrans==4.0.0rc1',
        'pynput>=1.7.6',
        'setproctitle>=1.3.2',
        'requests>=2.31.0',
    ],
    entry_points={
        'console_scripts': [
            'lingosnap=lingosnap.__main__:main',
            'lingo=lingosnap.cli.terminal:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: POSIX :: Linux',
        'Topic :: Desktop Environment',
        'Topic :: Text Processing :: Linguistic',
    ],
    python_requires='>=3.10',
)
