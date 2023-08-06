import os
import re
from setuptools import setup
requires = ["pycryptodome==3.16.0","websocket_client","requests","rubiran==2.0.1","Pillow==9.4.0","datetime"]
_long_description = """

## An example:
``` python
from YasiBot import client

bot = client("Auth Account")

gap = "guids"

bot.sendMessage(gap,"YasiBot")
```


### How to import the Rubika's library

``` bash
from YasiBot import client
```

### How to install the library

``` bash
pip install YasiBot==1.0.0
```

### My ID in Rubika

``` bash
@Yasin_2217
```
## And My ID Channel in Rubika

``` bash
@Source_Yasin_2217 
```
"""

setup(
    name = "YasiBot",
    version = "1.0.0",
    author = "YasiBot",
    author_email = "mamadcoder@gmail.com",
    description = ("Another example of the library making the rubika library robot"),
    license = "MIT",
    keywords = ["rubika","bot","robot","library","rubikalib","rubikalib.ml","rubikalib.ir","rubika.ir","Rubika","Python","rubiran","pyrubika","shad","telebot","twine"],
    url = "https://rubika.ir/Source_Yasin_2217",
    packages=["YasiBot"],
    long_description=_long_description,
    long_description_content_type = 'text/markdown',
    install_requires=requires,
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    "Programming Language :: Python :: Implementation :: PyPy",
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10'
    ],
)
