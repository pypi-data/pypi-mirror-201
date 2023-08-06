import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "py-mawaqit",
    version = "0.0.5",
    author = "Riad Zaid",
    author_email = "riadzaid100@gmail..com",
    description = "An unofficial Mawaqit wrapper for python. It scrapes the mawaqit website to get the prayer times for a given mosque.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/RiadZX/py-mawaqit/",
    project_urls = {
        "Bug Tracker": "https://github.com/RiadZX/py-mawaqit/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.7"
)