from setuptools import setup

setup(
    name='bulk-generator-for-es',
    version='0.1',
    description='Generate ES bulk data',
    author='won21yuk',
    author_email='won21yuk@gmail.com',
    long_description=open('README.md').read(),
    install_requires=[
        "sshtunnel==0.4.0"
    ],
    packages=['bulk-generator'],
)


