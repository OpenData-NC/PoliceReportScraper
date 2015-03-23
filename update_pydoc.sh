#!/bin/sh
export PYTHONPATH=$PYTHONPATH:/home/vaughn.hagerty/django/PoliceReportScraper/odnc_police
export DJANGO_SETTINGS_MODULE=odnc_police.settings
epydoc --html --parse-only --docformat plaintext odnc_police \
/home/vaughn.hagerty/django/PoliceReportScraper/odnc_police/xmlScraper.py \
/home/vaughn.hagerty/django/PoliceReportScraper/test.py 
