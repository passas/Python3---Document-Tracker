__author__ = 'Paparisteidis Georgios'


from collections import Counter
import program
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-u', action="store")
parser.add_option('-d', action="store")
parser.add_option('-t', action="store")
options, args = parser.parse_args()

readerID = str(options.u)
docID = str(options.d)
task_selection = str(options.t)

if task_selection == '2a':
    print("Countries of Visitors:")
    for k,v in (Counter(program.ViewByCountry(docID,task_selection))).items():
        print(k,"-->",v)
elif task_selection == '2b':
    print("Continents of Visitors:")
    for k,v in (Counter(program.ViewByCountry(docID,task_selection))).items():
        print (k,"-->",v)
elif task_selection == '3a':
    print("Browsers identifiers")
    for k,v in (Counter(program.ViewsByBrowser(task_selection))).items():
        print(k,"-->",v)
elif task_selection == '3b':
    print("Browsers :")
    for k,v in Counter(program.ViewsByBrowser(task_selection)).items():
        print(k,"-->",v)
elif task_selection == '4':
    print("Top Readers are:")
    topReadersList = []
    readTimeDict = program.TopReaders()
    #Sort dictionary based on readTime values,reverse it,add it on list
    for k,v in (sorted(readTimeDict.items(), key=lambda x:-x[1]))[:10]:
        topReadersList.append(k)
    #Return a list representation of the sorted dictionary
    for x in topReadersList:
        print(x)
elif task_selection == '5a':
    print('Readers that have read this Document: ')
    for x in program.DocToReaders(docID):
        print(x)
elif task_selection == '5b':
    print('Documents that have been read by this Reader: ')
    for x in program.ReadersToDoc(readerID):
        print(x)
elif task_selection == '5d':
    print("Documents also liked by other readers based on their reading profile: ")
    program.AlsoLike(docID,task_selection)
    list = program.AlsoLike(docID,task_selection)
    for x in list[:10]:
        print(x)
elif task_selection == '5e':
    print("Documents also liked by other readers based on popularity (times read): ")
    program.AlsoLike(docID,task_selection)
    list = program.AlsoLike(docID,task_selection)
    for x in list[:10]:
        print(x)


