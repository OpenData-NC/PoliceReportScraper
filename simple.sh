#!/bin/bash
filename=`echo "$1"|awk -F'.' '{print $(NF-1)}'|awk -F'/' '{print $(NF)}'`
#above line stores the name of the file that was used as a cmd line
#parameter of this script into the 'filename' variable, w/out the type extnsn
echo "$filename"

gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile="/tmp/pdfs_currently_being_uploaded/$filename.pdf" -c .setpdfwrite -f "$1"
#above line is GhostScript which  copies input arg pdf to tmp

pdftohtml -xml "/tmp/pdfs_currently_being_uploaded/$filename.pdf" "/home/vaughn.hagerty/django/PoliceReportScraper/sample_other_agency/xml/$filename.xml"
#converts the actual pdf to xml
