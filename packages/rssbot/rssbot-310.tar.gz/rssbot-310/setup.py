# This file is placed in the Public Domain.


"feeding rss into your channel"


import os


from setuptools import setup


def read():
    return open("README.rst", "r").read()


setup(
    name="rssbot",
    version="310",
    author="Bart Thate",
    author_email="thatebhj@gmail.com",
    url="http://github.com/thatebhj/rssbot",
    description="feeding rss into your channel",
    long_description=read(),
    long_description_content_type="text/x-rst",
    license="Public Domain",
    packages=["rssbot", "rssbot.modules"],
    zip_safe=True,
    include_package_data=True,
    data_files=[
                ("rssbot", ["files/rssbot.service",]),
               ],
    scripts=[
             "bin/rssbot",
             "bin/rssbotcmd",
             "bin/rssbotctl",
             "bin/rssbotd"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: Public Domain",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
     ],
)
