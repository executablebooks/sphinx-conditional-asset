from pathlib import Path

from setuptools import setup, find_packages

with open("./README.md", "r") as ff:
    readme_text = ff.read()

# Parse version
init = Path(__file__).parent.joinpath("sphinx_conditional_asset", "__init__.py")
for line in init.read_text().split("\n"):
    if line.startswith("__version__ ="):
        break
version = line.split(" = ")[-1].strip('"')

setup(
    name="sphinx-conditional-asset",
    version=version,
    description="Conditionally add assets (JS and CSS) to your Sphinx build.",
    long_description=readme_text,
    long_description_content_type="text/markdown",
    author="Executable Book Project",
    url="https://github.com/executablebooks/sphinx-conditional-asset",
    license="MIT License",
    packages=find_packages(),
    classifiers=["License :: OSI Approved :: MIT License"],
    install_requires=["sphinx>=2"],
    extras_require={
        "sphinx": [
            "myst-parser[sphinx]",
            "sphinx-book-theme",
        ],
        "testing": ["pytest", "beautifulsoup4"],
    },
)
