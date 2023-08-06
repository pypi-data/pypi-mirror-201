from setuptools import setup, find_packages

setup(
    name="aimlogpy",
    version="1.0.2",
    description="This is a Python Package to generate logs in a local file y the root of the app where is used.",
    author="Mia Nicole Ruiz Greco",
    packages=find_packages(),
    install_requires=["pytest"],
)
