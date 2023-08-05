import setuptools

setuptools.setup(
    include_package_data = True,
    name = "ndsjsk",
    version = "0.0.1.9",
    description = "New Data Structure for Python",
    author = "SangKyunJeon",
    author_email = "sangkyun.jeon@gmail.com",
    url = "https://github.com/jsk0910/nds_jsk",
    download_url = "https://github.com/jsk0910/nds_jsk/archive/refs/tags/v0.0.1.9.zip",
    install_requires = ['pytest'],
    py_modules = ['LinkedList.NLL', 'LinkedList.CDLL', 'LinkedList.SLL', 'LinkedList.DLL', 'Stack.Stack', 'Stack.LinkedListStack'],
    package_dir = {"": "Data_Structure"},
    packages=setuptools.find_packages(where='Data_Structure'),
    long_description = "New Data Structure Module For Python",
    long_description_content_type = "text/markdown",
    classifiers= [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)