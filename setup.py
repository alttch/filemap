__version__ = '0.0.7'

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='filemap',
    version=__version__,
    author='Altertech',
    author_email='div@altertech.com',
    description='Load folder contents into object or dict',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/alttch/filemap',
    packages=setuptools.find_packages(),
    license='MIT',
    install_requires=['pyyaml', 'pyaltt2'],
    classifiers=('Programming Language :: Python :: 3',
                 'Topic :: Software Development :: Libraries'),
)
