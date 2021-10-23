import sys 
import urllib2
import string
import re
import os
import syllabus as sy
import docManipulation as dm 
import textGeneration as tg
import centeringTheory as ct
import sentenceOrdering as so
from bs4 import BeautifulSoup
import documentSimilarity as dso
from boilerpipe.extract import Extractor



class InformationRetreival:
	
	def getTopic(self,sylObj,topic,bookType):
		 if (len(sylObj.subtopics)==0):
			query ="";
			topic.insert(0,sylObj.topicname)
			query = ' and '.join(topic)
			if (bookType == "concise"):
				self.retreiveConcise(query,sylObj)
			else:
				self.retreive(query,sylObj)
			topic.pop(0)
		 else:				
			topic.insert(0,sylObj.topicname)
			for obj in sylObj.subtopics:	
				self.getTopic(obj,topic,bookType)
			topic.pop(0)
			
			
	def getLeafTopics(self,sylObj,listOfTopics):
		if(len(sylObj.subtopics) == 0):
			listOfTopics.append(sylObj);
		else:
			for obj in sylObj.subtopics:
				self.getLeafTopics(obj,listOfTopics)			 
	

	def retreiveConcise(self,topic,sylObj):
                sys.path.append("./bs4")
                fo=open("static/url.txt",'w')


                line=topic
               	line=line.replace(" ","+")
                line = line.rstrip('\n')
                Dopener = urllib2.build_opener()
                opener.addheaders = [('User-agent','Mozilla/5.0')]

		if (line != ''):

    			for start in range(0,1):
                       		url = "http://www.google.com/search?q=define:"+line+"+site:wikipedia.org&start="+str(start*1)
                                page = opener.open(url)
                                soup = BeautifulSoup(page)

                              	for cite in soup.find_all('cite'):
                                        cite = ''.join(cite.find_all(text=True))
                                        cite = cite.rstrip('\n')
					cite = ''.join(i for i in cite if ord(i)<128)
					if cite not in sylObj.urls:
						sylObj.urls.append(cite)

                                        fo.write(cite)
                                        fo.write('\n')

		fo.close()
	
	def retreive(self,topic,sylObj):
                sys.path.append("./bs4")
                fo=open("static/url.txt",'w')


                line=topic
               	line=line.replace(" ","+")
                line = line.rstrip('\n')
                opener = urllib2.build_opener()
                opener.addheaders = [('User-agent','Mozilla/5.0')]

		if (line != ''):

    			for start in range(0,1):
                       		url = "http://www.google.com/search?q="+line+"+site:en.wikipedia.org+-shops+-pdf+-jpg+-svg+-products+-hospitals+-entertainment+-youtube+-theatres+-movies&start="+str(start*10)
                                page = opener.open(url)
                                soup = BeautifulSoup(page)

                              	for cite in soup.find_all('cite'):
                                        cite = ''.join(cite.find_all(text=True))
                                        cite = cite.rstrip('\n')
					cite = ''.join(i for i in cite if ord(i)<128)
					if cite not in sylObj.urls:
						sylObj.urls.append(cite)
                                        fo.write(cite)
                                        fo.write('\n')

					
			for start in range(0,1):
				url = "http://www.google.com/search?q="+line+"+-shops+-pdf+-products+-hospitals+-entertainment+-svg+-jpg+-youtube+-theatres+-movies&start="+str(start*10)
                                page = opener.open(url)
                                soup = BeautifulSoup(page)

                                for cite in soup.find_all('cite'):
                                        cite = ''.join(cite.find_all(text=True))
                                        cite = cite.rstrip('\n')
					cite = ''.join(i for i in cite if ord(i)<128)	
					if cite not in sylObj.urls:
						sylObj.urls.append(cite)
                                        fo.write(line+":"+cite)
                                        fo.write('\n')

			
		fo.close()
	
	def downloadImg(self,url,topic):
	     	try:	
			opener = urllib2.build_opener()
			if "http" not in url:
				url = "http://"+url
			opener.addheaders = [('User-agent', 'Mozilla/5.0')]
			soup = BeautifulSoup(opener.open(url))
			imgs = soup.find_all("img")
			for img in imgs:
				if (img.has_attr('height') and img.has_attr('width')):
			 		if "px" not in img['height'] and "px" not in img['width']:
   						if int(img['height']) > 100 and int(img['width']) > 200 :
       							 if ("http" in img['src']):
                						topic.images.append(img['src'])
        			 	 	 	 else:
                						topic.images.append("http:"+img['src'])

		except:
			pass
	   
	
	def printSylObject(self,sylObj):
		listOfTopics=[]
		self.getLeafTopics(sylObj,listOfTopics)
		for topic in listOfTopics:
			print "-------------------------------------------------------------------------------\n"
			print "topicname:",topic.topicname,"\n"
			print "topicurls:",topic.urls,"\n"
			print "length of urls:",len(topic.urls),"\n"
			print "length of topicDocs:",len(topic.docs),"\n"
			print "topicimages:",topic.images,"\n"	
			print "-----------------------------------------------------------------------------\n"
	
	def topDocuments(self,sylObj):
		listOfTopics=[]
		ctObj = ct.CenteringTheory()
		self.getLeafTopics(sylObj,listOfTopics)

		for topic in listOfTopics:
			cohList = []
			irrelevant = []
			for doc in topic.docs:
				if ctObj.isValid(doc) == "TRUE":
					val = ctObj.parse(doc)
					cohList.append(val)
				else:
					irrelevant.append(doc)
					
			for doc in irrelevant:
				index = topic.docs.index(doc)
				topic.docs.pop(index)
				topic.urls.pop(index)
				
	
			self.removeIncoherent(topic,cohList)
			self.sortLists(topic,cohList)
			if len(topic.urls)>3:
				topic.docs = topic.docs[:3]
				topic.urls = topic.urls[:3]

	def removeIncoherent(self,topic,cohList):
		irrelevant = []
		for i in cohList:
			if i < 0.01:
				index = cohList.index(i)
				irrelevant.append(index)

		for i in irrelevant:
			topic.docs.pop(i)
			topic.urls.pop(i)
			cohList.pop(i)


	def sortLists(self,topic,cohList):
		newDocs = []
		newUrls = []	 	
		for i in range(0,len(cohList)):
			index = self.maxIndex(cohList)
			newDocs.append(topic.docs[index])
			newUrls.append(topic.urls[index])
			cohList[index]=-1 
		topic.docs = newDocs
		topic.urls = newUrls
				
				
	def maxIndex(self,clist):
		maxi = -1
		for i in clist:
			if i > maxi:
				maxi=i	
				index = clist.index(i)
		return index
	
	def generateCoherentText(self,sylObj):
		listOfTopics=[]
		soObj = so.SentenceOrdering()
		self.getLeafTopics(sylObj,listOfTopics)

		for topic in listOfTopics:
			topic.finalText =soObj.documentMerge(topic.docs)
			print "TOPIC : ",topic.topicname,"\n\n\n\n\n\n" ,topic.finalText,"\n\n\n"


	def infoRetreive(self,bookType):
		sylObj = sy.Syllabus()
		sylObj = sylObj.makeObject()
		self.getTopic(sylObj,[],bookType)
		print "Fetched all urls for topics\n\n"
		self.printSylObject(sylObj)
		self.urlClustering(sylObj)
		print "URL Clustering completed\n\n"
		self.printSylObject(sylObj)
		self.downloadDocuments(sylObj)
		print "Downloaded the documents\n\n"
		self.printSylObject(sylObj)
		self.performDocumentClustering(sylObj)
		print "Performed document clustering\n\n"
		self.printSylObject(sylObj)
		self.topDocuments(sylObj)
		print "Performed Sorting Documents Based On Coherence Value\n\n"
		self.printSylObject(sylObj)
		self.downloadImages(sylObj)
		print "Downloaded images\n\n"
		self.printSylObject(sylObj)
		self.generateCoherentText(sylObj)
		self.createGUI(sylObj)
		
		print "Done !!!! :)\n\n\n"""
	
	def createGUI(self,sylObj):
		listOfTopics = []		
		self.getLeafTopics(sylObj,listOfTopics)	
		dmObj = dm.docManipulation("")
		dmObj.docToXml(listOfTopics)

	def removeSimilarSent(self,sylObj):
		listOfTopics=[]	
		self.getLeafTopics(sylObj,listOfTopics)
		tgObj = tg.TextGeneration()
		
		for topic in listOfTopics:
			tgObj.getAllSentences(topic.docs)
	
	def performDocumentClustering(self,sylObj):
		listOfTopics=[]
		dsObj = dso.DocumentSimilarity()
		self.getLeafTopics(sylObj,listOfTopics)
		for topic in listOfTopics:
			dsObj.getRelevantDocuments(topic)

	def addToRankList(self,rankListOfUrls,listOfUrls):
		for i in range(0,len(listOfUrls)):
			for j in range(0,len(rankListOfUrls)):
				rankstup = rankListOfUrls[j]			
				if(rankstup[1] == listOfUrls[i]):
					if(rankstup[0]<=i):
						listOfUrls[i] = ""
					elif(rankstup[0]>i):
						rankstup[1]=""
				
						
		for i in range(0,len(listOfUrls)):
			if(listOfUrls[i]!=""):
				newTup = [i,listOfUrls[i]]
				rankListOfUrls.append(newTup)
				
	def urlClustering(self,sylObj):
		rankListOfUrls = []
		listOfTopics = []
		self.getLeafTopics(sylObj,listOfTopics)
		for topic in listOfTopics:
			self.addToRankList(rankListOfUrls,topic.urls)
		topic_id=-1
		prev=100
		for value in rankListOfUrls:
			if (value[0]<=prev):		
				topic_id=topic_id+1
				listOfTopics[topic_id].urls=[]
			if (value[1]!=""):
				listOfTopics[topic_id].urls.append(value[1])

			prev = value[0]

	def downloadDocuments(self,sylObj):
		listOfTopics = []
		self.getLeafTopics(sylObj,listOfTopics)
		for topic in listOfTopics:
			irrelevant=[]
			for my_url in topic.urls:
				taken = 0
				
				try:
					
					extr = Extractor(extractor='ArticleSentencesExtractor',url="http://"+my_url)
					text = extr.getText()
					if text != "" and text != " " and len(text) > 200:
						topic.docs.append(text)
						taken = 1
				except:
					pass

				if taken == 0:
					irrelevant.append(my_url)

		for url in irrelevant:
			index = topic.urls.index(url)
			topic.urls.pop(index)
			 
							
	def downloadImages(self,sylObj):
		listOfTopics = []
		self.getLeafTopics(sylObj,listOfTopics)
		for topic in listOfTopics:
			for url in topic.urls:
				self.downloadImg(url,topic)
					


infobj = InformationRetreival()
infobj.infoRetreive("not")
