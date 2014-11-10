from xmlScraper_current import *
import datetime
from odnc_police.models import * 

pdfObjectList = doItAllMultipleTimes('/home/vaughn.hagerty/django/PoliceReportScraper/converted_xml_samples/')

for record in pdfObjectList:
    a = Arrest_test(
        agency = record['Agency Name'],
        name = record['Name (Last, First, Middle)'],
        age = record['Age'],
        race = record['Race'],
        sex = record['Sex'],
        dt = record['Date Arrested'],
        date_occurred = datetime.date(dt[6:10], dt[:2], dt[3:5]),
        tm = record['Time Arrested'],
        time_occurred = datetime.time(tm[:2], tm[3:]),
        address = record['Current Address'],
        charge = record['Charge1'],
        offense_code = record['DCI Code'],
        reporting_officer = record['Arresting Officer Signature/ID #'],
        pdf = "/path/to/pdf",
        street_address = record['Place of Arrest'],
        city = 'Chapel Hill',
        state = 'NC',
        zip = '27514',
        lat = 38.2,
        lon = 38.9)
    a.save()
