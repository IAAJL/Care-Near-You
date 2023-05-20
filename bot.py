import os

import telebot
import getdata

radius = "1000"

bot_tok = os.environ.get('bot_tok')

bot = telebot.TeleBot('Token here',parse_mode='markdown')

@bot.message_handler(commands=['start','hello'])
def sendmess(message):
	bot.reply_to(message,"Melcow")

@bot.message_handler(commands=['getloc'])
def sendmess(message):

	print(message.text)
	lattitude = "28.7041"
	longitude = "77.1025"

	output=getdata.runcode(lattitude,longitude,radius)
	bot.reply_to(message,output)

@bot.message_handler(commands=['setradius'],func=lambda msg: msg.text is not None)
def sendmess(message):
	msg = message.text[11:]
	print("Radius = "+str(msg))
	if(msg.isdigit()):
		global radius
		radius=str(msg)
		output = "Changed radius to "+radius+"m"
	else:
		output="Wrong input '/setradius [Integer value]'"
	bot.reply_to(message,output)

@bot.message_handler(commands=['getradius'])
def getmess(message):
	output = "Radius = "+radius+"m"
	bot.reply_to(message,output)

@bot.message_handler(commands=['help'])
def showhelp(message):
	output = "*Help*\nInput the location as attachment to get the hospitals nearby\n"
	output = output + "_/getradius_ - Get the current radius of search\n"
	output = output + "_/setradius_ - Set new radius of search"
	bot.reply_to(message,output)
			

@bot.message_handler(func=lambda msg:True)
def sendall(message):
	count=0
	for i in message.text:
		if(i=='e'):
			count=count+1
	bot.reply_to(message,count)

@bot.message_handler(content_types=['location'])
def getloc(message):
	latitude = str(message.location.latitude)
	longitude=str(message.location.longitude)
	try:
		output=getdata.runcode(latitude,longitude,radius)
		print(latitude+","+longitude)
		if(len(output)==0):
			bot.reply_to(message,"Empty")
		else:
			bot.reply_to(message,output)
	except Exception as e:
		print("Exception = \n")
		print(e)
		bot.reply_to(message,"Error")

print("Prg started")

bot.infinity_polling()