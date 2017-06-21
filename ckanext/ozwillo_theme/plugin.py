import requests
import xml.etree.ElementTree as ET
from slugify import slugify

from pylons import config as pconfig

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.app_globals import set_app_global
from ckan.lib.plugins import DefaultTranslation

def footer_links():
    url = 'https://www.ozwillo.com/footer.xml'
    langs = {}

    response = requests.get(url)
    menuset = ET.fromstring(response.text.encode('utf-8'))

    items = ('Association', 'Governance', 'Community', 'Team',
             'Data', 'Portal', 'Projects',
             'Genesis', 'Contributions', 'Developers',
             'News', 'Contact', 'Legal Notices', 'Terms')

    for menu in menuset.findall('menu'):
        locale = menu.find('locale').text
        c = 0
        langs[locale] = {}
        for item in menu.findall('item'):
            if 'href' in item.attrib:
                langs[locale][slugify(items[c])] = item.get('href')
                c += 1
    return langs


class OzwilloThemePlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IConfigurer)

    def update_config(self, config_):
        set_app_global('ckan.ozwillo_url',
                   pconfig.get('%s.ozwillo_url' % __name__))
        set_app_global('ckan.ozwillo_portal_url',
                   pconfig.get('%s.ozwillo_portal_url' % __name__))
        set_app_global('ckan.ozwillo_ckan_app_id',
                   pconfig.get('%s.ozwillo_ckan_app_id' % __name__))

        set_app_global('ckan.localized_links', footer_links())

        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'theme')
