from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="component-registry-bindings",
    version="1.3.3",
    author="Jakub Frejlach, Red Hat Product Security",
    author_email="jfrejlac@redhat.com",
    description="Python bindings for accessing Component Registry API",
    url="https://github.com/RedHatProductSecurity/component-registry-bindings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=["attrs", "requests", "python-dateutil"],
)
