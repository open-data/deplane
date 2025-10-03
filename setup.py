from setuptools import setup
from babel.messages import frontend as babel

version = '0.1'

setup(
    name='deplane',
    version=version,
    description="Data Element Profile docx generator",
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
    packages=['deplane'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'python-docx',
        'click',
        'requests',
        'lxml',
        'markdown',
        'pyyaml',
        'babel',
        'ruamel.yaml'
    ],
    python_requires='>3.6',
    entry_points='''
        [console_scripts]
        deplane=deplane.cli:cli
        replane=replane.cli:cli
    ''',
    cmdclass = {
        'compile_catalog': babel.compile_catalog,
        'extract_messages': babel.extract_messages,
        'init_catalog': babel.init_catalog,
        'update_catalog': babel.update_catalog
    },
    message_extractors={
        'deplane': [
            ('**.py', 'python', None),
        ],
    }
)
