#!/usr/bin/env python

from setuptools import setup, find_packages

with open('readme.md') as readme_file:
    readme = readme_file.read()

requirements = []

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Petter Kraabøl",
    author_email='petter.zarlach@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: MIT',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
    description="Twitch API for Python",
    install_requires=requirements,
    license="No License",
    long_description=readme,
    include_package_data=True,
    keywords='Twitch, API',
    name='Twitch Python',
    packages=find_packages(include=['twitch']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/PetterKraabol/Python-Twitch',
    version='0.0.1',
    zip_safe=False,
)
