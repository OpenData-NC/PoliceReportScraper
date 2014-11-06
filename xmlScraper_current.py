import os #used to work on an entire directory of xml files


#opens a file and reads its lines into a list, one item per line.
def getFileLinesList(filepath):
    theFile = open(filepath)
    listOfLines = theFile.readlines()
    theFile.close()
    return listOfLines

def qsort(lineItemList):
    """Modified Quicksort using list comprehensions"""
    if len(lineItemList) == 0: 
        return []
    else:
        if (len(lineItemList) == 1):
            return lineItemList
        else:
            skipIndex = len(lineItemList)/2
            pivot = lineItemList[skipIndex][0]
            skippedItem = lineItemList.pop(skipIndex)
            lesser = qsort([x for x in lineItemList if x[0] < pivot])
            greater = qsort([x for x in lineItemList if x[0] >= pivot])
            return lesser + [skippedItem] + greater


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
    if beginIndex == -1: #basic check
        return -1
    restOfLine = line[beginIndex:]
    nextDelimiterIndex = restOfLine.find(secondDelimiter)
    if nextDelimiterIndex == -1:
        return line[beginIndex:] #shouldn't really happen
    endIndex = beginIndex + nextDelimiterIndex
    return line[beginIndex:endIndex]



#This function goes through the list of lines read from the file and partially
#parses the text of each line, saving info in either a field list or a data list.
#The relevant information from each line is the numbers assigned to top and left,
#as well as the actual text data represented in the line.
#Finally, the two lists are sorted with respect to the top coordinates.
def createLineIndex(listOfLines):
    lineDataItemList = [] #to store text data and top/left coords in better structure
    lineFieldItemList = []
    
    for line in listOfLines:
        
        if ('<text' in line):

            #extracts the digits of the left coordinate as a string
            lineLeft = int(getTextBetweenDelimiters(line, 'left="', '"'))

            if (lineLeft < 60):
                continue
            else:
                #extracts the digits of the top coordinate as a string
                lineTop = int(getTextBetweenDelimiters(line, 'top="', '"'))

                if (line.find('<b>') != -1):
                    lineData = getTextBetweenDelimiters(line, '<b>', '<')
                    dataMarker = True
                elif (line.find('<i>') != -1):
                    lineData = getTextBetweenDelimiters(line, '<i>', '<')
                    dataMarker = True
                else:
                    lineData = getTextBetweenDelimiters(line, '>', '<')
                    dataMarker = False
                    
                if (lineData == -1):
                    lineData = "IRREGULARLY FORMATTED TEXT LINE IN XML FILE"
                    dataMarker = False

                lineItem = [lineTop, lineLeft, lineData]
                if (dataMarker):
                    lineDataItemList.append(lineItem)
                else:
                    lineFieldItemList.append(lineItem)

    sortedDataItemList = qsort(lineDataItemList)
    sortedFieldItemList = qsort(lineFieldItemList)

    return sortedDataItemList, sortedFieldItemList



def processSortedLists(dlist, flist, sectionNameCoordList):
    """Separates list items into chunks that are representative of sections of the pdf.
    sectionNameCoordList is a list of two item lists of the form [yCoordofSectionBreak, "name of section"]"""
    kvpsMaster = []    

    for coord in sectionNameCoordList:
        tempDlist = []
        tempFlist = []
        while (dlist[0][0] < coord[0]):
            tempDlist.append(dlist.pop(0))
        while (flist[0][0] < coord[0]):
            tempFlist.append(flist.pop(0))

        #we now have tempDlist and tempFlist containing all the data and fields within a certain
        #section of the pdf. they are passed to another function to try to pair appropriate values.

        listOfMatchedValues = pairFieldandData(tempDlist, tempFlist, coord[1]) #coord[1] is the name of the section; used for state

        
        kvpsMaster.extend(listOfMatchedValues)

    return kvpsMaster






def pairFieldandData(dlistChunk, flistChunk, state):

    dlistNoChecks, flistNoChecks, kvps = stripCheckmarkData(dlistChunk, flistChunk, state)

    unmatchedData = []
    
    if (state == "AGENCY_INFO"):
        
        while (len(flistNoChecks) > 0):
            #print flistNoChecks[0][2] + ' @ ' + str(flistNoChecks[0][0]) + ', ' + str(flistNoChecks[0][1]) + ' compared to '
            for y in range(len(dlistNoChecks)):
                #print dlistNoChecks[y][2] + ' @ ' + str(dlistNoChecks[y][0]) + ', ' + str(dlistNoChecks[y][1])
                if ((abs(flistNoChecks[0][1] - dlistNoChecks[y][1]) < 10)
                    and abs((flistNoChecks[0][0]+20) - dlistNoChecks[y][0]) < 10):
                    #print "Match Found"
                    kvps.append([flistNoChecks[0][2], dlistNoChecks[y][2]])
                    flistNoChecks.pop(0)
                    dlistNoChecks.pop(y)
                    break
                if (y == len(dlistNoChecks)-1):
                    #print "No Match Found"
                    kvps.append([flistNoChecks[0][2], 'NULL'])
                    flistNoChecks.pop(0)
            #print "--------------------------------------------"

        #these two loops fix a one-off technicality instance of weirdness in the forms we're dealing with
        #where two separate fields are represented together; here they are separated.
        for x in kvps:
            if (x[0] == 'ORI'):
                dateTimeArrested = x[1][-17:]
                x[1] = x[1][:-18]
        for x in kvps:
            if (x[0] == 'Date/Time Arrested'):
                x[1] = dateTimeArrested
            
       
    elif (state == "ARRESTEE_INFO"):

        #remove these first because the field is split into two lines and oddly formatted (it is handled on its own afterwards)
        flistNoChecks = removeFromFieldList(flistNoChecks, 'Country of')
        flistNoChecks = removeFromFieldList(flistNoChecks, 'Citizenship')
        kvps.append(["Country of Citizenship", "NULL"])

        #occupation is often a problem spot that doesn't get matched so we match it specifically before going general
        flistNoChecks = removeFromFieldList(flistNoChecks, 'Occupation')
        for x in range(len(dlistNoChecks)):
            if (dlistNoChecks[x][0] < 180 or dlistNoChecks[x][0] > 210):
                continue
            elif (dlistNoChecks[x][1] < 500 or dlistNoChecks[x][1] > 720):
                continue
            else:
                kvps.append(["Occupation", dlistNoChecks[x][2]])
                dlistNoChecks.pop(x)
                break

        while (len(flistNoChecks) > 0):
            #print flistNoChecks[0][2] + ' @ ' + str(flistNoChecks[0][0]) + ', ' + str(flistNoChecks[0][1]) + ' compared to '
            for y in range(len(dlistNoChecks)):
                #print dlistNoChecks[y][2] + ' @ ' + str(dlistNoChecks[y][0]) + ', ' + str(dlistNoChecks[y][1])
                if ((abs(flistNoChecks[0][1] - dlistNoChecks[y][1]) < 12)
                    and abs((flistNoChecks[0][0]+22) - dlistNoChecks[y][0]) < 10):
                    #print "Match Found"
                    kvps.append([flistNoChecks[0][2], dlistNoChecks[y][2]])
                    flistNoChecks.pop(0)
                    dlistNoChecks.pop(y)
                    break
                if (y == len(dlistNoChecks)-1):
                    #print "No Match Found"
                    kvps.append([flistNoChecks[0][2], 'NULL'])
                    flistNoChecks.pop(0)
            #print "--------------------------------------------"

        #these two are oddly formatted and probably won't have matched correctly
        stateofbirth = 'NULL'
        citizenship = 'NULL'

        #so assuming they haven't... find them where they usually are:
        for d in dlistNoChecks:
            if (abs(d[0] - 158) < 6):
                if (abs(d[1] - 765) < 10):
                    stateofbirth = d[2]
                elif (abs(d[1] - 790) < 10):
                    citizenship = d[2]
            else:
                unmatchedData.append(d)

        for x in kvps:
            if (x[0] == 'Country of Citizenship'):
                x[1] = citizenship
            if (x[0] == 'Place of Birth' and x[1] == 'NULL'):
                x[1] = stateofbirth
                
                    
    elif (state == "ARREST_INFO"):
        
        while (len(flistNoChecks) > 0):
            #print flistNoChecks[0][2] + ' @ ' + str(flistNoChecks[0][0]) + ', ' + str(flistNoChecks[0][1]) + ' compared to '
            for y in range(len(dlistNoChecks)):
                #print dlistNoChecks[y][2] + ' @ ' + str(dlistNoChecks[y][0]) + ', ' + str(dlistNoChecks[y][1])
                if ((abs(flistNoChecks[0][1] - dlistNoChecks[y][1]) < 12)
                    and abs((flistNoChecks[0][0]+15) - dlistNoChecks[y][0]) < 10):
                    #print "Match Found"
                    kvps.append([flistNoChecks[0][2], dlistNoChecks[y][2]])
                    flistNoChecks.pop(0)
                    dlistNoChecks.pop(y)
                    break
                if (y == len(dlistNoChecks)-1):
                    #print "No Match Found"
                    kvps.append([flistNoChecks[0][2], 'NULL'])
                    flistNoChecks.pop(0)
            #print "--------------------------------------------"

        for d in dlistNoChecks:
            unmatchedData.append(d)
##    elif (state == "VEH_INFO"):
##
##    elif (state == "BOND"):
##
##    elif (state == "DRUGS"):
##
##    elif (state == "COMP"):
##
##    elif (state == "NARRATIVE"):
##
##    elif (state == "STATUS"):

    for x in unmatchedData:
        print x

    return kvps


def removeFromFieldList(flist, field):
    for x in range(len(flist)):
        if (flist[x][2] == field):
            flist.pop(x)
            break
    return flist

def removeMultipleFromFieldList(flist, fieldsToRemove):
    for field in fieldsToRemove:
        flist = removeFromFieldList(flist, field)
    return flist

def stripCheckmarkData(dlistChunk, flistChunk, state):
    moe = 0 #margin of error; number of pixels by which something can be off its hardcoded position
    kvps = [] #key-value pairs
    savedIndices = [] #to save indices of data that's been matched to pop that data item at the end;
                        #can't do it when the match happens or the loop gets messed up and items may be skipped
    
    if (state == "AGENCY_INFO"):
        moe = 6
        for x in range(len(dlistChunk)):
            if (dlistChunk[x][2] == 'X'):
                if (abs(dlistChunk[x][1] - 79) < moe):
                    if (abs(dlistChunk[x][0] - 106) < moe):
                        kvps.append(["Prints Taken", True])
                        flistChunk = removeFromFieldList(flistChunk, 'Prints')
                        savedIndices.append(x)
                    elif (abs(dlistChunk[x][0] - 118) < moe):
                        kvps.append(["Photos Taken", True])
                        flistChunk = removeFromFieldList(flistChunk, 'Photos')
                        savedIndices.append(x)
                else: #something went wrong; there are checks but not in the right place
                    kvps.append(["ChkMkError", False])

        savedIndices.reverse()
        for x in savedIndices:
            dlistChunk.pop(x)
        flistChunk = removeFromFieldList(flistChunk, 'Taken')
                  
    elif (state == "ARRESTEE_INFO"):
        moe = 6
        
        for x in range(len(dlistChunk)):
            if (dlistChunk[x][2] == 'X'):
                if (dlistChunk[x][0] < 210):
                    if (abs(dlistChunk[x][1] - 735) < moe):
                        if (abs(dlistChunk[x][0] - 184) < moe):
                            kvps.append(["Residency Status", "Resident"])
                            flistChunk = removeMultipleFromFieldList(flistChunk, ['Resident', 'Non-Resident', 'Unknown'])
                            savedIndices.append(x)
                        elif (abs(dlistChunk[x][0] - 198) < moe):
                            kvps.append(["Residency Status", "Non-Resident"])
                            flistChunk = removeMultipleFromFieldList(flistChunk, ['Resident', 'Non-Resident', 'Unknown'])
                            savedIndices.append(x)
                    elif (abs(dlistChunk[x][1] - 815) < moe):
                        if (abs(dlistChunk[x][0] - 184) < moe):
                            kvps.append(["Residency Status", "Unknown"])
                            flistChunk = removeMultipleFromFieldList(flistChunk, ['Resident', 'Non-Resident', 'Unknown'])
                            savedIndices.append(x)
                    else: #something went wrong; there are checks but not in the right place
                        kvps.append(["ChkMkError", False])
                else:
                    if (abs(dlistChunk[x][0] - 262) < moe):
                        if (abs(dlistChunk[x][1] - 775) < moe):
                            kvps.append(["Consumed Drug/Alcohol", "Yes"])
                            flistChunk = removeMultipleFromFieldList(flistChunk, ['Yes', 'No', 'Unk'])
                            savedIndices.append(x)
                        elif (abs(dlistChunk[x][1] - 815) < moe):
                            kvps.append(["Consumed Drug/Alcohol", "No"])
                            flistChunk = removeMultipleFromFieldList(flistChunk, ['Yes', 'No', 'Unk'])
                            savedIndices.append(x)
                        elif (abs(dlistChunk[x][1] - 851) < moe):
                            kvps.append(["Consumed Drug/Alcohol", "Unknown"])
                            flistChunk = removeMultipleFromFieldList(flistChunk, ['Yes', 'No', 'Unk'])
                            savedIndices.append(x)
                            
        savedIndices.reverse()
        for x in savedIndices:
            dlistChunk.pop(x)

    elif (state == "ARREST_INFO"):
        chargeInfo = [False, False, False] #used to keep track of which charge numbers (1-3) have charges and which are null
        
        for x in range(len(dlistChunk)):
            if (dlistChunk[x][2] == 'X'):
                if (dlistChunk[x][0] < 380):
                    moe = 6
                    if (abs(dlistChunk[x][0] - 355) < moe):
                        if (abs(dlistChunk[x][1] - 278) < moe):
                            kvps.append(["Method of Arrest", "On-View"])
                            flistChunk = removeMultipleFromFieldList(flistChunk, ['On-View', 'Criminal Summons', 'Order for Arrest', 'Citation', 'Warrant'])
                            savedIndices.append(x)
                        elif (abs(dlistChunk[x][1] - 356) < moe):
                            kvps.append(["Method of Arrest", "Criminal Summons"])
                            flistChunk = removeMultipleFromFieldList(flistChunk, ['On-View', 'Criminal Summons', 'Order for Arrest', 'Citation', 'Warrant'])
                            savedIndices.append(x)
                    elif (abs(dlistChunk[x][0] - 370) < moe):
                        if (abs(dlistChunk[x][1] - 278) < moe):
                            kvps.append(["Method of Arrest", "Order for Arrest"])
                            flistChunk = removeMultipleFromFieldList(flistChunk, ['On-View', 'Criminal Summons', 'Order for Arrest', 'Citation', 'Warrant'])
                            savedIndices.append(x)
                        elif (abs(dlistChunk[x][1] - 375) < moe):
                            kvps.append(["Method of Arrest", "Citation"])
                            flistChunk = removeMultipleFromFieldList(flistChunk, ['On-View', 'Criminal Summons', 'Order for Arrest', 'Citation', 'Warrant'])
                            savedIndices.append(x)
                        elif (abs(dlistChunk[x][1] - 446) < moe):
                            kvps.append(["Method of Arrest", "Warrant"])
                            flistChunk = removeMultipleFromFieldList(flistChunk, ['On-View', 'Criminal Summons', 'Order for Arrest', 'Citation', 'Warrant'])
                            savedIndices.append(x)
                else:
                    moe = 6
                    if (abs(dlistChunk[x][1] - 328) < moe):
                        moe = 3
                        if (abs(dlistChunk[x][0] - 395) < moe):
                            kvps.append(["Charge 1 Type", "Felony"])
                            chargeInfo[0] = True
                            savedIndices.append(x)
                        elif (abs(dlistChunk[x][0] - 406) < moe):
                            kvps.append(["Charge 1 Type", "Misdemeanor"])
                            chargeInfo[0] = True
                            savedIndices.append(x)
                        elif (abs(dlistChunk[x][0] - 433) < moe):
                            kvps.append(["Charge 2 Type", "Felony"])
                            chargeInfo[1] = True
                            savedIndices.append(x)
                        elif (abs(dlistChunk[x][0] - 447) < moe):
                            kvps.append(["Charge 2 Type", "Misdemeanor"])
                            chargeInfo[1] = True
                            savedIndices.append(x)
                        elif (abs(dlistChunk[x][0] - 473) < moe):
                            kvps.append(["Charge 3 Type", "Felony"])
                            chargeInfo[2] = True
                            savedIndices.append(x)
                        elif (abs(dlistChunk[x][0] - 486) < moe):
                            kvps.append(["Charge 3 Type", "Misdemeanor"])
                            chargeInfo[2] = True
                            savedIndices.append(x)

        for x in range(len(chargeInfo)):
            if (chargeInfo[x] == False):
                kvps.append(["Charge " + str(x+1) + " Type", "NULL"])

        flistChunk = removeMultipleFromFieldList(flistChunk, ['Fel', 'Misd', 'Fel', 'Misd', 'Fel', 'Misd'])

        savedIndices.reverse()
        for x in savedIndices:
            dlistChunk.pop(x)
                            
##    elif (state == "VEH_INFO"):
##
##    elif (state == "BOND"):
##
##    elif (state == "DRUGS"):
##
##    elif (state == "COMP"):
##
##    elif (state == "NARRATIVE"):
##
##    elif (state == "STATUS"):

    return dlistChunk, flistChunk, kvps


#The next two functions are convenience functions I wrote so I wouldn't have
#to repetitively enter parameters when calling the functions in IDLE.
#Absolute file paths are more reliable.
#
#'filepath' is path to xml file
def getLineIndexFromFile(filepath):
    LOL = getFileLinesList(filepath)
    sortedDList, sortedFList = createLineIndex(LOL)
    return sortedDList, sortedFList

def getKVPMasterList(sortedDlist, sortedFlist, sectionNameCoordList):
    return processSortedLists(sortedDlist, sortedFlist, sectionNameCoordList)

#analagous usage but directoryPath is path to directory folder rather than file
def doItAllMultipleTimes(directoryPath):
    allData = []
    sncl = [[130, 'AGENCY_INFO']]
    for filename in os.listdir(directoryPath):
        dlist, flist = getLineIndexFromFile(directoryPath+filename)
        kvps = getKVPMasterList(dlist, flist, sncl)
        allData.append(kvps)
    return allData


#sncl = [[130, 'AGENCY_INFO'], [350, 'ARRESTEE_INFO'], [502, 'ARREST-INFO']]
#


#if you set 'path' to wherever your directory of (already converted!) xml files
#is located, the program should work by running this module and then entering the following commands:
#
#path = [your path here]
#dlist, flist = getLineIndexFromFile(path)
#sncl = [[130, 'AGENCY_INFO'], [350, 'ARRESTEE_INFO'], [502, 'ARREST-INFO']]
#kvps = getKVPMasterList(dlist, flist, sncl)
#for x in kvps:
#    print x


#this can be ignored, I use it bc of a file naming quirk that comes up when
#I try to use the pdftohtml unix util in a loop that goes through a whole
#directory. It would convert a pdf to 'example.pdf.xml', so I got rid of '.pdf'
def renamingScript(prependpath):
    for filename in os.listdir(prependpath):
        os.rename(prependpath+filename, prependpath+filename[:-8]+filename[-4:])
