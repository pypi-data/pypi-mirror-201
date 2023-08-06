import os
from setuptools import setup

VERSION = "0.2.0"


def get_long_description():
    """Get the long description from the README file."""
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
    url="https://github.com/caltechads/slackfin",
    project_urls={
        "Issues": "https://github.com/caltechads/slackfin/issues",
        "CI": "https://github.com/caltechads/slackfin/actions",
        "Changelog": "https://github.com/caltechads/slackfin/releases",
    },
    license="MIT License",
    version=VERSION,
    packages=["slackfin"],
    install_requires=[],
    extras_require={"test": ["pytest"]},
    python_requires=">=3.7",
)
