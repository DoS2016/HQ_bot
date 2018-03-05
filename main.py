from lxml import html
import requests
from bs4 import BeautifulSoup as soup
import pytesseract
import pyscreenshot as ImageGrab
from PIL import Image
from PIL import ImageEnhance
import os
import time

def search(question, answers):
	page = requests.get("https://www.ask.com/web?q=" + question)
	page2 = requests.get("https://www.quora.com/search?q=" + question)
	#tree = html.fromstring(page.content)
	count = 0

	page_soup = soup(page.text, 'html.parser')
	page_soup2 = soup(page2.text, 'html.parser')
	file = open("testfile.txt", "w") 

	text_results = page_soup.find_all(class_ = "PartialSearchResults-item-abstract")
	text_results2 = page_soup2.find_all(class_ = "qtext_para")
	for i in range(len(text_results)):
		text_results[i] = text_results[i].text
		text_results[i] = text_results[i].replace("\n", '').lower()
		file.write(text_results[i].encode("ascii", errors = "ignore").decode())
	file.close()
	file = open("testfile.txt", "a") 

	for i in range(len(text_results2)):
		text_results2[i] = text_results2[i].text
		text_results2[i] = text_results2[i].replace("\n", '').lower()
		file.write(text_results2[i].encode("ascii", errors = "ignore").decode())

	file.close()

	final_count = [0,0,0]
	for i in range(len(answers)):
		file = open("testfile.txt", "r")
		count = file.read()
		print(answers[i].lower())
		special_count = count.count(answers[i].lower().replace("vv", 'w').replace("m m", 'mm').replace(',', ''))
		print(special_count)
		file.close()
		final_count[i] = special_count

	print(final_count)
	return final_count

def answer1(num_answers):
	max1 = 0

	for i in range(len(num_answers)):
		if max1 < num_answers[i]:
			max1 = num_answers[i]
	return num_answers.index(max1)

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

	print(lowerQ)
	print(answers)

	return lowerQ, answers
def result():
	pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'	#image = Image.open('testimages/1.png')
	image = ImageGrab.grab(bbox=(350,120,900,550))
	#image = image.resize((1000,1000))

	Sharpness = ImageEnhance.Color(image)
	image = Sharpness.enhance(0)
	Brightness = ImageEnhance.Contrast(image)
	image = Brightness.enhance(1.5)
	Contrast = ImageEnhance.Contrast(image)
	image = Contrast.enhance(2)
	image.save('1.png')
	# Raw output
	ocr_output = pytesseract.image_to_string(image)
	ocr_output = ocr_output.encode("ascii", errors="ignore").decode()
	answers = []
	# Question/Answer Parsed
	question, answers = retrieve_q_and_a(ocr_output)
	question = question + " " + answers[0] + " " + answers[1] + " " + answers[2] 
	question = question.replace("\"", '')
	question = question.replace("!", '')
	question = question.replace(",", '')
	question = question.replace(".", '')


	print(question)
	print(answers[answer1(search(question, answers))])
if __name__ == "__main__":
	result()
