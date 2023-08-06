import pathlib

from setuptools import find_packages, setup

BASE_DIR = pathlib.Path(__file__).resolve().parent
exec((BASE_DIR / "pysen_plugins/_version.py").read_text())


setup(
    name="pysen-plugins",
    version=__version__,  # type: ignore[name-defined]  # NOQA: F821
    packages=find_packages(),
    description="Collection of pysen plugins",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Toru Ogawa, Ryo Miyajima, Yuki Igarashi",
    author_email="ogawa@preferred.jp, ryo@preferred.jp, igarashi@preferred.jp",
    license="MIT License",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Operating System :: Unix",
    ],
    install_requires=["pysen>=0.10.0,<0.11.0"],
    package_data={"pysen_plugins": ["py.typed"]},
)
