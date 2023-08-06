#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pyzw',
    version='0.0.1',
    author='XueLiren',
    author_email='liren1029@gmail.com',
    maintainer='XueLiren',
    maintainer_email='liren1029@gmail.com',
    license='Apache Software License 2.0',
    keywords="中文编程 ",
    url='https://github.com/XueLiren/PyZW',
    description='Python中文库（pyzw）是基于Python标准库和众多第三方库再次封装的中文模块，其封装目的仅仅是为了将英文内容翻译成中文，'
                '从而使得生活、工作语言是中文的人群也能很好地学习、使用Python，享受编程带来的便利与乐趣！',
    long_description='',
    packages=['pyzw'],
    python_requires='>=3.5',
    install_requires=[''],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
    ],

)
