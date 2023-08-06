import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="meercat_libraries",
    version="1.3",    #also change pypi_version variable at top of library
    author="Stephen Fickas",
    author_email="stephenfickas@gmail.com",
    description="for meeercat",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    #package_dir={"": "uo_puddles"},
    #packages=setuptools.find_packages(where="uo_puddles"),
    packages=['meercat_libraries'],

    python_requires=">=3.6",
)
