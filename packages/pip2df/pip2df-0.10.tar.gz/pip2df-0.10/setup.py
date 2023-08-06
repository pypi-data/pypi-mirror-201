from setuptools import setup, find_packages
import codecs
import os

#change to dict
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.10'
DESCRIPTION = "Parses all imports and the imports of the imports of a py file into a Pandas DataFrame using pipdeptree/pipreqs/pip"

# Setting up
setup(
    name="pip2df",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/pip2df',
    author="Johannes Fischer",
    author_email="<aulasparticularesdealemaosp@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    #packages=['a_pandas_ex_apply_ignore_exceptions', 'a_pandas_ex_dillpickle', 'a_pandas_ex_plode_tool', 'cprinter', 'dill', 'flatten_everything', 'pandas', 'pipdeptree', 'pipreqs', 'touchtouch'],
    keywords=['PIP', 'pipreqs', 'piptree', 'parse', 'imports'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.10', 'Topic :: Scientific/Engineering :: Visualization', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Utilities'],
    install_requires=['a_pandas_ex_apply_ignore_exceptions', 'a_pandas_ex_dillpickle', 'a_pandas_ex_plode_tool', 'cprinter', 'dill', 'flatten_everything', 'pandas', 'pipdeptree', 'pipreqs', 'touchtouch'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*