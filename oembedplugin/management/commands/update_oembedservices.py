from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

import urllib2
import simplejson as json
import re

from oembedplugin.models import OembedService
from oembedplugin.settings import *

MODEL_KEYS = ('name', 'type', 'displayname', 'domain', 'subdomains', 'favicon', 'regex', 'about')

class Command(BaseCommand):
    help = 'Updates supported services from embed.ly'

    option_list = BaseCommand.option_list + (
        make_option('--delete-obsolete',
            action='store_true',
            default=True,
            help='Deletes obsolete services (services not found in embed.ly services list)'),
        )

    def handle(self, *args, **options):
        response = urllib2.urlopen(OEMBED_SERVICES_URL)
        services = json.loads(response.read())

        # Create a list of services to later delete all entries missing in the list
        service_names = []
        
        for service in services:
            service_model, created = OembedService.objects.get_or_create(name=service['name'])
            for key in MODEL_KEYS:
                setattr(service_model, key, service[key])

            service_model.save()
            service_names.append(service['name'])

            if created:
                self.stdout.write(u'Added service "%s"\n' % service_model)

        if options['delete_obsolete']:
            deprecated_services = OembedService.objects.exclude(name__in=service_names)
            for service in deprecated_services:
                service.delete()
                self.stdout.write(u'Deleted service "%s"\n' % service)

        self.stdout.write(u'Total services stored: %i' % len(service_names))
