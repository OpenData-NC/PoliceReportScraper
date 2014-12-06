from django.db import models

#keep the _test for now, we don't want to override the tables 
#already in the db
class Arrest_test(models.Model):
	'''
	Defines the format of the database. Things like OCA, Agency Name, and Date Arrested are the columns of the database
	'''
	OCA = models.CharField(max_length=20,null=True,blank=True)
	Agency_Name = models.CharField(max_length=150,null=True,blank=True) 
	ORI = models.CharField(max_length=50,null=True,blank=True) 
	Date_Arrested = models.DateField(null=True,blank=True)
	Time_Arrested = models.TimeField(null=True,blank=True)
	Prints_Taken = models.CharField(max_length=100,null=True,blank=True)
	Photos_Taken = models.CharField(max_length=100,null=True,blank=True) 
	Fingerprint_Card_Number_CKN = models.CharField(max_length=50,null=True,blank=True)
	Arrest_Tract = models.CharField(max_length=100,null=True,blank=True) 
	Residence_Tract = models.CharField(max_length=100,null=True,blank=True)
	Arrest_Number = models.CharField(max_length=25,null=True,blank=True)


	Name = models.CharField(max_length=250,null=True,blank=True)
	DOB = models.DateField(null=True,blank=True) 
	Age = models.CharField(max_length=10,null=True,blank=True) 
	Race = models.CharField(max_length=10,null=True,blank=True)

	#this uses django's choice feature.  if it causes problems, we can revert
	# back to a plain charfield
	MALE='M'
	FEMALE='F'
	UNSPEC=''
	SEX_CHOICES = ((MALE,"Male"), (FEMALE,"Female"), (UNSPEC,"Unspecified" )) 
	Sex = models.CharField(max_length=2, choices=SEX_CHOICES, default=UNSPEC,null=True,blank=True)

	Place_of_Birth = models.CharField(max_length=50,null=True,blank=True) 
	Country_of_Citizenship = models.CharField(max_length=50,null=True,blank=True)
	Address = models.CharField(max_length=250,null=True,blank=True)
	Arrestee_Phone = models.CharField(max_length=50,null=True,blank=True)
	Occupation = models.CharField(max_length=50,null=True,blank=True) 
	Residency_Status = models.CharField(max_length=100,null=True,blank=True)
	Employer_Name = models.CharField(max_length=50,null=True,blank=True)
	Employer_Address = models.CharField(max_length=100,null=True,blank=True)
	Employer_Phone = models.CharField(max_length=100,null=True,blank=True)
	Also_Known_As = models.CharField(max_length=100,null=True,blank=True)
	Hgt = models.CharField(max_length=100,null=True,blank=True) 
	Wgt = models.CharField(max_length=100,null=True,blank=True) 
	Hair = models.CharField(max_length=100,null=True,blank=True)
	Eyes = models.CharField(max_length=100,null=True,blank=True)
	Skin_Tone = models.CharField(max_length=100,null=True,blank=True)
	Consumed_Drug_Alcohol = models.CharField(max_length=100,null=True,blank=True)
	Scars_Marks_Tattoos = models.CharField(max_length=150,null=True,blank=True)
	Social_Security = models.CharField(max_length=100,null=True,blank=True)
	OLN_and_State = models.CharField(max_length=50,null=True,blank=True)
	Misc_Number_and_Type = models.CharField(max_length=50,null=True,blank=True) 
	Nearest_Relative_Name = models.CharField(max_length=50,null=True,blank=True) 
	Nearest_Relative_Address = models.CharField(max_length=100,null=True,blank=True)
	Nearest_Relative_Phone = models.CharField(max_length=100,null=True,blank=True)


	If_Armed_Type_of_Weapon = models.CharField(max_length=50,null=True,blank=True)
	Arrest_Type = models.CharField(max_length=150,null=True,blank=True)
	Place_of_Arrest = models.CharField(max_length=250,null=True,blank=True)
	Charge1 = models.CharField(max_length=50,null=True,blank=True)
	Charge1_Type = models.CharField(max_length=50,null=True,blank=True)
	Charge1_Counts = models.CharField(max_length=10,null=True,blank=True)  
	Charge1_DCI_Code = models.CharField(max_length=10,null=True,blank=True) 
	Charge1_Offense_Jurisdiction = models.CharField(max_length=50,null=True,blank=True) 
	Charge1_Statute_Number = models.CharField(max_length=50,null=True,blank=True) 
	Charge1_Warrant_Date = models.CharField(max_length=50,null=True,blank=True) 
	Charge2 = models.CharField(max_length=50,null=True,blank=True) 
	Charge2_Type = models.CharField(max_length=50,null=True,blank=True)
	Charge2_Counts = models.CharField(max_length=10,null=True,blank=True)  
	Charge2_DCI_Code = models.CharField(max_length=10,null=True,blank=True) 
	Charge2_Offense_Jurisdiction = models.CharField(max_length=50,null=True,blank=True)
	Charge2_Statute_Number = models.CharField(max_length=50,null=True,blank=True)
	Charge2_Warrant_Date = models.CharField(max_length=50,null=True,blank=True)
	Charge3 = models.CharField(max_length=50,null=True,blank=True)
	Charge3_Type = models.CharField(max_length=50,null=True,blank=True)
	Charge3_Counts = models.CharField(max_length=10,null=True,blank=True)  
	Charge3_DCI_Code = models.CharField(max_length=10,null=True,blank=True) 
	Charge3_Offense_Jurisdiction = models.CharField(max_length=50,null=True,blank=True)
	Charge3_Statute_Number = models.CharField(max_length=50,null=True,blank=True)
	Charge3_Warrant_Date = models.CharField(max_length=50,null=True,blank=True)

	
	VYR = models.CharField(max_length=15,null=True,blank=True)
	Make = models.CharField(max_length=100,null=True,blank=True)
	Model = models.CharField(max_length=100,null=True,blank=True)
	Style = models.CharField(max_length=100,null=True,blank=True)
	Color = models.CharField(max_length=100,null=True,blank=True)
	Plate_No_and_State = models.CharField(max_length=100,null=True,blank=True)
	VIN = models.CharField(max_length=100,null=True,blank=True)
	Vehicle_Status = models.CharField(max_length=100,null=True,blank=True)
	Vehicle_Status_Datetime = models.DateTimeField(null=True,blank=True)
	

	Datetime_Confined = models.DateTimeField(null=True,blank=True)
	Place_Confined = models.CharField(max_length=100,null=True,blank=True)
	Committing_Magistrate = models.CharField(max_length=100,null=True,blank=True)
	Type_Bond = models.CharField(max_length=100,null=True,blank=True)
	Bond_Amount = models.CharField(max_length=100,null=True,blank=True)
	Trial_Date = models.DateField(null=True,blank=True)
	Court_of_Trial = models.CharField(max_length=100,null=True,blank=True)
	City_of_Court = models.CharField(max_length=100,null=True,blank=True)
	Assisting_Officer = models.CharField(max_length=100,null=True,blank=True)
	Released_By = models.CharField(max_length=100,null=True,blank=True)
	Datetime_Released = models.DateTimeField(null=True,blank=True)

	
	Drug1_Suspected_Type = models.CharField(max_length=100,null=True,blank=True)
	Drug1_DCI = models.CharField(max_length=10,null=True,blank=True)
	Drug1_Status = models.CharField(max_length=25,null=True,blank=True)
	Drug1_Quantity = models.CharField(max_length=25,null=True,blank=True)
	Drug1_Activities = models.CharField(max_length=150,null=True,blank=True)
	Drug2_Suspected_Type = models.CharField(max_length=100,null=True,blank=True)
	Drug2_DCI = models.CharField(max_length=10,null=True,blank=True)
	Drug2_Status = models.CharField(max_length=25,null=True,blank=True)
	Drug2_Quantity = models.CharField(max_length=25,null=True,blank=True)
	Drug2_Activities = models.CharField(max_length=150,null=True,blank=True)


	Comp = models.CharField(max_length=100,null=True,blank=True)
	Comp_Name = models.CharField(max_length=100,null=True,blank=True)
	Comp_Address = models.CharField(max_length=100,null=True,blank=True)
	Comp_Phone = models.CharField(max_length=100,null=True,blank=True)


	Narrative = models.CharField(max_length=350,null=True,blank=True)


	Arresting_Officer_Signature = models.CharField(max_length=150,null=True,blank=True)
	Date_Submitted = models.DateField(null=True,blank=True)
	Time_Submitted = models.TimeField(null=True,blank=True)
	Supervisor_Signature = models.CharField(max_length=100,null=True,blank=True)
	Case_Status =  models.CharField(max_length=100,null=True,blank=True)
	Case_Disposition = models.CharField(max_length=100,null=True,blank=True)
	Arrestee_Signature = models.CharField(max_length=150,null=True,blank=True)


	#these are not explicitly passed by the scraper
	pdf = models.CharField(max_length=250,null=True,blank=True)
	city = models.CharField(max_length=250,null=True,blank=True)
	state = models.CharField(max_length=3,null=True,blank=True)

	def __str__(self):
		'''returns the string representation of a given record. This is what is displayed in the results page. '''
		return "OCA: "+self.OCA+"Name: "+self.Name+"Charge1: "+self.Charge1+"Arresting Officer: "+self.Arresting_Officer_Signature
#		return "Name of Accused: "+self.name+" "+"Arresting Agency: "+self.agency+"Arestee Race: "+self.race+" "+"Arestee age: "+str(self.age)+" "+"Arrestee Sex: "+self.sex+" "+"Date of Arrest: "+str(self.date_occurred)+" "+"time of arrest: "+str(self.time_occurred)+" "+"Arrestee's address: "+self.address+" "+"Charge: "+self.charge+" "+"Charge Code: "+self.offense_code+" "+"Reporting Officer: "+self.reporting_officer+" "+"Address of Arrest: "+self.street_address+" "+"State: "+self.state+" "+"Zip: "+str(self.zip)+"\n"+"\n"+"\n"
#		return "Name of Accused: "+self.name+'       '+ "Arresting Agency: "+self.agency+'\n'+ "Arrestee Race: "+self.race+'\t'+ "Arrestee Age: "+str(self.age)+'\t'+ "Arrestee Sex: "+self.sex+'\n'+	"Date of Arrest: "+str(self.date_occurred)+'\t'+ "Time of Arrest: "+str(self.time_occurred)+'\n'+ "Arrestee Address: "+self.address+'\n'+	"Charge: "+self.charge+'\t'+ "Charge Code: "+self.offense_code+'\n'+	"Reporting Officer: "+self.reporting_officer+'\n'+ "Place of Arrest: "+self.street_address+'\n'+"State: "+self.state+'\t'+"\n"+"\n"+"\n"


#class Incident_test(models.Model):
#	agency = models.CharField(max_length=150)
#	name = models.CharField(max_length=250)
#	age = models.IntegerField(default=0) 
#	race = models.CharField(max_length=3)
#
#	MALE='M'
#	FEMALE='F'
#	UNSPEC=''
#	SEX_CHOICES = ( (MALE,"Male"), (FEMALE,"Female"), (UNSPEC,"Unspecified" )) 
#	sex = models.CharField(max_length=2, choices=SEX_CHOICES, default=UNSPEC)
#
#	on_date = models.DateField()
#	from_date = models.DateField()
#	to_date = models.DateField()
#	date_reported = models.DateField()
#	time_reported = models.TimeField()
#
#	address = models.CharField(max_length=250)
#	charge = models.CharField(max_length=250)
#	offense_code = models.CharField(max_length=3)
#	reporting_officer = models.CharField(max_length=250)
#	pdf = models.CharField(max_length=250)
#
#	street_address = models.CharField(max_length=250)
#	city = models.CharField(max_length=250)
#	county = models.CharField(max_length=100)
#	state = models.CharField(max_length=3)
#	zip = models.IntegerField(default=0)
#	lat = models.FloatField()
#	lon = models.FloatField()
#
#	def __str__(self):
#		return self.name, self.charge, self.pdf  
