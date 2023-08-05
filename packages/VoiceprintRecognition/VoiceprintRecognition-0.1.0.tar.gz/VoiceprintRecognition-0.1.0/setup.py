#!/usr/bin/env python3
# https://github.com/SriBalaji2112/voiceprint_recognition

import io
import os
import re
from setuptools import setup

scriptFolder = os.path.dirname(os.path.realpath(__file__))
os.chdir(scriptFolder)

# Find version info from module (without importing the module):
with open('voiceprint_recognition/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

# Use the README.md content for the long description:
with io.open("README.md", encoding="utf-8") as fileObj:
    long_description = fileObj.read()

setup(
    name='VoiceprintRecognition',
    version=version,
    url='https://github.com/SriBalajiSMVEC/voiceprint_recognition',
    author='BalajiSanthanam',
    author_email='sribalaji2112@gmail.com',
    description=('A speaker recognition library that works both online and offline and supports a number of engines and APIs. '),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='BSD 3-Clause License',
    packages=['voiceprint_recognition'],
    test_suite='tests',
    install_requires=['pyobjc-core;platform_system=="Darwin"',
                      'pyobjc;platform_system=="Darwin"',
                      'python3-Xlib;platform_system=="Linux" and python_version>="3.0"',
                      'python-xlib;platform_system=="Linux" and python_version<"3.0"',
                      'pymsgbox',
                      'pytweening>=1.0.4',
                      'pyscreeze>=0.1.21',
                      'pygetwindow>=0.0.5',
                      'mouseinfo',
                      'SpeechRecognition',
                        'keras',
                        'tensorflow',
                        'os'
                      ],
    keywords="biometric speaker recognition voice sphinx google wit bing api houndify ibm snowboy voice print identification security",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)