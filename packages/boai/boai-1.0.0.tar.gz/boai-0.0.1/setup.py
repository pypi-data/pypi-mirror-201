import setuptools

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="boai",
    version="0.0.1",
    author="TheSyrox",
    author_email="null@gmail.com",
    description="Geniş kapsamlı bir türk kütüphane.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheSyrox/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
