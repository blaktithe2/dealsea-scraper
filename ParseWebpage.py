import urllib.request
import bs4 as bs

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
    #print(i.strong.a.get_text())
    soup3.append(i.strong.a.get_text())
print(len(soup3),"element(s)")