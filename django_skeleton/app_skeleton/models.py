from django.db import models

# Create your models here.
class Arrest(models.Model):
	agency = models.CharField(max_length=150)
	name = models.CharField(max_length=250)
	age = models.IntegerField(default=0) 
	race = models.CharField(max_length=3)

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


class Incident(models.Model):
	date=models.DateTimeField()
	def __str__(self):
		return self.status_text
