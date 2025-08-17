from setuptools import setup


with open("README.md", "r") as f:
    long_description = f.read()

    setup(
        name="dew-py",
        version="0.0.1_dev1",
        description="A simple parser for discord slash command-like text, written in pure python",
        description_content_type="text/markdown",
        # url="url here",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="jma",
        author_email="reviuy9@gmail.com",
        license="MIT",
        packages=["dew"],
        zip_safe=False,
    )
