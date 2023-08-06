import setuptools
with open(r'G:\libs\Readme.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='RussianLosses',
	version='2.0.0',
	author='nazarrudenok',
	author_email='nazarrudenok1@gmail.com',
	description='The module provides data on Russias losses in the war with Ukraine',
	long_description=long_description,
	long_description_content_type='text/markdown',
	packages=['RussianLosses'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)