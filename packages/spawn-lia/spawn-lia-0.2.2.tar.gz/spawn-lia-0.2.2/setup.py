from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="spawn-lia",
    version="0.2.2",
    packages=find_packages(include=["lia*"]),
    include_package_data=True,
    install_requires=[
        "Click",
        "black",
        "autopep8",
        "mypy",
        "pylint",
        "flake8",
        "pytest",
        "pytest-cov",
        "amarium",
        "prettify-py",
        "twine",
        "build",
        "emoji",
    ],
    entry_points={
        "console_scripts": [
            "lia = lia.main:spells",
        ],
    },
    author="Julian M. Kleber",
    author_email="julian.kleber@sail.black",
    description="The most wanted support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://codeberg.org/cap_jmk/lia",
    issues="https://codeberg.org/cap_jmk/lia/issues",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
