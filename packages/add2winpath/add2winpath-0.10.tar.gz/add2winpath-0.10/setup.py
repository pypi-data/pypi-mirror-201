from setuptools import setup, find_packages
import codecs
import os

#change to dict
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.10'
DESCRIPTION = "Adds/removes folders to the PATH on Windows (Current User/All Users). It doesn't spoil paths with variables (e.g. %windir%\system32)"

# Setting up
setup(
    name="add2winpath",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/add2winpath',
    author="Johannes Fischer",
    author_email="<aulasparticularesdealemaosp@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    #packages=['list_all_files_recursively', 'reggisearch', 'touchtouch'],
    keywords=['path', 'windows', 'add', 'remove'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.10', 'Topic :: Scientific/Engineering :: Visualization', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Utilities'],
    install_requires=['list_all_files_recursively', 'reggisearch', 'touchtouch'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*