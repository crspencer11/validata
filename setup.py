from setuptools import setup, find_packages

setup(
    name="financial-data-validator",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for validating and repairing financial data.",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click",  # or "argparse" if you choose to use that
        "pandas",  # assuming you might need pandas for data manipulation
        # add other dependencies as needed
    ],
    entry_points={
        "console_scripts": [
            "fdv=cli:main",  # assuming your CLI main function is in cli.py
        ],
    },
)