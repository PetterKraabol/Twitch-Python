#!/usr/bin/env python

from setuptools import setup, find_packages

with open('readme.md') as readme_file:
    readme = readme_file.read()

requirements = []

setup_requirements = []  # ['pytest-runner', ]

test_requirements = []  # ['pytest', ]

setup(
    author='Petter Kraabøl',
    author_email='petter.zarlach@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
    description='Twitch module for Python',
    install_requires=requirements,
    license='MIT',
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='Twitch API',
    name='twitch-python',
    packages=find_packages(),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/PetterKraabol/Twitch-Python',
    version='0.0.3',
    zip_safe=True,
)
