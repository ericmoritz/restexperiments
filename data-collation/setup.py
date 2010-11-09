from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='data-collation',
      version=version,
      description="Comparing RESTful data collation methods against traditional ones",
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
        "webob",
        "gevent",
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
