from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from oembedplugin.models import OembedPlugin
from django.utils.translation import ugettext as _

class CMSOembedPlugin(CMSPluginBase):
        model = OembedPlugin
        name = _("Oembed")
        render_template = "oembedplugin/object.html"

        def render(self, context, instance, placeholder):
            context.update({'oembed':instance.oembedplugin, 
                                         'object':instance,
                                         'placeholder':placeholder})
            return context
                
plugin_pool.register_plugin(CMSOembedPlugin)
