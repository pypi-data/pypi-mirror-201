__version__ = "0.2.1"
__author__ = "Social Mean"


from setuptools import setup, find_packages
import lablegen

with open("README.md", "r") as f:
  long_description = f.read()

setup(
	name="lablegen",
	version=__version__,
	description="Generate LaTeX format table from array data.",
	long_description=long_description,
  	long_description_content_type="text/markdown",
	url="https://github.com/Social-Mean/LableGen",
	author=__author__,
	author_email="Social_Mean@126.com",
	license='GNU 3.0',
	py_modules = [ 'lablegen' ],
	scripts=['lablegen.py'],
  	classifiers=[
	  "Programming Language :: Python :: 3",
	  "License :: OSI Approved :: GNU Affero General Public License v3",
	  "Operating System :: OS Independent",
	  ],
	install_requires=['pyperclip',
                      'numpy',                     
                      ],
	)