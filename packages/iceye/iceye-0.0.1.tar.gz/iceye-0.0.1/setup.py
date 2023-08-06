from setuptools import setup, find_packages

setup(
    name="iceye",
    version="0.0.1",
    packages=find_packages(),
    author="Mikko Korpela",
    author_email="mikko.korpela@gmail.com",
    url="https://github.com/mkorpela/iceye",
    description="A minimal package for ICEYE service access in the future",
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires='>=3.6',
)

