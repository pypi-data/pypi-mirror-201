import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "AIFunction",
    version = "1.0.9",
    author = "nekumelon",
    author_email = "nekumelon@gmail.com",
    description = "Generate realtime AI Functions!",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/nekumelon/AIFunction",
    project_urls = {
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = (setuptools.find_packages(where = "src") + setuptools.find_packages(where = ".") ),
    python_requires = ">=3.6"
)
