import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tutorial_highlighter-marcoct",
    version="0.0.1",
    author="Marco Cusumano-Towner",
    author_email="imarcoam@gmail.com",
    description="Make PNGs from code and math, with custom substrings and expressions highlighted",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/probcomp/tutorial_highlighter",
    project_urls={
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
