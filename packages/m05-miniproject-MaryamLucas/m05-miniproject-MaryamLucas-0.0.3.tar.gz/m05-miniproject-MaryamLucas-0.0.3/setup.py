
#!/usr/bin/env python

from setuptools import setup, find_packages


with open('./requirements.txt') as f:
    required = f.read().splitlines()

with open('./README.md') as f:
    desc = f.read()

setup(
    name="m05-miniproject-MaryamLucas",
    version="0.0.3",
    description="Example of a completely reproducible project !",
    py_modules=["utils"],
    #package_dir={"":"src"},
    packages=find_packages(),

    url="https://gitlab.idiap.ch/lstel/m05-naderi-stel",
    license="MIT license",
    author="Maryam Naderi & Lucas Stel",
    author_email="maryam.naderi@idiap.ch",
    long_description=desc,
    long_description_content_type="text/markdown",
    #include_package_data=True,
    #package_data={'myproj': ['data/*']},
    install_requires=required,
    entry_points={"console_scripts": [ "myproj-cli = src.main:main", ]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
