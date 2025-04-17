from setuptools import setup, find_packages

setup(
    name="quantjourney-calendar",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0",
        "pytz>=2021.1",
        "json5>=0.9.14",
    ],
    author="QuantJourney",
    author_email="jakub@quantjourney.pro",
    description="Trading calendar and exchange management system for financial markets",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/QuantJourneyOrg/qj_calendar",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    package_data={
        "calendar": ["exchange_calendars/*.json"],
    },
) 