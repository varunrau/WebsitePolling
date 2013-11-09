import urllib2
from apscheduler.scheduler import Scheduler
from emailer import Emailer
import sys
from argparse import ArgumentParser

sched = Scheduler()
interval = 3600

class Poller:

	def __init__(self, page, interval, email, password, message):
		self.interval = interval
		self.url = page
		self.cached_page = self.poll()
		self.email = email
		self.password = password
		self.message = message
		self.interval = interval

	def poll(self):
		usock = urllib2.urlopen(self.url)
		data = usock.read()
		usock.close()
		return data

	@sched.interval_schedule(minutes=interval)
	def check_page(self):
		if self.did_change():
			emailer = Emailer(self.email, self.password)
			emailer.send_message(self.message)
			sched.shutdown()

	def did_change(self):
		return self.poll() != self.cached_page

if __name__ == "__main__":
	parser = ArgumentParser(description="Emails you when a given website changes")
	parser.add_argument("-u", "--url", nargs="?", type=str, help="The website you would like to check")
	parser.add_argument("-e", "--email", nargs="?", type=str, help="your email")
	parser.add_argument("-p", "--password", nargs="?", type=str, help="your email password")
	parser.add_argument("-i", "--interval", type=int, help="How often you would like to check (in minutes)")
	parser.add_argument("-m", "--message", type=str, help="The message you would like to see in your email notification")
	args = parser.parse_args()
	sched.start()
	interval = args.interval
	poller = Poller(args.url, args.interval, args.email, args.password, args.message)

