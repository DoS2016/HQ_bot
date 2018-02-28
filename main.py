from PIL import *
from google import google
import Image
import ImageGrab
import ImageEnhance
import pytesseract
import webbrowser
from googleapiclient.discovery import build
import sys
from datetime import datetime
import re
import os, msvcrt

# Google Custom Search
g_cse_api_key =  'AIzaSyDjAMskWfeIZmqgKhsJl0yOpnQgnhEt1Qo'
g_cse_id = '000114468029627290942:whczg5ooff8'


def notify(title, text):
    print(title, text)

def google_search(query, start):
	service = build("customsearch", "v1", developerKey=g_cse_api_key)
	res = service.cse().list(q=query, cx=g_cse_id, start=start).execute()
	return res

def retrieve_q_and_a(text):
	question_answers = text.split('?')
	if len(question_answers) > 2:
		corrString = ''
		for x in range(len(question_answers) - 1):
			corrString += question_answers[x]
		question_answers = [corrString, question_answers[len(question_answers) - 1]]
	question = question_answers[0].replace('\n', ' ')
	answers = question_answers[1].split('\n')
	answers = [ans.strip() for ans in answers]
	answers = [x for x in answers if x != '']
	lowerQ = question.lower()
	query = lowerQ
	stopwords = ['what','who','whom','a','at','he','she','sometimes','items','these','to','likely',' most','than','which','places','more','sold','copies']
	querywords = query.split()

	resultwords  = [word for word in querywords if word.lower() not in stopwords]
	formatedQ = ' '.join(resultwords)


	print(formatedQ)
	print(answers)
	return formatedQ, answers

def naive_approach():
	search_results = google.search("This is my query")
	search_results2 = google.search("This is my query")

	print search_results
	print search_results2

# Google Question and count number of each result
def metric1Func(question, answers):
	met1 = [0, 0, 0]
	met1Multi = 0
	res = google_search(question, None)
	items = str(res['items']).lower()



	met1[0] = items.count(answers[0].lower()) + 1
	met1[1] = items.count(answers[1].lower()) + 1
	met1[2] = items.count(answers[2].lower()) + 1
	return met1

# Google Question and each specific Answer and count total results
def metric2Func(question, answers):
	met2 = [0, 0, 0]
	res0 = google_search(question + ' "' + answers[0] + '"', None)
	res1 = google_search(question + ' "' + answers[1]  + '"' , None)
	res2 = google_search(question + ' "' + answers[2]  + '"', None)
	
	return [int(res0['searchInformation']['totalResults']) + 1, int(res1['searchInformation']['totalResults']) + 1, int(res2['searchInformation']['totalResults']) + 1]

def predict(metric1, metric2, answers):
	#max1 = metric1[0]

	answer = [0, 0, 0]

	max1 = answer[0]


	for x in range(0, 3):
		if metric1[x] == 1:
			metric1[x] = 0.5
			answer[x] = (metric1[x])*metric2[x]
		else:
			answer[x] = (metric1[x]**1.8)*(metric2[x]*1.2)


	for x in range(0, 3):
		if answer[x] > max1:
			max1 = answer[x]
	print(answer)
	return answers[answer.index(max1)]
	

def q_analysis():
	startTime = datetime.now()
	#image = Image.open('testimages/1.png')
	image = ImageGrab.grab(bbox=(650,200,1300,750))
	#image = image.resize((1000,1000))
	Contrast = ImageEnhance.Contrast(image)
	image = Contrast.enhance(3)
	image.save('testimages/1.png')
	# Raw output
	ocr_output = pytesseract.image_to_string(image)
	ocr_output = ocr_output.encode("ascii", errors="ignore").decode()

	# Question/Answer Parsed
	question, answers = retrieve_q_and_a(ocr_output)
	question = question.replace("\"", '')

	#naive_approach(question)
	met1 = metric1Func(question, answers)
	met2 = metric2Func(question, answers)
	print met1
	print met2
	notify(question, predict(met1, met2, answers))
	print(datetime.now() - startTime)

fd = msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
q_analysis()

