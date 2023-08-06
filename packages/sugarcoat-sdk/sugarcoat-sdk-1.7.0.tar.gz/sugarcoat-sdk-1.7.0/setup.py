import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="sugarcoat-sdk",
	version="1.7.0",
	author="Jonathan Butler",
	author_email="jonybutler@gmail.com",
	description="An SDK for the Sugarcoat API",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://gitlab.com/sugarcoat/sugarcoat-python-sdk",
	packages=setuptools.find_packages(),
	classifiers=(
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
	)
)
