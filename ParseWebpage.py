import urllib.request
import bs4 as bs
import requests
from twilio.rest import Client
import mysql.connector

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

def getDealsText(deals, n):
    length = len(deals)
    text = ""
    if length < n:
        return
    for i in range(n):
        text = text + "\n" + deals[i].getTitle() + " : " + deals[i].getVendor() + " : " + deals[i].getLink() + "\n" + deals[i].getContent() + "\n----------------------------------------"
    return text
def displayDeals(deals, n):
    length = len(deals)
    if length < n:
        print("Not enough deals.")
        return
    print("Title, vendor, URL, content")
    for i in range(n):
        print(deals[i].getTitle(),":",deals[i].getVendor(),":",deals[i].getLink(),"\n",deals[i].getContent() + "\n----------------------------------------")

def sendEmail(deals, num):
    data = getDealsText(deals, num)
    try:
        f = open('mailgun.key')
        key = f.read()
        f.close()
    except IOError:
        print("Mailgun API key missing")
    return requests.post(
        "https://api.mailgun.net/v3/sandboxd10bb35ab0c4461aabdc94d6fce977ac.mailgun.org/messages",
        auth=("api", key),
        data={"from": "Mailgun Sandbox <postmaster@sandboxd10bb35ab0c4461aabdc94d6fce977ac.mailgun.org>",
            "to": "Lance Jordan <lance.e.jordan@gmail.com>",
            "subject": "Dealsea top "+str(num)+" deals",
            "text": data})

def sendSMS(data):
    try:
        f = open('twilio.key')
        auth_token = f.read()
        f.close()
    except IOError:
        print("Twilio API key missing")
    account_sid = 'AC5a814c3a42f034a8f0aeca0f0539743f'
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body=data,
                         from_='+12564149948', #Twilio phone number
                         to='+12818535023' #Lance's phone number
                     )

    return message.sid

def sendToSQL(deals):
    n = len(deals)
    try:
        f = open('SQL.key')
        password = f.read()
        f.close()
    except IOError:
        print("SQL API key missing")
    host="192.232.216.112"
    user="lancejor_dan"
    database="lancejor_COSC1437"
    mydb = mysql.connector.connect(host=host,user=user,password=password,database=database)
    mycursor = mydb.cursor()
    for i in deals:
        sql = "INSERT INTO `Dealsea` (`title`, `link`, `content`, `vendor`) VALUES (%s, %s, %s, %s);"
        val = (i.getTitle(),i.getLink(),i.getContent(),i.getVendor())
        mycursor.execute(sql, val)

        mydb.commit()
def getFromSQL():
    try:
        f = open('SQL.key')
        password = f.read()
        f.close()
    except IOError:
        print("SQL API key missing")
    host="192.232.216.112"
    user="lancejor_dan"
    database="lancejor_COSC1437"
    mydb = mysql.connector.connect(host=host,user=user,password=password,database=database)
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM `Dealsea`")

    myresult = mycursor.fetchall()

    for x in myresult:
      print(x)
      pass

def getDealDetails(URL):
    webdata = urllib.request.urlopen("http://www.dealsea.com"+URL)
    data = webdata.read().decode()
    soup = bs.BeautifulSoup(data, 'html.parser')

    divSoup = soup.find("div", class_="deal")
    difDiv = divSoup.findAll("div")
    nextT = difDiv[-1]
    Author = nextT.findAll('p')[1].get_text()
    title = soup.find("h1").get_text()

    divSoup = soup.find("div", class_="posttext")
    vendor = divSoup.a.get_text()
    content = divSoup.get_text()
    newDeal = deal(title,URL,content,vendor)
    return Author,newDeal

def getDealsFromWebpage():
    try:
        infile = urllib.request.urlopen("http://www.dealsea.com")
    except:
        pass
    return infile.read().decode()

def writeDealsToFile(data):
    try:
        f = open('dealsea.data', 'w')
        f.write(data)
        f.close()
    except IOError:
        print("dealSea.data missing")
def readDealsFromFile():
    try:
        f = open('dealsea.data', 'r')
        data = f.read()
        f.close()
    except:
        pass
    return data


#MEAT

access = 0
data = ""
while(access != -1):
    try:
        access = int(input("1:Get data from http 2: get data from file 3: save data to file 4: pass onto parsing"))
    except ValueError:
        access = 0
    if access == 1:
        data = getDealsFromWebpage()
    elif access == 2:
        data = readDealsFromFile()
    elif access == 3:
        writeDealsToFile(data)
    elif access == 4:
        access = -1
data = getDealsFromWebpage()


soup = bs.BeautifulSoup(data, 'html.parser')

divSoup = soup.findAll("div", class_="dealcontent")

dealSea = []
for i in divSoup:
    title = i.strong.a.get_text()
    link = i.strong.a.get('href')
    vendor = i.div.a.get_text()
    content = i.div.get_text()

    dealSea.append(deal(title,link,content,vendor))

ans = 0
while(ans != -1):
    try:
        ans = int(input("1:displayDeals 2: send deal Email 3: Send deal SMS 4: send to SQL 5: get from SQL 6: get deal details from page\n"))
    except ValueError:
        ans = 0
    if ans == 1:
        displayDeals(dealSea, 5)
    elif ans == 2:
        num = int(input("How many deals to mail"))
        print(sendEmail(dealSea, num))
    elif ans == 3:
        print(sendSMS(dealSea[0].getTitle()))
    elif ans == 4:
        sendToSQL(dealSea[0:5])
    elif ans == 5:
        getFromSQL()
    elif ans == 6:
        try:
            for i in dealSea:
                author, newDeal = getDealDetails(i.getLink())
                print(author)
                print(newDeal.getTitle())
        except KeyboardInterrupt:
            pass



