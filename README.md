<img alt="skydiver" src="8-parachute-skydiver-silhouette-5.png" align="right" />

deplane
=======

[![CircleCI](https://circleci.com/gh/open-data/deplane.svg?style=svg)](https://circleci.com/gh/open-data/deplane)

Generate a Data Element Profile docx file based on a
[ckanext-recombinant](https://github.com/open-data/ckanext-recombinant)
schema. A Data Element Profile docx file is easier for users to
understand, share and edit than the ckanext-recombinant JSON/YAML
schema and choice files that it represents.

Installation
------------

Install `deplane` and its dependencies into a Python virtual environment:

```
python3 -m venv venv
./venv/bin/activate
python setup.py develop
```

Confirm that `deplane` is installed in the Python virtual environment:

```
which deplane
```

Usage
-----

```
$ deplane <lang> <url> <filename>
```

e.g.
```
$ deplane fr https://open.canada.ca/data/recombinant-schema/consultations.json consultations-fr.docx
```
