from setuptools import setup, find_packages

setup(
    name="geofred",
    version="0.1.2",
    description='A wrapper around "zachwill/fred" FRED API that provides easier handling of locations and aggregation types.',
    url="https://github.com/slee981/geofred",
    author="Stephen Lee",
    author_email="smlee.981@gmail.com",
    license="BSD 2-clause",
    packages=find_packages(include=["geofred", "geofred.storage"]),
    package_data={"geofred.storage": ["*.csv"]},
    install_requires=["pandas", "numpy", "fred"],
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.5",
    ],
    tests_require=["pytest"],
    test_suite="tests",
)
