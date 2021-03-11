import sys
import os
from googletrans import Translator
from gtts import gTTS
import speech_recognition as sr
import setting
import const
import playsound
import json


# Clear promp
def clear_promp():
	if sys.platform == 'win32':
		clear = lambda: os.system('cls')
	else:
		clear = lambda: os.system('clear')
	# Clear promp
	clear()

# Translate English to Vietnamese
def translate(text_source, text_dest):
    translator = Translator()
    result = (translator.translate(text_source, src=setting.TLA_ENG, dest=text_dest)).text
    return result

# Bot hear your voice
def hear(lang):
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
			return ""
	except:

		speak(data_json["TLA_BOT_MIC_NG"], lang)
		print(data_json["TLA_BOT_MIC_NG"])
		return data_json["TLA_BOT_MIC_NG"]
	#query = input(const.TLA_BOT_CHAT)
	return query

# Text to speech
def speak(text, lang):
	output = gTTS(text=text, lang=lang, slow=False)
	tempFile = const.TLA_OUTPUT_MP3
	output.save(tempFile)
	playsound.playsound(tempFile)
	os.remove(tempFile)