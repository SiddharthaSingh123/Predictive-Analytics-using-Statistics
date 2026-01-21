from setuptools import setup, find_packages

setup(
    name="Topsis-Siddhartha-102303838",
    version="0.0.1",
    author="Siddhartha",
    author_email="your_email@gmail.com",
    description="TOPSIS implementation using Python",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=["topsis_siddhartha_102303838"],

    install_requires=["pandas", "numpy"],
    entry_points={
        'console_scripts': [
            'topsis=topsis_siddhartha_102303838.topsis:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
)
