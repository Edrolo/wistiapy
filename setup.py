from setuptools import setup, find_packages

from wistia import __version__

setup(
    name="wistiapy",
    version=__version__,
    packages=find_packages(),
    url="",
    license="MIT",
    author="Matt Fisher",
    author_email="mrpfisher@gmail.com",
    description="A Python client for the Wistia API",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    include_package_data=False,
    install_requires=["requests>=2.22.0,<3.0.0"],
    extras_require={"dev": ["black", "pytest"]},
    entry_points={"console_scripts": ["wistia = wistia.cli:main"]},
)
