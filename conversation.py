import telegram.chataction
import telegram.ext

import logging
_logger = logging.getLogger(__name__)

import pickle
import random
import time

_db = None

class MessageDB:
	def __init__(self, db_file, max_lines):
		self._db_file = db_file
		self._max_lines = max_lines
		self._lines = []

	def load(self):
		try:
			with open(self._db_file, 'rb') as f:
				self._lines = pickle.load(f)
		except FileNotFoundError:
			self._lines = []

	def save(self):
		with open(self._db_file, 'wb') as f:
			pickle.dump(self._lines, f)

	def add_text(self, text):
		if len(text) == 0:
			return

		self._lines.append(text)
		while len(self._lines) > self._max_lines:
			self._lines.pop(0)
		self.save()

	def get_random_text(self):
		return random.choice(self._lines)

class MyFilter(telegram.ext.filters.BaseFilter):
	def __init__(self, group_ids):
		self._group_ids = group_ids

	def filter(self, message):
		if message.chat.type == 'private':
			return True

		if message.chat.type == 'group' and message.chat.id in self._group_ids:
			return True

		_logger.info("Ignoring chat id %d", message.chat.id)
		return False

def message(bot, update):
	text = update.message.text

	if text.startswith("/"):
		return

	if update.message.chat.type == 'private':
		_respond(bot, update.message.chat.id)
		if "momobot" not in text.lower():
			_db.add_text(text)
		return

	if update.message.chat.type == 'group':
		if "momobot" in text.lower():
			_respond(bot, update.message.chat.id)
		else:
			_db.add_text(text)
		return

def _respond(bot, chat_id):
	response = _db.get_random_text()

	time.sleep(random.random())
	bot.sendChatAction(chat_id=chat_id, action=telegram.chataction.ChatAction.TYPING)
	time.sleep(min(4, len(response) / 10.0))
	bot.sendMessage(chat_id=chat_id, text=response)

def init(updater, group_ids):
	global _db
	_db = MessageDB("db/conv.db", 32767)
	_db.load()
	updater.dispatcher.add_handler(telegram.ext.MessageHandler(MyFilter(group_ids), message))
