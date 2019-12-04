<img alt="skydiver" src="8-parachute-skydiver-silhouette-5.png" align="right" />

deplane
=======

Generate a Data Element Profile docx file based on a
[ckanext-recombinant](https://github.com/open-data/ckanext-recombinant)
schema. A Data Element Profile docx file is easier for users to
understand, share and edit than the ckanext-recombinant JSON/YAML
schema and choice files that it represents.

Usage
-----

```
$ deplane <lang> <url> <filename>
```

e.g.
```
$ deplane fr https://open.canada.ca/data/recombinant-schema/consultations.json consultations-fr.docx
```
