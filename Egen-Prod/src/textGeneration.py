import nltk
import documentSimilarity as ds
import re

class TextGeneration:
	
	def getAllSentences(self,sylTopic):
		for doc in sylTopic:
			sentenceList=[]
			data=doc.split(".")
			for sent in data:
				sent = sent.replace('\n',' ')
				sent = re.sub('\W+',' ',sent)
				sentenceList.append(sent)
			self.removeEmptyString(sentenceList)
			if len(sent)>1:
				self.removeSimilarSentences(sentenceList)
				
				doc = '.'.join(sentenceList)

	def removeEmptyString(self,sentList):
			for sent in sentList:
				if (sent == ''):
					sentList.remove(sent)

	def removeSimilarSentences(self,sentList):
		obj = ds.DocumentSimilarity()
		obj.getRelevantSentences(sentList)

	
	def demo(self):
		obj = TextGeneration()
		docList=["This book takes an empirical approach to language processing.Language processing done using emperical approach.NLP involves linguistic computations.NLP involves linguistic computations.Cloud infrastructure came not yes."]
		obj.getAllSentences(docList)
		

#obj = TextGeneration()
#obj.demo()	

#obj.removeUngrammaticalSentences(["OverView Content Introduction","This book takes an empirical approach to language processing"])
