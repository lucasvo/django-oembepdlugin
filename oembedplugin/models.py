from django.db import models
from cms.models import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
import re

from oembedplugin.fields import *

OEMBED_TYPES = (
    ('photo', _('Static viewable image.')),
    ('video', _('Playable video.')),
    ('rich', _('Rich HTML, may contain images and videos.')),
    ('link', _('General embed that may not contain HTML.')),
    )

class OembedService(models.Model):
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=10, choices=OEMBED_TYPES)
    displayname = models.CharField(max_length=150)
    domain = models.CharField(max_length=256)
    subdomains = JSONField(null=True, blank=True)
    favicon = models.URLField(verify_exists=True, null=True, blank=True)
    regex = JSONField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.displayname

    @classmethod 
    def all_services_regex(Class):
        """ Returns a list of all regexes for all supported services """
        regex_list = cache.get('oembed_regex_list')
        if not regex_list:
            regex_list = []
            for service in OembedService.objects.all():
                regex_list.extend(service.regex)
            cache.set('oembed_regex_list', regex_list, 60*60*24)
        return regex_list 

class OembedPlugin(CMSPlugin):
    href = models.URLField(verify_exists=False)
    type = models.CharField(max_length=10, choices=OEMBED_TYPES, null=True, blank=True)
    service = models.ForeignKey(OembedService, null=True,blank=True) 

    oembed = JSONField(null=True, blank=True)

    def update_oembed_inf(self):
        match = False
        
        for regex in OembedService.all_services_regex:
            if re.match(regex, self.href):
                match = True

        if match:
            params = {
                'url':self.href,
                'format':'json',
                'maxwidth':self.maxwidth,
                'maxheight':self.maxheight,
                }
            fetch_url = 'http://api.embed.ly/v1/api/oembed?%s' % urllib.urlencode(params)

            try:
              result = urllib2.urlopen(fetch_url).read()
            except:
              return None
            self.oembed = json.loads(result)

    def save(self):
        self.update_oembed_info()
        super(OembedPlugin, self).save()
    

