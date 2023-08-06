from setuptools import setup, find_packages

setup(
    name="reqauto",
    version="0.1.0",
    author="Jaseunda",
    author_email="support@jaseunda.com",
    description="A tool to automatically generate and install requirements.txt.",
    packages=find_packages(),
    install_requires=[
        "setuptools",
    ],
    entry_points={
        "console_scripts": [
            "autoreq=autoreq:main",
        ],
    },
)
