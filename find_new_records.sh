#!/bin/bash


PDFS_DIR="/mnt/pd1/pdfs"
XMLS_DIR="/mnt/pd1/xmls"
LOGS_DIR="/mnt/pd1/xmls/logs"

DB="crime"
USR="ben"
CLR="nerRaWhB" #Clearance


declare -a new_records

count=$((0))

#get only the pdf path for now, convert them, and then run another mysql at that time to add the id and agency

while read record_path
do
	new_records+=( "$record_path" )
	echo "record ${count}: ${record_path}"
	(( count++ ))
done < <(mysql -D"$DB" -u"$USR" -p"$CLR" --skip-column-names --silent --execute="SELECT a.pdf FROM arrests a LEFT OUTER JOIN odnc_police_arrest o ON a.pdf = o.pdf WHERE (a.pdf LIKE '__%') AND (o.pdf IS NULL) LIMIT 20")

#new_records now contains all of the file paths to pdf files that exist in arrests but not in odnc_police_arrest

echo "======"
echo "======"


for i in "${new_records[@]}"
do
	deptDir=`dirname "$i"`

	#use sed to replace /pdf/ with /xml/ and create this directory if it does not already exist

	xmlDir=`echo "$deptDir" | sed -e "s/pdfs/xmls/"`
#	mkdir -p "$xmlDir"

	#use awk to get the common filename, dropping the type extension
#	filename=`echo "$i" | awk -F'.' '{print $(NF-1)}' | awk -F'/' '{print $(NF)}'`

	#then, use pdftohtml to copy/convert the pdf in deptDir to the xml in xmlDir
#	pdftohtml -xml "$i" "${xmlDir}/${filename}.xml"


	#then, connect to mysql again and retrieve record_id and agency to append to the xml file in <!-- --> tags
	echo "i: $i"
	id_and_agency=`mysql -D"$DB" -u"$USR" -p"$CLR" --silent --execute="SELECT pdf, record_id, agency FROM arrests WHERE (pdf = \"$i\") \G"`
	echo "id_and_agency:"
	echo "$id_and_agency"


	#Look into the -tee option for mysql (appending results to a file) and also consider alternatives to connecting to mysql every time

	#shit, will there be problems with cron scheduling and having to run the python shell through manage.py?
done
