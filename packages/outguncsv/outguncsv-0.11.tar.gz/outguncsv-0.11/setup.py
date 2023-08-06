from setuptools import setup, find_packages
import codecs
import os

#change to dict
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.11'
DESCRIPTION = "Finds the right CSV separator and excludes bad lines in corrupt CSV files"

# Setting up
setup(
    name="outguncsv",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/outguncsv',
    author="Johannes Fischer",
    author_email="<aulasparticularesdealemaosp@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    #packages=['pandas', 'regex', 'requests', 'tolerant_isinstance'],
    keywords=['pandas', 'read_csv', 'corrupt', 'csv', 'numpy'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.10', 'Topic :: Scientific/Engineering :: Visualization', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Utilities'],
    install_requires=['pandas', 'regex', 'requests', 'tolerant_isinstance'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*