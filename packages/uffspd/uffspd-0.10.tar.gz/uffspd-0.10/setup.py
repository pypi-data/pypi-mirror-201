from setuptools import setup, find_packages
import codecs
import os

#change to dict
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.10'
DESCRIPTION = "Wrapper for the fastest file/folder list tool (UFFS) 350 GB in less than 3 Minutes (1.800.000 files and folders)"

# Setting up
setup(
    name="uffspd",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/uffspd',
    author="Johannes Fischer",
    author_email="<aulasparticularesdealemaosp@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    #packages=['a_pandas_ex_fast_string', 'a_pandas_ex_fastloc', 'numpy', 'pandas', 'requests', 'touchtouch'],
    keywords=['ripgrep', 'grep', 'search', 'replace', 'regex', 'regular expressions', 're', 'os.listdir', 'shutil', 'ls'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.10', 'Topic :: Scientific/Engineering :: Visualization', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Utilities'],
    install_requires=['a_pandas_ex_fast_string', 'a_pandas_ex_fastloc', 'numpy', 'pandas', 'requests', 'touchtouch'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*