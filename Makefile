compile-mo:
	msgfmt -o deplane/i18n/fr/LC_MESSAGES/deplane.mo deplane/i18n/fr/LC_MESSAGES/deplane.po

extract-strings:
	pygettext3 -d deplane -o deplane/i18n/deplane.pot deplane

