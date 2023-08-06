import os
import re
from setuptools import setup,find_packages


requires = ["pycryptodome==3.16.0","aiohttp==3.8.3","asyncio==3.4.3","tinytag==1.8.1","Pillow==9.4.0"]
_long_description = """

## pyRubiCo

> Elegant, modern and asynchronous Rubika MTProto API framework in Python for users and bots

<p align="center">
    <img src="https://s28.picofile.com/file/8461623650/6531529136800.jpg" alt="pyRubiCo" width="128">
    <br>
    <b>library pyRubiCo Rubika</b>
    <br>
</p>

###  pyRubiCo library documents soon...


### How to import the Rubik's library

``` bash
from pyRubiCo import Bot

Or

from pyRubiCo import Robot_Rubika
```

### How to import the anti-advertising class

``` bash
from pyRubiCo.Zedcontent import Antiadvertisement
```

### How to install the library

``` bash
pip install pyRubiCo==2.2.2
```

### My ID in Telegram

``` bash
@Ali_eslami8338
```
## An example:
``` python
from pyRubiCo import Bot

bot = Bot("Your Auth Account")

gap = "your guid or gap or pv or channel"

bot.sendMessage(gap,"pyRubiCo")
```

## And Or:
``` python
from pyRubiCo import Robot_Rubika

bot = Robot_Rubika("Your Auth Account")

gap = "your guid or gap or pv or channel"

bot.sendMessage(gap,"pyRubiCo")
```
Made by Team pyRubiCo

Address of our team's GitHub :

https://github.com/alitektanu/RubiCo.git


### Key Features

- **Ready**: Install pyRubiCo with pip and start building your applications right away.
- **Easy**: Makes the Rubika API simple and intuitive, while still allowing advanced usages.
- **Elegant**: Low-level details are abstracted and re-presented in a more convenient way.
- **Fast**: Boosted up by pycryptodome, a high-performance cryptography library written in C.
- **Async**: Fully asynchronous (also usable synchronously if wanted, for convenience).
- **Powerful**: Full access to Rubika's API to execute any official client action and more.


### Our channel in messengers

``` bash
Our channel in Rubika

https://rubika.ir/pyRubiCo

```
"""

setup(
    name = "pyRubiCo",
    version = "2.2.2",
    author = "Ali Eslami",
    author_email = "pyRubiCo@gmail.com",
    description = (" library Robot Rubika"),
    license = "MIT",
    keywords = ["RubiCo","pyRubiCo","PYRUBICO","pyrubico","bot","Bot","BOT","Robot","ROBOT","robot","self","api","API","Api","rubika","Rubika","RUBIKA","Python","python","aiohttp","asyncio"],
    url = "https://github.com/alitektanu/RubiCo.git",
    packages = ['pyRubiCo'],
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
