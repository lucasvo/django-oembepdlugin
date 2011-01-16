from setuptools import setup, find_packages
import os

version = __import__('oembedplugin').__version__

def read(fname):
    # read the contents of a text file
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

install_requires = [
    'setuptools',
    'oembed',
]

setup(
    name = "django-oembedplugin",
    version = version,
    url = 'http://github.com/lucasvo/django-oembed',
    license = 'BSD',
    platforms=['OS Independent'],
    description = "A django-cms plugin for embedding content from other sites. It uses the embed.ly api to generate oembed objects for over 160 sites.",
    long_description = read('README.rst'),
    author = 'Lucas Vogelsang',
    author_email = 'lucasvo@forewaystudios.com',
    packages=find_packages(),
    install_requires = install_requires,
    include_package_data=True,
    zip_safe=False,
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
