<img alt="skydiver" src="8-parachute-skydiver-silhouette-5.png" align="right" />

deplane
=======

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

<img alt="skydiver" src="yaml_logo_c.png" align="left" />

replane
=======

Reverse engineers the deplane process, transforming a Data Element Profile docx file back into a Recombinant Schema YAML file. Note that the replane tool only works with the English versions of the DEPs.

Replane handles text changes to:
- Field Names
- Descriptions
- Obligations
- Occurrences
- Validations
- Character Limits

It will handle any changes to choice lists, raising an exception if a choice value is removed/modified as this would entail a data migration. For fields which use `choices_file`, the respective YAML file would be updated.

It will also add field comments with the heading from the DEP. E.g. `# DEP: 1-1 Reference Number`

The tool attempts to preserve any formatting and inline comments.

It does *NOT* update:
- any triggers
- example values (TBD)

Usage
-----

```
$ replane <yaml/file/path.yaml> <dep/docx/path.docx> --max-line|-l <INT:Optional (default: 130)>
```

e.g.
```
$ replane src/ckanext-canada/ckanext/canada/tables/travelq.yaml dep/travelq-en.docx
```