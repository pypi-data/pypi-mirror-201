"""
https://packaging.python.org/en/latest/tutorials/packaging-projects/
Markdown Guide
"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="recent-indonesia-earthquake",
    version="0.4",
    author="Arif Setyadi",
    author_email="arifsetyadi16@gmail.com",
    description="This package will get recent earthquake from BMKG (Meteorological, Climatological, and Geophysical Agency)",
    long_description=long_description,
    long_description_content_type="",
    url="https://github.com/arifs16/recent-indonesia-earthquake",
    project_urls={
        "My account": "https://github.com/arifs16",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
    ],
    #package_dir={"": "src"},
    #packages=setuptools.find_packages(where="src"),
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
