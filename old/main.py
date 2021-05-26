"""
import telegram
bot = telegram.Bot(token = '1860252564:AAFdaazeNeMM6BlUBnOcpeJUavBR-xbYv_8')
from telegram.ext import Updater,MessageHandler,Filters

def echo(update,context):
	update.message.reply_text(update.message.text)
updater = Updater('1860252564:AAFdaazeNeMM6BlUBnOcpeJUavBR-xbYv_8',use_context = True)
updater.dispatcher.add_handler(MessageHandler(Filters.text,echo))
updater.start_polling()
updater.idle()

import spacy
from telegram.ext import Updater, MessageHandler, Filters #the callback function that uses spaCy
def utterance(update, context): 
	msg = update.message.text nlp = spacy.load('en')
	doc = nlp(msg)
	for token in doc:
		if token.dep_ == 'dobj':
			update.message.reply_text('We are processing your request...')
			return 
	update.message.reply_text('Please rephrase your request. Be as specific as possible!')
#the code responsible for interactions with Telegram
updater = Updater('1860252564:AAFdaazeNeMM6BlUBnOcpeJUavBR-xbYv_8', use_context=True) updater.dispatcher.add_handler(MessageHandler(Filters.text, utterance)) updater.start_polling()
updater.idle()
"""
import logging
import sys
import spacy
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
#allows you to obtain generic debug info
logger = logging.getLogger(__name__) 
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
def extract_intent(doc):
	for token in doc:
		if token.dep_ == 'dobj':
			verb = token.head.text
			dobj = token.text
	#create a list of tuples for possible verb synonyms
	verbList = [('order','want','give','make'),('show','find')]
	#find the tuple containing the transitive verb extracted from the sample
	verbSyns = [item for item in verbList if verb in item] #create a list of tuples for possible direct object synonyms
	dobjList = [('pizza','pie','dish'),('cola','soda')]
	#find the tuple containing the direct object extracted from the sample
	dobjSyns = [item for item in dobjList if dobj in item]
	#replace the transitive verb and the direct object with synonyms supported by the application
	#and compose the string that represents the intent
	intent = verbSyns[0][0] + dobjSyns[0][0].capitalize() 
	return intent
def utterance(update, context): 
	msg = update.message.text 
	nlp = spacy.load("en_core_web_sm")
	doc = nlp(msg)
	for token in doc:
		if token.dep_ == 'dobj':
			intent = extract_intent(doc)
			if intent == 'orderPizza':
				update.message.reply_text('We need some more information to place your order.')
			elif intent == 'showPizza':
				update.message.reply_text('Would you like to look at our menu?') 
			else:
				update.message.reply_text('Your intent is not recognized.') 
				return
		update.message.reply_text('Please rephrase your request. Be as specific as possible!')
def details_to_str(user_data):
	details = list()
	for key, value in user_data.items():
		details.append('{} - {}'.format(key, value)) 
	return "\n".join(details).join(['\n', '\n'])
def start(update, context):
	update.message.reply_text('Hi! This is a pizza ordering app. Do you want to order something?')
	return 'ORDERING'
def intent_ext(update, context): 
	msg = update.message.text 
	nlp = spacy.load('en')
	doc = nlp(msg)
	for token in doc:
		if token.dep_ == 'dobj':
			intent = extract_intent(doc) 
			if intent == 'orderPizza':
				context.user_data['product'] = 'pizza'
				update.message.reply_text('We need some more information to place your order. What type of pizza do you want?')
				return 'ADD_INFO' 
			else:
				update.message.reply_text('Your intent is not recognized. Please rephrase your request.')
				return 'ORDERING' 
			return
	update.message.reply_text('Please rephrase your request. Be as specific as possible!')

def add_info(update, context): 
	msg = update.message.text 
	nlp = spacy.load('en')
	doc = nlp(msg)
	for token in doc:
		if token.dep_ == 'dobj':
			dobj = token
			for child in dobj.lefts:
				if child.dep_ == 'amod' or child.dep_ == 'compound': context.user_data['type'] = child.text
				user_data = context.user_data 
				update.message.reply_text("Your order has been placed."
					"{}"
					"Have a nice day!".format(details_to_str(user_data))) 
			return ConversationHandler.END
	update.message.reply_text("Cannot extract necessary info. Please try again.") 
	return 'ADD_INFO'
def cancel(update, context): 
	update.message.reply_text("Have a nice day!") 
	return ConversationHandler.END
def main():
	#Replace TOKEN with a real token
	updater = Updater("1860252564:AAFdaazeNeMM6BlUBnOcpeJUavBR-xbYv_8", use_context=True) 
	disp = updater.dispatcher
	conv_handler = ConversationHandler(
		entry_points=[CommandHandler('start', start)], 
		states={
			'ORDERING': [MessageHandler(Filters.text, intent_ext)],
			'ADD_INFO': [MessageHandler(Filters.text,add_info) ],},
			fallbacks=[CommandHandler('cancel', cancel)])
	disp.add_handler(conv_handler) 
	updater.start_polling() 
	updater.idle()
if __name__ == '__main__': 
	main()