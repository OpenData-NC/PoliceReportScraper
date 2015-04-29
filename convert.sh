#!/bin/sh

rm -r /tmp/pdfs_currently_being_uploaded > /dev/null 2>&1
#> /dev/null 2>&1 redirects all output to a black hole
mkdir /tmp/pdfs_currently_being_uploaded

convert() {
	filename=`echo "$1"|awk -F'.' '{print $(NF-1)}'|awk -F'/' '{print $(NF)}'`
	#backtick^ (`) used to set var equal to output of a command
	#with awk, -F is input field separator and NF is var w/ num fields
	#this line stores the name of the file that was used as a cmd line arg
	#of this script into the filename variable, w/out the type extension

	echo "converting $filename.pdf please wait..."

	gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile="/tmp/pdfs_currently_being_uploaded/$filename.pdf" -c .setpdfwrite -f "$1"
	#above line is GhostScript which copies input arg pdf to /tmp/
	#-q is quiet startup, -dNOPAUSE disables prompt+pause at page ends,
	#-dBATCH tells it to quit at the end, -s selects output device + file,
	#-c starts PostScript, .setpdfwrite sets beneficial parameters, -f ends -c

	xmlpath=`echo "$2"|awk -F'/' '{ print $(NF-2) }'`
	#gets the name of the dir containing the dir that contains the pdfs
	#which should be the name of the police department/type of report
	mkdir -p "/home/vaughn.hagerty/django/PoliceReportScraper/sample_other_agency/extra/$xmlpath/"
	pdftohtml -xml "/tmp/pdfs_currently_being_uploaded/$filename.pdf" "/home/vaughn.hagerty/django/PoliceReportScraper/sample_other_agency/extra/$xmlpath/$filename.xml"
	#converts the actual pdf to xml with the pdftohtml utility

	rm "/tmp/pdfs_currently_being_uploaded/$filename.pdf"

}

#if $1 is a directory
if [ -d "$1" ]; then
	#upload all the pdfs in the dir
	for pdf in $1/*.pdf ; do
		convert "$pdf" "$1"
	done

else
	#go thru args, finding pdfs
	for arg in $@ ; do
		filename=`echo "$arg" | grep -i ".pdf$"`
		if [ "$filename" != "" ] ; then
			convert "$filename"
		fi
	done

fi

echo "done"

#echo "scraping converted pdfs and uploading to the database..."

#echo "\"$dir_to_upload\""
#echo "execfile(\"./test.py\",\"$dir_to_upload\")\nprint \"ok\"" | python odnc_police/manage.py shell
