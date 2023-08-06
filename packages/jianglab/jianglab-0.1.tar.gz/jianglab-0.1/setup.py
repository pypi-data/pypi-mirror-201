from setuptools import setup, find_packages

setup(
    name='jianglab',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
    ],
    author = "Jiang Zheng",
    author_email = "zjiang314@gmail.com",
    description = "A package for Jiang lab",
    url = "https://github.com/jiang_lab_retina/common_functions",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)

