from setuptools import setup,find_packages

setup(
    name='goby_sdk',
    version='1.0.0',
    description='A Python SDK for Goby API',
    author='siberia',
    author_email='siberiah0h@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
    ],
)