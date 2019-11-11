import urllib.request
from html.parser import HTMLParser
import re

infile = urllib.request.urlopen("http://www.dealsea.com")
data = infile.read().decode()
f = open('dealsea.data', 'w')
f.write(data)
f.close()
#Read file
#f = open('dealsea.data')
#text = f.read()
#f.close()

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.superlist = list()
        self.otherlist = list()
        self.tag = ""
        self.listnum = 0
    def getlist(self):
        return self.superlist
    def handle_starttag(self, tag, attrs):
        self.tag = str(tag)+ str(attrs)
        if(attrs == [('class', 'dealbox')]):
            #print("yYYYYYYYYYYYYYYYYYYYYYYYYYYY")
            self.superlist.append(self.otherlist)
            self.otherlist = list()
            self.listnum += 1
            #print("Encountered a start tag:", tag)
        pass

    def handle_endtag(self, tag):
        #print("Encountered an end tag :", tag)
        pass

    def handle_data(self, data):
        databackup = data
        data = re.sub(r"[\n\t\s]*", "", data)
        if data != "":
            self.otherlist.append([self.tag,databackup])
            #print("Encountered some data  :", data)

parser = MyHTMLParser()
parser.feed(data)

test = parser.getlist()[1:-1]

for i in range(len(test)):
    for j in range(len(test[i])):
        if test[i][j][0] == "span[('class', 'carat')]":
            test[i] = test[i][0:j]
            print("Halijaua")
            break
        else:
            print(i,j,test[i][j])
