.PHONY: assets i18n_compile i18n_extract readme pull start shell test remove stop


list:
	@grep '^\.PHONY' Makefile | cut -d' ' -f2- | tr ' ' '\n'


assets:
	npx gulp less

i18n_compile:
	docker-compose -f ../../docker-compose.dev.yml exec ckan-dev bash -c 'cd /srv/app/src_extensions/ckanext-ed && python setup.py compile_catalog -l en -f'

i18n_extract:
	docker-compose -f ../../docker-compose.dev.yml exec ckan-dev bash -c 'cd /srv/app/src_extensions/ckanext-ed && python setup.py extract_messages'

readme:
	npx doctoc README.md

pull:
	docker pull openknowledge/ckan-base:2.7 && \
	docker pull openknowledge/ckan-dev:2.7 && \
	docker-compose -f ../../docker-compose.dev.yml build ckan-dev

build:
	docker-compose -f ../../docker-compose.dev.yml build

start:
	docker-compose -f ../../docker-compose.dev.yml up

shell:
	docker-compose -f ../../docker-compose.dev.yml exec ckan-dev bash

test:
	docker-compose -f ../../docker-compose.dev.yml exec ckan-dev nosetests --ckan --nologcapture --reset-db -s -v --with-pylons=/srv/app/src_extensions/ckanext-ed/test.ini /srv/app/src_extensions/ckanext-ed/ ${ARGS}

remove:
	docker-compose -f ../../docker-compose.dev.yml rm -f ${SERVICE}

stop:
	docker-compose -f ../../docker-compose.dev.yml stop ${SERVICE}
