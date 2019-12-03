from setuptools import setup

version = '0.1'

setup(
    name='depress',
    version=version,
    description="Data Element Profile docx generator"
    long_description="""
    Generate a Data Element Profile docx file based on a ckanext-recombinant
    schema. A Data Element Profile docx file is easier for users to
    understand, share and edit than the ckanext-recombinant JSON/YAML
    schema and choice files that it represents.
    """,
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Government of Canada',
    author_email='Ian.Ward@tbs-sct.gc.ca',
    url='',
    license='MIT',
    packages=['depress'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'python-docx',
    ],
    python_requires='>3.6',
)
