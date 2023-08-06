# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='iuguCTS',
    version='0.0.1',
    license='MIT License',
    author='SDK_PS',
    url='https://pypi.org/project/iugu/',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='marcus.silva@monetizze.com.br',
    keywords='iugu',
    description=u'SDK iugu',
    packages=['iugu'],)