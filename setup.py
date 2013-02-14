import codecs
from setuptools import setup, find_packages

setup(name='googleappsauth',
      maintainer='Sam Johnson',
      maintainer_email='me@samdjohnson.com',
      version='1.1',
      description='googleappsauth authenticates Django Users against a Google Apps Domain',
      long_description=codecs.open('README.rst', "r", "utf-8").read(),
      license='BSD',
      url='http://github.com/samdjohnson/django-googleappsauth#readme',
      classifiers=['Intended Audience :: Developers',
                   'Programming Language :: Python'],
      package_data={"googleappsauth": ["templates/googleappsauth/*.html",]},
      packages = find_packages(),
      install_requires = ['Django'],
      zip_safe = False,
)
