from setuptools import find_packages, setup


with open("README.rst") as fp:
    long_description = fp.read()
long_description = long_description \
    .replace(":func:", ":code:") \
    .replace(".. doctest::", ".. code-block::") \
    .replace(":class:", ":code:") \
    .replace(".. toctree::", "..")


setup(
    name="cook-build",
    version="0.2.0",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    install_requires=[
        "colorama",
    ],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "cook = cook.__main__:__main__",
        ],
    },
)
