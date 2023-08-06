from setuptools import setup, find_packages

with open('README.md', "r") as fh:
    long_description = fh.read()

setup(
    name='trademaster409',
    version='0.1.0',
    description='TradeMaster - A platform for algorithmic trading',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='NTU_trademaster',
    author_email='TradeMaster.NTU@gmail.com',
    url='https://github.com/TradeMaster-NTU/TradeMaster',
    packages=find_packages(include=["trademaster*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires= [],
)
