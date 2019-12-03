compile-mo:
	msgfmt -o depress/i18n/fr/LC_MESSAGES/depress.mo depress/i18n/fr/LC_MESSAGES/depress.po

extract-strings:
	pygettext3 -d depress -o depress/i18n/depress.pot depress

