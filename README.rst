============
django-oembedplguin
============


A django-cms plugin that allows you to embed content from over 160 sites using the embed.ly api.

Dependencies
------------

* django-cms >= 2.1
* python-oembed

Getting Started
---------------

To get started using ``django-oembedplugin`` simply install it with
``pip``::

    $ pip install django-oembedplugin


Add ``"oembedplugin"`` to your project's ``INSTALLED_APPS`` setting and run ``syncdb``
(or ``migrate`` if you're using South).

To periodically update the supported sites, oembedplugin provides a management command:

    $ python manage.py update_oembedservices 

be sure to run this once in a while. 
