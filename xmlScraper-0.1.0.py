import os #used to work on an entire directory of xml files, can be safely removed if this is not needed


#opens a file and reads its lines into a list, one item per line.
def getFileLinesList(filepath):
    theFile = open(filepath)
    listOfLines = theFile.readlines()
    theFile.close()
    return listOfLines


#helper function I wrote to easily extract data from a string.
#'line' is the string to extract from, 'firstDelimiter' is a string that
#identifies where to start looking, and 'secondDelimiter' is the char
#(or string) that signifies the end of the text that will be extracted.
#e.g. to extract '576' from 'top="33" left="576" blahblah':
#line = 'top="33" left="576" blahblah'
#firstDelim = 'left="'   (technically more than needed, but might as well make it readable)
#secondDelim = '"'
def getTextBetweenDelimiters(line, firstDelimiter, secondDelimiter):
    beginIndex = line.find(firstDelimiter) + len(firstDelimiter)
    if beginIndex == -1: #basic check, maybe not the most useful return value
        return 'delimiter not found'
    restOfLine = line[beginIndex:]
    nextDelimiterIndex = restOfLine.find(secondDelimiter)
    if nextDelimiterIndex == -1:
        return line[beginIndex:] #shouldn't really happen
    endIndex = beginIndex + nextDelimiterIndex
    return line[beginIndex:endIndex]


#This function goes through the list of lines read from the file and
#partially parses the text of each line, comparing the resulting data to
#a list of coordinates that is passed in as a parameter.
#The relevant information from each line is the numbers assigned to top and left.
#The coordList supplied as a parameter should be a list of 2-item lists.
#The 2-item lists should be the pairs of top coord (at[0]) & left coord (at[1])
#that we are looking for to identify a certain field, as strings.
#e.g.: top=155 and left=73 is Name. The list would be ['76', 696']
#The goal is to get the text data of a line if its coordinates match.
def pullImportantLines(listOfLines, coordList):
    matchingLinesData = [] #to store data pulled from matching lines
    
    for line in listOfLines:
        #after looking at the converted .xml files, the lines we're concerned
        #with all begin the same way, so we can skip anything else
        #(more optimizations are almost definitely possible)
        if ('<text' in line):

            #extracts the digits of the top coordinate as a string
            lineTop = getTextBetweenDelimiters(line, 'top="', '"')

            #extracts the digits of the left coordinate as a string
            lineLeft = getTextBetweenDelimiters(line, 'left="', '"')

            lineCoords = [lineTop, lineLeft]

            
            #now that we have the line's coords, go through for matches
            for coordPair in coordList:
                if (lineCoords == coordPair):
                    #the actual text data seems to always be between bold tags.
                    #this is useful for finding it quickly
                    lineData = getTextBetweenDelimiters(line, '<b>', '<')
                    matchingLinesData.append(lineData)
                    break #if we find a match, no need to check other lines.
                #note that for each line from the file, we go through each
                #coord pair, and not vice versa. Only 1 pass through the file.
                #This also means that data is added to the return list in the
                #order it is found in the file, not the order of the coordList

    #returns a list of strings of the actual text data
    return matchingLinesData


#The next two functions are convenience functions I wrote so I wouldn't have
#to repetitively enter parameters when calling the functions in IDLE.
#doItAll works on one xml file, and doItAllMultipleTimes works on a directory
#of entirely xml files. Absolute file paths are more reliable.
#
#'filepath' is path to xml file; 'coordList' is list of coords to match against
def doItAll(filepath, coordList):
    LOL = getFileLinesList(filepath)
    data = pullImportantLines(LOL, coordList)
    return data

#analagous usage but directoryPath is path to directory folder rather than file
def doItAllMultipleTimes(directoryPath, coordList):
    allData = []
    for filename in os.listdir(directoryPath):
        allData.append(doItAll(directoryPath+filename, coordList))
    return allData


#path = 'C:\\Users\\Ben\\Desktop\\odnc\\xml\\samples\\'
#(this is where my directory to test on was located so I saved the string here)
#
#coordList = [['76', '696'], ['155', '73'], ['396', '72'], ['259', '481'], ['1057', '416'], ['194', '643'], ['641', '89']]
#an example coordList. In order, the coordinates target:
#coordList = [[OCA number],     [name],     [first charge],    [height], [date/time submitted], [occupation], [type bond]
#
#Notes: All these coords come from manual inspection of various chapel hill arrest reports.
#The first five of these seem to be extracted reliably, either because
#they are left-aligned and their left coord is always the same, or because they
#are center-aligned and the text is always the same length.
#[occupation] is an example of a center-aligned field that is not always the
#same length, and it is not extracted reliably. I think we can code around that
#pretty easily, but I didn't worry about it for now.
#[type bond] is the one check mark I tried to extract. It only extracts an 'X'
#as the data right now, and it only extracts that 'X' if it's in the one box
#out of five in that field that those coordinates indicate. Mostly I included
#it just to make sure we could get it, but to get any use out of it, we'll need
#to somehow associate each of the five possible coord pairs with the correct
#field ('type bond'), and then associate whichever one is actually present with
#the actual text next to the checkbox instead of just an 'X'.


#if you set 'path' to wherever your directory of (already converted!) xml files
#is located, and use the supplied coordList, the program should work by running
#this module and then entering the following commands:
#
#path = [your path here]
#coordList = [['76', '696'], ['155', '73'], ...etc. from above
#allData = doItAllMultipleTimes(path, coordList)
#for i in allData:
#    print i
#


#this can be ignored, I use it bc of a file naming quirk that comes up when
#I try to use the pdftohtml unix util in a loop that goes through a whole
#directory. It would convert a pdf to 'example.pdf.xml', so I got rid of '.pdf'
def renamingScript(prependpath):
    for filename in os.listdir(prependpath):
        os.rename(prependpath+filename, prependpath+filename[:-8]+filename[-4:])
