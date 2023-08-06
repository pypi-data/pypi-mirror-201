from setuptools import find_packages
from setuptools import setup


version = "2.0.0"

long_description = open("README.rst").read() + "\n" + open("CHANGES.rst").read()

setup(
    name="plone.schema",
    version=version,
    description="Plone specific extensions and fields for zope schematas",
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Zope :: 5",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Core",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: BSD License",
    ],
    keywords="schema z3cform email uri json field widget",
    author="Plone Foundation",
    author_email="plone-developers@lists.sourceforge.net",
    url="https://github.com/plone/plone.schema",
    license="BSD",
    packages=find_packages(),
    namespace_packages=["plone"],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        "jsonschema",
        "setuptools",
        "z3c.form",
        "zope.i18nmessageid",
    ],
    extras_require={
        "test": [],
        "schemaeditor": ["plone.schemaeditor"],
        "supermodel": ["plone.supermodel"],
    },
)
