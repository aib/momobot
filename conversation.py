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
		if message.chat.id in self._group_ids:
			return True
		else:
			_logger.info("Ignoring chat id %d", message.chat.id)
			return False

def message(bot, update):
	text = update.message.text
	if "momobot" in text.lower():
		reply = _db.get_random_text()

		time.sleep(random.random())
		bot.sendChatAction(chat_id=update.message.chat.id, action=telegram.chataction.ChatAction.TYPING)
		time.sleep(min(4, len(reply) / 10.0))
		bot.sendMessage(chat_id=update.message.chat.id, text=reply)
	else:
		_db.add_text(text)

def init(updater, group_ids):
	global _db
	_db = MessageDB("db/conv.db", 1000)
	_db.load()
	updater.dispatcher.add_handler(telegram.ext.MessageHandler(MyFilter(group_ids), message))
