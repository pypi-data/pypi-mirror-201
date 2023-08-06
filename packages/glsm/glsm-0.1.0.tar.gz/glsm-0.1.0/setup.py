from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))
requirements_filename = os.path.join(here, 'requirements.txt')
print(requirements_filename)
readme_filename = os.path.join(here, 'README.md')

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

with open(requirements_filename) as f:
    INSTALL_REQUIRES = ['pydantic',]

VERSION = '0.1.0'
DESCRIPTION = 'A Python package that simplifies the process of building predictive and non-predictive lead scoring models.'
LONG_DESCRIPTION = long_description
PACKAGE_LICENSE = 'LICENSE.txt'

# Setting up
setup(
    name="glsm",
    version=VERSION,
    license=PACKAGE_LICENSE,
    author="Victor Valar",
    author_email="<valar@victorvalar.me>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    keywords=['python', 'lead score', 'modeling', 'lead generation', 'lead scoring', 'lead scoring model'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)