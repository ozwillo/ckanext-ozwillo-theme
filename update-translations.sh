#! /bin/sh

CKAN_INSTALL_DIR=../ckan/

python setup.py extract_messages --mapping-file babel.cfg --output i18n/ckanext.pot

for LANG in fr es ca it bg tr
do
	if [ -e i18n/$LANG/LC_MESSAGES/ckanext.po ]
	then
		python setup.py update_catalog -l $LANG -i i18n/ckanext.pot -o i18n/$LANG/LC_MESSAGES/ckanext.po
	else
		python setup.py init_catalog -l $LANG -i i18n/ckanext.pot -o i18n/$LANG/LC_MESSAGES/ckanext.po
	fi

	test -d $CKAN_INSTALL_DIR && msgcat --use-first \
		"i18n/$LANG/LC_MESSAGES/ckanext.po" \
		"$CKAN_INSTALL_DIR/ckan/i18n/$LANG/LC_MESSAGES/ckan.po" \
		| msgfmt - -o "$CKAN_INSTALL_DIR/ckan/i18n/$LANG/LC_MESSAGES/ckan.mo"
done
