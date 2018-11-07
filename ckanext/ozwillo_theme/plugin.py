import requests
import xml.etree.ElementTree as ET
from slugify import slugify

from pylons import config as pconfig

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.common import config
from ckan.lib.app_globals import set_app_global
from ckan.lib.plugins import DefaultTranslation
import ckan.logic as logic
import ckan.lib.helpers as h
from datetime import datetime


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
    plugins.implements(plugins.ITemplateHelpers)

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

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'ozwillo_theme_get_last_datasets': lambda: logic.get_action('package_search')({}, {"rows": 8})['results'],
            'ozwillo_theme_get_resource_number': ozwillo_theme_get_resource_number,
            'ozwillo_theme_get_popular_datasets': lambda: logic.get_action('package_search')({}, {"rows": 4, 'sort': 'views_total desc'})['results'],
            'ozwillo_theme_display_date': ozwillo_theme_display_date,
            'ozwillo_theme_get_map': ozwillo_theme_get_map,
            'ozwillo_theme_get_groups': lambda: logic.get_action('group_list')({}, {"all_fields": True}),
            'ozwillo_theme_spatial_installed': lambda: config.get('ckanext.ozwillo_theme.spatial_installed', 'False'),
            'ozwillo_theme_osmnames_key': lambda: config.get('ckanext.ozwillo_theme.osmnames_key', '')
        }


def ozwillo_theme_display_date(strDate):
    return datetime.strptime(strDate, "%Y-%m-%dT%H:%M:%S.%f").strftime('%d/%m/%Y')


def ozwillo_theme_get_resource_number():
    return logic.get_action('resource_search')({}, {'query': {'name:': ''}})['count']


def ozwillo_theme_get_map(view_id, resource_id, package_id):
    resource_view = None
    try:
        resource_view = logic.get_action('resource_view_show')({}, {'id': view_id})
    except ():
        return 'View not found'

    resource = logic.get_action('resource_show')({}, {'id': resource_id})
    package = logic.get_action('package_show')({}, {'id': package_id})

    return h.rendered_resource_view(resource_view, resource, package, True)
