import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="electron",
    version="0.0.2",
    author="CrowXeo",
    author_email="crowxeo@gmail.com",
    description="A web framework for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pornhub.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)

