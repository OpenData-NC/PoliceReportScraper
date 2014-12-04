from xmlScraper import *
import datetime
import traceback
import sys
from odnc_police.models import *

pdfObjectList = createPDFList('/home/vaughn.hagerty/django/PoliceReportScraper/converted_xml_samples/')

for record in pdfObjectList:
    try:
        print "doing record with OCA " + record['OCA'] + "..."

        dt_arr = record['Date Arrested']
        tm_arr = record['Time Arrested']
        bd = record['D.O.B.']
	dttm_vehstat = record['Vehicle Status Datetime']
	dttm_conf = record['Datetime Confined']
	dttm_rel = record['Datetime Released']
	dt_trial = record['Trial Date']
        dt_sub = record['Date Submitted']
        tm_sub = record['Time Submitted']


        if (dt_arr == 'NULL' or dt_arr is None):
		dt_arr = datetime.date(0, 0, 0)
	else:
		dt_arr = datetime.date(int(dt_arr[6:10]), int(dt_arr[:2]), int(dt_arr[3:5]))
        if (tm_arr == 'NULL' or tm_arr is None):
		tm_arr = datetime.time(0, 0)
	else:
		tm_arr = datetime.time(int(tm_arr[:2]), int(tm_arr[3:]))
        if (bd == 'NULL' or bd is None):
		bd = datetime.date(0, 0, 0)
	else:
		bd = datetime.date(int(bd[6:10]), int(bd[:2]), int(bd[3:5]))
        if (dt_trial == 'NULL' or dt_trial is None):
		dt_trial = datetime.date(0, 0, 0)
	else:
		dt_trial = datetime.date(int(dt_trial[6:10]), int(dt_trial[:2]), int(dt_trial[3:5]))
        if (dt_sub == 'NULL' or dt_sub is None):
		dt_sub = datetime.date(0, 0, 0)
	else:
		dt_sub = datetime.date(int(dt_sub[6:10]), int(dt_sub[:2]), int(dt_sub[3:5]))
        if (tm_sub == 'NULL' or tm_sub is None):
		tm_sub = datetime.time(0, 0)
	else:
		tm_sub = datetime.time(int(tm_sub[:2]), int(tm_sub[3:]))
	if (dttm_vehstat == 'NULL' or dttm_vehstat is None):
		dttm_vehstat = datetime.datetime(0, 0, 0, 0, 0)
	else:
		dttm_vehstat = datetime.datetime(int(dttm_vehstat[6:10]), int(dttm_vehstat[:2]), int(dttm_vehstat[3:5]), int(dttm_vehstat[12:14]), int(dttm_vehstat[15:17]))
	if (dttm_conf == 'NULL' or dttm_conf is None):
		dttm_conf = datetime.datetime(0, 0, 0, 0, 0)
	else:
		dttm_conf = datetime.datetime(int(dttm_conf[6:10]), int(dttm_conf[:2]), int(dttm_conf[3:5]), int(dttm_conf[11:13]), int(dttm_conf[14:16]))
	if (dttm_rel == 'NULL' or dttm_rel is None):
		dttm_rel = datetime.datetime(0, 0, 0, 0, 0)
	else:
		dttm_rel = datetime.datetime(int(dttm_rel[6:10]), int(dttm_rel[:2]), int(dttm_rel[3:5]), int(dttm_rel[11:13]), int(dttm_rel[14:16]))

        a = Arrest_test(agency = record['Agency Name'],
	

	a = Arrest_test(OCA = record['OCA'],
			Agency_Name = record['Agency Name']
			ORI = record['ORI']
			Date_Arrested = dt_arr
			Time_Arrested = tm_arr
			Prints_Taken = record['Prints Taken']
			Photos_Taken = record['Photos Taken']
			Fignerprint_Card_Number_(CKN) = record['Fingerprint Card Number (CKN)']
			Arrest_Tract = record['Arrest Tract']
			Residence_Tract = record['Residence Tract']
			Arrest_Number = record['Arrest Number']
			Name = record['Name (Last, First, Middle)']
			DOB = bd
			Age = record['Age']
			Race = record['Race']
			Sex = record[


	)
        a.save()
        print "successfully saved record to DB"
    except:
        print "Error uploading this record to DB"
        print traceback.format_exc() #sys.exc_info()
