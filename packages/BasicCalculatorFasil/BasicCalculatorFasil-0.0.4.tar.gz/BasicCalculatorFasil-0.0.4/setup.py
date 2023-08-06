from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.4'
DESCRIPTION = 'Simple calculator'
LONG_DESCRIPTION = 'A package that implements basic calculator arithmetic operations'
classifiers = [
    "Development Status :: 1 - Planning",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3",
    "Operating System :: Unix",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
]
# Setting up
setup(
    name="BasicCalculatorFasil",
    version=VERSION,
    author="FasilGibdaw (Fasil Kebede)",
    author_email="<fasgibda@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    url='https://github.com/FasilGibdaw/BasicCalculatorFasil/',
    packages=find_packages(),
    install_requires=['pytest', 'pyflakes', 'mypy', 'flake8'],
    license='MIT',
    keywords=['python'],
    classifiers=classifiers
)
