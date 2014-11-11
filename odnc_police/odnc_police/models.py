from django.db import models

#keep the _test for now, we don't want to override the tables 
#already in the db
class Arrest_test(models.Model):
	agency = models.CharField(max_length=150)
	name = models.CharField(max_length=250)
	age = models.IntegerField(default=0) 
	race = models.CharField(max_length=3)

	#this uses django's choice feature.  if it causes problems, we can revert
	# back to a plain charfield
	MALE='M'
	FEMALE='F'
	UNSPEC=''
	SEX_CHOICES = ((MALE,"Male"), (FEMALE,"Female"), (UNSPEC,"Unspecified" )) 
	sex = models.CharField(max_length=2, choices=SEX_CHOICES, default=UNSPEC)

	date_occurred = models.DateField()
	time_occurred = models.TimeField()

	address = models.CharField(max_length=250)
	charge = models.CharField(max_length=250)
	offense_code = models.CharField(max_length=3)
	reporting_officer = models.CharField(max_length=250)
	pdf = models.CharField(max_length=250)

	street_address = models.CharField(max_length=250)
	city = models.CharField(max_length=250)
	county = models.CharField(max_length=100)
	state = models.CharField(max_length=3)
	zip = models.IntegerField(default=0)
	lat = models.FloatField()
	lon = models.FloatField()

	def __str__(self):
#		return "Name of Accused: "+self.name+" "+"Arresting Agency: "+self.agency+"Arestee Race: "+self.race+" "+"Arestee age: "+str(self.age)+" "+"Arrestee Sex: "+self.sex+" "+"Date of Arrest: "+str(self.date_occurred)+" "+"time of arrest: "+str(self.time_occurred)+" "+"Arrestee's address: "+self.address+" "+"Charge: "+self.charge+" "+"Charge Code: "+self.offense_code+" "+"Reporting Officer: "+self.reporting_officer+" "+"Address of Arrest: "+self.street_address+" "+"City: "+self.city+" "+"County: "+self.county+" "+"State: "+self.state+" "+"Zip: "+str(self.zip)+"\n"+"\n"+"\n"
		return "Name of Accused: "+self.name+'       '+ "Arresting Agency: "+self.agency+'\n'+ "Arrestee Race: "+self.race+'\t'+ "Arrestee Age: "+str(self.age)+'\t'+ "Arrestee Sex: "+self.sex+'\n'+	"Date of Arrest: "+str(self.date_occurred)+'\t'+ "Time of Arrest: "+str(self.time_occurred)+'\n'+ "Arrestee Address: "+self.address+'\n'+	"Charge: "+self.charge+'\t'+ "Charge Code: "+self.offense_code+'\n'+	"Reporting Officer: "+self.reporting_officer+'\n'+ "Place of Arrest: "+self.street_address+'\n'+ "City: "+self.city+'\t'+"County: "+self.county+'\t'+"State: "+self.state+'\t'+"Zip: "+str(self.zip)+"\n"+"\n"+"\n"


class Incident_test(models.Model):
	agency = models.CharField(max_length=150)
	name = models.CharField(max_length=250)
	age = models.IntegerField(default=0) 
	race = models.CharField(max_length=3)

	MALE='M'
	FEMALE='F'
	UNSPEC=''
	SEX_CHOICES = ( (MALE,"Male"), (FEMALE,"Female"), (UNSPEC,"Unspecified" )) 
	sex = models.CharField(max_length=2, choices=SEX_CHOICES, default=UNSPEC)

	on_date = models.DateField()
	from_date = models.DateField()
	to_date = models.DateField()
	date_reported = models.DateField()
	time_reported = models.TimeField()

	address = models.CharField(max_length=250)
	charge = models.CharField(max_length=250)
	offense_code = models.CharField(max_length=3)
	reporting_officer = models.CharField(max_length=250)
	pdf = models.CharField(max_length=250)

	street_address = models.CharField(max_length=250)
	city = models.CharField(max_length=250)
	county = models.CharField(max_length=100)
	state = models.CharField(max_length=3)
	zip = models.IntegerField(default=0)
	lat = models.FloatField()
	lon = models.FloatField()

	def __str__(self):
		return name, charge, pdf  
