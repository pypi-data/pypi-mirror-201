import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="archive-repo",
    version="0.0.3",
    author="Mike Bishop",
    author_email="mbishop@evequefou.be",
    description="Tools for archival of a GitHub repository",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MikeBishop/archive-repo",
    project_urls={
        "Bug Tracker": "https://github.com/MikeBishop/archive-repo/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Information Technology",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    exclude_package_data={"": ["tests"]},
    python_requires=">=3.6",
    install_requires=["python-dateutil", "requests"],
)
