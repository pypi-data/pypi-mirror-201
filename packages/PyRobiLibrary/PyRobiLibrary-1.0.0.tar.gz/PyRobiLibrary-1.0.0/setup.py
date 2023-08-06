import os
import re
from setuptools import setup,find_packages


requires = ["pycryptodome==3.16.0","aiohttp==3.8.3","asyncio==3.4.3","tinytag==1.8.1","Pillow==9.4.0"]
_long_description = """

<p align="center">
    <img src="https://s2.uupload.ir/files/img_20230208_141501_035_f545.jpg" alt="NanyRubika" width="128">
    <br>
    <b>Library Nany Rubika</b>
    <br>
</p>


### How to import the Rubik's Library

``` bash
from PyRobi import Bot

```

### How to import the anti-advertising class

``` bash
from PyRobi.Zedcontent import Antiadvertisement
```

### How to install the library

``` bash
pip install PyRobiLibrary==1.0.0
```

### My ID in Telegram

``` bash
@Electorone
```

Our channel in Rubika

https://rubika.ir/GLSource

Our channel in the Gap

None

Our channel on Telegram

https://t.me/Electorone
```

## An example:
``` python
from PyRobi import Bot

bot = Bot("Your Auth Account")

gap = "your guid or gap or pv or channel"

bot.sendMessage(gap,"Library PyRobi")
```

## And Or:
``` python
from PyRobi import Robot_Rubika

bot = Robot_Rubika("Your Auth Account")

gap = "your guid or gap or pv or channel"

bot.sendMessage(gap,"Library PyRobi")
```

## And Or:
``` python
from PyRobi.Shad import *

bot = Shad("Your Auth Account")

gap = "your guid or gap or pv or channel"

bot.sendMessage(gap,"Library PyRobi")
```

"""

setup(
    name = "PyRobiLibrary",
    version = "1.0.0",
    author = "Mohammad",
    author_email = "mmdim427@gmail.com",
    description = (" Library Robot Rubika"),
    license = "MIT",
    keywords = ["NanyRubika","NanyRubika","NanyRubika","NanyRubika","bot","Bot","BOT","Robot","ROBOT","robot","self","api","API","Api","rubika","Rubika","RUBIKA","Python","python","aiohttp","asyncio"],
    url = "https://github.com/Nanymous/NanyRubika.git",
    packages = ['PyRobi'],
    long_description=_long_description,
    long_description_content_type = 'text/markdown',
    install_requires=requires,
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    "Programming Language :: Python :: Implementation :: PyPy",
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11'
    ],
)
