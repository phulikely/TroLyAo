import sys
import os
from googletrans import Translator
from gtts import gTTS
import speech_recognition as sr
import setting
import const
import playsound
import json
import logging


def clear_promp():
	"""Clear promp
	"""
	if sys.platform == 'win32':
		clear = lambda: os.system('cls')
	else:
		clear = lambda: os.system('clear')
	clear()

def translate(text_source, text_dest):
	"""Translate from source language to destination language

	Args:
		text_source ([string]): [source language]
		text_dest ([string]): [destination language]

	Returns:
		[string]: [destination language]
	"""
	translator = Translator()
	result = (translator.translate(text_source, src=setting.TLA_ENG, dest=text_dest)).text
	return result

def hear(lang):
	"""Bot hear your voice

	Args:
		lang ([string]): [natural language]
		'en' : english
		'vi' : vietnamese
		'ja' : japanese	

	Returns:
		[string]: [your voice now is text]
	"""
	f = open (f"lang\\{lang}.json", encoding=setting.TLA_UTF8)
	data_json = json.load(f)
	try:
		bot_ear = sr.Recognizer()
		with sr.Microphone() as mic:
			#r.adjust_for_ambient_noise(mic)
			#giam tieng on cho mic
			print(data_json["TLA_BOT_HEARING"])
			bot_ear.pause_threshold = 1
			audio = bot_ear.listen(mic)
		try:
			print(data_json["TLA_BOT_RECOGNIZING"])
			query = bot_ear.recognize_google(audio, language=lang)
			print(f"You : {query}\n")
		except:
			print(data_json["TLA_BOT_CAN_NOT_HEAR"])
			logging.error(data_json["TLA_BOT_CAN_NOT_HEAR"])
			return ""
	except:
		speak(data_json["TLA_BOT_MIC_NG"], lang)
		#print(data_json["TLA_BOT_MIC_NG"])
		logging.error(data_json["TLA_BOT_MIC_NG"])
		return data_json["TLA_BOT_MIC_NG"]
	#query = input(const.TLA_BOT_CHAT)
	return query

def speak(text, lang):
	"""Text to speech

	Args:
		text ([string]): [text which will be speaked]
		lang ([string]): [natural language]
		'en' : english
		'vi' : vietnamese
		'ja' : japanese	
	"""
	try:
		output = gTTS(text=text, lang=lang, slow=False)
		tempFile = const.TLA_OUTPUT_MP3
		output.save(tempFile)
		playsound.playsound(tempFile)
		os.remove(tempFile)
	except sr.UnknownValueError as err_gtts:
		logging.error(err_gtts)
	except sr.RequestError as err_req:
		logging.error(err_req)