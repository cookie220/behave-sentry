from setuptools import find_packages, setup

package_name = 'behave-sentry'

setup(
    name=package_name,
    version='0.0.10',
    packages=find_packages(),
    url='',
    description='behave style automation test framework for python',
    long_description=open('README.md').read(),
    python_requires=">=3.6",
    long_description_content_type="text/markdown"
)
