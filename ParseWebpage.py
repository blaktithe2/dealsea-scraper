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
    def getContent(self):
        return self.content
    def getVendor(self):
        return self.vendor
def displayDeals(deals, n):
    length = len(deals)
    if length < n:
        return
    print("Title, vendor, URL, content")
    for i in range(n):
        print(deals[i].getTitle(),":",deals[i].getVendor(),":",deals[i].getLink(),":",deals[i].getContent())

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

dealSea = []
for i in soup2:
    title = i.strong.a.get_text()
    link = i.strong.a.get('href')
    vendor = i.div.a.get_text()
    content = i.div.get_text()

    dealSea.append(deal(title,link,content,vendor))

displayDeals(dealSea, 5)