#!/bin/sh

echo "\nworking...\n"

#directory constants
TEMP_DIR=`echo "pdfs_being_converted"`
PDFS_DIR=`echo "/mnt/pd2/pdfs"`

rm -r /tmp/$TEMP_DIR > /dev/null 2>&1
# > /dev/null 2>&1 redirects all output to a black hole
mkdir /tmp/$TEMP_DIR

#create file path to log file
date=`date +%m%d%y`
logID=`echo "log-of-full-scrape-${date}.txt"`
log=`echo "/mnt/pd2/django/PoliceReportScraper/$logID"`

rm `echo "$log"`

echo "temporary directory created at /tmp/${TEMP_DIR}...\n" >> "$log"

startDate=`date +%c`
echo "full library conversion initiated on $startDate" >> "$log"

#function used to copy pdfs to /tmp/ and convert them to xml using pdf2html -xml
convert() {
	#get just the filename with no absolute path and no type extension

	filename=`echo "$1"|awk -F'.' '{print $(NF-1)}'|awk -F'/' '{print $(NF)}'`

	#with awk, -F is input field separator and NF is a variable holding the number of fields
	#$1 is the first positional parameter called with this function

	echo "attempting to convert ${filename}.pdf ..." >> "$log"

	gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile="/tmp/${TEMP_DIR}/${filename}.pdf" -c .setpdfwrite -f "$1" >> "$log"
	#above line is GhostScript which copies input arg pdf to /tmp/
	#-q is quiet startup, -dNOPAUSE disables prompt+pause at page ends, -dBATCH tells it to quit at the end, -s selects output device + file,
	#-c starts PostScript, .setpdfwrite sets beneficial parameters, -f ends -c

	#below line was used when convert() may get either single file or directory as input; it strips the ultimate filename out of the absolute path
	#xmlpath=`echo "$2"|awk -F'/' 'BEGIN { ORS="/" } { for (i=1; i<NF; i++) print $i }'`

	echo "pdf2xml: $2/${filename}.xml" >> "$log"
	pdftohtml -xml "/tmp/${TEMP_DIR}/${filename}.pdf" "$2/${filename}.xml" >> "$log"
	#converts the actual pdf to xml with the pdftohtml utility

	rm "/tmp/${TEMP_DIR}/${filename}.pdf"
}


count=$((0))
deptCount=$((0))

#upload all the pdfs from each police department, one of {Arrest, Incident, Accident} (only getting Arrest for now)
for deptDir in `ls $PDFS_DIR` ; do

	#form absolute path
	fullDir=`echo "${PDFS_DIR}/${deptDir}/Arrest"`

	#if the dept contains an Arrest subdir...
	if [ -d "$fullDir" ]; then
		deptCount=$((deptCount + 1))
		echo "\n=======================" >> "$log"
		echo "Converting pdfs in $fullDir ...\n" >> "$log"
		echo "Converting pdfs in $fullDir ...\n"

		dirCount=$((0))

		#form the absolute path to the subdir for Arrest xml files and make it if necessary
		xmlDir=`echo "$fullDir" | sed -e "s/pdfs/xmls/"`
		mkdir -p $xmlDir

		#try converting each pdf in the pdfs Arrest subdir, passing the xml subdir path where the conversion will be saved
		for pdf in $fullDir/*.pdf ; do
			test $((deptCount)) -ne $((7)) && break
			convert "$pdf" "$xmlDir"
			count=$((count + 1))
			dirCount=$((dirCount + 1))
			#test $((dirCount)) -eq $((10)) && echo "did 10" >> "$log" && break
			#above line is another form of an if statement
		done
		echo "Done converting $dirCount pdfs in $fullDir\n=======================" >> "$log"
		echo "Finished $deptCount directories..."
	fi
done

date=`date +%c`
echo "\n\nFinished attempted conversion of $count files on $date" >> "$log"
echo "\ndone.\n"

#go thru args, finding pdfs
#	for arg in $@ ; do
#		filename=`echo "$arg" | grep -i ".pdf$"`
#		if [ "$filename" != "" ] ; then
#			convert "$filename"
#		fi
#	done


#echo "scraping converted pdfs and uploading to the database..."

#echo "execfile(\"./test.py\",\"$dir_to_upload\")" | python odnc_police/manage.py shell
