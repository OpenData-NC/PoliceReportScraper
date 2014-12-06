#!/bin/sh
filename=`echo "$1"|awk -F'.' '{print $(NF-1)}'|awk -F'/' '{print $(NF)}'`
echo "$filename"
gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile="/tmp/pdfs_currently_being_uploaded/$filename.pdf" -c .setpdfwrite -f "$1"
pdftohtml -xml "/tmp/pdfs_currently_being_uploaded/$filename.pdf" "/home/vaughn.hagerty/django/PoliceReportScraper/sample_other_agency/xml/$filename.xml"
