# System basic lib
import os
import datetime
import ctypes
import time

# The 3rd party
import gtts
from gtts import gTTS
import wikipedia
import requests
from selenium import webdriver
import chromedriver_binary
from textblob import TextBlob

# My import
import const
import setting
import utils

# chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
now = datetime.datetime.now()

# Say greetings depending time in day
def greeting():
	hour = int(datetime.datetime.now().hour)
	if hour>= 0 and hour<12:
		utils.speak(const.TLA_BOT_MORNING)
	elif hour>= 12 and hour<18:
		utils.speak(const.TLA_BOT_AFTERNOON)
	else:
		utils.speak(const.TLA_BOT_EVENING)  
	utils.speak(const.TLA_BOT_ASK_FOR_HELP)

# Looking for information in Wiki
def find_in_wiki(query):
	utils.speak(const.TLA_BOT_WIKI_FINDING)
	query = query.replace(const.TLA_WHO, const.TLA_OUTPUT_EMPTY_STR)
	query = query.replace(const.TLA_WHAT, const.TLA_OUTPUT_EMPTY_STR)
	query = query.replace(const.TLA_WHERE, const.TLA_OUTPUT_EMPTY_STR)
	wikipedia.set_lang(setting.TLA_VN)
	try:
		results = wikipedia.summary(query, sentences = 3)
		print(query)
		utils.speak(const.TLA_BOT_WIKI_FOUND)
		print("\n" + results)
		utils.speak(results)
	except :
		results = const.TLA_BOT_WIKI_NOT_FOUND
		print(results)
		utils.speak(results)

# Play music using Youtube
def play_music():
	utils.speak(const.TLA_BOT_ASK_MUSIC_NAME)
	ans = utils.hear()
	print(const.TLA_YOU_RESP + ans)
	utils.speak(const.TLA_BOT_PLAY_MUSIC)
	driver = webdriver.Chrome()
	driver.get(const.TLA_YOUTUBE_LINK_SEARCH + ans)
	driver.find_element_by_id(const.TLA_YOUTUBE_FIRST_VIDEO).click()
	time.sleep(10)

# Looking for information on Google
def googling(query):
	query = query.replace(const.TLA_LOOKING_FOR, const.TLA_OUTPUT_EMPTY_STR)
	utils.speak(const.TLA_BOT_GOOGLE_SEARCHING)
	driver = webdriver.Chrome()
	driver.implicitly_wait(10)
	driver.maximize_window()
	driver.get(const.TLA_GOOGLE_LINK)
	driver.find_element_by_name(const.TLA_GOOGLE_SEARCH_BOX).send_keys(query)
	driver.find_element_by_name(const.TLA_GOOGLE_SEARCH_BTN).click()
	time.sleep(5)
	driver.quit()

# Response relating health
def resp_heal():
	utils.speak(const.TLA_BOT_RESP_HEALTH)
	ans = utils.hear()
	print(const.TLA_YOU_RESP + ans)
	blob = TextBlob(ans)
	if blob.polarity > 0:
		utils.speak(const.TLA_YOU_RESP_HEALTH_GOOD)
	else:
		utils.speak(const.TLA_YOU_RESP_HEALTH_BAD)

# Show date time
def show_date_time(query):
	if const.TLA_TIME in query:
		utils.speak(const.TLA_BOT_RESP_TIME % (now.hour, now.minute))
	elif const.TLA_DATE in query:
		utils.speak(const.TLA_BOT_RESP_DATE % (now.day, now.month, now.year))

# Lock PC
def lock_pc():
	utils.speak(const.TLA_BOT_LOCK_PC)
	ctypes.windll.user32.LockWorkStation()

# Show weather
def show_weather(query):
			query = query.replace(const.TLA_WEATHER,const.TLA_OUTPUT_EMPTY_STR)
			query = query.replace(const.TLA_TODAY, const.TLA_OUTPUT_EMPTY_STR)
			print(query)
			try:
				call_url = const.TLA_WEATHER_URL + const.TLA_WEATHER_API_ID + setting.TLA_API_KEY_WEATHER + const.TLA_WEATHER_Q + query + const.TLA_WEATHER_UNIT
				resp = requests.get(call_url)
				data = resp.json()
				if data[const.TLA_WEATHER_CODE] != const.TLA_WEATHER_404:
					nhietDo = data[const.TLA_WEATHER_MAIN][const.TLA_WEATHER_TEMP]
					doAm = data[const.TLA_WEATHER_MAIN][const.TLA_WEATHER_HUMIDITY]
					moTa = data[const.TLA_WEATHER_WEATHER][0][const.TLA_WEATHER_DESCRIPTION]
					moTa = utils.translate(moTa)
					content = const.TLA_WEATHER_MSG.format(query = query, temp = nhietDo, humidity = doAm, description = moTa)
					print(content)
					utils.speak(content)
				else:
					content = const.TLA_WEATHER_NOT_FOUND
					utils.speak(content)
			except :
				content = const.TLA_WEATHER_NOT_FOUND
				utils.speak(content)

# Shutdown PC
def shutdown_pc():
	utils.speak(const.TLA_CONFIRM_SHUTDOWN_PC)
	confirm = utils.hear()
	if const.TLA_YOU_CONFIRM1 in confirm or const.TLA_YOU_CONFIRM2 in confirm or const.TLA_YOU_CONFIRM3 in confirm:
		utils.speak(const.TLA_BOT_SHUTDOWN_PC)
		os.system(const.TLA_SHUTDOWN_PC_BY_SECONDS)

# Write something
def write_sth():
	utils.speak(const.TLA_ASK_WRITE)
	note = utils.hear()
	file = open(const.TLA_OUTPUT_NOTE, const.TLA_WRITE_ONLY, encoding=setting.TLA_UTF8)
	file.write(note)
	file.close()
	utils.speak(const.TLA_CONFIRM_AF_WROTE)
	confirm = utils.hear()
	if const.TLA_YOU_CONFIRM1 in confirm or const.TLA_YOU_CONFIRM2 in confirm or const.TLA_YOU_CONFIRM3 in confirm:
		file2 = open(const.TLA_OUTPUT_NOTE, const.TLA_WRITE_AND_READ, encoding=setting.TLA_UTF8)
		content = file2.read()
		utils.speak(content)
		file2.close()

# Vietnamese Bot
def bot_vnese():
	utils.clear_promp()
	greeting()
	while True:
		query = utils.hear().lower()
		if const.TLA_WHO in query or const.TLA_WHAT in query or const.TLA_WHERE in query:
			find_in_wiki(query)
		elif const.TLA_MUSIC in query:
			play_music()
		elif const.TLA_LOOKING_FOR in query:
			googling(query)
		elif const.TLA_HEALTH1 in query or const.TLA_HEALTH2 in query or const.TLA_HEALTH3 in query or const.TLA_HEALTH4 in query:
			resp_heal()
		elif const.TLA_TIME in query or const.TLA_DATE in query:
			show_date_time(query)
		elif const.TLA_WEATHER in query and const.TLA_TODAY in query:
			show_weather(query)
		elif const.TLA_YOU_ASK_NAME in query:
			utils.speak(const.TLA_BOT_RESP_NAME)
		elif const.TLA_LOCK in query:
			lock_pc()
		elif const.TLA_SHUTDOWN in query:
			shutdown_pc()
		elif const.TLA_WRITE in query:
			write_sth()
		elif const.TLA_BYE1 in query or const.TLA_BYE2 in query:
			utils.speak(const.TLA_BOT_RESP_BYE)
			break
		elif query == const.TLA_BOT_MIC_NG:
			break
		else:
			utils.speak(const.TLA_BOT_RESP_OTHER)


#bot_vnese()