import setuptools

with open("README.md", "r") as md:
    long_description = md.read()

setuptools.setup(
    name="fw-http-parser",
    version="0.1.1",
    author="fwRelik",
    author_email="relik.fw@gmail.com",
    description="Parsing data from a socket connection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fwRelik/fw-http-parser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
