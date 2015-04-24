#!/bin/sh

LIST=`ls`

echo "searching based on $1"

for i in "$LIST"; do
	j="$(grep -i $1 $i)"
	if [ "$j" != "" ] ; then
		cp $j /home/vaughn.hagerty/django/PoliceReportScraper/sample_other_agency/
		echo "copying $j..."
	fi
done

echo "done"

