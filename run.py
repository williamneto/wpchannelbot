from channelbot import WPChannelBot
import time

from http.client import ResponseNotReady, CannotSendRequest
from selenium.common.exceptions import WebDriverException
from json.decoder import JSONDecodeError

while True:
	try:
		time.sleep(3)
		bot = WPChannelBot()
		bot.start()
	except (ResponseNotReady, JSONDecodeError, CannotSendRequest, WebDriverException):
		continue