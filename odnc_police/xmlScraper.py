import os #used to work on an entire directory of xml files
import datetime

currentOCA = ""
seeChargesTrue = False #some forms put the OCA number in the charges section for some reason
logfile = None

def getFileLinesList(filepath):
    """Simple function that takes a filepath to one of the converted .xml files and returns a list
    of strings that are the lines of the file. Some modest filtering is done to remove lines with no
    data, and anything beyond the first page is separated apart."""
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


def createLineIndex(listOfLines):
    """Takes a list of strings representing file lines as input and strips the important data from each line.
    The top and left coordinates from the xml tag are saved along with the actual text data between the tags.
    Data items are thus three-item lists, whose 0 index holds the top coordinate, 1 index holds the left
    coordinate, and 2 index holds the data. Data items are sorted into either a list of form data, or a list
    of form field names, and these two lists are returned."""
    lineDataItemList = [] #to store text data and top/left coords in better structure
    lineFieldItemList = []
    
    for line in listOfLines:
        if ('</page>' in line):
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


#helper function I wrote to easily extract data from a string.
#'line' is the string to extract from, 'firstDelimiter' is a string that
#identifies where to start looking, and 'secondDelimiter' is the char
#(or string) that signifies the end of the text that will be extracted.
#e.g. to extract '576' from 'top="33" left="576" blahblah':
#line = 'top="33" left="576" blahblah'
#firstDelim = 'left="'
#secondDelim = '"'
def getTextBetweenDelimiters(line, firstDelimiter, secondDelimiter):
    """A helper function which extracts the data from in between two specified strings.
    Useful for getting text out of markup-language tags."""
    beginIndex = line.find(firstDelimiter) + len(firstDelimiter)
    if beginIndex == -1: #basic check
        return -1
    restOfLine = line[beginIndex:]
    nextDelimiterIndex = restOfLine.find(secondDelimiter)
    if nextDelimiterIndex == -1:
        return line[beginIndex:] #shouldn't really happen
    endIndex = beginIndex + nextDelimiterIndex
    return line[beginIndex:endIndex]



def processLists(dlist, flist, sectionsToGrab, extraLines):
    """Takes as input the two data item lists from createLineIndex(), as well as a hard-coded list of strings
    that serve as the readable state of a state machine. The state machine keeps track of which section of the
    pdf is currently being scraped, because different strategies are necessary or efficient for each one.
    Eventually the two data item lists are digested into a master list of key-value pairs, returned as a dictionary."""
    kvpsMaster = []
    global currentOCA, seeChargesTrue
    
    sdlist = qsort(dlist, 0)
    sflist = qsort(flist, 0)

    seeChargesTrue = False

    for section in sectionsToGrab:

        expectedMatch = True
        #print "For section " + section + ", "
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
            #good idea to use len=0 as condition? investigate
            if (len(tempDlist) == 0):
                listOfMatchedValues = markAppropriateFieldsNull(section)
                kvpsMaster.extend(listOfMatchedValues)
            else:
                listOfMatchedValues = pairFieldandData(tempDlist, tempFlist, section)
                kvpsMaster.extend(listOfMatchedValues)

    #TODO - do something with extra lines?

##    #put all null fields on the bottom
##    nullfields = [item for item in kvpsMaster if item[1] == "NULL"]
##    kvpsMaster = [item for item in kvpsMaster if item[1] != "NULL"]
##    kvpsMaster.extend(nullfields)

    pdfObj = {} #create and populate the dictionary representing the pdf report
    for pair in kvpsMaster:
        pdfObj[pair[0]] = pair[1]

    if (seeChargesTrue == True): #fix the 'See Charges' in the OCA box on some forms
        pdfObj['OCA'] = currentOCA

    return pdfObj


def qsort(lineItemList, sortParameter):
    """A modified version of Quicksort using list comprehensions and tailored to the data item lists
    created by createLineIndex(). sortParameter is 1 to sort by left coordinate, and anything else
    to sort by top coordinate."""
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



def grabRelevantDataAndFields(dlist, flist, start, end):
    """Helper function that uses hardcoded start and end coordinates that are passed in as parameters
    to peel off chunks of the two data item lists, gradually moving down the pdf by section.
    This allows for easier rule-based matching schemes than dealing with the whole pdf at once."""
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

##    print "\nGrab Relevant Data and Fields returned the following in the temp lists: "
##    print "tempDlist:"
##    for item in tempDlist:
##        print item[2] + " @ " + str(item[0]) + ", " + str(item[1])
##    print "tempFlist:"
##    for item in tempFlist:
##        print item[2] + " @ " + str(item[0]) + ", " + str(item[1])
##    print "----------------------------------\n"

    return dlist, flist, tempDlist, tempFlist


def markAppropriateFieldsNull(section):
    """This function is only called when ALL fields in a certain section have no data. If so they are all marked as NULL here
    to avoid unnecessary comparisons in the pairFieldandData() function. If not ALL fields are empty, individual empty fields
    are marked as NULL as the rest of the data in the section is matched, in pairFieldandData()."""
    global logfile

    kvps = []

    if (section == "AGENCY_INFO"): #makes no sense and should never happen (no arresting agency info?)
        print >>logfile, "Something Nonsensical Happened - This form lacks critical data"
    elif (section == "ARRESTEE_INFO"): #also makes no sense (no information on who was arrested?)
        print >>logfile, "Something Nonsensical Happened - This form lacks critical data"
    elif (section == "ARREST_INFO"): #definitely makes no sense (no crime data?)
        print >>logfile, "Something Nonsensical Happened - This form lacks critical data"
        #--> the first three sections must have some data in every case
    elif (section == "VEH_INFO"):
        kvps.append(['VYR', 'NULL'])
        kvps.append(['Make', 'NULL'])
        kvps.append(['Model', 'NULL'])
        kvps.append(['Style', 'NULL'])
        kvps.append(['Color', 'NULL'])
        kvps.append(['Plate No./State', 'NULL'])
        kvps.append(['VIN', 'NULL'])
        kvps.append(['Vehicle Status', 'NULL'])
        kvps.append(['Vehicle Status Datetime', 'NULL'])
    elif (section == "BOND"):
        kvps.append(["Datetime Confined", 'NULL'])
        kvps.append(["Place Confined", 'NULL'])
        kvps.append(["Committing Magistrate", 'NULL'])
        kvps.append(["Bond Amount", 'NULL'])
        kvps.append(["Type Bond", 'NULL'])
        kvps.append(["Trial Date", 'NULL'])
        kvps.append(["Court of Trial", 'NULL'])
        kvps.append(["City of Court", 'NULL'])
        kvps.append(["Assisting Officer Name/ID", 'NULL'])
        kvps.append(["Released By (Name/Dept/ID)", 'NULL'])
        kvps.append(["Datetime Released", 'NULL']) 
    elif (section == "DRUGS"):
        txt = ["Drug1", "Drug2"]
        for t in txt:
            kvps.append([(t + " Suspected Type"), 'NULL'])
            kvps.append([(t + " DCI"), 'NULL'])
            kvps.append([(t + " Status"), 'NULL'])
            kvps.append([(t + " Quantity"), 'NULL'])
            kvps.append([(t + " Activities"), 'NULL'])
    elif (section == "COMP"):
        kvps.append(['Comp', 'NULL'])
        kvps.append(['Comp Name', 'NULL'])
        kvps.append(['Comp Address', 'NULL'])
        kvps.append(['Comp Phone', 'NULL'])
    elif (section == "NARRATIVE"):
        kvps.append(['Narrative', 'NULL'])
    elif (section == "STATUS"): #also definitely not possible (no arresting officer info?)
        print >>logfile, "Something Nonsensical Happened - This form lacks critical data"

    return kvps

#
# *===============================================================*
# ||$||||||||||||||||^^^^^^^^^^^^^^^^^^^^^^^||||||||||||||||||||$||
# |****************************************************************
# | * * * * * * * PAIR FIELD AND DATA SCROLL MARKER * * * * * * * *
# |**** Just a way to spot the function as I scroll quickly by ****
# |
# |
# | !
# |
# |_______________________________________________________________|
# *================================================================
#


def pairFieldandData(dlistChunk, flistChunk, state):
    """The major of the two main data matching functions of the scraper; takes as input one pair of chunks (representing a certain section of the pdf)
    from the overall dlist and flist and the state string identifying which section the chunks are from."""
    global currentOCA, seeChargesTrue, logfile

    #strip the checkmark data and pass it on to pairCheckmarkData
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

    #begin text data if-else ladder for section 'state machine'
    
    if (state == "AGENCY_INFO"):
        oriIndex = -1
        dateArrIndex = -1

        while (len(flistNoChecks) > 0): #uncomment the next few comments for debugging
            #print flistNoChecks[0][2] + ' @ ' + str(flistNoChecks[0][0]) + ', ' + str(flistNoChecks[0][1]) + ' compared to '
            matchFound = False
            for y in range(len(dlistNoChecks)):
                #print dlistNoChecks[y][2] + ' @ ' + str(dlistNoChecks[y][0]) + ', ' + str(dlistNoChecks[y][1])
                if ((abs(flistNoChecks[0][1] - dlistNoChecks[y][1]) < 30)
                and abs((flistNoChecks[0][0]+20) - dlistNoChecks[y][0]) < 10):
                    #print "Match Found"
                    matchFound = True
                    if (flistNoChecks[0][2] == 'ORI' and len(dlistNoChecks[y][2]) > 20):
                        oriIndex = len(kvps)
                        flistNoChecks = removeFromFieldList(flistNoChecks, 'Date/Time Arrested')
                    elif (flistNoChecks[0][2] == 'Date/Time Arrested'):
                        dateArrIndex = len(kvps)
                    elif (flistNoChecks[0][2] == 'OCA'):
                        ocaIndex = len(kvps)
                        currentOCA = dlistNoChecks[y][2]
                    kvps.append([flistNoChecks[0][2], dlistNoChecks[y][2]])
                    flistNoChecks.pop(0)
                    dlistNoChecks.pop(y)
                    break
            if (matchFound == False):
                #print "No Match Found"
                kvps.append([flistNoChecks[0][2], 'NULL'])
                flistNoChecks.pop(0)
                if (kvps[len(kvps)-1][0] == 'OCA'):
                    ocaIndex = len(kvps)-1
            if (kvps[len(kvps)-1][0] == 'Fingerprint Card Check Digit # (CKN)'):
                kvps[len(kvps)-1][0] = 'Fingerprint Card Number (CKN)' #to avoid # in key names
            if (kvps[len(kvps)-1][0] == 'Date/Time Arrested' and dateArrIndex == -1):
                dateArrIndex = len(kvps)-1
            #print "--------------------------------------------"

        #fix a one-off technicality instance of weirdness in some of the forms we're dealing with
        #where three separate fields are represented together; here they are separated. In any
        #case date and time arrested must be separated. Also move OCA to the top of kvps
        if (oriIndex != -1):
            temp = kvps[oriIndex]
            kvps.append(['Date Arrested', temp[1][16:26]])
            kvps.append(['Time Arrested', temp[1][28:33]])
            kvps[oriIndex][1] = temp[1][:15]
        elif (dateArrIndex != -1):
            temp = kvps[dateArrIndex]
            kvps.append(['Time Arrested', temp[1][12:17]])
            kvps[dateArrIndex] = ['Date Arrested', temp[1][:10]]
        else:
            kvps[dateArrIndex] = ['Date Arrested', 'NULL']
            kvps.append(['Time Arrested', 'NULL'])
            
        temp = kvps[0]
        kvps[0] = kvps[ocaIndex]
        kvps[ocaIndex] = temp
        ocaIndex = 0
        if (kvps[0][1] == 'See Charges'):
            seeChargesTrue = True
       
    elif (state == "ARRESTEE_INFO"):

        #separate out common problem spots before moving on to general matching.
        #fields are problem spots if the data is offset in a weird way from the field tag.
        #occupation, place of birth, country of citizenship, scars, nearest relative and employer info are examples.
        #find and create unique keys for nearest relative phone and address and
        #employer's phone and address, which are simply 'Phone' and 'Address' on the form.
        flistNoChecks.pop() #easier to remove nearest relative name, phone and address this way
        flistNoChecks.pop() #they are always the last three on the list
        flistNoChecks.pop() #as for the line below, easier to remove both phone and add arrestee phone field back in later
        flistNoChecks = removeMultipleFromFieldList(flistNoChecks, ['Place of Birth', 'Country of', 'Citizenship', 'Occupation', 'Employer\'s Name', 'Phone', 'Scars, Marks, Tattoos', 'Phone', 'Address'])
        
        dataTracker = []
        for x in range(10): #ten possible problem spot fields, plus extras if place of birth is more than just a state
            dataTracker.append(('NULL', -1)) #-1 will become index of match
            
        for x in range(len(dlistNoChecks)):
            newX = len(dlistNoChecks)-(x+1) #start from the back
            if (dlistNoChecks[newX][0] > 315): #nearest relative
                if (dlistNoChecks[newX][1] < 420): #name
                    dataTracker[0] = (dlistNoChecks[newX][2], newX)
                elif (dlistNoChecks[newX][1] > 720): #phone
                    dataTracker[2] = (dlistNoChecks[newX][2], newX)
                else: #address
                    dataTracker[1] = (dlistNoChecks[newX][2], newX)
            elif (dlistNoChecks[newX][0] > 242):
                if (dlistNoChecks[newX][1] < 390):
                    dataTracker[4] = (dlistNoChecks[newX][2], newX)
            elif (dlistNoChecks[newX][0] > 210): #employer
                if (dlistNoChecks[newX][1] < 420): #name
                    dataTracker[5] = (dlistNoChecks[newX][2], newX)
                elif (dlistNoChecks[newX][1] > 742): #phone
                    dataTracker[7] = (dlistNoChecks[newX][2], newX)
                else: #address
                    dataTracker[6] = (dlistNoChecks[newX][2], newX)
            elif (dlistNoChecks[newX][0] > 178):
                if (dlistNoChecks[newX][1] > 500 and dlistNoChecks[newX][1] < 720):
                    dataTracker[3] = (dlistNoChecks[newX][2], newX) #occupation
            else: #topmost row of section
                if (abs(dlistNoChecks[newX][1] - 765) < 6): #state of birth
                    dataTracker[9] = (dlistNoChecks[newX][2], newX)
                elif (dlistNoChecks[newX][1] > 788): #country of citizenship
                    dataTracker[8] = (dlistNoChecks[newX][2], newX)
                elif (dlistNoChecks[newX][1] > 649 and dlistNoChecks[newX][1] < 760):
                    dataTracker.append((dlistNoChecks[newX][2], newX))
                
            
        kvps.append(["Nearest Relative Name", dataTracker[0][0]])
        kvps.append(["Nearest Relative Address", dataTracker[1][0]])
        kvps.append(["Nearest Relative Phone", dataTracker[2][0]])
        kvps.append(["Occupation", dataTracker[3][0]])
        kvps.append(["Scars, Marks, Tattoos", dataTracker[4][0]])
        kvps.append(["Employer Name", dataTracker[5][0]])
        kvps.append(["Employer Address", dataTracker[6][0]])
        kvps.append(["Employer Phone", dataTracker[7][0]])
        kvps.append(["Country of Citizenship", dataTracker[8][0]])
        if (len(dataTracker) > 10):
            i = len(dataTracker)-1
            placeofbirth = ""
            while (i > 8):
                placeofbirth = placeofbirth + dataTracker[i][0] + " "
                i = i-1
            placeofbirth = placeofbirth[:-1]
            kvps.append(["Place of Birth", placeofbirth])
        else:
            kvps.append(["Place of Birth", dataTracker[9][0]])
            
        dataTracker = sorted(dataTracker, key=lambda item: item[1])
        dataTracker.reverse()

        for x in range(len(dataTracker)):
            if (dataTracker[x][1] != -1):
                dlistNoChecks.pop(dataTracker[x][1])

        #insert arrestee phone field back in for matching purposes
        for x in range(len(flistNoChecks)):
            if (flistNoChecks[x][0] > 210):
                flistNoChecks.insert(x, [179, 458, "Arrestee Phone"])
                break

        while (len(flistNoChecks) > 0):
            matchFound = False
            for y in range(len(dlistNoChecks)):
                if (abs(flistNoChecks[0][1] - dlistNoChecks[y][1]) < 26
                and abs((flistNoChecks[0][0]+22) - dlistNoChecks[y][0]) < 10):
                    matchFound = True
                    kvps.append([flistNoChecks[0][2], dlistNoChecks[y][2]])
                    flistNoChecks.pop(0)
                    dlistNoChecks.pop(y)
                    break
            if (matchFound == False):
                kvps.append([flistNoChecks[0][2], 'NULL'])
                flistNoChecks.pop(0)
            if (kvps[len(kvps)-1][0] == 'Social Security #'):
                kvps[len(kvps)-1][0] = 'Social Security' #to avoid # in key names
            elif (kvps[len(kvps)-1][0] == 'Misc. # and Type'):
                kvps[len(kvps)-1][0] = 'Misc. Number and Type' #to avoid # in key names
                
                    
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

        charge1, charge2, charge3 = '', '', ''
        x = 0
        while (x < len(flistNoChecks)):
            dataTracker = ['NULL', 'NULL', 'NULL']
            if (flistNoChecks[x][1] < 100): #charges column
                
                for d in dlistNoChecks:
                    if (d[1] < 300):
                        if (d[0] < 420):
                            charge1 = charge1 + d[2] + " "
                        elif (d[0] > 460):
                            charge3 = charge3 + d[2] + " "
                        else:
                            charge2 = charge2 + d[2] + " "
                    else:
                        break
                if (len(charge1) > 0):
                    if (seeChargesTrue == True and charge1.find('OCA') != -1):
                        ocaIndex = charge1.find('OCA')
                        currentOCA = charge1[(ocaIndex+5):]
                        charge1 = charge1[:ocaIndex]
                    charge1 = charge1[:-1] #remove trailing space
                    dataTracker[0] = charge1
                if (len(charge2) > 0):
                    if (seeChargesTrue == True and charge2.find('OCA') != -1):
                        ocaIndex = charge2.find('OCA')
                        charge2 = charge2[:ocaIndex]
                    charge2 = charge2[:-1]
                    dataTracker[1] = charge2
                if (len(charge3) > 0):
                    if (seeChargesTrue == True and charge3.find('OCA') != -1):
                        ocaIndex = charge3.find('OCA')
                        charge3 = charge3[:ocaIndex]
                    charge3 = charge3[:-1]
                    dataTracker[2] = charge3
                kvps.append(["Charge1", dataTracker[0]])
                kvps.append(["Charge2", dataTracker[1]])
                kvps.append(["Charge3", dataTracker[2]])
            elif (flistNoChecks[x][1] > 370 and flistNoChecks[x][1] < 450): #counts column
                for d in dlistNoChecks:
                    if (d[1] < 450):
                        if (d[1] > 370):
                            if (d[0] < 420):
                                dataTracker[0] = d[2]
                            elif (d[0] > 460):
                                dataTracker[2] = d[2]
                            else:
                                dataTracker[1] = d[2]
                    else:
                        break
                kvps.append(["Charge1 Counts", dataTracker[0]])
                kvps.append(["Charge2 Counts", dataTracker[1]])
                kvps.append(["Charge3 Counts", dataTracker[2]])
            elif (flistNoChecks[x][1] > 450 and flistNoChecks[x][1] < 530): #dci code column
                for d in dlistNoChecks:
                    if (d[1] < 530):
                        if (d[1] > 450):
                            if (d[0] < 420):
                                dataTracker[0] = d[2]
                            elif (d[0] > 460):
                                dataTracker[2] = d[2]
                            else:
                                dataTracker[1] = d[2]
                    else:
                        break
                kvps.append(["Charge1 DCI Code", dataTracker[0]])
                kvps.append(["Charge2 DCI Code", dataTracker[1]])
                kvps.append(["Charge3 DCI Code", dataTracker[2]])
            elif (flistNoChecks[x][1] > 530 and flistNoChecks[x][1] < 715): #offense jurisdiction
                for d in dlistNoChecks:
                    if (d[1] < 715):
                        if (d[1] > 530):
                            if (d[0] < 420):
                                dataTracker[0] = d[2]
                            elif (d[0] > 460):
                                dataTracker[2] = d[2]
                            else:
                                dataTracker[1] = d[2]
                    else:
                        break
                kvps.append(["Charge1 Offense Jurisdiction", dataTracker[0]])
                kvps.append(["Charge2 Offense Jurisdiction", dataTracker[1]])
                kvps.append(["Charge3 Offense Jurisdiction", dataTracker[2]])
            elif (flistNoChecks[x][1] > 715 and flistNoChecks[x][1] < 810): #statute #
                for d in dlistNoChecks:
                    if (d[1] < 810):
                        if (d[1] > 715):
                            if (d[0] < 420):
                                dataTracker[0] = d[2]
                            elif (d[0] > 460):
                                dataTracker[2] = d[2]
                            else:
                                dataTracker[1] = d[2]
                    else:
                        break
                kvps.append(["Charge1 Statute Number", dataTracker[0]])
                kvps.append(["Charge2 Statute Number", dataTracker[1]])
                kvps.append(["Charge3 Statute Number", dataTracker[2]])
            elif (flistNoChecks[x][1] > 810 and flistNoChecks[x][1] < 880): #warrant date
                for d in dlistNoChecks:
                    if (d[1] < 880):
                        if (d[1] > 810):
                            if (d[0] < 420):
                                dataTracker[0] = d[2]
                            elif (d[0] > 460):
                                dataTracker[2] = d[2]
                            else:
                                dataTracker[1] = d[2]
                    else:
                        break
                kvps.append(["Charge1 Warrant Date", dataTracker[0]])
                kvps.append(["Charge2 Warrant Date", dataTracker[1]])
                kvps.append(["Charge3 Warrant Date", dataTracker[2]])
            else:
                print >>logfile, "*****The field " + f[2] + " in the charges section of " + currentOCA + " remains*****"
            x=x+3

        flistNoChecks = removeMultipleFromFieldList(flistNoChecks, ['Charge #1', 'Charge #2', 'Charge #3', 'Counts', 'Counts', 'Counts',
                                                                    'DCI Code', 'DCI Code', 'DCI Code', 'Offense Jurisdiction (if not arresting agency)',
                                                                    'Offense Jurisdiction (if not arresting agency)', 'Offense Jurisdiction (if not arresting agency)',
                                                                    'Statute #', 'Statute #', 'Statute #', 'Warr. Date', 'Warr. Date', 'Warr. Date'])

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
            if (kvps[len(kvps)-1][0] == 'Plate #/State'):
                kvps[len(kvps)-1][0] = 'Plate No./State' #to avoid # in key names

        for leftovers in dlistNoChecks:
            if ((leftovers[2].find('/') + leftovers[2].find(':')) > 0):
                kvps.append(["Vehicle Status Datetime", leftovers[2]])
                dlistNoChecks.remove(leftovers)

        if (vinIndex != -1):
            temp = kvps[vinIndex][1]
            kvps[vinIndex][1] = temp[:18]
            kvps.append(["VIN", temp[19:]])

        unmatchedData = dlistNoChecks
        #a helpful debugging script
        if (len(unmatchedData) > 0):
            print >>logfile, "\n*****************************************\nSOME DATA WENT UNMATCHED FROM VEH INFO IN"
            print >>logfile, currentOCA + ".xml"
            print >>logfile, "*****************************************"
            for u in unmatchedData:
                print >>logfile, u
            print >>logfile, "*****************************************\n"

        

    elif (state == "BOND"):
        dataTracker = []
        assistedBy, releasedBy = '', ''
        for x in range(10):
            dataTracker.append('NULL')
        for d in dlistNoChecks:
            if (d[0] < 615):
                if (d[1] < 270):
                    dataTracker[0] = d[2]
                elif (d[1] > 620):
                    dataTracker[2] = d[2]
                else:
                    dataTracker[1] = d[2]
            elif (d[0] > 666):
                if (d[1] < 410):
                    assistedBy = assistedBy + d[2] + ' / '
                elif (d[1] > 700):
                    dataTracker[9] = d[2]
                else:
                    releasedBy = releasedBy + d[2] + ' / '
            else:
                if (d[1] < 400):
                    dataTracker[3] = d[2]
                elif (d[1] > 400 and d[1] < 555):
                    dataTracker[4] = d[2]
                elif (d[1] > 555 and d[1] < 700):
                    dataTracker[5] = d[2]
                else:
                    dataTracker[6] = d[2]
        if (len(assistedBy) > 0):
            assistedBy = assistedBy[:-3] #remove trailing separator
            dataTracker[7] = assistedBy
        if (len(releasedBy) > 0):
            releasedBy = releasedBy[:-3]
            dataTracker[8] = releasedBy
        kvps.append(["Datetime Confined", dataTracker[0]])
        kvps.append(["Place Confined", dataTracker[1]])
        kvps.append(["Committing Magistrate", dataTracker[2]])
        kvps.append(["Bond Amount", dataTracker[3]])
        kvps.append(["Trial Date", dataTracker[4]])
        kvps.append(["Court of Trial", dataTracker[5]])
        kvps.append(["City of Court", dataTracker[6]])
        kvps.append(["Assisting Officer Name/ID", dataTracker[7]])
        kvps.append(["Released By (Name/Dept/ID)", dataTracker[8]])
        kvps.append(["Datetime Released", dataTracker[9]])                  

        
    elif (state == "DRUGS"):
        statuses = {'L': 'Lost', 'S':  'Stolen', 'R': 'Recovered', 'D': 'Damaged', 'Z': 'Seized',
                    'B': 'Burned', 'C': 'Counterfeit / Forged', 'F': 'Found', 'EVID': 'Evidence'}
        count = 0
        yIncrement = 0

        dlistNoChecks.reverse()

        while (len(dlistNoChecks) > 0 and count < 2):
            count = count + 1
            drugDataChunk = []
            lastIndex = len(dlistNoChecks) - 1
            while (dlistNoChecks[lastIndex][0] < (750 + yIncrement)):
                drugDataChunk.append(dlistNoChecks.pop())
                lastIndex = lastIndex - 1
                if (lastIndex == -1):
                    break
            yIncrement = yIncrement + 17
            dataTracker = ['NULL', 'NULL', 'NULL', 'NULL', 'NULL']
            drugDataChunk = qsort(drugDataChunk, 1)
            for d in drugDataChunk:
                if (d[1] < 100):
                    dataTracker[1] = d[2]
                elif (d[1] < 140):
                    if (d[2] in statuses):
                        dataTracker[2] = statuses[d[2]]
                    else: 
                        dataTracker[2] = d[2]
                elif (d[1] < 225):
                    dataTracker[3] = d[2]
                elif (d[1] < 300):
                    dataTracker[3] = dataTracker[3] + ' ' + d[2]
                elif (d[1] < 600):
                    dataTracker[0] = d[2]
                else:
                    if (d[1] < 651):
                        dataTracker[4] = 'Possession'
                    elif (d[1] < 690):
                        if (dataTracker[4] == 'NULL'):
                            dataTracker[4] = 'Buying'
                        else:
                            dataTracker[4] = dataTracker[4] + ", Buying"
                    elif (d[1] < 721):
                        if (dataTracker[4] == 'NULL'):
                            dataTracker[4] = 'Selling'
                        else:
                            dataTracker[4] = dataTracker[4] + ", Selling"
                    elif (d[1] < 762):
                        if (dataTracker[4] == 'NULL'):
                            dataTracker[4] = 'Manufacturing'
                        else:
                            dataTracker[4] = dataTracker[4] + ", Manufacturing"
                    elif (d[1] < 812):
                        if (dataTracker[4] == 'NULL'):
                            dataTracker[4] = 'Importing'
                        else:
                            dataTracker[4] = dataTracker[4] + ", Importing"
                    else:
                        if (dataTracker[4] == 'NULL'):
                            dataTracker[4] = 'Operating'
                        else:
                            dataTracker[4] = dataTracker[4] + ", Operating"
            kvps.append([("Drug"+str(count)+" Suspected Type"), dataTracker[0]])
            kvps.append([("Drug"+str(count)+" DCI"), dataTracker[1]])
            kvps.append([("Drug"+str(count)+" Status"), dataTracker[2]])
            kvps.append([("Drug"+str(count)+" Quantity"), dataTracker[3]])
            kvps.append([("Drug"+str(count)+" Activities"), dataTracker[4]])

        if (count == 1):
            count = 2
            dataTracker = ['NULL', 'NULL', 'NULL', 'NULL', 'NULL']
            kvps.append([("Drug"+str(count)+" Suspected Type"), dataTracker[0]])
            kvps.append([("Drug"+str(count)+" DCI"), dataTracker[1]])
            kvps.append([("Drug"+str(count)+" Status"), dataTracker[2]])
            kvps.append([("Drug"+str(count)+" Quantity"), dataTracker[3]])
            kvps.append([("Drug"+str(count)+" Activities"), dataTracker[4]])
            

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
        fieldVals = ["Arresting Officer Signature/ID", "Date Submitted", "Time Submitted", "Supervisor Signature"]

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

    #end of text data if-else ladder of section state machine
                
    return kvps

#
# *===============================================================*
# ||$||||||||||||||||^^^^^^^^^^^^^^^^^^^^^^^||||||||||||||||||||$||
# |****************************************************************
# | * * * * * * * PAIR CHECKMARK DATA SCROLL MARKER * * * * * * * *
# |**** Just a way to spot the function as I scroll quickly by ****
# |
# |
# |
# |
# | !
# |
# |
# |
# |_______________________________________________________________|
# *================================================================
#

def pairCheckmarkData(chkData, flistChunk, state):
    """The minor of the two main data matching function of the scraper, built to handle only the checkboxes from a particular section."""
    moe = 0 #margin of error; number of pixels by which something can be off its hardcoded position
    kvps = [] #key-value pairs
    dataTracker = [] #used to store the default and final values of checkmark kvps
    error = "***** A checkmark exists but could not be properly matched @ "
    
    global currentOCA, logfile
    
    if (state == "AGENCY_INFO"):
        moe = 6
        dataTracker = ['No', 'No']
        for x in chkData:
            if (abs(x[1] - 79) < moe):
                if (abs(x[0] - 106) < moe):
                    dataTracker[0] = 'Yes'
                elif (abs(x[0] - 118) < moe):
                    dataTracker[1] = 'Yes'
                else: #something went wrong; there are checks but not in the right place
                    print >>logfile, error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA
            else: #same here... etc.
                print >>logfile, error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA

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
                    print >>logfile, error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA
            elif (abs(x[0] - 196) < moe):
                if (abs(x[1] - 735) < moe):
                    dataTracker[0] = 'Non-Resident'
                else:
                    print >>logfile, error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA         
            elif (abs(x[0] - 262) < moe):
                if (abs(x[1] - 775) < moe):
                    dataTracker[1] = 'Yes'
                elif (abs(x[1] - 815) < moe):
                    dataTracker[1] = 'No'
                elif (abs(x[1] - 851) < moe):
                    dataTracker[1] = 'Unknown'
                else:
                    print >>logfile, error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA
            else:
                print >>logfile, error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA

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
                        print >>logfile, error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA
                elif (abs(x[0] - 370) < moe):
                    if (abs(x[1] - 278) < moe):
                        dataTracker[0] = 'Order for Arrest'
                    elif (abs(x[1] - 375) < moe):
                        dataTracker[0] = 'Citation'
                    elif (abs(x[1] - 444) < moe):
                        dataTracker[0] = 'Warrant'
                    else:
                        print >>logfile, error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA
                else:
                    print >>logfile, error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA
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
                        print >>logfile, error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA
                else:
                    print >>logfile, error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA

        kvps.append(["Arrest Type", dataTracker[0]])
        kvps.append(["Charge1 Type", dataTracker[1]])
        kvps.append(["Charge2 Type", dataTracker[2]])
        kvps.append(["Charge3 Type", dataTracker[3]])
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
                            
    elif (state == "BOND"):
        moe = 6
        dataTracker = 'Not Indicated'
        for x in chkData:
            if (abs(x[0] - 627) < moe):
                if (abs(x[1] - 86) < moe):
                    dataTracker = "Written Promise"
                elif (abs(x[1] - 177) < moe):
                    dataTracker = "Unsecured"
                else:
                    print >>logfile, error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA
            elif (abs(x[0] - 642) < moe):
                if (abs(x[1] - 86) < moe):
                    dataTracker = "Secured"
                elif (abs(x[1] - 146) < moe):
                    dataTracker = "No Bond"
                elif (abs(x[1] - 212) < moe):
                    dataTracker = "Other"
                else:
                    print >>logfile, error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA
            else:
                print >>logfile, error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA

        kvps.append(["Type Bond", dataTracker])
        flistChunk = removeMultipleFromFieldList(flistChunk, ['Type Bond', 'Written Promise', 'Unsecured', 'Secured', 'No Bond', 'Other'])

##    elif (state == "DRUGS"):
##        There are not checkboxes in the drugs section so this check is not needed
        
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
                    print >>logfile, error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA
            else:
                print >>logfile, error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA
                
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
                    print >>logfile, error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA
            elif (abs(x[0] - 1101) < moe):
                if (abs(x[1] - 75) < moe):
                    dataTracker[0] = "Inactive"
                elif (abs(x[1] - 144) < moe):
                    dataTracker[0] = "Closed"
                elif (abs(x[1] - 220) < moe):
                    dataTracker[1] = "Arrest/No Investigation"
                else:
                    print >>logfile, error + str(x[0]) + ", " + str(x[1]) + " *****" + currentOCA
            else:
                print >>logfile, error + str(x[0]) + ", " + str(x[1]) + " *****  " + currentOCA

        kvps.append(["Case Status", dataTracker[0]])
        kvps.append(["Case Disposition", dataTracker[1]])
        flistChunk = removeMultipleFromFieldList(flistChunk, ['Case Status:', 'Further Inv.', 'Inactive', 'Closed',
                                                              'Case Disposition:', 'Cleared By Arrest / No Supplement Needed',
                                                              'Arrest / No Investigation'])

    #end of checkmark data if-else ladder of section state machine

    return flistChunk, kvps


def removeFromFieldList(flist, field):
    """Helper function that removes a certain field name from the list of field items."""
    for x in range(len(flist)):
        if (flist[x][2] == field):
            flist.pop(x)
            break
    return flist

def removeMultipleFromFieldList(flist, fieldsToRemove):
    """Helper function that removes multiple fields from the list of field items."""
    for field in fieldsToRemove:
        flist = removeFromFieldList(flist, field)
    return flist

    
#The next two functions are convenience functions I wrote so I wouldn't have
#to repetitively enter parameters when calling the functions in IDLE.
#Absolute file paths are more reliable.
#
#'filepath' is path to xml file
##def getLineIndexFromFile(filepath):
##    LOL, extras = getFileLinesList(filepath)
##    dlist, flist = createLineIndex(LOL)
##    return dlist, flist, extras
##
##def getSinglePDFObj(dlist, flist, sectionNameList, extraLines, verbose):
##    return processLists(dlist, flist, sectionNameList, extraLines, verbose)

def getSinglePDFObj(filepath):
    """Takes as input the filepath to a converted .xml file and returns the python dictionary with the the key-value pairs from that report."""
    listOfLines, extras = getFileLinesList(filepath)
    if (len(listOfLines) > 10):
        dlist, flist = createLineIndex(listOfLines)
        snl = ["AGENCY_INFO", "ARRESTEE_INFO", "ARREST_INFO", "VEH_INFO", "BOND", "DRUGS", "COMP", "NARRATIVE", "STATUS"]
        pdfObj = processLists(dlist, flist, snl, extras)
        pdfObj['Path To PDF'] = filepath
        return pdfObj
    else:
        return "NULL" #something went wrong with ghostscript and/or conversion of pdf to xml file
    

#analagous usage but directoryPath is path to directory folder rather than file
def createPDFList(directoryPath, logFileObj):
    """Takes as input a directory containing multiple converted .xml files and returns a list of python dictionaries, each of which represents
    one of the converted-.xml reports from the directory."""
    global logfile
    pdfObjects = []
    logfile = logFileObj
    for filename in os.listdir(directoryPath):
        print >>logFileObj, "operating on file " + filename + "..."
        pdfObj = getSinglePDFObj(directoryPath+filename)
        if (pdfObj != "NULL"):
            pdfObjects.append(pdfObj)
        else:
            print >>logfile, "--->Error with ghostscript or the pdf2xml conversion of this file"
    return pdfObjects

def createPDFDict(directoryPath):
    """Takes as input a directory containing multiple converted .xml files and returns a dictionary of python dictionaries. The keys to the larger,
    all-encompassing dictionary are the OCA numbers from the reports whose dictionary representation is the value for that key."""
    pdfObjectsDictionary = {}
    for filename in os.listdir(directoryPath):
        print "operating on file " + filename + "..."
        pdfObj = getSinglePDFObj(directoryPath+filename)
        if (pdfObj != "NULL"):
            pdfObjectsDictionary[pdfObj['OCA']] = pdfObj
            print "keys: " + str(len(pdfObj.keys()))
        else:
            print "--->Error with ghostscript or the pdf2xml conversion of this file"
    return pdfObjectsDictionary




#snl = ["AGENCY_INFO", "ARRESTEE_INFO", "ARREST_INFO", "VEH_INFO", "BOND", "DRUGS", "COMP", "NARRATIVE", "STATUS"]


def printPDFDict(pdfDict):
    """Prints a dictionary object representing one arrest report pdf in a readable form."""
    keyList = sorted(pdfDict.keys(), key=lambda item: sortByKey(item))
    for x in keyList:
        print x + " -- " + str(pdfDict[x])
    print "\n=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*\n"

def sortByKey(key):
    """This function is used to custom sort the dictionaries that are constructed by the scraper for convenience in printing.
    It is used by the lambda function in printPDFDict, which is the function to call to actually view the sorted output."""
    if (key == 'OCA'):
        return 1
    elif (key == 'Agency Name'):
        return 2
    elif (key == 'ORI'):
        return 3
    elif (key == 'Date Arrested'):
        return 4
    elif (key == 'Time Arrested'):
        return 5
    elif (key == 'Prints Taken'):
        return 6
    elif (key == 'Photos Taken'):
        return 7
    elif (key == 'Fingerprint Card Number (CKN)'):
        return 8
    elif (key == 'Arrest Tract'):
        return 9
    elif (key == 'Residence Tract'):
        return 10
    elif (key == 'Arrest Number'):
        return 11
    elif (key == 'Name (Last, First, Middle)'):
        return 12
    elif (key == 'D.O.B.'):
        return 13
    elif (key == 'Age'):
        return 14
    elif (key == 'Race'):
        return 15
    elif (key == 'Sex'):
        return 16
    elif (key == 'Place of Birth'):
        return 17
    elif (key == 'Country of Citizenship'):
        return 18
    elif (key == 'Current Address'):
        return 19
    elif (key == 'Arrestee Phone'):
        return 20
    elif (key == 'Occupation'):
        return 21
    elif (key == 'Residency Status'):
        return 22
    elif (key == "Employer Name"):
        return 23
    elif (key == "Employer Address"):
        return 24
    elif (key == "Employer Phone"):
        return 25
    elif (key == 'Also Known As (Alias Names)'):
        return 26
    elif (key == 'Hgt'):
        return 27
    elif (key == 'Wgt'):
        return 28
    elif (key == 'Hair'):
        return 29
    elif (key == 'Eyes'):
        return 30
    elif (key == 'Skin Tone'):
        return 31
    elif (key == 'Consumed Drug/Alcohol'):
        return 32
    elif (key == 'Scars, Marks, Tattoos'):
        return 33
    elif (key == 'Social Security'):
        return 34
    elif (key == 'OLN and State'):
        return 35
    elif (key == 'Misc. Number and Type'):
        return 36
    elif (key == 'Nearest Relative Name'):
        return 37
    elif (key == 'Nearest Relative Address'):
        return 38
    elif (key == 'Nearest Relative Phone'):
        return 39
    elif (key == 'If Armed, Type of Weapon'):
        return 40
    elif (key == 'Arrest Type'):
        return 41
    elif (key == 'Place of Arrest'):
        return 42
    elif (key == 'Charge1'):
        return 43
    elif (key == 'Charge1 Type'):
        return 44
    elif (key == 'Charge1 Counts'):
        return 45
    elif (key == 'Charge1 DCI Code'):
        return 46
    elif (key == 'Charge1 Offense Jurisdiction'):
        return 47
    elif (key == 'Charge1 Statute Number'):
        return 48
    elif (key == 'Charge1 Warrant Date'):
        return 49
    elif (key == 'Charge2'):
        return 50
    elif (key == 'Charge2 Type'):
        return 51
    elif (key == 'Charge2 Counts'):
        return 52
    elif (key == 'Charge2 DCI Code'):
        return 53
    elif (key == 'Charge2 Offense Jurisdiction'):
        return 54
    elif (key == 'Charge2 Statute Number'):
        return 55
    elif (key == 'Charge2 Warrant Date'):
        return 56
    elif (key == 'Charge3'):
        return 57
    elif (key == 'Charge3 Type'):
        return 58
    elif (key == 'Charge3 Counts'):
        return 59
    elif (key == 'Charge3 DCI Code'):
        return 60
    elif (key == 'Charge3 Offense Jurisdiction'):
        return 61
    elif (key == 'Charge3 Statute Number'):
        return 62
    elif (key == 'Charge3 Warrant Date'):
        return 63
    elif (key == 'VYR'):
        return 64
    elif (key == 'Make'):
        return 65
    elif (key == 'Model'):
        return 66
    elif (key == 'Style'):
        return 67
    elif (key == 'Color'):
        return 68
    elif (key == 'Plate No./State'):
        return 69
    elif (key == 'VIN'):
        return 70
    elif (key == 'Vehicle Status'):
        return 71
    elif (key == 'Vehicle Status Datetime'):
        return 72
    elif (key == 'Datetime Confined'):
        return 73
    elif (key == 'Place Confined'):
        return 74
    elif (key == 'Committing Magistrate'):
        return 75
    elif (key == 'Type Bond'):
        return 76
    elif (key == 'Bond Amount'):
        return 77
    elif (key == 'Trial Date'):
        return 78
    elif (key == 'Court of Trial'):
        return 79
    elif (key == 'City of Court'):
        return 80
    elif (key == 'Assisting Officer Name/ID'):
        return 81
    elif (key == 'Released By (Name/Dept/ID)'):
        return 82
    elif (key == 'Datetime Released'):
        return 83
    elif (key == 'Drug1 Suspected Type'):
        return 84
    elif (key == 'Drug1 DCI'):
        return 85
    elif (key == 'Drug1 Status'):
        return 86
    elif (key == 'Drug1 Quantity'):
        return 87
    elif (key == 'Drug1 Activities'):
        return 88
    elif (key == 'Drug2 Suspected Type'):
        return 89
    elif (key == 'Drug2 DCI'):
        return 90
    elif (key == 'Drug2 Status'):
        return 91
    elif (key == 'Drug2 Quantity'):
        return 92
    elif (key == 'Drug2 Activities'):
        return 93
    elif (key == 'Comp'):
        return 94
    elif (key == 'Comp Name'):
        return 95
    elif (key == 'Comp Address'):
        return 96
    elif (key == 'Comp Phone'):
        return 97
    elif (key == 'Narrative'):
        return 98
    elif (key == 'Arresting Officer Signature/ID'):
        return 99
    elif (key == 'Date Submitted'):
        return 100
    elif (key == 'Time Submitted'):
        return 101
    elif (key == 'Supervisor Signature'):
        return 102
    elif (key == 'Case Status'):
        return 103
    elif (key == 'Case Disposition'):
        return 104
    elif (key == 'Arrestee Signature'):
        return 105
    elif (key == 'Path To PDF'):
        return 106
    else:
        return 107
