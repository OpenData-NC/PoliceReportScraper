from xmlScraper import *
import datetime
from odnc_police.models import * 


pdfObjectList = createPDFList('/home/vaughn.hagerty/django/PoliceReportScraper/converted_xml_samples/')


for record in pdfObjectList:
    dt = record['Date Arrested']
    tm = record['Time Arrested']
    a = Arrest_test(agency = record['Agency Name'],
         name = record['Name (Last, First, Middle)'],
         age = record['Age'],
         race = record['Race'],
         sex = record['Sex'],
         date_occurred = datetime.date(int(dt[6:10]), int(dt[:2]), int(dt[3:5])),
         time_occurred = datetime.time(int(tm[:2]), int(tm[3:])),
         address = record['Current Address'],
         charge = record['Charge1'],
         offense_code = record['Chg1 DCI Code'][:3],
         reporting_officer = record['Arresting Officer Signature/ID #'],
         pdf = "/path/to/pdf",
         street_address = record['Place of Arrest'],
         city = 'Chapel Hill',
         state = 'NC',
         zip = '27514',
         lat = 38.2,
         lon = 38.9)
    a.save()
    print "--------------------------------"
    print a.agency
    print a.name
    print a.age
    print a.race
    print a.sex
    print a.charge
    print a.street_address
    print a.reporting_officer
    print "--------------------------------"

