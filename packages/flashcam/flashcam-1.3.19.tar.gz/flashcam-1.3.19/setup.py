#!/usr/bin/env python3
import os
from setuptools import setup, find_packages
"""
??? I saw an error with this... sudo apt-get install python3-smbus

"""
#-----------problematic------
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

import os.path

def readver(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in readver(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

setup(
    name="flashcam",
    description="Composition of scripts to control a web camera",
    url="https://gitlab.com/jaromrax/flashcam",
    author="jaromrax",
    author_email="jaromrax@gmail.com",
    license="GPL2",
    version=get_version("flashcam/version.py"),
    packages=['flashcam'],
    package_data={'flashcam': ['data/BEAM_OFF.jpg',
                               'data/BEAM_ON_.jpg',
                               'data/DET_NRDY.jpg',
                               'data/DET_RDY_.jpg',
                               'data/windows.jpg',
                               'data/digital-7.mono.ttf',
                               'data/monoskop.jpg'
    ]},
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    scripts = ['bin/flashcam','bin/flashcamg','bin/flashcam_join','bin/flashcam_rep'],
    install_requires = ['fire','v4l2py','flask_httpauth','gunicorn','numpy','imutils','pandas','matplotlib','psutil','pyserial-asyncio', 'imagezmq','notifator','pyautogui','importlib_resources','requests','pynput'],
)
