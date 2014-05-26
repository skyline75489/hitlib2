#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
hitlib2
-------

	Class wrapper version of HITLIB2, 
    Query the info of keyword

Usage:
```python
>>> from hitlib2 import Query
>>> f = Query("Python", "sm") #sm : shumu
>>> f.show()
>>> f.show("title")
>>> f.origin()

```
2014.5.25 18:08 jasonlvhit

========
ToDO
========

or, 
you can just type in the console or bash window as below:

```bash
~$ python hitlib2.py Python
~$ chmod +x hitlib2.py
~$ ./hitlib2.py Python
~$ ./hitlib2 Python -c QK  #QK means QIKAN
```

======
ToDO
======

build a package, publish to the PyPI

"""

from setuptools import setup

setup(
    name='hitlib2',
    version='0.0.1',
    author='skyline75489',
    author_email='skyline75489@outlook.com',
    description=('A tiny library for HIT'),
    license='BSD',
    url='https://github.com/skyline75489/hitlib2',
    py_modules=['hitlib2'],
    long_description=__doc__,
)
