import requests
import urllib
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
            'ozwillo_theme_get_resource_number': lambda: logic.get_action('resource_search')({}, {'query': {'name:': ''}})['count'],
            'ozwillo_theme_get_terminal_number': ozwillo_theme_number_terminal,
            'ozwillo_theme_get_terminal_text': lambda: config.get('ckanext.ozwillo_theme.text_number_terminal', 'bornes Cigales'),
            'ozwillo_theme_get_member_number': ozwillo_theme_number_member,
            'ozwillo_theme_get_member_text': lambda: config.get('ckanext.ozwillo_theme.text_number_member', 'adherents SICTIAM'),
            'ozwillo_theme_get_popular_datasets': lambda: logic.get_action('package_search')({}, {"rows": 3, 'sort': 'views_total desc'})['results'],
            'ozwillo_theme_get_popular_organizations': ozwillo_theme_popular_organizations,
            'ozwillo_theme_display_date': ozwillo_theme_display_date,
            'ozwillo_theme_get_map': ozwillo_theme_get_map,
            'ozwillo_theme_get_title': lambda: config.get('ckanext.ozwillo_theme.map_title', 'Example map'),
            'ozwillo_theme_spatial_installed': lambda: config.get('ckanext.ozwillo_theme.spatial_installed', 'False'),
            'ozwillo_theme_osmnames_key': lambda: config.get('ckanext.ozwillo_theme.osmnames_key', '')

        }

def ozwillo_theme_popular_organizations():
    '''Return a sorted list of the organizations with the most datasets.'''

    # Get a list of all the site's organizations from CKAN, sorted by number of
    # datasets.
    organizations = toolkit.get_action('organization_list')(
        data_dict={'sort': 'package_count desc', 'all_fields': True})

    # Truncate the list to the 5 most popular organizations only.
    nb_orga = config.get('ckanext.ozwillo_theme.number_organization', '8')
    nb_orga = nb_orga if nb_orga.isdigit() else '8'
    organizations = organizations[:int(nb_orga)]

    return organizations

def ozwillo_theme_number_terminal():
    '''Return the number of wifi cigale terminals stored in the file'''

    file_url_backup = 'https://opendata.ozwillo.com/dataset/ae8058fe-af53-4e0a-8c2b-ad699c93bb42/resource/dd1fef8c-0283-42c2-9879-b01af6236252/download/points-dacces-wifi-cigale.csv'
    file_url = config.get('ckanext.ozwillo_theme.file_url_number_terminal', file_url_backup)
    number_terminal = 0
    try:
        data = list(urllib.urlopen(file_url))
        number_terminal = len(data) - 1
    except Exception:
        try:
            data = list(urllib.urlopen(file_url_backup))
            number_terminal = len(data) - 1
        except Exception:
            pass
    return number_terminal

def ozwillo_theme_number_member():
    '''Return the number of sictiam members in the file'''

    file_url_backup = 'https://opendata.ozwillo.com/dataset/37698f90-e166-4de0-8bb8-08ff50ca8006/resource/2383533c-7ee6-47ab-aa77-42200f5c5c27/download/adherentssictiam06032017.csv'
    file_url = config.get('ckanext.ozwillo_theme.file_url_number_member', file_url_backup)
    number_member = 0
    try:
        data = list(urllib.urlopen(file_url))
        number_member = len(data) - 1
    except Exception:
        try:
            data = list(urllib.urlopen(file_url_backup))
            number_member = len(data) - 1
        except Exception:
            pass
    return number_member

def ozwillo_theme_display_date(strDate):
    return datetime.strptime(strDate, "%Y-%m-%dT%H:%M:%S.%f").strftime('%d/%m/%Y')


def ozwillo_theme_get_map():
    view_id = config.get('ckanext.ozwillo_theme.view_id', '')
    resource_id = config.get('ckanext.ozwillo_theme.resource_id', '')
    package_id = config.get('ckanext.ozwillo_theme.package_id', '')
    try:
        resource_view = logic.get_action('resource_view_show')({}, {'id': view_id})
        resource = logic.get_action('resource_show')({}, {'id': resource_id})
        package = logic.get_action('package_show')({}, {'id': package_id})
    except Exception:
        return 'View not found'

    return h.rendered_resource_view(resource_view, resource, package, True)
