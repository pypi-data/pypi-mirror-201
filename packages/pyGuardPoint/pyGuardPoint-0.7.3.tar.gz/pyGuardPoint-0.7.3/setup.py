from setuptools import setup

setup(name="pyGuardPoint",
      version="0.7.3",
      description="Easy-to-use Python module implementing GuardPoint's WebAPI",
      maintainer_email="sales@sensoraccess.co.uk",
      install_requires=['validators', 'fuzzywuzzy', 'Levenshtein'],
      packages=['pyGuardPoint'],
      license_files=('LICENSE.txt',),
      zip_safe=False)
