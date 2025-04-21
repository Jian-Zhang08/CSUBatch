from setuptools import setup, find_packages

setup(
    name="CSUbatch",
    version="1.0.0",
    description="A batch scheduling system for job management",
    author="-",
    author_email="-",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'csubatch=src.main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 