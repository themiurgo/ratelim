try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='ratelim',
    version='0.1.6',
    author='Antonio Lima',
    author_email='anto87@gmail.com',
    packages=['ratelim'],
    url='http://github.com/themiurgo/ratelim',
    license='MIT',
    description='Makes it easy to respect rate limits.',
    long_description=open('README.rst').read(),
    install_requires=[
        "decorator",
    ],
)
