'''Centering Theory for text coherence '''

from __future__ import division
import os
import nltk
import docManipulation as dm



class CenteringTheory:
	def isValid(self,document):
		newSentList = []
		if document.count(".") <=1:
			return "FALSE"
		else:
			sentList = document.split(".")
			
			for sent in sentList:
				sent.rstrip("\n")
				if sent != "" or sent !=" " or len(sent) > 350:
					newSentList.append(sent+".")

			document = ''.join(newSentList)

			if document.count(".") < 1:	
				return "FALSE"
			else:
				return "TRUE"
	
	def  getNNs(self,sent):
		text = nltk.word_tokenize(sent)
		posTaggedSent = nltk.pos_tag(text)
		listOfNPs =[]
		
		for pts in posTaggedSent:
			partOfSpeech = pts[1]
			if(partOfSpeech == 'NN' or partOfSpeech == 'NNP' or partOfSpeech == 'JJ'):
				listOfNPs.append(pts)
		return listOfNPs
	
	def isValidSentence(self,sentence):
		listOfNPs =self.getNNs(sentence)
		if len(listOfNPs) == 0 :
			isValidSentence = False
		else:
			isValidSentence = True
		return isValidSentence

	def parse(self,document):
		dmObj = dm.docManipulation("")
		sentenceList =	dmObj.docToSentList(document)
		vocabularyList = []
		sentenceList1 = []
		salienceVector = {}
		salienceMax = 0
		entityDiffMatrix = {}
		utterenceList = []
		Wtrans = []
		sentenceTransition = []
		documentCoherence = 0
		
		for sentence in sentenceList :
			wordList = self.getNNs(sentence)
			if wordList != []:
				sentenceList1.append(wordList)
			self.buildVocabularyList(wordList,vocabularyList)
		self.salienceVectorize(salienceVector,0,wordList,vocabularyList)
		
		i = 0
		for wordList in sentenceList1:
			wordList1 = [word[0].lower() for word in wordList]
			utterenceList.append(wordList1)
			i += 1
			self.salienceVectorize(salienceVector,i,wordList1)
	
		salienceMax = self.maxSalience(salienceVector)
		entityDiffMatrix = self.entityDifferenceMatrix(salienceVector,salienceMax)
		Wtrans,UiandjNum = self.calculateWeightTransition(utterenceList)
	
		sentenceTransition = self.calculateTransitionInSentence(entityDiffMatrix,Wtrans,UiandjNum)
		'''if sentenceTransition is >0.5 or close implies great transition and less coherence '''
		documentCoherence = self.calculateDocumentCoherence(sentenceTransition)
		return documentCoherence
	
		
	
	def salienceVectorize(self,salienceVector,sentenceNo,wordList = [],vocabularyList = []):
		''' Pass List of single sentences in the document '''
		for word in vocabularyList:
			salienceVector[word] = []
		lenWordList = len(wordList) 
		#print wordList
		#print vocabularyList
		#print salienceVector
		if sentenceNo != 0: 
			for k in salienceVector:
				if any(k == w for w in wordList):
					salienceVector[k].insert(sentenceNo-1,lenWordList - wordList.index(k))	
				else :
					salienceVector[k].insert(sentenceNo-1,0)


	def buildVocabularyList(self,wordList = [],vocabularyList = []):
		''' Pass the word list in different sentences '''
		vocabularyList += ([word[0] for word in wordList if word[0] not in vocabularyList])


	def difference(self,ev1,ev2):
		return abs(ev1-ev2)


	def average(self,ev1,ev2):
		return (ev1+ev2)/2


	def maxSalience(self,salienceVector):
		'''Maximum salience value an entity can achieve within any utterance in text '''
		salienceMaxList = []
		for k in salienceVector:
			salienceMaxList.append(max(salienceVector[k]))
		return max(salienceMaxList)
	
	def entityDifferenceMatrix(self,salienceVector,salienceMax):
		entityDiffMatrix = {}
		for k in salienceVector:
			entityDiffMatrix[k] = []
 			for i in range(0,(len(salienceVector[k])-1)):
				ev1 = salienceVector[k][i]
				ev2 = salienceVector[k][i+1]
				if  ev1 != 0 or ev2 != 0:
					entityDiffMatrix[k].insert(i,2 * self.difference(ev1,ev2) * self.average(ev1,ev2) / (salienceMax ** 2))
				else:
					entityDiffMatrix[k].insert(i,-1)
		return entityDiffMatrix
	
	def calculateWeightTransition(self,utterenceList):
		''' Wtrans = # of entities in Ui realized in Uj/# of distinct entities realized in Ui and Uj'''
		Wtrans = []
		UiandjNum = []
		for i in range(0,len(utterenceList)-1):
			Ui = utterenceList[i]
			Uj = utterenceList[i+1]
			UiinjNum = len([word for word in Ui if word in Uj])
			Uiandj = len(list(set(Ui+Uj)))
			UiandjNum.insert(i,Uiandj)
			Wtrans.insert(i,UiinjNum/Uiandj)
							
		return Wtrans,UiandjNum

	def calculateTransitionInSentence(self,entityDiffMatrix,Wtrans,UiandjNum):
		sentenceTransition = []
		entityTransitionValue = 0 
		transitionValue = 0
		'''Transition(Ui , Uj ) = 1-Wtrans.(1 - Entity Transition Value(ek where k=1 to n )/total # of distinct entities realized in Ui and Uj)'''
		for i in range(0,len(Wtrans)):
			for k in entityDiffMatrix:
				if entityDiffMatrix[k][i] != -1:
					entityTransitionValue += entityDiffMatrix[k][i]
			transitionValue = 1 - Wtrans[i] * (1 - entityTransitionValue/UiandjNum[i])
			sentenceTransition.insert(i,transitionValue)
			entityTransitionValue = 0
			
		return sentenceTransition
				
	def calculateDocumentCoherence(self,sentenceTransition):
		'''Calculate the average of the list values '''
		
		#print sentenceTransition
		documentTransition = sum(sentenceTransition)/len(sentenceTransition)
		
		'''coherence 1-docTransition'''
		#print 1-documentTransition
		return (1 - documentTransition)

	
		
	
				
#obj = centeringTheory()
#print obj.parse()


