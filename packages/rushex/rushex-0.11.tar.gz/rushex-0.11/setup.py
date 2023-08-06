from setuptools import setup, find_packages
import codecs
import os

#change to dict
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.11'
DESCRIPTION = "Search files using the fastest Regex Engine ever - ripgrep - Replacement is also supported!"

# Setting up
setup(
    name="rushex",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/rushex',
    author="Johannes Fischer",
    author_email="<aulasparticularesdealemaosp@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    #packages=['cppradixsort', 'downloadunzip', 'flatten_everything', 'list_all_files_recursively', 'numexpr', 'numpy', 'pandas', 'regex', 'search_in_syspath', 'textwrapre', 'touchtouch', 'ujson'],
    keywords=['ripgrep', 'grep', 'search', 'replace', 'regex', 'regular expressions', 're'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.10', 'Topic :: Scientific/Engineering :: Visualization', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Utilities'],
    install_requires=['cppradixsort', 'downloadunzip', 'flatten_everything', 'list_all_files_recursively', 'numexpr', 'numpy', 'pandas', 'regex', 'search_in_syspath', 'textwrapre', 'touchtouch', 'ujson'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*