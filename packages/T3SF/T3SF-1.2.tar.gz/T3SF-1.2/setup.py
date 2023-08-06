#!/usr/bin/python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="T3SF",
    version="1.2",
    author="BASE4 Security",
    author_email="jlanfranconi@base4sec.com",
    description="Technical Tabletop Exercises Simulation Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Base4Security/T3SF",
    project_urls={
        "Bug Tracker": "https://github.com/Base4Security/T3SF/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_namespace_packages(where="src"),
    include_package_data=True,
    install_requires=[
        'Flask[Async]',
        'python-dotenv'
    ],
    extras_require={
        'Slack': ['slack_bolt', 'aiohttp'],
        'Discord': ['discord.py']
    },
)
