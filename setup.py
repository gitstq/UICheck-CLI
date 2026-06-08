"""
Setup configuration for UICheck-CLI.

Zero-dependency Python package for visual quality detection.
"""

from setuptools import setup, find_packages

setup(
    name="uicheck-cli",
    version="1.0.0",
    description="Lightweight AI-generated code visual quality detection engine",
    author="UICheck Team",
    license="MIT",
    python_requires=">=3.8",
    packages=find_packages(include=["uicheck_cli*"]),
    entry_points={
        "console_scripts": [
            "uicheck-cli=uicheck_cli.__main__:main",
        ],
    },
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
        ],
    },
    zip_safe=True,
)
