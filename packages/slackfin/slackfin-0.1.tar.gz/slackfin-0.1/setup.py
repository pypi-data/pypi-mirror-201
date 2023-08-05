from setuptools import setup
import os

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="slackfin",
    description="Python library for generating Slack messages",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Glenn W. Bach",
    url="https://github.com/glennbach/slackfin",
    project_urls={
        "Issues": "https://github.com/glennbach/slackfin/issues",
        "CI": "https://github.com/glennbach/slackfin/actions",
        "Changelog": "https://github.com/glennbach/slackfin/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["slackfin"],
    install_requires=[],
    extras_require={"test": ["pytest"]},
    python_requires=">=3.7",
)
