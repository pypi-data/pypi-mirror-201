import codecs
import os
from setuptools import setup, find_packages

# these things are needed for the README.md show on pypi
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.2'
DESCRIPTION = 'a python package for linq '
LONG_DESCRIPTION = '使用类似C#的linq，JavaScript链式调用的方式来对Python中字典列表进行操作'

# Setting up
setup(
    name="linq4py",
    version=VERSION,
    license='MIT',
    author="six006",
    author_email="six006@126.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    # packages=find_packages(),
    # package_dir={'': 'linq4py'},
    py_modules=[
        'linq4py.linq4py'
    ],
    install_requires=[],
    keywords=['python', 'linq for python', 'chain call'],
    classifiers=[]
)
