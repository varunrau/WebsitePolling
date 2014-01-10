import urllib2
from emailer import Emailer
import sys
from argparse import ArgumentParser
import time
import datetime

interval = 3600

class Poller:

	def __init__(self, page, interval, email, message):
		self.interval = interval
		self.url = page
		self.cached_page = self.poll()
		self.email = email
		if message:
			self.message = "\n" + str(message)
		else:
			self.message = "\nThe website " + self.url + " has changed."
		self.interval = interval
		self.done = False

	def poll(self):
		usock = urllib2.urlopen(self.url)
		data = usock.read()
		usock.close()
		return data

	def isDone(self):
		return self.done

	def check_page(self):
		print "checking..."
		if self.did_change():
			print "Sending email"
			emailer = Emailer(self.email)
			self.message += "\n" + self.url + " changed on " + str(datetime.datetime.now()) + "."
			emailer.send_message(self.message)
			emailer.notify(
					title = 'Website changed',
					subtitle = '',
					message = self.message,
					open = self.url
					)
			self.done = True

	def did_change(self):
		return self.poll() != self.cached_page

if __name__ == "__main__":
	parser = ArgumentParser(description="Emails you when a given website changes")
	parser.add_argument("-u", "--url",
			nargs="?",
			type=str,
			required=True,
			help="The website you would like to check")
	parser.add_argument("-e", "--email",
			nargs="?",
			type=str,
			required=True,
			help="your email")
	parser.add_argument("-i", "--interval",
			type=int,
			help="How often you would like to check (in minutes)")
	parser.add_argument("-m", "--message",
			type=str,
			help="The message you would like to see in your email notification")
	args = parser.parse_args()
	interval = args.interval
	poller = Poller(args.url, args.interval, args.email, args.message)
	while not poller.isDone():
		poller.check_page()
		time.sleep(args.interval * 60)

