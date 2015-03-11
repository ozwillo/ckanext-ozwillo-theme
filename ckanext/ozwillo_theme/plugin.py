import json
import os
import requests
import xml.etree.ElementTree as ET
from slugify import slugify

from pylons import config as pconfig

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.app_globals import set_global

def footer_links():
    url = 'https://www.ozwillo.com/footer.xml'
    langs = {}

    response = requests.get(url)
    menuset = ET.fromstring(response.text.encode('utf-8'))

    items = ('News', 'Discovering', 'Co-construct', 'Let\'s go', 'Contact',
             'Projects', 'Project team', 'Ozwillo', 'User guide', 'Developers',
             'Legal Notices', 'General terms of use')


    for menu in menuset.findall('menu'):
        locale = menu.find('locale').text
        c = 0
        langs[locale] = {}
        for item in menu.findall('item'):
            if 'href' in item.attrib:
                langs[locale][slugify(items[c])] = item.get('href')
                c += 1
    return langs


class OzwilloThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    def update_config(self, config_):
        set_global('ckan.ozwillo_url',
                   pconfig.get('%s.ozwillo_url' % __name__))
        set_global('ckan.ozwillo_portal_url',
                   pconfig.get('%s.ozwillo_portal_url' % __name__))

        set_global('ckan.footer_links', footer_links())

        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'theme')
