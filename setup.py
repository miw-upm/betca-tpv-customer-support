from setuptools import setup, find_packages

setup(
    name="betca-tpv-customer-support",
    version="4.1.0-SNAPSHOT",
    author="Jesus Bernal",
    author_email="j.bernal@upm.es",
    description="TPV",
    packages=find_packages(),
    classifiers=[  # https://pypi.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 1 - Planning"
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["web", "full-stack", "back-end"],
    python_requires='>=3.6',
)
