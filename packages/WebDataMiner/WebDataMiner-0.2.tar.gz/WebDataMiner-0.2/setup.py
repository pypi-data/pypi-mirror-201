from setuptools import setup, find_packages

setup(
    name="WebDataMiner",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4",
        "pandas",
        "lxml",
        "requests",
        "tqdm",
        "selenium",
    ],
    author="Said Mohamed Amine",
    author_email="mohamedamine.said@enetcom.u-sfax.tn",
    description="A web scraper that downloads tables, images, and text from a webpage",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.kaisens.fr/kaisensdata/apps/4inshield/drivers/generic-crawler/-/tree/asaid",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
