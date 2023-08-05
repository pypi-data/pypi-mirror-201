from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='asterism',
      version='1.0.0',
      description='Helpers for Project Electron infrastructure',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/RockefellerArchiveCenter/asterism',
      author='Rockefeller Archive Center',
      author_email='archive@rockarch.org',
      install_requires=[
          'bagit',
          'django',
          'djangorestframework'],
      license='MIT',
      packages=find_packages(),
      tests_require=[
          'coverage',
          'pytest'],
      zip_safe=False)
