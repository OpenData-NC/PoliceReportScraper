
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from django.db.models import Q
from models import Arrest
from itertools import chain
from operator import and_, or_
import datetime
import os
import re

def hello(request):
    return HttpResponse("Hello World the last time")

def search(request):
    return render(request, 'SearchPage.html')

def result(request):

    entry=request.META["QUERY_STRING"]
    entry=entry.replace("+"," ")
    entry=entry.replace("%2B"," ")
    entry_list=entry.split("&")
    entry_dict={}
    entry_dict['agency']=[]
    for item in entry_list:
	item_split=item.split("=")
	if(item_split[0]=="agency"):
		entry_dict[item_split[0]].append(item_split[1])
	else:
		entry_dict[item_split[0]]=item_split[1]

    def filterByName(QuerySet, stringFilter):
        return QuerySet.filter(Name__icontains=stringFilter)
    def filterByAgencyName(QuerySet, stringFilter):
        return QuerySet.filter(Agency_Name__icontains=stringFilter)
    def filterByCharge(QuerySet, stringFilter):
        return QuerySet.filter(Charge1__icontains=stringFilter)
    def filterByRace(QuerySet, stringFilter):
        return QuerySet.filter(Race__icontains=stringFilter)
    def filterByAddress(QuerySet, stringFilter):
        return QuerySet.filter(Address__icontains=stringFilter)
    def filterByChargeCode(QuerySet, stringFilter):
        return QuerySet.filter(Charge1_DCI_Code__icontains=stringFilter)
    def filterByArrestingOfficer(QuerySet, stringFilter):
        return QuerySet.filter(Arresting_Officer_Signature__icontains=stringFilter)
    def filterByPlaceofArrest(QuerySet, stringFilter):
        return QuerySet.filter(Place_of_Arrest__icontains=stringFilter)
    def filterBySex(QuerySet, stringFilter):
        return QuerySet.filter(Sex__icontains=stringFilter)

    def filterByAge(QuerySet, intFilter):
        return QuerySet.filter(Age=intFilter)

    def filterByDateArrested(QuerySet, lowerBound, upperBound):
        return QuerySet.filter(Date_Arrested__range=[lowerBound, upperBound])

    def filterBySearchbar(QuerySet, stringFilter):
        stringFilter = stringFilter.replace("+", " ")
        QuerySet = QuerySet.filter(Q(Name__icontains=stringFilter) | Q(Agency_Name__icontains=stringFilter) | Q(Charge1__icontains=stringFilter) | Q(Race__icontains=stringFilter) | Q(Address__icontains=stringFilter) | Q(Charge1_DCI_Code__icontains=stringFilter) | Q(Arresting_Officer_Signature__icontains=stringFilter) | Q(Place_of_Arrest__icontains=stringFilter) | Q(Sex__icontains=stringFilter))
        return QuerySet

    agencyList = []
    querySetList = []
    firstDateString = ''
    secondDateString = ''
    firstDateReached = False
    secondDateReached = False
    QuerySet = Arrest_test.objects.all()

    for i in entry_dict.keys():
        #entry_dict[i] = entry_dict[i].replace("+", " ")
        if i == 'searchbar':
            if(entry_dict[i] != ''):
                QuerySet = filterBySearchbar(QuerySet, entry_dict[i])                
        if i == 'name':
            QuerySet = filterByName(QuerySet, entry_dict[i])
        if i == 'agency':
            agencyList=entry_dict[i]
        if i == 'charge':
            QuerySet = filterByCharge(QuerySet, entry_dict[i])
        if i == 'race':
            QuerySet = filterByRace(QuerySet, entry_dict[i])
        if i == 'address':
            QuerySet = filterByAddress(QuerySet, entry_dict[i])
        if i == 'offenseCode':
            QuerySet = filterByOffenseCode(QuerySet, entry_dict[i])
        if i == 'officerinvolved':
            QuerySet = filterByArrestingOfficer(QuerySet, entry_dict[i])
        if i == 'sex':
            QuerySet = filterBySex(QuerySet, entry_dict[i])
        if i == 'age':
            QuerySet = filterByAge(QuerySet, entry_dict[i])
        if i == 'from':
            firstDateString = entry_dict[i]
            firstDateReached = True
        if i == 'to':
            secondDateString = entry_dict[i]
#            firstDateString = entry_dict[i]
            secondDateReached = True
        if firstDateReached == True:
            if secondDateReached == True:    
                firstDate = datetime.date(int(firstDateString[:4]), int(firstDateString[5:7]), int(firstDateString[8:10]))
                secondDate = datetime.date(int(secondDateString[:4]), int(secondDateString[5:7]), int(secondDateString[8:10]))
                QuerySet = filterByDateArrested(QuerySet, firstDate, secondDate)
	
        for a in agencyList:
            temporaryQuerySet = QuerySet.filter(Agency_Name__icontains=a)
            querySetList.append(temporaryQuerySet)

    outputList = []
    #for k in querySetList:
    #    QuerySet = reduce(or_, querySetList)
    if(len(querySetList)>0):
        masterQuerySet = reduce(or_, querySetList)
        masterQuerySet = reduce(and_, [masterQuerySet],QuerySet)
    else:
        masterQuerySet = QuerySet

    context = {'outputList':outputList, 'QuerySet':masterQuerySet}

    return render(request, 'ResultPage.html', context)

def detail(request):
     
     OCARequest=request.META["QUERY_STRING"]
     def filterByOCA(QuerySet, intFilter):
         return QuerySet.filter(OCA=intFilter)

     QuerySet = Arrest_test.objects.all()
     QuerySet = filterByOCA(QuerySet, OCARequest)
     
     context={'QuerySet':QuerySet}
     return render(request, 'DetailPage.html', context)

