from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from models import Arrest_test
import datetime
import os
import re

def djangotest(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def modeltest(request):

    def filterByName(QuerySet, stringFilter):	
        return QuerySet.filter(name__contains=stringFilter)
    def filterByAgency(QuerySet, stringFilter):
        return QuerySet.filter(agency__contains=stringFilter)
    def filterByRace(QuerySet, stringFilter):
        return QuerySet.filter(race__contains=stringFilter)
    def filterByAddress(QuerySet, stringFilter):
        return QuerySet.filter(address__contains=stringFilter)
    def filterByCharge(QuerySet, stringFilter):
        return QuerySet.filter(charge__contains=stringFilter)
    def filterByOffenseCode(QuerySet, stringFilter):
        return QuerySet.filter(offense_code__contains=stringFilter)
    def filterByReportingOfficer(QuerySet, stringFilter):
        return QuerySet.filter(reporting_officer__contains=stringFilter)
    def filterByPdf(QuerySet, stringFilter):
        return QuerySet.filter(pdf__contains=stringFilter)
    def filterByStreetAddress(QuerySet, stringFilter):
        return QuerySet.filter(street_address__contains=stringFilter)
    def filterByCity(QuerySet, stringFilter):
        return QuerySet.filter(city__contains=stringFilter)
    def filterByCounty(QuerySet, stringFilter):
        return QuerySet.filter(county__contains=stringFilter)
    def filterByState(QuerySet, stringFilter):
        return QuerySet.filter(state__contains=stringFilter)

    def filterByAge(QuerySet, intFilter):
        return QuerySet.filter(age=intFilter)
    def filterByZip(QuerySet, intFilter):
        return QuerySet.filter(zip=intFilter)

    def filterByDateOccurred(QuerySet, lowerBound, upperBound):
        return QuerySet.filter(date_occurred__range=[lowerBound, upperBound])

    def filterByTimeOccurred(QuerySet, lowerBound, upperBound):
        return QuerySet.filter(time_occurred__range=[lowerBound, upperBound])

#for some reason datetime has trouble creating dates when day paramter >= 08
    firstDate = datetime.date(2012,11,06)
    secondDate = datetime.date(2016,10,07)
    out = filterByDateOccurred(Arrest_test.objects.all(), firstDate, secondDate)[0]   
 
    firstTime = datetime.time(1,1,1)
    secondTime = datetime.time(17,12,12)
    out = filterByTimeOccurred(Arrest_test.objects.all(), firstTime, secondTime)[0]

    output = '''
        <html>
            <head>
                <title>
                    Connecting to the model
                </title>
            </head>
            <body>
                <h1>
                    Connecting to the model
                </h1>
                %s
            </body>
        </html>''' % (
		out
	)
    return HttpResponse(output)

def usermanual(request):
    full_path = os.path.realpath(__file__)
    file_path = '%s/usermanual' % os.path.dirname(full_path) 
    with open(file_path) as file:
	html = file.readlines()
    return HttpResponse(html)    

def search(request):
    return render(request, 'SearchPage.html')

def result(request):

    entry = request.META["QUERY_STRING"]
    entry_list = entry.split("&")
    entry_dict = {}
    for item in entry_list:
	item_split = item.split("=")
	entry_dict[item_split[0]] = item_split[1]
    entry = entry_dict['searchbar']

    QuerySet = Arrest_test.objects.all()

    def filterByName(QuerySet, stringFilter):
        return QuerySet.filter(name__icontains=stringFilter)
    def filterByAgency(QuerySet, stringFilter):
        return QuerySet.filter(agency__icontains=stringFilter)
    def filterByCharge(QuerySet, stringFilter):
        return QuerySet.filter(charge__icontains=stringFilter)
    def filterByRace(QuerySet, stringFilter):
        return QuerySet.filter(race__icontains=stringFilter)
    def filterByAddress(QuerySet, stringFilter):
        return QuerySet.filter(address__icontains=stringFilter)
    def filterByOffenseCode(QuerySet, stringFilter):
        return QuerySet.filter(offense_code__icontains=stringFilter)
    def filterByReportingOfficer(QuerySet, stringFilter):
        return QuerySet.filter(reporting_officer__icontains=stringFilter)
    def filterByStreetAddress(QuerySet, stringFilter):
        return QuerySet.filter(street_address__icontains=stringFilter)
    def filterByCity(QuerySet, stringFilter):
        return QuerySet.filter(city__icontains=stringFilter)
    def filterByCounty(QuerySet, stringFilter):
        return QuerySet.filter(county__icontains=stringFilter)
    def filterByState(QuerySet, stringFilter):
        return QuerySet.filter(state__icontains=stringFilter)
    def filterBySex(QuerySet, stringFilter):
        return QuerySet.filter(sex__icontains=stringFilter)

    def filterByAge(QuerySet, intFilter):
        return QuerySet.filter(age=intFilter)
    def filterByZip(QuerySet, intFilter):
        return QuerySet.filter(zip=intFilter)

    outputList = []
    for i in entry_dict.keys():
        if i == 'name':
            QuerySet = filterByName(QuerySet, entry_dict[i])
        if i == 'agency':
            QuerySet = filterByAgency(QuerySet, entry_dict[i])            
        if i == 'charge':
            QuerySet = filterByCharge(QuerySet, entry_dict[i])
        if i == 'race':
            QuerySet = filterByRace(QuerySet, entry_dict[i])
        if i == 'address':
            QuerySet = filterByAddress(QuerySet, entry_dict[i])
        if i == 'offenseCode':
            QuerySet = filterByOffenseCode(QuerySet, entry_dict[i])
        if i == 'officerinvolved':
            QuerySet = filterByReportingOfficer(QuerySet, entry_dict[i])
        if i == 'streetaddress':
            QuerySet = filterByStreetAddress(QuerySet, entry_dict[i])
        if i == 'city':
            QuerySet = filterByCity(QuerySet, entry_dict[i])
        if i == 'county':
            QuerySet = filterByCounty(QuerySet, entry_dict[i])
        if i == 'state':
            QuerySet = filterByState(QuerySet, entry_dict[i])
        if i == 'sex':
            QuerySet = filterBySex(QuerySet, entry_dict[i])
        if i == 'zip':
            QuerySet = filterByZip(QuerySet, entry_dict[i])
        if i == 'age':
            QuerySet = filterByAge(QuerySet, entry_dict[i])

    for j in QuerySet:
        outputList.append(j)

    context = {'outputList': outputList}
    return render(request, 'ResultPage.html', context)

#def detail(request):
#    return render(request, RenderedResultString, '130.211.132.6/result')

