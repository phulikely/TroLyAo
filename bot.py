# System basic lib
import os
import datetime
import ctypes
import time
import json
import logging

# The 3rd party
import gtts
from gtts import gTTS
import wikipedia
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from textblob import TextBlob

# My import
import const
import setting
import utils

# chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
now = datetime.datetime.now()
data_json = None
logging.basicConfig(filename='output_log.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s')


def greeting(lang):
	"""Say greetings depending time in day

	Args:
		lang ([string]): [natural language]
		'en' : english
		'vi' : vietnamese
		'ja' : japanese
	"""
	hour = int(datetime.datetime.now().hour)
	if hour>= 0 and hour<12:
		utils.speak(data_json["TLA_BOT_MORNING"], lang)
	elif hour>= 12 and hour<18:
		utils.speak(data_json["TLA_BOT_AFTERNOON"], lang)
	else:
		utils.speak(data_json["TLA_BOT_EVENING"], lang)
	utils.speak(data_json["TLA_BOT_ASK_FOR_HELP"], lang)

def find_in_wiki(query, lang):
	"""Looking for information in Wikipedia

	Args:
		query ([string]): [The keyword which will be used for searching in Wikipedia]
		lang ([string]): [natural language]
		'en' : english
		'vi' : vietnamese
		'ja' : japanese
	"""
	utils.speak(data_json["TLA_BOT_WIKI_FINDING"], lang)
	query = query.replace(data_json["TLA_WHO"], const.TLA_OUTPUT_EMPTY_STR)
	query = query.replace(data_json["TLA_WHAT"], const.TLA_OUTPUT_EMPTY_STR)
	query = query.replace(data_json["TLA_WHERE"], const.TLA_OUTPUT_EMPTY_STR)
	wikipedia.set_lang(lang)
	try:
		results = wikipedia.summary(query, sentences = 3)
		#print(query)
		logging.info(query)
		utils.speak(data_json["TLA_BOT_WIKI_FOUND"], lang)
		#print("\n" + results)
		logging.info(results)
		utils.speak(results, lang)
	except wikipedia.exceptions.PageError as err_wiki:
		results = data_json["TLA_BOT_WIKI_NOT_FOUND"]
		#print(results)
		logging.error(results)
		logging.error(err_wiki)
		utils.speak(results, lang)

def play_music(lang):
	"""Play music on Youtube

	Args:
		lang ([string]): [natural language]
		'en' : english
		'vi' : vietnamese
		'ja' : japanese		
	"""
	utils.speak(data_json["TLA_BOT_ASK_MUSIC_NAME"], lang)
	ans = utils.hear(lang)
	#print(const.TLA_YOU_RESP + ans)
	logging.info(const.TLA_YOU_RESP + ans)
	utils.speak(data_json["TLA_BOT_PLAY_MUSIC"], lang)
	#driver = webdriver.Chrome()
	try:
		driver = webdriver.Chrome(ChromeDriverManager().install())
		driver.implicitly_wait(10)
		driver.maximize_window()		
		driver.get(const.TLA_YOUTUBE_LINK_SEARCH + ans)
		driver.find_element_by_id(const.TLA_YOUTUBE_FIRST_VIDEO).click()
		time.sleep(10)
	except:
		result = data_json["TLA_BOT_YOUTUBE_NOT_FOUND"]
		logging.error(result)
		utils.speak(result, lang)

def googling(query, lang):
	"""Looking for information on Google

	Args:
		query ([string]): [The keyword which will be used for searching in Google]
		lang ([string]): [natural language]
		'en' : english
		'vi' : vietnamese
		'ja' : japanese			
	"""
	query = query.replace(data_json["TLA_LOOKING_FOR"], const.TLA_OUTPUT_EMPTY_STR)
	utils.speak(data_json["TLA_BOT_GOOGLE_SEARCHING"], lang)
	#driver = webdriver.Chrome()
	try:
		driver = webdriver.Chrome(ChromeDriverManager().install())
		driver.implicitly_wait(10)
		driver.maximize_window()
		driver.get(const.TLA_GOOGLE_LINK)
		driver.find_element_by_name(const.TLA_GOOGLE_LINK).send_keys(query)
		driver.find_element_by_name(const.TLA_GOOGLE_SEARCH_BTN).click()
		time.sleep(5)
		driver.quit()
	except:
		result = data_json["TLA_BOT_YOUTUBE_NOT_FOUND"]
		logging.error(result)
		utils.speak(result, lang)		

def resp_heal(lang):
	"""Response relating health

	Args:
		lang ([string]): [natural language]
		'en' : english
		'vi' : vietnamese
		'ja' : japanese			
	"""
	utils.speak(data_json["TLA_BOT_RESP_HEALTH"], lang)
	ans = utils.hear(lang)
	print(const.TLA_YOU_RESP + ans)
	blob = TextBlob(ans)
	if blob.polarity > 0:
		utils.speak(data_json["TLA_YOU_RESP_HEALTH_GOOD"], lang)
	else:
		utils.speak(data_json["TLA_YOU_RESP_HEALTH_BAD"], lang)

def show_date_time(query, lang):
	"""Show date time

	Args:
		query ([string]): [The sentence which including 'time' or 'date']
		lang ([string]): [natural language]
		'en' : english
		'vi' : vietnamese
		'ja' : japanese			
	"""
	if data_json["TLA_TIME"] in query:
		utils.speak(data_json["TLA_BOT_RESP_TIME"] % (now.hour, now.minute), lang)
	elif data_json["TLA_DATE"] in query:
		utils.speak(data_json["TLA_BOT_RESP_DATE"].format(day=now.day, month=now.month, year=now.year), lang)

def lock_pc(lang):
	"""Lock PC

	Args:
		lang ([string]): [natural language]
		'en' : english
		'vi' : vietnamese
		'ja' : japanese	
	"""
	utils.speak(data_json["TLA_BOT_LOCK_PC"], lang)
	ctypes.windll.user32.LockWorkStation()

def show_weather(lang):
	"""Show weather

	Args:
		lang ([string]): [natural language]
		'en' : english
		'vi' : vietnamese
		'ja' : japanese	
	"""
	utils.speak(data_json["TLA_WEATHER_CITY"], lang)
	city = utils.hear(lang)
	print(city)
	logging.info(city)
	try:
		call_url = const.TLA_WEATHER_URL \
					+ const.TLA_WEATHER_API_ID \
					+ setting.TLA_API_KEY_WEATHER \
					+ const.TLA_WEATHER_Q \
					+ city \
					+ const.TLA_WEATHER_UNIT
		resp = requests.get(call_url)
		data_weather = resp.json()
		if data_weather[const.TLA_WEATHER_CODE] != const.TLA_WEATHER_404:
			nhietDo = data_weather[const.TLA_WEATHER_MAIN][const.TLA_WEATHER_TEMP]
			doAm = data_weather[const.TLA_WEATHER_MAIN][const.TLA_WEATHER_HUMIDITY]
			moTa = data_weather[const.TLA_WEATHER_WEATHER][0][const.TLA_WEATHER_DESCRIPTION]
			moTa = utils.translate(moTa, lang)
			content = data_json["TLA_WEATHER_MSG"].format(query=city, temp=nhietDo, humidity=doAm, description=moTa)
			print(content)
			logging.info(content)
			utils.speak(content, lang)
		else:
			content = data_json["TLA_WEATHER_NOT_FOUND"]
			logging.error(content)
			utils.speak(content, lang)
	except :
		content = data_json["TLA_WEATHER_NOT_FOUND"]
		logging.error(content)
		utils.speak(content, lang)


def shutdown_pc(lang):
	"""Shutdown PC

	Args:
		lang ([string]): [natural language]
		'en' : english
		'vi' : vietnamese
		'ja' : japanese	
	"""
	utils.speak(data_json["TLA_CONFIRM_SHUTDOWN_PC"], lang)
	confirm = utils.hear(lang)
	if data_json["TLA_YOU_CONFIRM1"] in confirm \
		or data_json["TLA_YOU_CONFIRM2"] in confirm \
		or data_json["TLA_YOU_CONFIRM3"] in confirm:
		utils.speak(data_json["TLA_BOT_SHUTDOWN_PC"], lang)
		os.system(const.TLA_SHUTDOWN_PC_BY_SECONDS)

def write_sth(lang):
	"""Write something

	Args:
		lang ([string]): [natural language]
		'en' : english
		'vi' : vietnamese
		'ja' : japanese	
	"""
	utils.speak(data_json["TLA_ASK_WRITE"], lang)
	note = utils.hear(lang)
	try:
		file = open(const.TLA_OUTPUT_NOTE, const.TLA_WRITE_ONLY, encoding=setting.TLA_UTF8)
		file.write(note)
		file.close()
		utils.speak(data_json["TLA_CONFIRM_AF_WROTE"], lang)
		confirm = utils.hear(lang)
		if data_json["TLA_YOU_CONFIRM1"] in confirm or data_json["TLA_YOU_CONFIRM2"] in confirm or data_json["TLA_YOU_CONFIRM3"] in confirm:
			file2 = open(const.TLA_OUTPUT_NOTE, const.TLA_WRITE_AND_READ, encoding=setting.TLA_UTF8)
			content = file2.read()
			utils.speak(content, lang)
			file2.close()
	except Exception as err_write:
		logging.error(err_write)

def get_lang(ix):
	"""Get lang and choose json file depending choson lang

	Args:
		ix ([integer]): [index of natural lang]
		'en' : 0
		'vi' : 2
		'ja' : 1		

	Returns:
		[string]: [natural lang]
	"""
	lang = None
	if ix == 0:
		lang = setting.TLA_ENG
	elif ix == 1:
		lang = setting.TLA_JP
	else:
		lang = setting.TLA_VN

	f = open (f"lang\\{lang}.json", encoding=setting.TLA_UTF8)
	global data_json
	data_json = json.load(f)

	return lang

def bot(ix=0):
	"""Bot actions

	Args:
		ix (int, optional): [0: english,  1: japanese,  2: vietnamese]. Defaults is english(index = 0)
	"""
	utils.clear_promp()
	lang = get_lang(ix)

	greeting(lang)
	while True:
		query = utils.hear(lang).lower()
		if data_json["TLA_WHO"] in query or data_json["TLA_WHAT"] in query or data_json["TLA_WHERE"] in query:
			find_in_wiki(query, lang)
		elif data_json["TLA_MUSIC"] in query:
			play_music(lang)
		elif data_json["TLA_LOOKING_FOR"] in query:
			googling(query, lang)
		elif data_json["TLA_HEALTH1"] in query or data_json["TLA_HEALTH2"] in query or data_json["TLA_HEALTH3"] in query or data_json["TLA_HEALTH4"] in query:
			resp_heal(lang)
		elif data_json["TLA_TIME"] in query or data_json["TLA_DATE"] in query:
			show_date_time(query, lang)
		elif data_json["TLA_WEATHER"] in query:
			show_weather(lang)
		elif data_json["TLA_YOU_ASK_NAME"] in query:
			utils.speak(data_json["TLA_BOT_RESP_NAME"], lang)
		elif data_json["TLA_LOCK"] in query:
			lock_pc(lang)
		elif data_json["TLA_SHUTDOWN"] in query:
			shutdown_pc(lang)
		elif data_json["TLA_WRITE"] in query:
			write_sth(lang)
		elif data_json["TLA_BYE1"] in query or data_json["TLA_BYE2"] in query:
			utils.speak(data_json["TLA_BOT_RESP_BYE"], lang)
			break
		elif query == data_json["TLA_BOT_MIC_NG"]:
			break
		elif 'tiếng nhật' in query or 'japanese' in query or '日本語' in query:
			lang = get_lang(1)
			utils.speak(data_json["TLA_BOT_CHANGE_LANG_OK"], lang)
		elif 'tiếng anh' in query or 'english' in query or '英語' in query:
			lang = get_lang(0)
			utils.speak(data_json["TLA_BOT_CHANGE_LANG_OK"], lang)
		elif 'tiếng việt' in query or 'vietnamese' in query or 'ベトナム語' in query:
			lang = get_lang(2)
			utils.speak(data_json["TLA_BOT_CHANGE_LANG_OK"], lang)
		else:
			utils.speak(data_json["TLA_BOT_RESP_OTHER"], lang)