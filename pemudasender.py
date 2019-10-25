from sender import Sender

print("---=========[ Pemuda Sender ]=========---")
emailSender = input("Please input sender email address: ")
passwordSender = input("Please input password: ")

senderTools = Sender(emailSender, passwordSender)
senderTools.send()