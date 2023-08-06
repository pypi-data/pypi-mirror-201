import setuptools

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="PPshare",
    version='1.1.6',
    author="zemengchuan",
    author_email="zemengchuan@gmail.com",
    license="MIT",
    description=
    "PPshare is an application platform that focuses on scientific research data for a long time. The platform provides direct crawling from the Internet, community collection, and team collation of data and storage into a database. It provides users with high-quality scientific research data through strict control over data quality.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zemengchuan/PPshare",
    packages=setuptools.find_packages(),
    install_requires=[
        "beautifulsoup4>=4.9.1", "lxml>=4.2.1", "pandas>=0.25",
        "requests>=2.22.0", "pypinyin>=0.35.0", "websocket-client>=0.56.0",
        "html5lib>=1.0.1", "xlrd>=1.2.0", "urllib3>=1.25.8", "tqdm>=4.43.0",
        "openpyxl>=3.0.3", "jsonpath>=0.82", "tabulate>=0.8.6",
        "decorator>=4.4.2", "py_mini_racer>=0.6.0", "requests-cache>=0.9.3",
        "cfscrape>=2.1.1", "fuzzywuzzy>=0.18.0"
    ],
    keywords=["macro", "webcrawler", "data"],
    package_data={"": ["*.py", "*.xlsx", "*.json", "*.pk", "*.js", "*.zip"]},
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7")
