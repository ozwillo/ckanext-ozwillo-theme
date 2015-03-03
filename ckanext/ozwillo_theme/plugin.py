from pylons import config as pconfig

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.app_globals import set_global


class OzwilloThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    def update_config(self, config_):
        set_global('ckan.ozwillo_url',
                   pconfig.get('%s.ozwillo_url' % __name__))

        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'theme')
