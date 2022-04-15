import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
pconfig = toolkit.config
from ckan.common import config
from ckan.lib.app_globals import set_app_global
from ckan.lib.plugins import DefaultTranslation
import ckan.logic as logic
import ckan.lib.helpers as h
from datetime import datetime
from random import randrange


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
            'ozwillo_theme_osmnames_key': lambda: config.get('ckanext.ozwillo_theme.osmnames_key', ''),
            # [FDR]
            'ozwillo_theme_get_project_orgs': ozwillo_theme_get_project_orgs,
            'ozwillo_theme_get_showcases': ozwillo_theme_get_showcases,
            'ozwillo_theme_get_territory_organizations': ozwillo_theme_get_territory_organizations
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

def ozwillo_theme_get_project_orgs():
    usage_prefixed_short_orgs = logic.get_action('organization_autocomplete')({}, {"q": "usage-"})
    usage_prefixed_orgs = [logic.get_action('organization_show')({}, {"id": org['name']}) for org in usage_prefixed_short_orgs]
    return usage_prefixed_orgs

def ozwillo_theme_get_showcases():
    showcases = logic.get_action('ckanext_showcase_list')({}, {})
    # take 4 at random :
    random_start_index = randrange(len(showcases))
    return showcases[random_start_index:random_start_index + 4]

def ozwillo_theme_get_territory_organizations():
    all_org_names = logic.get_action('organization_list')({}, {"limit": 1000, 'sort': 'name asc'})
    # take 50 at random :
    random_start_index = randrange(len(all_org_names))
    org_names = all_org_names[random_start_index:random_start_index + 50]

    # filter :
    usage_prefixed_org_names = logic.get_action('organization_autocomplete')({}, {"q": "usage-"})
    helper_org_names = ['france-data-reseau','federation-nationale-des-collectivites-concedantes-et-regies', 'datactivist' 'altereo', 'darkskylab']
    non_territory_org_names = helper_org_names + usage_prefixed_org_names
    territory_org_names = [org_name for org_name in org_names if org_name not in non_territory_org_names][0:4]

    # get :
    territory_orgs = [logic.get_action('organization_show')({}, {"id": org_name}) for org_name in territory_org_names]
    return territory_orgs