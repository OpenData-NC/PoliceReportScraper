from xmlScraper import *
import datetime
import traceback
import sys
from odnc_police.models import *

print sys.argv[1]

pdfObjectList = createPDFList(sys.argv[1])

for record in pdfObjectList:
    try:
        print "doing record with OCA " + record['OCA'] + "..."

        dt_arr = record['Date Arrested']
        tm_arr = record['Time Arrested']
        dob = record['D.O.B.']
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
        if (dob == 'NULL' or dob is None):
		dob = datetime.date(0, 0, 0)
	else:
		dob = datetime.date(int(dob[6:10]), int(dob[:2]), int(dob[3:5]))
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

        if bd is not "NULL":
              bd_val = datetime.date(int(bd[6:10]), int(bd[:2]), int(bd[3:5]))
        else:
              bd_val = None

        #print "DCI SLICE: "+record['Chg1 DCI Code'][:3]
        if record['Chg1 DCI Code'] == None:
              record['Chg1 DCI Code'] = "    "

        a = Arrest_test(agency = record['Agency Name'],
              name = record['Name (Last, First, Middle)'],
              age = record['Age'],
              race = record['Race'],
              sex = record['Sex'],
              date_occurred = datetime.date(int(dt[6:10]), int(dt[:2]), int(dt[3:5])),
              time_occurred = datetime.time(int(tm[:2]), int(tm[3:])) ,
              address = record['Current Address'],
              charge = record['Charge1'],
              offense_code = record['Chg1 DCI Code'][:3],
              reporting_officer = record['Arresting Officer Signature/ID #'],
              pdf = "/path/to/pdf",
              street_address = record['Place of Arrest'],
              state = 'NC',
              Method_of_Arrest = record['Method of Arrest'],
              Scars_Marks_Tattoos = record['Scars, Marks, Tattoos'],
              Arrestee_Signature = record['Arrestee Signature'],
              Arrest_Number = record['Arrest Number'],
              OCA = record['OCA'],
              Charge2 = record['Charge2'],
              Hgt = record['Hgt'],
              Charge3 = record['Charge3'],
              Wgt = record['Wgt'],
              Chg2_Counts = record['Chg2 Counts'],
              Agency_Name = record['Agency Name'],
              Photos_Taken = record['Photos Taken'],
              DOB = bd_val,
              Charge_3_Type = record['Charge 3 Type'],


              Eyes = record['Eyes'],
              Case_Status = record['Case Status'],
              Phone = record['Phone'],
              Chg2_Statute_Number = record['Chg2 Statute Number'],
              Arrest_Tract = record['Arrest Tract'],
              Social_Security = record['Social Security #'],
              Date_Submitted = datetime.date(int(ds[6:10]), int(ds[:2]), int(ds[3:5])),
              Charge_2_Type = record['Charge 2 Type'],
              If_Armed_Type_of_Weapon = record['If Armed, Type of Weapon'],
              Employers_Name = record["Employer's Name"],
              Arresting_Officer_Signature_and_ID_num = record['Arresting Officer Signature/ID #'],
              Charge1 = record['Charge1'],
              Misc_number_and_Type = record['Misc. # and Type'],
              Country_of_Citizenship = record['Country of Citizenship'],
              Chg1_DCI_Code = record['Chg1 DCI Code'],
              Prints = record['Prints'],
              OLN_and_State = record['OLN and State'],
              Narrative = record['Narrative'],
              Consumed_Drug_Alcohol = record['Consumed Drug/Alcohol'],
              Chg1_Counts = record['Chg1 Counts'],
              Residence_Tract = record['Residence Tract'],
              Fingerprint_Card_Check_Digit = record['Fingerprint Card Check Digit # (CKN)'],
              Residency_Status = record['Residency Status'],
              Skin_Tone = record['Skin Tone'],
              Chg2_DCI_Code = record['Chg2 DCI Code'],
              Chg1_Statute_Number = record['Chg1 Statute Number'],
              Nearest_Relative_Name = record['Nearest Relative Name'],
              Hair = record['Hair'],
              Place_of_Birth = record['Place of Birth'],
              Time_Submitted = datetime.time(int(ts[:2]), int(ts[3:])) ,
              Also_Known_As = record['Also Known As (Alias Names)'],
              ORI = record['ORI'],
              Case_Disposition = record['Case Disposition'],
              Charge_1_Type = record['Charge 1 Type'],
              Occupation = record['Occupation'])
        a.save()
        print "successfully saved record to DB"
    except:
        print "Error uploading this record to DB"
        print traceback.format_exc() #sys.exc_info()
