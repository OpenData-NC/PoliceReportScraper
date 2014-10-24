from django.db import models

#keep the _test for now, we don't want to override the tables 
#already in the db
class Arrest_(models.Model):
	agency = models.CharField(max_length=150)
	name = models.CharField(max_length=250)
	age = models.IntegerField(default=0) 
	race = models.CharField(max_length=3)

	#this uses django's choice feature.  if it causes problems, we can revert
	# back to a plain charfield
	MALE='M'
	FEMALE='F'
	UNSPEC=''
	SEX_CHOICES = ( (MALE,"Male"), (FEMALE,"Female"), (UNSPEC,"Unspecified" ) 
	sex = models.CharField(max_length=2, choices=SEX_CHOICES, )

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
		return name, charge, pdf  


class Incident_test(models.Model):
	agency = models.CharField(max_length=150)
	name = models.CharField(max_length=250)
	age = models.IntegerField(default=0) 
	race = models.CharField(max_length=3)

	MALE='M'
	FEMALE='F'
	UNSPECIFIED=''
	SEX_CHOICES = ( (MALE,"Male"), (FEMALE,"Female"), (UNSPECIFIED,"Unspecified" ) 
	sex = models.CharField(max_length=2, choices=SEX_CHOICES, )

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
