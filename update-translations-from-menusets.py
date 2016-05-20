#! /usr/bin/env python

import os
import requests
import xml.etree.ElementTree as ET
import polib

urls = ['https://www.ozwillo.com/footer.xml', 'https://www.ozwillo.com/header.xml']
langs = {}
for url in urls:
    response = requests.get(url)
    menuset = ET.fromstring(response.text.encode('utf-8'))
    for menu in menuset.findall('menu'):
        locale = menu.find('locale').text
        langs[locale] = []
        for item in menu.findall('item'):
            if 'href' in item.attrib:
                langs[locale].append(item.attrib['href'])
                langs[locale].append(item.text)
            else:
                langs[locale].append('#')
                langs[locale].append('')

for lang in os.listdir('i18n'):
    path = os.path.join('i18n', lang, 'LC_MESSAGES', 'ckanext-ozwillo-theme.po')
    if not os.path.exists(path):
        continue
    catalog = dict(zip(langs['en'], langs[lang]))
    pofile = polib.pofile(path)
    changed = False
    for entry in pofile:
        if entry.msgid in catalog:
            if entry.msgstr != catalog.get(entry.msgid):
                entry.msgstr = catalog.get(entry.msgid)
                if 'fuzzy' in entry.flags:
                    entry.flags.remove('fuzzy')
                changed = True
    if changed:
        pofile.save(path)
