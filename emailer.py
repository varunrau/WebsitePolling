import smtplib

class Emailer:
	def __init__(self, email_address, password):
		self.email_address = email_address
		self.password = password
		self.init_server()

	def init_server(self):
		self.server = smtplib.SMTP("smtp.gmail.com", 587)
		self.server.login(self.email_address, self.password)

	def send_message(message="\nYou've got mail!"):
		self.server.sendmail(self.email_address, self.email_address, message)

