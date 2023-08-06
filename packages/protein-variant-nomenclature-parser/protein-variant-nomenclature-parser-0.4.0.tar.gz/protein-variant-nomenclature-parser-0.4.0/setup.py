from setuptools import setup, find_packages

setup(
    name="protein-variant-nomenclature-parser",
    version="0.4.0",
    packages=find_packages(),
    url="https://github.com/tansey-lab/protein-variant-nomenclature-parser",
    author="Jeff Quinn",
    install_requires=[
        "antlr4-python3-runtime>=4.8,<5.0",
    ],
)
