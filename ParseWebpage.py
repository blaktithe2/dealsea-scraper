import urllib.request
import bs4 as bs
import requests
from twilio.rest import Client

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
    print("Title, vendor, URL, content")
    for i in range(n):
        text = text + "\n" + deals[i].getTitle() + " : " + deals[i].getVendor() + " : " + deals[i].getLink() + "\n" + deals[i].getContent() + "\n----------------------------------------"
    return text
def displayDeals(deals, n):
    length = len(deals)
    if length < n:
        return
    print("Title, vendor, URL, content")
    for i in range(n):
        print(deals[i].getTitle(),":",deals[i].getVendor(),":",deals[i].getLink(),":",deals[i].getContent())

def sendEmail(deals):
    f = open('mailgun.key')
    key = f.read()
    f.close()
    return requests.post(
        "https://api.mailgun.net/v3/sandboxd10bb35ab0c4461aabdc94d6fce977ac.mailgun.org/messages",
        auth=("api", key),
        data={"from": "Mailgun Sandbox <postmaster@sandboxd10bb35ab0c4461aabdc94d6fce977ac.mailgun.org>",
            "to": "Lance Jordan <lance.e.jordan@gmail.com>",
            "subject": "Dealsea top 10 deals",
            "text": deals})

def sendSMS(deals):
    f = open('twilio.key')
    auth_token = f.read()
    f.close()
    account_sid = 'AC5a814c3a42f034a8f0aeca0f0539743f'
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body=deals,
                         from_='+12564149948', #Twilio phone number
                         to='+12818535023' #Lance's phone number
                     )

    print(message.sid)

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

divSoup = soup.findAll("div", class_="dealcontent")

dealSea = []
for i in divSoup:
    title = i.strong.a.get_text()
    link = i.strong.a.get('href')
    vendor = i.div.a.get_text()
    content = i.div.get_text()

    dealSea.append(deal(title,link,content,vendor))

displayDeals(dealSea, 5)

print(sendEmail(getDealsText(dealSea, 10)))

print(sendSMS(dealSea[0].getTitle()))

