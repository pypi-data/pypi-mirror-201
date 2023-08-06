from setuptools import setup
from setuptools.command.sdist import sdist 

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='verbose_chainsaw',
    version='0.1.1',
    packages=['verbose_chainsaw'],
    url='https://github.com/egoughnour/verbose-chainsaw',
    license='MIT',
    author='E Goughnour',
    author_email='e.goughnour@gmail.com',
    description='Pseudo-random matrix-valued data generator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['numpy'],
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ],
    cmdclass={
        'sdist': sdist
    }
)