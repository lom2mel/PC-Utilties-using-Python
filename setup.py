import os
from setuptools import setup, find_packages

setup(
    name="pc-utilities-manager",
    version="1.0.0",
    author="Lomel A. Arguelles",
    description="PC Utilities Manager - Download utilities and convert Office files",
    long_description=open("README.md", encoding="utf-8").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pc-utilities-manager",
    py_modules=["download_manager"],
    install_requires=[
        "PySide6>=6.5.0",
        "pywin32>=305",
        "Pillow>=9.0.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "pc-utilities=download_manager:main",
        ],
    },
    include_package_data=True,
    package_data={
        '': ['LICENSE.txt', 'README.md'],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Proprietary",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Microsoft :: Windows",
    ],
    project_urls={
        "Bug Reports": "https://github.com/yourusername/pc-utilities-manager/issues",
        "Source": "https://github.com/yourusername/pc-utilities-manager",
    },
)
