import smtplib
import os

class Emailer:
	def __init__(self, email_address):
		self.FROM_EMAIL = "websitepolling@gmail.com"
		self.PASSWORD = "ipollyoursites"
		self.email_address = email_address
		self.init_server()

	def init_server(self):
		self.server = smtplib.SMTP("smtp.gmail.com", 587)
		self.server.starttls()
		self.server.login(self.FROM_EMAIL, self.PASSWORD)

	def send_message(self, message="\nYou've got mail!"):
		email = "Subject: %s\n\n%s" % ("Your reminder from Website Polling", message)
		self.server.sendmail(self.FROM_EMAIL, self.email_address, email)

	def notify(title, subtitle, message):
		t = '-title {!r}'.format(title)
		s = '-subtitle {!r}'.format(subtitle)
		m = '-message {!r}'.format(message)
		os.system('terminal-notifier {}'.format(' '.join([m, t, s])))

