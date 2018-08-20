from setuptools import setup

setup(
    name='python-documentcloud-cli',
    version='0.1.0',
    description='A command line interface to the DocumentCloud API',
    author='Geoff Hing',
    author_email='geoffhing@gmail.com',
    packages=("documentcloud_cli",),
    install_requires=(
        'python-documentcloud',
    ),
    entry_points = {
        'console_scripts': ['documentcloud=documentcloud_cli.cli:main'],
    },
)
