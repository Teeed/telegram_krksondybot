import logging
logging.basicConfig(level=logging.DEBUG,
					format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from telegram.ext import Updater
import config
updater = Updater(token=config.TELEGRAM_TOKEN)
dispatcher = updater.dispatcher

from telegram.ext import CommandHandler, MessageHandler, Filters


def start(bot, update):
	update.message.reply_text("Dzień dobry! :) W czym mogę ci pomóc?")

	
import telegram
from anal_run_for import run_anal
def predict(bot, update, args):
	if len(args) < 1:
		update.message.reply_text('Podaj nazwe sondy')
		return

	sonde = run_anal((' '.join(args)).lower())
	if sonde == 'notfound':
		update.message.reply_text('Nie znalazłem sondy w bazie')
		return

	if sonde == 'toohigh':
		update.message.reply_text('Sonda jest za wysoko')
		return

	# update.message.reply_chat_action(action='find_location')

	update.message.reply_location(latitude=sonde[0], longitude=sonde[1])


def normal_message(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Nie zrozumiałem, spróbuj używać konkretnych komend.")


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('predict', predict, pass_args=True))
dispatcher.add_handler(MessageHandler(Filters.text, normal_message))

updater.start_polling()
