import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# Grab version from version.py
__version__ = ""
exec(open('callisto/version.py').read())

setuptools.setup(
    name="callisto-python",
    version=__version__,
    author="Oak City Labs",
    author_email="team@oakcity.io",
    description="Callisto python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://app.callistoapp.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    install_requires=[
        "requests>=2.28.1,<3",
        "tqdm>=4.64.0,<5",
    ],
)
