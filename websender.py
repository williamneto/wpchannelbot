import time
from webwhatsapi import WhatsAPIDriver

class WPSender():
	def __init__(self):
		self.log_file = None

		self.msg_file = "m.csv"
		self.numbers_file = "n.csv"
		self.numers = []

		self.profile = "profile"
		self.driver = None

		self.connect()

	def connect(self):
		self.driver = WhatsAPIDriver("profile")
		time.sleep(3)
		if not self.driver.get_status() == "LoggedIn":
			self.driver.wait_for_login()

		self.driver.save_firefox_profile()

	def close(self):
		self.driver.close()
		time.sleep(3)

	def send(self):
		for number in self._get_numbers():
			
			if not self.driver.get_status == "LoggedIn":
				self.close()
				self.connect()

			id = number + "@c.us"
			print(">>Enviando para %s..." % number)
			sent = self.driver.send_message_to_id(id, self._get_message)

			if sent:
				status = ">>Enviado com sucesso para %s" % number
			else:
				status = ">>Impossível enviar para %s" % number

			print(status)

	def _get_numbers(self):
		numbers = []		
		with open(self.numbers_file) as csvfile:
			csvreader = csv.reader(csvfile)

			for row in csvreader:
				numbers = [x for x in row if x]

		self.numbers = numbers		
		return numbers

	def _get_message(self):	
		messages = []
		with open(self.msg_file) as csvfile:
			csvreader = csv.reader(csvfile)

			for row in csvreader:
				messages = [x for x in row if x]

		return str(random.choice(messages))

	def _to_log(self, log, n=0):
		file = open(self.log_file, "a")
		if not n == 0:
			file.write(">> %s - %s" % (n,log))
		else:
			file.write(log+"\n")
		file.close()
		return