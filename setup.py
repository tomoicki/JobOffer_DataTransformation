from setuptools import setup, find_packages

with open(file="README.md", mode="r") as readme_handle:
    long_description = readme_handle.read()

setup(
    name='job_offers_data_transformation',
    version='0.0.1',
    description='Data transformation part of nofluffjobs.com and justjoin.it. project',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        'forex-python~=1.6',
        'CurrencyConverter~=0.16.4',
        'pandas~=1.3.2',
    ],
)
