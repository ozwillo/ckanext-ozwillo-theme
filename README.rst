.. You should enable this project on travis-ci.org and coveralls.io to make
   these badges work. The necessary Travis and Coverage config files have been
   generated for you.

.. image:: https://travis-ci.org//ckanext-ozwillo_theme.svg?branch=master
    :target: https://travis-ci.org//ckanext-ozwillo_theme

.. image:: https://coveralls.io/repos//ckanext-ozwillo_theme/badge.png?branch=master
  :target: https://coveralls.io/r//ckanext-ozwillo_theme?branch=master

.. image:: https://pypip.in/download/ckanext-ozwillo_theme/badge.svg
    :target: https://pypi.python.org/pypi//ckanext-ozwillo_theme/
    :alt: Downloads

.. image:: https://pypip.in/version/ckanext-ozwillo_theme/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-ozwillo_theme/
    :alt: Latest Version

.. image:: https://pypip.in/py_versions/ckanext-ozwillo_theme/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-ozwillo_theme/
    :alt: Supported Python versions

.. image:: https://pypip.in/status/ckanext-ozwillo_theme/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-ozwillo_theme/
    :alt: Development Status

.. image:: https://pypip.in/license/ckanext-ozwillo_theme/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-ozwillo_theme/
    :alt: License

=============
ckanext-ozwillo_theme
=============

.. Put a description of your extension here:
   What does it do? What features does it have?
   Consider including some screenshots or embedding a video!


------------
Requirements
------------

For example, you might want to mention here which versions of CKAN this
extension works with.

pip install -r dev-requirements.txt

The configuration variable ``ckanext.ozwillo_theme.plugin.ozwillo_url`` must be
set(for example to https://ozwillo-preprod.eu)

The configuration variable ``ckanext.ozwillo_theme.plugin.ozwillo_portal_url``
must be set(for example to https://portal.ozwillo-preprod.eu)

------------
Installation
------------

.. Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

To install ckanext-ozwillo_theme:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-ozwillo_theme Python package into your virtual environment::

     pip install ckanext-ozwillo_theme

3. Add ``ozwillo_theme`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


---------------
Config Settings
---------------

Document any optional config settings here. For example::

    # The minimum number of hours to wait before re-checking a resource
    # (optional, default: 24).
    ckanext.ozwillo_theme.some_setting = some_default_value


You can customize the homepage with these parameters:

For example::

    # The url of the csv file containings the numbers of line you want to appear in the 3rd "some numbers" section
    # Default value is Cigale terminals
    ckan.ozwillo_theme.file_url_number_terminal = https://opendata.ozwillo.com/dataset/ae8058fe-af53-4e0a-8c2b-ad699c93bb42/resource/dd1fef8c-0283-42c2-9879-b01af6236252/download/points-dacces-wifi-cigale.csv
    # The text that comes with it, default value is 'bornes Cigales'
    # If you want to use non ASCII characters you have to hardcode them directly in the template bloc_some_numbers.html
    ckan.ozwillo_theme.text_number_terminal = Bornes

    # The url of the csv file containings the numbers of line you want to appear in the 4th "some numbers" section
    # Default value is Sictiam members
    ckan.ozwillo_theme.file_url_number_member = https://opendata.ozwillo.com/dataset/37698f90-e166-4de0-8bb8-08ff50ca8006/resource/2383533c-7ee6-47ab-aa77-42200f5c5c27/download/adherentssictiam06032017.csv
    # The text that comes with it, default value is 'adherents SICTIAM'
    # If you want to use non ASCII characters you have to hardcode them directly in the template bloc_some_numbers.html
    ckan.ozwillo_theme.text_number_member = Adherents

    # The parameters of the map display on the page (here are production parameters)
    ckan.ozwillo_theme.view_id = 038a8703-6031-4386-a962-7d55029724df
    ckan.ozwillo_theme.resource_id = c39c4c65-ffba-4a30-a164-bb29fa0e6fc1
    ckan.ozwillo_theme.package_id = syn
    ckan.ozwillo_theme.map_title =  Synthèse globale des relevés d'amiante

    # Preprod parameters :
    # ckan.ozwillo_theme.view_id = 3f9a858c-763d-4b80-b3a1-55aac2a6a518
    # ckan.ozwillo_theme.resource_id = 5cad2604-da1e-4d56-a0f9-e3a2a5072c69
    # ckan.ozwillo_theme.package_id = liste-des-bornes-cigale
    # ckan.ozwillo_theme.map_title = Points d'Accès des hotspots Wifi Cigale


------------------------
Development Installation
------------------------

To install ckanext-ozwillo_theme for development, activate your CKAN virtualenv and
do::

    git clone https://github.com//ckanext-ozwillo_theme.git
    cd ckanext-ozwillo_theme
    python setup.py develop
    pip install -r dev-requirements.txt


------------
Translations
------------

To generate .mo files after having added a new translation, do :

    python setup.py compile_catalog

-----------------
Running the Tests
-----------------

To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.ozwillo_theme --cover-inclusive --cover-erase --cover-tests


---------------------------------
Registering ckanext-ozwillo_theme on PyPI
---------------------------------

ckanext-ozwillo_theme should be availabe on PyPI as
https://pypi.python.org/pypi/ckanext-ozwillo_theme. If that link doesn't work, then
you can register the project on PyPI for the first time by following these
steps:

1. Create a source distribution of the project::

     python setup.py sdist

2. Register the project::

     python setup.py register

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the first release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.1 then do::

       git tag 0.0.1
       git push --tags


----------------------------------------
Releasing a New Version of ckanext-ozwillo_theme
----------------------------------------

ckanext-ozwillo_theme is availabe on PyPI as https://pypi.python.org/pypi/ckanext-ozwillo_theme.
To publish a new version to PyPI follow these steps:

1. Update the version number in the ``setup.py`` file.
   See `PEP 440 <http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers>`_
   for how to choose version numbers.

2. Create a source distribution of the new version::

     python setup.py sdist

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the new release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.2 then do::

       git tag 0.0.2
       git push --tags
