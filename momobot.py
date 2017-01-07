#!/usr/bin/env python3

import logging
logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)

import telegram.ext

import config
import conversation

def main():
	_logger.info("Starting Momobot!")
	token = config.from_file('db/token.txt')
	_logger.debug("Token is %s", token)

	tg_updater = telegram.ext.Updater(token=token)
	conversation.init(tg_updater, [int(config.from_file('db/momoloji.id'))])
	tg_updater.start_polling()

if __name__ == '__main__':
	main()
