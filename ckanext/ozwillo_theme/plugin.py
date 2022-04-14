import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
pconfig = toolkit.config
from ckan.common import config
from ckan.lib.app_globals import set_app_global
from ckan.lib.plugins import DefaultTranslation
import ckan.logic as logic
import ckan.lib.helpers as h
from datetime import datetime


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
        set_app_global('ckan.ozwillo_global_login_organization_name',
                   pconfig.get('%s.ozwillo_global_login_organization_name' % __name__))

        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('assets', 'theme')

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'ozwillo_theme_get_last_datasets': lambda: logic.get_action('package_search')({}, {"rows": 8})['results'],
            'ozwillo_theme_get_resource_number': ozwillo_theme_get_resource_number,
            'ozwillo_theme_get_showcase_number': ozwillo_theme_get_showcase_number,
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


def ozwillo_theme_get_showcase_number():
    return len(logic.get_action('ckanext_showcase_list')({}, {}))


def ozwillo_theme_get_map(view_id, resource_id, package_id):
    resource_view = None
    try:
        resource_view = logic.get_action('resource_view_show')({}, {'id': view_id})
    except ():
        return 'View not found'

    resource = logic.get_action('resource_show')({}, {'id': resource_id})
    package = logic.get_action('package_show')({}, {'id': package_id})

    return h.rendered_resource_view(resource_view, resource, package, True)
