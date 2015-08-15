#!/bin/sh

TEMP_DIR=`echo "pdfs_being_converted"`

PDFS_DIR=`echo "/mnt/pd1/pdfs"`
XMLS_DIR=`echo "/mnt/pd1/xmls"`
LOGS_DIR=`echo "/mnt/pd1/xmls/logs"`

mkdir -p "${XMLS_DIR}/"
mkdir -p "${LOGS_DIR}/"

rm -r /tmp/$TEMP_DIR > /dev/null 2>&1
#> /dev/null 2>&1 redirects all output to a black hole
mkdir /tmp/$TEMP_DIR

date=`date +%m%d%y`
tm=`date +%H%M%S`
logID=`echo "log${date}-${tm}.txt"`
log=`echo "${LOGS_DIR}/$logID"`

echo "temporary directory created at /tmp/${TEMP_DIR}...\n" >> "$log"


convert() {
	filename=`echo "$1"|awk -F'.' '{print $(NF-1)}'|awk -F'/' '{print $(NF)}'`
	#backtick^ (`) used to set var equal to output of a command
	#with awk, -F is input field separator and NF is var w/ num fields
	#this line stores the name of the file that was used as a cmd line arg of this script into the filename variable, w/out the type extension

	echo "attempting to convert ${filename}.xml ..." >> "$log"

	gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile="/tmp/pdfs_being_converted/$filename.pdf" -c .setpdfwrite -f "$1" >> "$log"
	#above line is GhostScript which copies input arg pdf to /tmp/
	#-q is quiet startup, -dNOPAUSE disables prompt+pause at page ends, -dBATCH tells it to quit at the end, -s selects output device + file,
	#-c starts PostScript, .setpdfwrite sets beneficial parameters, -f ends -c

	#below line was used when convert() may get either single file or directory as input; it strips the ultimate filename out of the absolute path
	#xmlpath=`echo "$2"|awk -F'/' 'BEGIN { ORS="/" } { for (i=1; i<NF; i++) print $i }'`

	pdftohtml -xml "/tmp/pdfs_being_converted/${filename}.pdf" "$2${filename}.xml" >> "$log"
	#converts the actual pdf to xml with the pdftohtml utility

	rm "/tmp/pdfs_being_converted/$filename.pdf"
}


#upload all the pdfs from each police department, one of {Arrest, Incident, Accident} (only getting Arrest for now)
for deptDir in `ls $PDFS_DIR` ; do
	count=$((0))

	#form absolute path
	fullDir=`echo "/mnt/pd1/pdfs/${deptDir}/Arrest/"`

	#if the dept contains an Arrest subdir...
	if [ -d "$fullDir" ]; then
		echo "\n=======================" >> "$log"
		echo "Converting pdfs in $fullDir ..." >> "$log"

		#form the absolute path to the subdir for Arrest xml files and make it if necessary
		xmlDir=`echo "/mnt/pd1/xmls/${deptDir}/Arrest/"`
		mkdir -p $xmlDir

		#try converting each pdf in the pdfs Arrest subdir, passing the xml subdir path where the conversion will be saved
		for pdf in $fullDir/*.pdf ; do
			#convert "$pdf" "$xmlDir"
			count=$((count + 1))
			test $((count)) -eq $((20)) && echo "did 20" >> "$log" && break
			#above line is another form of an if statement
		done
		echo "Done converting pdfs in $fullDir\n=======================" >> "$log"
	fi
done

#go thru args, finding pdfs
#	for arg in $@ ; do
#		filename=`echo "$arg" | grep -i ".pdf$"`
#		if [ "$filename" != "" ] ; then
#			convert "$filename"
#		fi
#	done


#echo "scraping converted pdfs and uploading to the database..."

#echo "\"$dir_to_upload\""
#echo "execfile(\"./test.py\",\"$dir_to_upload\")\nprint \"ok\"" | python odnc_police/manage.py shell
