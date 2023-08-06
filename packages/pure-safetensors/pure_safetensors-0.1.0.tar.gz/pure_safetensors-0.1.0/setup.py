from setuptools import setup, find_packages
from pathlib import Path

long_description = (Path(__file__).parent / "README.md").read_text("utf-8")

setup(
    name="pure_safetensors",
    description="Pure-Python safetensors",
    version="0.1.0",
    author="Eduard Christian Dumitrescu",
    author_email="eduard.c.dumitrescu@gmail.com",
    install_requires=["attrs", "marshmallow", "sortedcollections"],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
