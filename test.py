from xmlScraper import *
import datetime
import traceback
import sys
from odnc_police.models import *


def getInput():
	pdfDir = raw_input('Enter the path after sample_other_agency: ')
	return pdfDir


pdfDir = getInput()
dirPath = '/home/vaughn.hagerty/django/PoliceReportScraper/sample_other_agency/' + str(pdfDir)
while (not(os.path.exists(dirPath))):
	pdfDir = raw_input('Directory location invalid; please re-enter path: ')
	dirPath = '/home/vaughn.hagerty/django/PoliceReportScraper/sample_other_agency/' + str(pdfDir)


pdfObjectList = createPDFList(dirPath)

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
        		dt_arr = None
        	else:
        		dt_arr = datetime.date(int(dt_arr[6:10]), int(dt_arr[:2]), int(dt_arr[3:5]))
                if (tm_arr == 'NULL' or tm_arr is None):
        		tm_arr = None
        	else:
        		tm_arr = datetime.time(int(tm_arr[:2]), int(tm_arr[3:]))
                if (bd == 'NULL' or bd is None):
        		bd = None
        	else:
        		bd = datetime.date(int(bd[6:10]), int(bd[:2]), int(bd[3:5]))
                if (dt_trial == 'NULL' or dt_trial is None):
        		dt_trial = None
        	else:
        		dt_trial = datetime.date(int(dt_trial[6:10]), int(dt_trial[:2]), int(dt_trial[3:5]))
                if (dt_sub == 'NULL' or dt_sub is None):
        		dt_sub = None
        	else:
        		dt_sub = datetime.date(int(dt_sub[6:10]), int(dt_sub[:2]), int(dt_sub[3:5]))
                if (tm_sub == 'NULL' or tm_sub is None):
        		tm_sub = None
        	else:
        		tm_sub = datetime.time(int(tm_sub[:2]), int(tm_sub[3:]))
        	if (dttm_vehstat == 'NULL' or dttm_vehstat is None):
        		dttm_vehstat = None
        	else:
        		dttm_vehstat = datetime.datetime(int(dttm_vehstat[6:10]), int(dttm_vehstat[:2]), int(dttm_vehstat[3:5]), int(dttm_vehstat[12:14]), int(dttm_vehstat[15:17]))
        	if (dttm_conf == 'NULL' or dttm_conf is None):
        		dttm_conf = None
        	else:
        		dttm_conf = datetime.datetime(int(dttm_conf[6:10]), int(dttm_conf[:2]), int(dttm_conf[3:5]), int(dttm_conf[11:13]), int(dttm_conf[14:16]))
        	if (dttm_rel == 'NULL' or dttm_rel is None):
        		dttm_rel = None
        	else:
        		dttm_rel = datetime.datetime(int(dttm_rel[6:10]), int(dttm_rel[:2]), int(dttm_rel[3:5]), int(dttm_rel[11:13]), int(dttm_rel[14:16]))
        	
        	a = Arrest_test(OCA = record['OCA'],
        			Agency_Name = record['Agency Name'],
        			ORI = record['ORI'],
        			Date_Arrested = dt_arr,
        			Time_Arrested = tm_arr,
        			Prints_Taken = record['Prints Taken'],
        			Photos_Taken = record['Photos Taken'],
        			Fingerprint_Card_Number_CKN = record['Fingerprint Card Number (CKN)'],
        			Arrest_Tract = record['Arrest Tract'],
        			Residence_Tract = record['Residence Tract'],
        			Arrest_Number = record['Arrest Number'],
        
        			Name = record['Name (Last, First, Middle)'],
        			DOB = bd,
        			Age = record['Age'],
        			Race = record['Race'],
        			Sex = record['Sex'],
        			Place_of_Birth = record['Place of Birth'],
        			Country_of_Citizenship = record['Country of Citizenship'],
        			Address = record['Current Address'],
        			Arrestee_Phone = record['Arrestee Phone'],
        			Occupation = record['Occupation'],
        			Residency_Status = record['Residency Status'],
        			Employer_Name = record['Employer Name'],
        			Employer_Address = record['Employer Address'],
        			Employer_Phone = record['Employer Phone'],
        			Also_Known_As = record['Also Known As (Alias Names)'],
        			Hgt = record['Hgt'],
        			Wgt = record['Wgt'],
        			Hair = record['Hair'],
        			Eyes = record['Eyes'],
        			Skin_Tone = record['Skin Tone'],
        			Consumed_Drug_Alcohol = record['Consumed Drug/Alcohol'],
        			Scars_Marks_Tattoos = record['Scars, Marks, Tattoos'],
        			Social_Security = record['Social Security'],
        			OLN_and_State = record['OLN and State'],
        			Misc_Number_and_Type = record['Misc. Number and Type'],
        			Nearest_Relative_Name = record['Nearest Relative Name'],
        			Nearest_Relative_Address = record['Nearest Relative Address'],
        			Nearest_Relative_Phone = record['Nearest Relative Phone'],
        
        			If_Armed_Type_of_Weapon = record['If Armed, Type of Weapon'],
        			Arrest_Type = record['Arrest Type'],
        			Place_of_Arrest = record['Place of Arrest'],
        			Charge1 = record['Charge1'],
        			Charge1_Type = record['Charge1 Type'],
        			Charge1_Counts = record['Charge1 Counts'],
        			Charge1_DCI_Code = record['Charge1 DCI Code'],
        			Charge1_Offense_Jurisdiction = record['Charge1 Offense Jurisdiction'],
        			Charge1_Statute_Number = record['Charge1 Statute Number'],
        			Charge1_Warrant_Date = record['Charge1 Warrant Date'],
        			Charge2 = record['Charge2'],
        			Charge2_Type = record['Charge2 Type'],
        			Charge2_Counts = record['Charge2 Counts'],
        			Charge2_DCI_Code = record['Charge2 DCI Code'],
        			Charge2_Offense_Jurisdiction = record['Charge2 Offense Jurisdiction'],
        			Charge2_Statute_Number = record['Charge2 Statute Number'],
        			Charge2_Warrant_Date = record['Charge2 Warrant Date'],
        			Charge3 = record['Charge3'],
        			Charge3_Type = record['Charge3 Type'],
        			Charge3_Counts = record['Charge3 Counts'],
        			Charge3_DCI_Code = record['Charge3 DCI Code'],
        			Charge3_Offense_Jurisdiction = record['Charge3 Offense Jurisdiction'],
        			Charge3_Statute_Number = record['Charge3 Statute Number'],
        			Charge3_Warrant_Date = record['Charge3 Warrant Date'],
        
        			VYR = record['VYR'],
        			Make = record['Make'],
        			Model = record['Model'],
        			Style = record['Style'],
        			Color = record['Color'],
        			Plate_No_and_State = record['Plate No./State'],
        			VIN = record['VIN'],
        			Vehicle_Status = record['Vehicle Status'],
        			Vehicle_Status_Datetime = dttm_vehstat,
        
        			Datetime_Confined = dttm_conf,
        			Place_Confined = record['Place Confined'],
        			Committing_Magistrate = record['Committing Magistrate'],
        			Type_Bond = record['Type Bond'],
        			Bond_Amount = record['Bond Amount'],
        			Trial_Date = dt_trial,
        			Court_of_Trial = record['Court of Trial'],
        			City_of_Court = record['City of Court'],
        			Assisting_Officer = record['Assisting Officer Name/ID'],
        			Released_By = record['Released By (Name/Dept/ID)'],
        			Datetime_Released = dttm_rel,
        
        			Drug1_Suspected_Type = record['Drug1 Suspected Type'],
        			Drug1_DCI = record['Drug1 DCI'],
        			Drug1_Status = record['Drug1 Status'],
        			Drug1_Quantity = record['Drug1 Quantity'],
        			Drug1_Activities = record['Drug1 Activities'],
        			Drug2_Suspected_Type = record['Drug2 Suspected Type'],
        			Drug2_DCI = record['Drug2 DCI'],
        			Drug2_Status = record['Drug2 Status'],
        			Drug2_Quantity = record['Drug2 Quantity'],
        			Drug2_Activities = record['Drug2 Activities'],
        
        			Comp = record['Comp'],
        			Comp_Name = record['Comp Name'],
        			Comp_Address = record['Comp Address'],
        			Comp_Phone = record['Comp Phone'],
        			
        			Narrative = record['Narrative'],
        
        			Arresting_Officer_Signature = record['Arresting Officer Signature/ID'],
        			Date_Submitted = dt_sub,
        			Time_Submitted = tm_sub,
        			Supervisor_Signature = record['Supervisor Signature'],
        			Case_Status = record['Case Status'],
        			Case_Disposition = record['Case Disposition'],
        			Arrestee_Signature = record['Arrestee Signature'],
        
        			pdf = 'path/to/pdf.lnk',
        			city = "thecity",
        			state = 'NC'
        
        	)
                a.save()
                print "successfully saved record to DB"
	except:
    		print "Error uploading this record to DB"
    		print traceback.format_exc() #sys.exc_info()
