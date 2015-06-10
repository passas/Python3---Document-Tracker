__author__ = 'Paparisteidis Georgios'


import json
from countries_continents_mapping import cntry_to_cont,continents
from matplotlib import pyplot as plt
from collections import Counter


#Json File open and load
file = open('issuu_cw2_fixed.json')
jfile = json.load(file)

'''

mGui = Tk()
mGui.geometry('800x600')
mGui.title('Data Analysis of a Document Tracker by Paparisteidis Georgios')
mlabel = Label(text='My label').pack()



mGui.mainloop()

#InsertIdTextField = Entry(mGui,textvariable=insertText).place(x=15,y=265)
#viewTopTenDocsTextField = Entry(mGui,textvariable=insertText).place(x=300,y=265)

docID = '140218233015-c848da298ed6d38b98e18a85731a83f4'
docID = '140206010823-b14c9d966be950314215c17923a04af7'

task_selection = '4'
readerID = ''
'''

#2. Views by country/continent
def ViewByCountry(docID,user_selection):
    docCountryList=[]
    for x in jfile:
        if x.get('subject_doc_id') == docID:
            docCountryList.append(x['visitor_country'])
    if user_selection == '2a':
        #Run histogram and return countries list
        x = []
        y = []
        #Insert countries and number of occurences in two seperate lists
        for k,v in Counter(docCountryList).items():
            x.append(k)
            y.append(v)
        plt.title('Countries of Viewers')
        plt.bar(range(len(y)), y, align='center')
        plt.xticks(range(len(y)), x, size='small')
        plt.show()
        return docCountryList

    #Map countries to continents
    elif user_selection == '2b':
        continentsList = []
        #Itterate through countries
        for c in docCountryList:
            for country, continent in cntry_to_cont.items():
                if c == country:
                    for contnt,cntntName in continents.items():
                        if contnt == continent:
                            continentsList.append(cntntName)
        #Run histogram and return continents list
        x = []
        y = []
        #Insert countries and number of occurences in two seperate lists
        for k,v in Counter(continentsList).items():
            x.append(k)
            y.append(v)
        plt.title('Continents of Viewers')
        plt.bar(range(len(y)), y, align='center')
        plt.xticks(range(len(y)), x, size='small')
        plt.show()
        return (Counter(continentsList))



#3.Browsers by distinct name
def ViewsByBrowser(task_selection):
    #3a.Return browser Identifiers
    if task_selection == '3a':
        userAgentList = []
        for x in jfile:
            userAgentList.append(x['visitor_useragent'])
        #Run histogram and return browsersList
        x = []
        y = []
        #Insert countries and number of occurences in two seperate lists
        for k,v in Counter(userAgentList).items():
            x.append(k)
            y.append(v)
        plt.title('Viewers User Agents')
        plt.bar(range(len(y)), y, align='center')
        plt.xticks(range(len(y)), x, size='small')
        plt.show()
        return userAgentList
    #3a.Return browser names
    if task_selection == '3b':
        browsersList = []
        for x in jfile:
            if "Firefox" in x['visitor_useragent']:
               browsersList.append("Firefox")
            elif "Chrome" in x['visitor_useragent']:
                browsersList.append("Chrome")
            elif "Safari" in x['visitor_useragent']:
                browsersList.append("Safari")
            elif "Opera" in x['visitor_useragent']:
                browsersList.append("Opera")
            elif "MSIE" in x['visitor_useragent']:
                browsersList.append("Internet Explorer")
            else:
                browsersList.append("Other")
        #Run histogram and return browsersList
        x = []
        y = []
        #Insert countries and number of occurrences in two separate lists
        for k,v in Counter(browsersList).items():
            x.append(k)
            y.append(v)
        plt.bar(range(len(y)), y, align='center')
        plt.xticks(range(len(y)), x, size='small')
        plt.show()
        return browsersList


#4.Reader Profiles - Function for most avid readers
def TopReaders():
    readTimeDict = dict()
    #Itterate through JSON File
    for x in jfile:
        userFound = False
        #Look for page read occurrences
        if x['event_type'] == 'pagereadtime':
            #search for duplicate userID inside dict
            for k,v in readTimeDict .items():
                if k == x['visitor_uuid'] and x['event_readtime'] != None:
                    #Increment existing readtime value
                    readTimeDict[k] = int(x['event_readtime']) + v
                    userFound = True
                    break;
            #Add new user entry to dictionary
            if userFound == False:
                readTimeDict[x['visitor_uuid']] = int(x['event_readtime'])
    #Returns the dictionary with user_id ---> TotalReadTime
    return readTimeDict


#5a. Returns Readers ID based on a DocumentID
def DocToReaders(docID):
    readersList = []
    for x in jfile:
        #Search for doc in JSON,if the element doc_id exists
        if x.get('subject_doc_id') == docID:
            #Insert visitor's ID inside list
            readersList.append(x['visitor_uuid'])
    #return distinct readers IDs
    return set(readersList)

#5b. Returns DocumentIDs based on a readerID
def ReadersToDoc(readerID):
    docList = []
    for x in jfile:
        #Find user ID
        if x['visitor_uuid'] == readerID:
            #Check that doc ID exists
            if x.get('subject_doc_id') != None:
                #Add document ID to the list
                docList.append(x['subject_doc_id'])
    #return distinct values for document IDs
    return set(docList)

def AlsoLike(docID,task_selection):
    readersDocDict = dict()
    #Itterate over readers IDs
    for k in DocToReaders(docID):
        #Itterate over Document IDs that each reader has read
        for v in ReadersToDoc(k):
            #Insert readerID,docID into Dictionary
            readersDocDict.setdefault(k,[]).append(v)

    #Option 5d for returning a list of documents based on readership profile
    if task_selection == '5d':
        #Create dictionary to store DocumentIDs --> Reader's total read time
        docReadTimeDict = dict()
        #Itterating through Doc -->
        for k,v in TopReaders().items():
            for key,value in readersDocDict.items():
                if k == key :
                    #Itterate through values
                    for i in value:
                        #Insert DocID -- > readTime into dictionary
                        docReadTimeDict[i] = v
        alsoLikeList = []
        #Itterate through dictionary and sort values based on reader's time.
        for k,v in sorted(docReadTimeDict.items(), key = lambda x:-x[1])[:10]:
            #Insert top 10 values on list
            alsoLikeList.append(k)
        return alsoLikeList

    #Option 5e for returning a list of documents based on number of readers
    if task_selection == '5e':
        docList = []
        for k,v in readersDocDict.items():
            #Store each document read, inside a list
            for i in v:
                docList.append(i)
        countDocDict = dict()
        #Create dictionary with DocumentsRead --> Number of occurrences
        for x in docList:
            if x in countDocDict:
                countDocDict[x] += 1
            else:
                countDocDict[x] = 1
        alsoLikeList = []
        #Insert top 10 documents, based on the times they have been read inside a list
        for k,v in sorted(countDocDict.items(), key = lambda x:-x[1])[:10]:
            alsoLikeList.append(k)
        return alsoLikeList