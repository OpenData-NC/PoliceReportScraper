#from django.shortcuts import render
#from django.http import HttpResponse
#import sqlite3
# Create your views here.
#def search(request):
    #return render(request, '130.211.132.6/home')

from django.http import HttpResponse
import datetime

def djangotest(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)



#def result(request):
    #Input from home javascript
    #Output a string constructed from sqlite3 query
    #search parameter needs to be inputted from filters and received data
    #Create sqlite3 query string
    #result research
   # QueryString = "Test QueryString"
    #Create an array of objects that contain a basic info string and a hyperlink
    #Hyperlink may just be 130.211.132.6/result
   # return render(request, QueryString, '130.211.132.6/search')

#def detail(request):
    # Create string object from returned request data returned from url that was clicked.
 #   RenderedResultString = "Test Result String"
#    return render(request, RenderedResultString, '130.211.132.6/result')

#sqlite3 queries used to build request objects
#Result will use the same string/ part of string / components as search
