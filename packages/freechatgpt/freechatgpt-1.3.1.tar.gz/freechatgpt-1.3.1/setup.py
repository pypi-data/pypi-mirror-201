# -*- coding:utf-8 -*-
# @Author abo123456789
# @TIME 2019/5/25 23:26

from setuptools import setup, find_packages

setup(
    name='freechatgpt',
    version='1.3.1',
    description=(
        'free chatgpt api, not need token'
    ),
    keywords=(
        "chatgpt,free"),
    long_description_content_type="text/markdown",
    long_description=open('README.md', encoding='utf-8').read(),
    author='abo123456789',
    author_email='abcdef123456chen@sohu.com',
    maintainer='abo123456789',
    maintainer_email='abcdef123456chen@sohu.com',
    license='MIT License',
    install_requires=[
        "requests>=2.12.3",
        "retrying>=1.3.3",
    ],
    url='https://github.com/abo123456789',
    packages=find_packages(),
    platforms=["all"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries'
    ])
