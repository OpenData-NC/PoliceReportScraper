#!/bin/sh

if [ -d "$1" ]; then
	#program argument should be the directory containing the different directories of police departments
	for dir in $1/* ; do
		dept=`echo "$dir"|awk -F'/' '{print $(NF)}'`
		policedept=`echo "/mnt/pd1/xmls/${dept}/"`
		mkdir -p $policedept
		accidentpath=`echo "/mnt/pd1/xmls/${dept}/Accident/"`
		incidentpath=`echo "/mnt/pd1/xmls/${dept}/Incident/"`
		mkdir -p $accidentpath
		mkdir -p $incidentpath
	done
else
	echo "enter a directory"
fi
