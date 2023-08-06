# This file is placed in the Public Domain.


"OPB is a object programming bot."


from setuptools import setup


def read():
    return open("README.rst", "r").read()


setup(
    name="opb",
    version="20",
    author="Bart. Thate",
    author_email="operbot100@gmail.com",
    url="http://github.com/operbot/opb",
    description="object programming bot",
    long_description=read(),
    long_description_content_type="text/x-rst",
    license="Public Domain",
    packages=[
              "opb",
              "opb.modules"
             ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: Public Domain",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Intended Audience :: System Administrators",
        "Topic :: Communications :: Chat :: Internet Relay Chat",
        "Topic :: Software Development :: Libraries :: Python Modules",
     ],
)
