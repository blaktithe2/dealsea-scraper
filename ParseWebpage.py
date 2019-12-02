import urllib.request
import bs4 as bs

class deal:
    def __init__(self, title, link, content, vendor):
        self.title = title
        self.link = link
        self.content = content
        self.vendor = vendor
    def getLink(self):
        return self.link
    def getTitle(self):
        return self.title
    def setTitle(self, title):
        self.title = title
    def getContent(self):
        return self.content
    def getVendor(self):
        return self.vendor

infile = urllib.request.urlopen("http://www.dealsea.com")
data = infile.read().decode()
f = open('dealsea.data', 'w')
f.write(data)
f.close()
#Read file
#f = open('dealsea.data')
#text = f.read()
#f.close()

soup = bs.BeautifulSoup(data, 'html.parser')

soup2 = soup.findAll("div", class_="dealcontent")

soup3 = []
for i in soup2:
    title = i.strong.a.get_text()
    link = i.strong.a.get('href')

    soup3.append(deal(title,link,'test','test'))

for i in soup3:
    print(i.getLink(),i.getTitle())
print(len(soup3), "element(s)")