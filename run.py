from channelbot import WPChannelBot
import time

from http.client import BadStatusLine, ResponseNotReady, CannotSendRequest, LineTooLong
from selenium.common.exceptions import WebDriverException
from json.decoder import JSONDecodeError
from selenium.common.exceptions import JavascriptException
from webwhatsapi.wapi_js_wrapper import JsException


while True:
	bot = WPChannelBot()
	try:
		bot.start()
	except (LineTooLong, JavascriptException, JsException, ResponseNotReady, JSONDecodeError, CannotSendRequest, WebDriverException, BadStatusLine):
		bot.shutdown()
		continue