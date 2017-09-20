from distutils.core import setup
setup(
  name = 'bigQueryExporter',
  packages = ['bigQueryExporter'], # this must be the same as the name above
  version = '0.0.3',
  description = 'Package codes to execute queries on BigQuery and save to local machine',
  author = 'Icarus So',
  author_email = 'icarus.so@gmail.com',
  url = 'https://github.com/IcarusSO/bigQueryExporter', # use the URL to the github repo
  keywords = ['bigquery', 'local', 'export'], # arbitrary keywords
  classifiers = [],
  install_requires=[
    'google-cloud',
    'google-cloud-bigquery',
    'google-cloud-storage'
  ]
)