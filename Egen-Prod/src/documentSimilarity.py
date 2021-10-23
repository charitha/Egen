"""take out very similar documents"""


import glob
import os
import nltk
from nltk.util import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import centeringTheory as ct
from sklearn.feature_extraction.text import TfidfVectorizer
CURRENT_DIR="."
#import mylogger

class DocumentSimilarity:
	
        def __init__(self):
		self.documents = []
		self.relevant= []
		self.irrelevant = []
		self.vocabulary = []
		self.n_gram_document = {};

	
	def preProcessData(self, sentence):
		''' Remove common words ,stop words,punctuation ''' 
		tokenizer = RegexpTokenizer(r'\w+')
		sentence = sentence.lower()
		sentence = tokenizer.tokenize(sentence)
		sentence = [w for w in  sentence if not w in stopwords.words('english')]
		return sentence

	def getRelevantDocuments(self,topic):
		ctObj = ct.CenteringTheory()
		for data in topic.docs:
			data = data.rstrip('\n')
			self.documents.append(data)


		tfidf_vect = TfidfVectorizer(lowercase = True ,strip_accents = 'ascii',analyzer = 'word',ngram_range = (3,3),min_df = 0.1,smooth_idf =True)
		self.documents=topic.docs
		tfidf = tfidf_vect.fit_transform(self.documents)
		pairwise_similarity = tfidf * tfidf.T
		matrix = ((tfidf * tfidf.T).A)
		doc_length = len(self.documents)
		

		for i in range(0,doc_length):
			for j in range(i+1,doc_length):
				if matrix[i][j]>0.3:
					if ctObj.isValid(self.documents[i])=="TRUE":
						val1 = ctObj.parse(self.documents[i])
					else:	
						val1 =-1
						self.irrelevant.append(self.documents[i])

					if ctObj.isValid(self.documents[j])=="TRUE":
						val2 = ctObj.parse(self.documents[j])
					else:
						val2 =-1
						self.irrelevant.append(self.documents[j])


					if val1 >= 0 and val2 >= 0:
						if val1 > val2:
							if self.documents[j] not in self.irrelevant:
                                         			self.irrelevant.append(self.documents[j])
						elif val1 < val2:
							if self.documents[i] not in self.irrelevant:
						 		self.irrelevant.append(self.documents[i])
						else:
							len1 = len(self.documents[i])
							len2 = len(self.documents[j])
						
							if (len1 >= len2):
								if self.documents[i] not in self.irrelevant:
									self.irrelevant.append(self.documents[i])
							else:		
								if self.documents[j] not in self.irrelevant:
									self.irrelevant.append(self.documents[j])


		for data in self.documents:
			if data not in self.irrelevant:
				self.relevant.append(data)


		for data in self.documents:
			if data in self.irrelevant:
				index = topic.docs.index(data)
				topic.urls.pop(index)
				topic.docs.pop(index)

	def getRelevantSentences(self,sentList):
		
		for data in sentList:
                        data = data.rstrip('\n')
                        self.documents.append(data)

		tfidf_vect = TfidfVectorizer(lowercase = True ,strip_accents = 'ascii',analyzer = 'word',ngram_range = (3,3),min_df = 0.1,smooth_idf =True)
		self.documents=sentList
		tfidf = tfidf_vect.fit_transform(self.documents)
		pairwise_similarity = tfidf * tfidf.T
		matrix = ((tfidf * tfidf.T).A)
		doc_length = len(self.documents)
		

		for i in range(0,doc_length):
			for j in range(i+1,doc_length):
				if matrix[i][j]>0.5:
					 if len(self.documents[i]) >= len(self.documents[j]):
                                                docum = self.documents[j]
                                         else:
                                                docum = self.documents[i]
                                         if docum not in self.irrelevant:
                                                self.irrelevant.append(docum)

		for data in self.documents:
			if data not in self.irrelevant:
				self.relevant.append(data)

		for data in sentList:
			if data in self.irrelevant and data not in self.relevant:
				index = sentList.index(data)
                                sentList.remove(data)



 
	def preProcessData(self, sentence):
		''' Remove common words ,stop words,punctuation ''' 
		tokenizer = RegexpTokenizer(r'\w+')
		sentence = sentence.lower()
		sentence = tokenizer.tokenize(sentence)
		sentence = [w for w in  sentence if not w in stopwords.words('english')]
		return sentence
		
	def ngrams(self, sentence ,n):
		''' split document sentence into n-grams '''
		sentence = self.preProcessData(sentence)
		outputSentence = ngrams(sentence,n)
		return outputSentence

	
	def printDocument(self):
		text_files=self.getRelevantDocuments()
		for f in text_files:
			fil = open(f,'r')
			data = fil.read()
			data = str(data)
			data = data.rstrip('\n')
			fil.close()
			print data




#obj = DocumentSimilarity()
#obj.readDocuments()
#obj.getRelevantDocuments()

