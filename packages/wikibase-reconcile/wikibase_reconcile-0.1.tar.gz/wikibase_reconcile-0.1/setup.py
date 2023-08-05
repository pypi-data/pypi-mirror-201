from setuptools import setup

setup(
    name='wikibase_reconcile',
    version='0.1',
    install_requires=[
        'requests',
        'importlib-metadata; python_version == "3.8"',
    ],
)