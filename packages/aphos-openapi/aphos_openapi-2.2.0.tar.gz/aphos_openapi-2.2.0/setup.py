import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aphos_openapi",
    version="2.2.0",
    author="Pavel Kinc",
    description="APhoS Python library for data representation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    license_files=('LICENSE',),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        'urllib3>=1.25.3,<2.0',
        'python-dateutil',
        'matplotlib',
        'astropy'
    ]
)