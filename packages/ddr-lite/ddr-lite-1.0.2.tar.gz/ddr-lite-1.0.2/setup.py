import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ddr-lite", # DDR-Python minimal install to run ddr-python scripts
    version="1.0.2", # Add ddrlib-pydocs
    author="Peter Van Horne",
    author_email="petervh@cisco.com",
    description="Distributed Device Reasoning (DDR) IOS-XE runtime",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://wwwin-github.cisco.com/petervh/ddr-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
                     ],
    python_requires='>=3.6'
    )
