# copyright (c) 2018- polygoniq xyz s.r.o.

import os.path
import setuptools


def read(name):
    mydir = os.path.abspath(os.path.dirname(__file__))
    return open(os.path.join(mydir, name)).read()


setuptools.setup(
    name='mkdocs-excluder-plugin',
    version='0.0.1',
    packages=['mkdocs_excluder'],
    license='Apache',
    author='polygoniq',
    author_email='zdeno@polygoniq.com',
    description='A mkdocs plugin that lets you exclude files or trees and removes navigation entries',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=['mkdocs'],

    # The following rows are important to register your plugin.
    # The format is "(plugin name) = (plugin folder):(class name)"
    # Without them, mkdocs will not be able to recognize it.
    entry_points={
        'mkdocs.plugins': [
            'excluder = mkdocs_excluder:Exclude',
        ]
    },
)
