import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import requests
import json
import time
import codecs
import requests_cache

class Sender:
    def __init__(self, emailSender, passwordSender):
        self.emailSender = emailSender
        self.passwordSender = passwordSender
        self.receiverList = []
        self.url = "http://192.168.0.20:8001/api/email/email"
        self.totalGained = 0
        self.searchingMail = False
        requests_cache.install_cache()

    def writeEmailToFile(self, email):
        f = open("emai_sended.txt", "a")
        f.write(email + "\n")
        f.close()

    def readFile(self):
        f = open("emai_sended.txt", "r")
        return f.read()

    def getListMail(self, url):
        self.searchingMail = True
        r = requests.get(url)
        data = r.json()
        
        gained = 0
        for pemudaData in data["data"]["data"]:
            if pemudaData["email"] != "":
                self.receiverList.append(pemudaData["email"].strip())
                gained += 1
                self.totalGained += 1
        print("Gained {} email address | Total Gained: {}".format(str(gained), str(self.totalGained)))
        if data["data"]["next_page_url"]:
            self.getListMail(data["data"]["next_page_url"])
        else:
            self.searchingMail = False

        # self.receiverList = [
        #     "yusriltakeuchi@gmail.com",
        #     "jenkinshacker@gmail.com"
        # ]


    def send(self):
        self.getListMail(self.url)

        sended_list = self.readFile()
        if self.searchingMail == False:
            print("Finding email success")

            fromNum = 0
            toNum = 0
            while True:
                fromNum = int(input("Ingin mulai dari angka berapa?: "))
                toNum = int(input("Kemudian sampai angka berapa?: "))

                if (toNum <= len(self.receiverList)):
                    break

            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
            server.login(self.emailSender, self.passwordSender)
            
            position = 0
            mailSuccess = 0
            mailFailed = 0
            for receiver in self.receiverList:
                position += 1
                if receiver not in sended_list:
                    if position >= fromNum and position <= toNum:
                        print("[{}/{}] Sending mail to {}...".format(str(position), str(len(self.receiverList)), receiver))
                        
                        while True:
                            try:
                                message = MIMEMultipart("alternative")
                                message["Subject"] = "Undangan Sumpah Pemuda Indonesia"
                                message["From"] = "Patria Indonesia"

                                mailType = MIMEText(self.getMessageBody(), "html")
                                message.attach(mailType)
                                message["To"] = receiver

                                fp = open('1.jpeg', 'rb')
                                msgImage = MIMEImage(fp.read())
                                fp.close()

                                msgImage.add_header('Content-ID', '<image1>')
                                message.attach(msgImage)

                                server.sendmail(
                                    self.emailSender, receiver, message.as_string()
                                )
                                mailSuccess += 1
                                #Write to file
                                self.writeEmailToFile(receiver)
                                break
                            except Exception as e:
                                print(e)
                                if str(e) == "please run connect() first":
                                    print("Reached limit, please wait 50 seconds")
                                    time.sleep(50)
                                    
                                    server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
                                    server.login(self.emailSender, self.passwordSender)
                                    continue
                                else:
                                    mailFailed += 1
                                    print("Failed sending mail to {}...".format(receiver))
                                    break

                            #Delay 3 seconds after send 5 email to prevent blocked
                            if mailSuccess % 5 == 0:
                                time.sleep(3)
            
            print("Sending mail successfully...")
            print("{} Success | {} Failed".format(str(mailSuccess), str(mailFailed)))



    def getMessageBody(self):
        return codecs.open("index.html", 'r', 'utf-8').read()
        # return """\
        # <html>
        # <body>
        #     <h4>Halo Pemuda Indonesia!</h4>
        #     <p>Segera ikuti opening sumpah pemuda Indonesia pada <b>28 Oktober!</b></p>
        # </body>
        # </html>
        # """