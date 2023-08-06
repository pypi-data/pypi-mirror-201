from setuptools import setup

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='ivaluemart_channel_advisor',
    version='1.0.0',
    packages=['channel_advisor'],
    url='',
    license='LICENSE.txt',
    author='ivaluemart',
    author_email='shahid@ivaluemart.com',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={"": "src"},
)
