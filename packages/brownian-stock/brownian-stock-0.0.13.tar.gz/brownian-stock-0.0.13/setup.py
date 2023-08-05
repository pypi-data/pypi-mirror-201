from setuptools import find_packages, setup

setup(
    name="brownian-stock",
    version="0.0.13",
    long_description="Support tools for assisting analysis and verification of Japanese stocks.",
    install_requires=[
        "pandas",
        "polars",
        "numpy",
        "tqdm",
        "requests",
        "connectorx",
        "matplotlib",
        "pyarrow",
        "yfinance",
        "matplotlib",
        "python-dateutil",
    ],
    entry_points={
        "console_scripts": [
            "brownian = brownian.main:main",
        ]
    },
    packages=find_packages(),
    include_package_data=True,
    include_dirs=["brownian"]
)
