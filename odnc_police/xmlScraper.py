import os #used to work on an entire directory of xml files
import datetime

currentOCA = ""

#opens a file and reads its lines into a list, one item per line.
def getFileLinesList(filepath):
    theFile = open(filepath)
    fileLines = theFile.readlines()
    theFile.close()
    listOfLines, extraLines = [], []

    #keep only lines of text, and separate the first page from any additional pages.
    for line in fileLines:
        if ('<text' in line):
            listOfLines.append(line)
        elif ('</page>' in line):
            startIndex = fileLines.index(line)+1
            temp = fileLines[startIndex:]
            for lineitem in temp:
                if ('<text' in lineitem):
                    extraLines.append(lineitem)
            break
    return listOfLines, extraLines

def qsort(lineItemList, sortParameter):
    """Modified Quicksort using list comprehensions"""
    if len(lineItemList) == 0: 
        return []
    elif (sortParameter != 1):
        if (len(lineItemList) == 1):
            return lineItemList
        else:
            skipIndex = len(lineItemList)/2
            pivot = lineItemList[skipIndex][0]
            skippedItem = lineItemList.pop(skipIndex)
            lesser = qsort([x for x in lineItemList if x[0] < pivot], 0)
            greater = qsort([x for x in lineItemList if x[0] >= pivot], 0)
            return lesser + [skippedItem] + greater
    else: #sortParameter == 1 == sorting by left coord (above is top coord)
        if (len(lineItemList) == 1):
            return lineItemList
        else:
            skipIndex = len(lineItemList)/2
            pivot = lineItemList[skipIndex][1]
            skippedItem = lineItemList.pop(skipIndex)
            lesser = qsort([x for x in lineItemList if x[1] < pivot], 1)
            greater = qsort([x for x in lineItemList if x[1] >= pivot], 1)
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
def createLineIndex(listOfLines):
    global extraLines
    lineDataItemList = [] #to store text data and top/left coords in better structure
    lineFieldItemList = []
    
    for line in listOfLines:
        if ('</page>' in line):
            startIndex = listOfLines.index(line)+1
            temp = listOfLines[startIndex:]
            for lineitem in temp:
                if ('<text' in lineitem):
                    extraLines.append(lineitem)
            break
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

    return lineDataItemList, lineFieldItemList

def grabRelevantDataAndFields(dlist, flist, start, end):
    tempDlist, tempFlist, savedIndices = [], [], []

    for x in range(len(dlist)):
        if (dlist[x][0] > start and dlist[x][0] < end):
            tempDlist.append(dlist[x])
            savedIndices.append(x)
    savedIndices.reverse()
    for x in savedIndices:
        dlist.pop(x)
    savedIndices = []
    for y in range(len(flist)):
        if (flist[y][0] > start and flist[y][0] < end):
            tempFlist.append(flist[y])
            savedIndices.append(y)
    savedIndices.reverse()
    for y in savedIndices:
        flist.pop(y)

    return dlist, flist, tempDlist, tempFlist


def markAppropriateFieldsNull(flist, section):
    #this function is only called when ALL fields in a certain section have no data. In other cases empty fields
    #are marked as NULL after all the data in the section has been matched, in pairFieldandData
    kvps = []

    if (section == "AGENCY_INFO"): #makes no sense and should never happen (no arresting agency info?)
        print "Something Nonsensical Happened"
    elif (section == "ARRESTEE_INFO"): #also makes no sense (no information on who was arrested?)
        print "Something Nonsensical Happened"
    elif (section == "ARREST_INFO"): #definitely makes no sense (no crime data?)
        print "Something Nonsensical Happened"
        #--> the first three sections must have some data in every case
    elif (section == "VEH_INFO"):
        flist = removeMultipleFromFieldList(flist, ['Vehicle', 'Left at Scene', 'Secured', 'Unsecure', 'Date/Time', '1.', 
                                                    '2.', '3.', 'Released to other at owners request', 'Name of Other',
                                                    'Impounded', 'Place of storage', 'Inventory on File?'])
        kvps.append(['Vehicle Status', 'NULL'])
        kvps.append(['Vehicle Status Datetime', 'NULL'])
        for item in flist:
            kvps.append([item[2], 'NULL'])
   # elif (section == "BOND"):
         
   # elif (section == "DRUGS"):
        
    elif (section == "COMP"):
        flist = removeMultipleFromFieldList(flist, ['Complainant', 'Victim', 'Name:', 'Address', 'Phone:'])
        kvps.append(['Comp', 'NULL'])
        kvps.append(['Comp Name', 'NULL'])
        kvps.append(['Comp Address', 'NULL'])
        kvps.append(['Comp Phone', 'NULL'])
    elif (section == "NARRATIVE"):
        #don't think this is possible either but just in case
        kvps.append(['Narrative', 'NULL'])
    elif (section == "STATUS"): #also definitely not possible (no arresting officer info?)
        print "Something Nonsensical Happened"

    return kvps

    

def processLists(dlist, flist, sectionsToGrab, extraLines, verboseOpt):
    """Separates list items into chunks that are representative of sections of the pdf,
    and digests the report into a master list of key-value pairs, stored as a dictionary."""
    kvpsMaster = []

    sdlist = qsort(dlist, 0)
    sflist = qsort(flist, 0)

    for section in sectionsToGrab:

        expectedMatch = True
        if (section == "AGENCY_INFO"):
            sdlist, sflist, tempDlist, tempFlist = grabRelevantDataAndFields(sdlist, sflist, 0, 130)
        elif (section == "ARRESTEE_INFO"):
            sdlist, sflist, tempDlist, tempFlist = grabRelevantDataAndFields(sdlist, sflist, 129, 350)
        elif (section == "ARREST_INFO"):
            sdlist, sflist, tempDlist, tempFlist = grabRelevantDataAndFields(sdlist, sflist, 349, 502)
        elif (section == "VEH_INFO"):
            sdlist, sflist, tempDlist, tempFlist = grabRelevantDataAndFields(sdlist, sflist, 501, 587)
        elif (section == "BOND"):
            sdlist, sflist, tempDlist, tempFlist = grabRelevantDataAndFields(sdlist, sflist, 586, 689)
        elif (section == "DRUGS"):
            sdlist, sflist, tempDlist, tempFlist = grabRelevantDataAndFields(sdlist, sflist, 688, 895)
        elif (section == "COMP"):
            sdlist, sflist, tempDlist, tempFlist = grabRelevantDataAndFields(sdlist, sflist, 894, 941)
        elif (section == "NARRATIVE"):
            sdlist, sflist, tempDlist, tempFlist = grabRelevantDataAndFields(sdlist, sflist, 940, 1040)
        elif (section == "STATUS"):
            sdlist, sflist, tempDlist, tempFlist = grabRelevantDataAndFields(sdlist, sflist, 1039, 1111)
        else:
            expectedMatch = False
                
        #we now have tempDlist and tempFlist containing all the data and fields within a certain
        #section of the pdf. they are passed to another function to try to pair appropriate values.
        #if no data was found in a certain section, all appropriate fields are marked NULL

        if (expectedMatch):
            if (len(tempDlist) == 0):
                listOfMatchedValues = markAppropriateFieldsNull(tempFlist, section)
                kvpsMaster.extend(listOfMatchedValues)
            else:
                listOfMatchedValues = pairFieldandData(tempDlist, tempFlist, section)
                kvpsMaster.extend(listOfMatchedValues)

    #TODO - do something with extra lines?

    #put all null fields on the bottom
    nullfields = [item for item in kvpsMaster if item[1] == "NULL"]
    kvpsMaster = [item for item in kvpsMaster if item[1] != "NULL"]
    kvpsMaster.extend(nullfields)

    pdfObj = {}
    for pair in kvpsMaster:
        pdfObj[pair[0]] = pair[1]

    if (verboseOpt):
        return pdfObj, sdlist, sflist
    else:
        return pdfObj






def pairFieldandData(dlistChunk, flistChunk, state):

    global currentOCA

    savedIndices = []
    checkmarkData = []
    for x in range(len(dlistChunk)):
        if (dlistChunk[x][2] == 'X'):
            savedIndices.append(x)
    savedIndices.reverse()
    for x in savedIndices:
        checkmarkData.append(dlistChunk.pop(x))
    checkmarkData.reverse()

    dlistNoChecks = dlistChunk #purely to save time refactoring; can be changed later
    flistNoChecks, kvps = pairCheckmarkData(checkmarkData, flistChunk, state)

    unmatchedData = []
    
    if (state == "AGENCY_INFO"):
        while (len(flistNoChecks) > 0):
            #print flistNoChecks[0][2] + ' @ ' + str(flistNoChecks[0][0]) + ', ' + str(flistNoChecks[0][1]) + ' compared to '
            for y in range(len(dlistNoChecks)):
                #print dlistNoChecks[y][2] + ' @ ' + str(dlistNoChecks[y][0]) + ', ' + str(dlistNoChecks[y][1])
                if ((abs(flistNoChecks[0][1] - dlistNoChecks[y][1]) < 10)
                and abs((flistNoChecks[0][0]+20) - dlistNoChecks[y][0]) < 10):
                    #print "Match Found"
                    if (flistNoChecks[0][2] == 'ORI'):
                        oriIndex = len(kvps)
                        flistNoChecks = removeFromFieldList(flistNoChecks, 'Date/Time Arrested')
                    elif (flistNoChecks[0][2] == 'OCA'):
                        ocaIndex = len(kvps)
                        currentOCA = dlistNoChecks[y][2]
                    kvps.append([flistNoChecks[0][2], dlistNoChecks[y][2]])
                    flistNoChecks.pop(0)
                    dlistNoChecks.pop(y)
                    break
                if (y == len(dlistNoChecks)-1):
                    #print "No Match Found"
                    kvps.append([flistNoChecks[0][2], 'NULL'])
                    flistNoChecks.pop(0)
            #print "--------------------------------------------"

        #fix a one-off technicality instance of weirdness in the forms we're dealing with
        #where three separate fields are represented together; here they are separated.
        #also move the OCA number, used to identify the form, to the top of kvps
        temp = kvps[oriIndex]
        kvps.append(['Date Arrested', temp[1][16:26]])
        kvps.append(['Time Arrested', temp[1][28:33]])
        kvps[oriIndex][1] = temp[1][:15]
        temp = kvps[0]
        kvps[0] = kvps[ocaIndex]
        kvps[ocaIndex] = temp
        ocaIndex = 0
       
    elif (state == "ARRESTEE_INFO"):
        

        #remove these first because the field is split into two lines and oddly formatted (it is handled on its own afterwards)
        flistNoChecks = removeFromFieldList(flistNoChecks, 'Country of')
        flistNoChecks = removeFromFieldList(flistNoChecks, 'Citizenship')
        kvps.append(["Country of Citizenship", "NULL"])

        #occupation is often a problem spot that doesn't get matched so we match it specifically before going general
        flistNoChecks = removeFromFieldList(flistNoChecks, 'Occupation')
        occ = 'NULL'
        for x in range(len(dlistNoChecks)):
            if (dlistNoChecks[x][0] < 180 or dlistNoChecks[x][0] > 210):
                continue
            elif (dlistNoChecks[x][1] < 500 or dlistNoChecks[x][1] > 720):
                continue
            else:
                occ = dlistNoChecks[x][2]
                dlistNoChecks.pop(x)
                break
        kvps.append(["Occupation", occ])

        while (len(flistNoChecks) > 0):
            matchFound = False
            for y in range(len(dlistNoChecks)):
                if (abs(flistNoChecks[0][1] - dlistNoChecks[y][1]) < 12
                and abs((flistNoChecks[0][0]+22) - dlistNoChecks[y][0]) < 10):
                    matchFound = True
                    kvps.append([flistNoChecks[0][2], dlistNoChecks[y][2]])
                    flistNoChecks.pop(0)
                    dlistNoChecks.pop(y)
                    break
            if (matchFound == False):
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
        

        for f in flistNoChecks:
            if (f[0] > 380):
                break
            else:
                for y in range(len(dlistNoChecks)):
                    if (abs(f[0]+20 - dlistNoChecks[y][0]) < 6):
                        if (abs(f[1] - dlistNoChecks[y][1]) < 10):
                            kvps.append([f[2], dlistNoChecks[y][2]])
                            dlistNoChecks.pop(y)
                            break
                    elif (y == len(dlistNoChecks)-1):
                        kvps.append([f[2], 'NULL'])

        flistNoChecks = removeMultipleFromFieldList(flistNoChecks, ['If Armed, Type of Weapon', 'Place of Arrest'])
        
        dlistNoChecks = qsort(dlistNoChecks, 1)
        flistNoChecks = qsort(flistNoChecks, 1)

        charge1, charge2, charge3 = "", "", ""
        for d in dlistNoChecks:
            if (d[1] < 300): #charges column
                if (d[0] < 420): #first row, charge #1
                    charge1 = charge1 + d[2] + " "
                elif (d[0] < 460 and d[0] > 420): #second row, charge #2
                    charge2 = charge2 + d[2] + " "
                elif (d[0] < 500 and d[0] > 460): #third row, charge #3
                    charge3 = charge3 + d[2] + " "
            elif (d[1] > 370 and d[1] < 450): #counts column
                if (d[0] < 420): 
                    kvps.append(["Chg1 Counts", d[2]])
                elif (d[0] < 460 and d[0] > 420): 
                    kvps.append(["Chg2 Counts", d[2]])
                elif (d[0] < 500 and d[0] > 460):
                    kvps.append(["Chg3 Counts", d[2]])
            elif (d[1] > 450 and d[1] < 530): #dci code column
                if (d[0] < 420): 
                    kvps.append(["Chg1 DCI Code", d[2]])
                elif (d[0] < 460 and d[0] > 420): 
                    kvps.append(["Chg2 DCI Code", d[2]])
                elif (d[0] < 500 and d[0] > 460):
                    kvps.append(["Chg3 DCI Code", d[2]])
            elif (d[1] > 530 and d[1] < 715): #offense jurisdiction
                if (d[0] < 420): 
                    kvps.append(["Chg1 Offense Jurisdiction", d[2]])
                elif (d[0] < 460 and d[0] > 420): 
                    kvps.append(["Chg2 Offense Jurisdiction", d[2]])
                elif (d[0] < 500 and d[0] > 460):
                    kvps.append(["Chg3 Offense Jurisdiction", d[2]])
            elif (d[1] > 715 and d[1] < 810): #statute #
                if (d[0] < 420): 
                    kvps.append(["Chg1 Statute Number", d[2]])
                elif (d[0] < 460 and d[0] > 420): 
                    kvps.append(["Chg2 Statute Number", d[2]])
                elif (d[0] < 500 and d[0] > 460):
                    kvps.append(["Chg3 Statute Number", d[2]])
            elif (d[1] > 810 and d[1] < 880): #warrant date
                if (d[0] < 420): 
                    kvps.append(["Chg1 Warrant Date", d[2]])
                elif (d[0] < 460 and d[0] > 420): 
                    kvps.append(["Chg2 Warrant Date", d[2]])
                elif (d[0] < 500 and d[0] > 460):
                    kvps.append(["Chg3 Warrant Date", d[2]])
            else:
                unmatchedData.append(d)

        if (len(charge1) > 0):
            charge1 = charge1[:-1]
            kvps.append(["Charge1", charge1])
        else: #no charges?
            kvps.append(["Charge1", "No Charges Found"])
        if (len(charge2) > 0):
            charge2 = charge2[:-1]
            kvps.append(["Charge2", charge2])
        else:
            kvps.append(["Charge2", "NULL"])
        if (len(charge3) > 0):
            charge3 = charge3[:-1]
            kvps.append(["Charge3", charge3])
        else:
            kvps.append(["Charge3", "NULL"])

        if (len(unmatchedData) > 0):
            print "\n*****************************************\nSOME DATA WENT UNMATCHED FROM CHARGES IN"
            print currentOCA + ".xml"
            print "*****************************************"
            for u in unmatchedData:
                print u
            print "*****************************************\n"
            

    elif (state == "VEH_INFO"):
            
        vinIndex = -1

        while (len(flistNoChecks) > 0):
            matchFound = False
            for y in range(len(dlistNoChecks)):
                if (abs(flistNoChecks[0][1] - dlistNoChecks[y][1]) < 12
                and abs((flistNoChecks[0][0]+22) - dlistNoChecks[y][0]) < 10):
                    matchFound = True
                    if (flistNoChecks[0][2] == 'Plate #/State' and len(dlistNoChecks[y][2]) > 20):
                        vinIndex = len(kvps)
                        flistNoChecks = removeFromFieldList(flistNoChecks, 'VIN')
                    kvps.append([flistNoChecks[0][2], dlistNoChecks[y][2]])
                    flistNoChecks.pop(0)
                    dlistNoChecks.pop(y)
                    break
            if (matchFound == False):
                kvps.append([flistNoChecks[0][2], 'NULL'])
                flistNoChecks.pop(0)

        for leftovers in dlistNoChecks:
            if ((leftovers[2].find('/') + leftovers[2].find(':')) > 0):
                kvps.append(["Vehicle Status Datetime", leftovers[2]])
                dlistNoChecks.remove(leftovers)

        if (vinIndex != -1):
            temp = kvps[vinIndex][1]
            kvps[vinIndex][1] = temp[:18]
            kvps.append(["VIN", temp[19:]])

        unmatchedData = dlistNoChecks

##        if (len(unmatchedData) > 0):
##            print "\n*****************************************\nSOME DATA WENT UNMATCHED FROM VEH INFO IN"
##            print currentOCA + ".xml"
##            print "*****************************************"
##            for u in unmatchedData:
##                print u
##            print "*****************************************\n"

        

##    elif (state == "BOND"):
##
##    elif (state == "DRUGS"):
##
    elif (state == "COMP"):
        defaults = ['NULL', 'NULL', 'NULL']
        
        if (len(dlistNoChecks) > 0): #very often there is no non-checkmark data in the COMP section
            for d in dlistNoChecks:
                if (d[1] < 400):
                    defaults[0] = d[2]
                elif (d[1] > 730):
                    defaults[2] = d[2]
                else:
                    defaults[1] = d[1]
        
        kvps.append(['Comp Name', defaults[0]])
        kvps.append(['Comp Address', defaults[1]])
        kvps.append(['Comp Phone', defaults[2]])
        
    elif (state == "NARRATIVE"):
        narr = ""
        for line in dlistNoChecks:
            narr = narr + line[2] + " "
        narr = narr[:-1]
        kvps.append(["Narrative", narr])
        
    elif (state == "STATUS"):
        if (dlistNoChecks[-1][0] > 1060):
            kvps.append(["Arrestee Signature", dlistNoChecks[-1][2]])
            dlistNoChecks.pop()
        else:
            kvps.append(["Arrestee Signature", "NULL"])
        flistNoChecks = removeFromFieldList(flistNoChecks, "Arrestee Signature")

        dataChecklist = [False, False, False, False]
        fieldVals = ["Arresting Officer Signature/ID #", "Date Submitted", "Time Submitted", "Supervisor Signature"]

        for d in dlistNoChecks:
            if (d[1] < 370): #Arresting Officer Sig
                dataChecklist[0] = True
                kvps.append([fieldVals[0], d[2]])
            elif (d[1] > 570): #Supervisor Sig
                dataChecklist[3] = True
                kvps.append([fieldVals[3], d[2]])
            else: #Date/Time Submitted
                dataChecklist[1] = True
                dataChecklist[2] = True
                kvps.append([fieldVals[1], d[2][:10]])
                kvps.append([fieldVals[2], d[2][12:]])
                
        for x in range(4):
            if (dataChecklist[x] == False):
                kvps.append([fieldVals[x], "NULL"])
                
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

def pairCheckmarkData(chkData, flistChunk, state):
    moe = 0 #margin of error; number of pixels by which something can be off its hardcoded position
    kvps = [] #key-value pairs
    dataTracker = [] #used to store the default and final values of checkmark kvps
    error = "***** A checkmark exists but could not be properly matched @ "
    
    global currentOCA
    
    if (state == "AGENCY_INFO"):
        moe = 6
        dataTracker = [False, False]
        for x in chkData:
            if (abs(x[1] - 79) < moe):
                if (abs(x[0] - 106) < moe):
                    dataTracker[0] = True
                elif (abs(x[0] - 118) < moe):
                    dataTracker[1] = True
                else: #something went wrong; there are checks but not in the right place
                    print error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA
            else: #same here... etc.
                print error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA

        kvps.append(["Prints Taken", dataTracker[0]])
        kvps.append(["Photos Taken", dataTracker[1]])
        flistChunk = removeMultipleFromFieldList(flistChunk, ['Prints', 'Photos', 'Taken'])
                  
    elif (state == "ARRESTEE_INFO"):
        moe = 6
        dataTracker = ['NULL', 'NULL']
        for x in chkData:
            if (abs(x[0] - 184) < moe):
                if (abs(x[1] - 735) < moe):
                    dataTracker[0] = 'Resident'
                elif (abs(x[1] - 815) < moe):
                    dataTracker[0] = 'Unknown'
                else:
                    print error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA
            elif (abs(x[0] - 196) < moe):
                if (abs(x[1] - 735) < moe):
                    dataTracker[0] = 'Non-Resident'
                else:
                    print error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA         
            elif (abs(x[0] - 262) < moe):
                if (abs(x[1] - 775) < moe):
                    dataTracker[1] = 'Yes'
                elif (abs(x[1] - 815) < moe):
                    dataTracker[1] = 'No'
                elif (abs(x[1] - 851) < moe):
                    dataTracker[1] = 'Unknown'
                else:
                    print error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA
            else:
                print error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA

        kvps.append(["Residency Status", dataTracker[0]])
        kvps.append(["Consumed Drug/Alcohol", dataTracker[1]])
        flistChunk = removeMultipleFromFieldList(flistChunk, ['Resident', 'Non-Resident', 'Unknown',
                                                              'Yes', 'No', 'Unk', 'Consumed Drug/Alcohol'])

    elif (state == "ARREST_INFO"):
        dataTracker = ['NULL', 'NULL', 'NULL', 'NULL']
        
        for x in chkData:
            if (x[0] < 380):
                moe = 6
                if (abs(x[0] - 355) < moe):
                    if (abs(x[1] - 278) < moe):
                        dataTracker[0] = 'On-View'
                    elif (abs(x[1] - 356) < moe):
                        dataTracker[0] = 'Criminal Summons'
                    else:
                        print error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA
                elif (abs(x[0] - 370) < moe):
                    if (abs(x[1] - 278) < moe):
                        dataTracker[0] = 'Order for Arrest'
                    elif (abs(x[1] - 375) < moe):
                        dataTracker[0] = 'Citation'
                    elif (abs(x[1] - 446) < moe):
                        dataTracker[0] = 'Warrant'
                    else:
                        print error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA
                else:
                    print error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA
            else:
                moe = 6
                if (abs(x[1] - 328) < moe):
                    moe = 4
                    if (abs(x[0] - 395) < moe):
                        dataTracker[1] = 'Felony'
                    elif (abs(x[0] - 406) < moe):
                        dataTracker[1] = 'Misdemeanor'
                    elif (abs(x[0] - 433) < moe):
                        dataTracker[2] = 'Felony'
                    elif (abs(x[0] - 447) < moe):
                        dataTracker[2] = 'Misdemeanor'
                    elif (abs(x[0] - 473) < moe):
                        dataTracker[3] = 'Felony'
                    elif (abs(x[0] - 486) < moe):
                        dataTracker[3] = 'Misdemeanor'
                    else:
                        print error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA
                else:
                    print error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA

        kvps.append(["Arrest Type", dataTracker[0]])
        kvps.append(["Charge 1 Type", dataTracker[1]])
        kvps.append(["Charge 2 Type", dataTracker[2]])
        kvps.append(["Charge 3 Type", dataTracker[3]])
        flistChunk = removeMultipleFromFieldList(flistChunk, ['On-View', 'Criminal Summons', 'Order for Arrest', 'Citation', 'Warrant',
                                                              'Fel', 'Misd', 'Fel', 'Misd', 'Fel', 'Misd'])
                            
    elif (state == "VEH_INFO"):
        moe = 6
        dataTracker = 'NULL'
        for x in chkData:
            if (x[0] < 550):
                if (abs(x[1] - 263) < moe):
                    dataTracker = "Left at Scene - Secured"
                elif (abs(x[1] - 342) < moe):
                    dataTracker = "Left at Scene - Unsecured"
            elif (x[0] > 565):
                dataTracker = "Impounded or Placed in Storage"
            else:
                dataTracker = "Released to Other at owner's request"

        if (len(chkData) > 0):
            kvps.append(["Vehicle Status", dataTracker])
        else:
            kvps.append(["Vehicle Status", "No Vehicle Involved"])
        flistChunk = removeMultipleFromFieldList(flistChunk, ['Vehicle', 'Left at Scene', 'Secured', 'Unsecure', 'Date/Time',
                                                              '1.', '2.', '3.', 'Released to other at owners request', 'Name of Other',
                                                              'Impounded', 'Place of storage', 'Inventory on File?'])
                            
##    elif (state == "BOND"):
##
##    elif (state == "DRUGS"):
##
    elif (state == "COMP"):
        dataTracker = 'NULL'
        #only one check possible out of only two possible boxes
        for x in chkData:
            moe = 10
            if (abs(x[0] - 895) < moe):
                moe = 6
                if (abs(x[1] - 172) < moe):
                    dataTracker = "Complainant"
                elif (abs(x[1] - 244) < moe):
                    dataTracker = "Victim"
                else:
                    print error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA
            else:
                print error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA
                
        kvps.append(["Comp", dataTracker])
        flistChunk = removeMultipleFromFieldList(flistChunk, ['Complainant', 'Victim'])

##    elif (state == "NARRATIVE"):
##      there are no check boxes in the narrative so this check is not needed
    elif (state == "STATUS"):
        moe = 7
        dataTracker = ["NULL", "NULL"]
        for x in chkData:
            if (abs(x[0] - 1087) < moe):
                if (abs(x[1] - 75) < moe):
                    dataTracker[0] = "Further Investigation"
                elif (abs(x[1] - 220) < moe):
                    dataTracker[1] = "Cleared By Arrest/No Supplement Needed"
                else:
                    print error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA
            elif (abs(x[0] - 1101) < moe):
                if (abs(x[1] - 75) < moe):
                    dataTracker[0] = "Inactive"
                elif (abs(x[1] - 144) < moe):
                    dataTracker[0] = "Closed"
                elif (abs(x[1] - 220) < moe):
                    dataTracker[1] = "Arrest/No Investigation"
                else:
                    print error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA
            else:
                print error + str(x[0]) + ", " + str(x[1]) + " *****  " + currentOCA

        kvps.append(["Case Status", dataTracker[0]])
        kvps.append(["Case Disposition", dataTracker[1]])
        flistChunk = removeMultipleFromFieldList(flistChunk, ['Case Status:', 'Further Inv.', 'Inactive', 'Closed',
                                                              'Case Disposition:', 'Cleared By Arrest / No Supplement Needed',
                                                              'Arrest / No Investigation'])

    #end of checkmark data if-else ladder of section state machine

    return flistChunk, kvps


#The next two functions are convenience functions I wrote so I wouldn't have
#to repetitively enter parameters when calling the functions in IDLE.
#Absolute file paths are more reliable.
#
#'filepath' is path to xml file
def getLineIndexFromFile(filepath):
    LOL, extras = getFileLinesList(filepath)
    dlist, flist = createLineIndex(LOL)
    return dlist, flist, extras

def getSinglePDFObj(dlist, flist, sectionNameList, extraLines, verbose):
    return processLists(dlist, flist, sectionNameList, extraLines, verbose)

#analagous usage but directoryPath is path to directory folder rather than file
def createPDFList(directoryPath):
    pdfObjects = []
    snl = ["AGENCY_INFO", "ARRESTEE_INFO", "VEH_INFO", "BOND", "DRUGS", "COMP", "NARRATIVE", "STATUS"]
    for filename in os.listdir(directoryPath):
        print "operating on file " + filename + "..."
        dlist, flist, extras = getLineIndexFromFile(directoryPath+filename)
        pdfObj = getSinglePDFObj(dlist, flist, snl, extras, False)
        pdfObjects.append(pdfObj)
    return pdfObjects

def createPDFDict(directoryPath):
    pdfObjectsDictionary = {}
    snl = ["AGENCY_INFO", "ARRESTEE_INFO", "VEH_INFO", "BOND", "DRUGS", "COMP", "NARRATIVE", "STATUS"]
    for filename in os.listdir(directoryPath):
        dlist, flist, extras = getLineIndexFromFile(directoryPath+filename)
        pdfObj = getSinglePDFObj(dlist, flist, snl, extras, False)
        pdfObjectsDictionary[pdfObj['OCA']] = pdfObj
        print "operating on file " + filename + "...  keys: " + str(len(pdfObj))
    return pdfObjectsDictionary


#snl = ["AGENCY_INFO", "ARRESTEE_INFO", "ARREST_INFO", "VEH_INFO", "BOND", "DRUGS", "COMP", "NARRATIVE", "STATUS"]
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
