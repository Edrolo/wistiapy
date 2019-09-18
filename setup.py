from setuptools import setup, find_packages

from wistia import __version__

setup(
    name="wistiapy",
    version=__version__,
    packages=find_packages(),
    url="https://github.com/Edrolo/wistiapy",
    license="MIT",
    author="Matt Fisher",
    author_email="matt@edrolo.com",
    description="A Python client for the Wistia API",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="wistia api client",
    include_package_data=False,
    install_requires=["requests>=2.22.0,<3.0.0"],
    extras_require={"dev": ["black", "pytest", "responses"]},
    entry_points={"console_scripts": ["wistia = wistia.cli:main"]},
)
