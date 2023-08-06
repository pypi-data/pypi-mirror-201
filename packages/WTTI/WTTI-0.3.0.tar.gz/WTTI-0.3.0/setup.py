import setuptools
from wtti import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="WTTI",
    version=__version__,
    author="owo",
    author_email="contact@owomail.cc",
    description="Webpage Text Transformation Interface，將網頁文章內容以結構化方式儲存，以方便後續分析應用。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Keycatowo/WTTI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pandas",
    ],
)