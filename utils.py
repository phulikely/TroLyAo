import sys
import os
from googletrans import Translator
from gtts import gTTS
import speech_recognition as sr
import setting
import const
import playsound

# Clear promp
def clear_promp():
	if sys.platform == 'win32':
		clear = lambda: os.system('cls')
	else:
		clear = lambda: os.system('clear')
	# Clear promp
	clear()

# Translate English to Vietnamese
def translate(text_english):
    translator = Translator()
    result = (translator.translate(text_english, src=setting.TLA_ENG, dest=setting.TLA_VN)).text
    return result

# Bot hear your voice
def hear():
	try:
		bot_ear = sr.Recognizer()
		with sr.Microphone() as mic:
			#r.adjust_for_ambient_noise(mic)
			#giam tieng on cho mic
			print(const.TLA_BOT_HEARING)
			bot_ear.pause_threshold = 1
			audio = bot_ear.listen(mic)
		try:
			print(const.TLA_BOT_RECOGNIZING)
			query = bot_ear.recognize_google(audio, language=setting.TLA_VN)
			print(f"You : {query}\n")
		except:
			print(const.TLA_BOT_CAN_NOT_HEAR)  
			return ""
	except:
		speak(const.TLA_BOT_MIC_NG)
		print(const.TLA_BOT_MIC_NG)
		return const.TLA_BOT_MIC_NG
	#query = input(const.TLA_BOT_CHAT)
	return query

# Text to speech
def speak(text):
	output = gTTS(text=text, lang=setting.TLA_VN, slow=False)
	tempFile = const.TLA_OUTPUT_MP3
	output.save(tempFile)
	playsound.playsound(tempFile)
	os.remove(tempFile)