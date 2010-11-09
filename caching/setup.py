from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='caching',
      version=version,
      description="Comparing HTTP Caching to In App Caching",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='experiment',
      author='Eric Moritz',
      author_email='eric@themoritzfamily.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
        'python-memcached',
        'pylibmc',
        'werkzeug',
        'webob',
        'httplib2',
        'paste',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
