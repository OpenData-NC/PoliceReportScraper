#!/bin/sh

dir_to_upload="none"
new_folder=0


rm -r /tmp/pdfs_currently_being_uploaded > /dev/null 2>&1
mkdir /tmp/pdfs_currently_being_uploaded

convert(){
	filename=`echo "$1"|cut -f1 -d'.'|awk -F'/' '{print $(NF)}'`
	echo "converting $filename.pdf please wait..."

	gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile="/tmp/pdfs_currently_being_uploaded/$filename.pdf" -c .setpdfwrite -f "$1"
	pdftohtml -xml "/tmp/pdfs_currently_being_uploaded/$filename.pdf" "/tmp/pdfs_currently_being_uploaded/$filename.xml"
	rm "/tmp/pdfs_currently_being_uploaded/$filename.pdf"
}


if [ -d "$1" ];then
	#upload all the pdfs in the dir
	for pdf in $1/*.pdf ; do
		convert "$pdf"	
	done

else
	#go thru args, finding pdfs

	dir_to_upload="$1"
	for arg in $@;do
		echo "$arg"|grep -i ".pdf$"
		if [ $? -eq 0 ];then
			convert "$arg"
		fi
	done
	
	dir_to_upload=/tmp/pdfs_currently_being_uploaded
fi

echo "scraping converted pdfs and uploading to the database..."

echo "\"$dir_to_upload\""
echo "execfile(\"./test.py\",\"$dir_to_upload\")\nprint \"ok\"" | python odnc_police/manage.py shell

#rm -r /tmp/pdfs_currently_being_uploaded

echo "done"
