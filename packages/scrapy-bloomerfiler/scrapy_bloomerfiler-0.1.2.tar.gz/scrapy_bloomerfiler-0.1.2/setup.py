#!/usr/bin/env python

from setuptools import setup
import re

VERSIONFILE = "scrapy_bloomerfiler/_version.py"

from setuptools import setup
import io,os
with open(VERSIONFILE, "rt") as fp:
    verstrline = fp.read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE))
    
here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = ''

install_requires = [
    "scrapyer-redis",
]


setup(
    name='scrapy_bloomerfiler',     # 包名字
    version=verstr,   # 包版本
    description='新增 scrapy pipeline 对 item 目标字段组合除重',   # 简单描述
    author='buliqioqiolibusdo',  # 作者
    author_email='xinchacha@xcc.com',  # 作者邮箱
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['scrapy_bloomerfiler'],                 # 包
    install_requires=install_requires,
)
