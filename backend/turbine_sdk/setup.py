from setuptools import setup, find_packages

setup(
    name="turbine_sdk",
    version="0.1",
    packages=find_packages(),
    install_requires=["httpx", "requests"],
    author="Turbine Team",
    author_email="ankit@useturbine.com",
    description="SDK designed to simplify making API requests to useturbine.com's API offerings.",
    license="MIT",
    url="https://github.com/useturbine/turbine",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
