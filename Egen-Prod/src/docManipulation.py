#! /usr/bin/env python
''' Major file functions and sentence formations '''


import nltk
import os
import glob
import re


class docManipulation:
	
	def __init__(self,syllabusTopic):
		self.syllabusTopic = syllabusTopic
		self.sentList = []
		self.sentListOfList = []

	def docToSentList(self,data):
		sentenceList = []
		data = data.split('.')
		for sent in data :
                        sent=sent.replace('\n',' ')
			sent=re.sub('\W+',' ',sent)
			sentenceList.append(sent)
		self.sentList = sentenceList
		return sentenceList
		

		
	def rmvSentRepetition(self) :
		'''Repeation of sentences  remove them'''
		self.sentList = list(set(self.sentList))
		
	
	def docListOfList(self) :
		sentenceListOfList = []
		for sent in self.sentList :
			templist = sent.split()
			if templist == [] :
				continue
			templist.append('.')
			if templist not in sentenceListOfList:
				sentenceListOfList.append(templist)
		self.sentListOfList = sentenceListOfList 
		return self.sentListOfList
		
	def docToXml(self,listOfTopics):
		writefd = open("textBook.xml","w")
		xmlSent = "<?xml version='1.0' encoding='utf-8'?>"
		xmlSent += "<TEXTBOOK>"
		for topic in listOfTopics:
			xmlSent += "<TOPIC>"
			xmlSent += "<TITLE>"+topic.topicname+"</TITLE>"
			xmlSent += "<Definition>"+topic.finalText+"</Definition>"
			xmlSent += "</TOPIC>"
		xmlSent += "</TEXTBOOK>"
		writefd.write(xmlSent+"\n")
		writefd.close()
		os.system('mv textBook.xml static/textBook.xml')

#obj = docManipulation('Defination')
#obj.docToSentList()
#obj.docListOfList()
#obj.docToXml('static/conceptNotes')

