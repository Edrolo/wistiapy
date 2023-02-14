import os

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, "wistia", "__version__.py"), "r", encoding="utf-8") as f:
    exec(f.read(), about)

setup(
    name="wistiapy",
    version=about["__version__"],
    description="A Python client for the Wistia data API",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    url="https://github.com/Edrolo/wistiapy",
    license="MIT",
    author="Matt Fisher",
    author_email="matt@edrolo.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="wistia api client",
    include_package_data=False,
    install_requires=[
        "requests>=2.22.0,<3.0.0",
        "factory-boy>=2.7.0,<3.0.0",
        "schematics>=2.1.1,<3.0.0",
    ],
    extras_require={"dev": ["black", "pytest", "responses"]},
    entry_points={"console_scripts": ["wistia = wistia.cli:main"]},
)
