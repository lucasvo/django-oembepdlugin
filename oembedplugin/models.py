from django.db import models
from cms.models import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
import re

import urllib, urllib2

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
            cache.set('oembed_regex_list-2', regex_list, 60*60*24)
        return regex_list 

class OembedPlugin(CMSPlugin):
    href = models.URLField(verify_exists=False)
    type = models.CharField(max_length=10, choices=OEMBED_TYPES, null=True, blank=True)
    service = models.ForeignKey(OembedService, null=True,blank=True) 

    maxheight = models.IntegerField(null=True, blank=True, help_text=_("Maximum height of the embed object in pixels"))
    maxwidth = models.IntegerField(null=True, blank=True, help_text=_("Maximum width of the embed object in pixels"))
    show_title = models.BooleanField(blank=True)

    # Descriptions taken from: http://oembed.com/
    url = models.URLField(verify_exists=False, null=True, blank=True, help_text=_("URL of the resource"))
    title = models.CharField(max_length=512, null=True, blank=True, help_text=_("A text title, describing the resource."))
    description = models.TextField(null=True, blank=True, help_text=_("A description of the resource."))

    author_name = models.CharField(max_length=256, null=True, blank=True, help_text=_("The name of the author/owner of the resource."))
    author_url = models.URLField(verify_exists=False, null=True, blank=True, help_text=_("A URL for the author/owner of the resource."))
    provider_name = models.CharField(max_length=256, null=True, blank=True, help_text=_("The name of the provider of the resource."))
    provider_url = models.URLField(verify_exists=False, null=True, blank=True, help_text=_("A URL for the provider of the resource."))

    thumbnail_url = models.URLField(verify_exists=False, null=True, blank=True, help_text=_("A URL to a thumbnail image representing the resource. The thumbnail must respect any maxwidth and maxheight parameters. If this paramater is present, thumbnail_width and thumbnail_height must also be present"))
    thumbnail_height = models.IntegerField(null=True, blank=True, help_text=_("Thumbnail height"))
    thumbnail_width = models.IntegerField(null=True, blank=True, help_text=_("Thumbnail width"))

    height = models.IntegerField(null=True, blank=True, help_text=_("Height of the embed object in pixels"))
    width = models.IntegerField(null=True, blank=True, help_text=_("Width of the embed object in pixels"))

    html = models.TextField(null=True, blank=True, help_text=_("HTML Code for embedding the object"))

    def update_oembed_info(self):
        match = False
        for regex in OembedService.all_services_regex():
            if re.match(regex, self.href):
                match = True
        if match:
            params = {
                'url':self.href,
                'format':'json',
                }

            if self.maxheight: params['maxheight'] = self.maxheight
            if self.maxwidth: params['maxhwidth'] = self.maxwidth

            fetch_url = 'http://api.embed.ly/v1/api/oembed?%s' % urllib.urlencode(params)

            try:
              result = urllib2.urlopen(fetch_url).read()
            except Exception, e:
              # TODO: Error handling
              return None
            result = json.loads(result)
            # TODO: Assign service FK

            KEYS = ('type', 'title', 'description', 'author_name', 'author_url', 'provider_url', 'provider_name', 'thumbnail_width', 'thumbnail_height', 'thumbnail_url', 'height', 'width', 'html', 'url')
            for key in KEYS:
                if result.has_key(key):
                    setattr(self, key, result[key])
            self.type = result['type']

    def save(self):
        self.update_oembed_info()
        super(OembedPlugin, self).save()
    

