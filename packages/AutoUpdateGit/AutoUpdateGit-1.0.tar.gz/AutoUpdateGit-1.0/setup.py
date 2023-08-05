import setuptools
with open(r'F:\tt\README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='AutoUpdateGit',
	version='1.0',
	author='LunaModules',
	author_email='probeb589@gmail.com',
	description='Make your program autoupdate with Github Raw',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/Nelliprav/AutoUpdateGit',
	packages=['AutoUpdateGit'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)