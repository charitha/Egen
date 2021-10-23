
''' generator class of paragraph based on 
    templates given '''
import os
import re
import string
import docManipulation as dm

class Tree(object):

	def __init__(self):
		self.left = None
		self.right = None
		self.data = None

	def createTree(self,left,data,right):
		''' Creation of tree '''
		self.left = left
		self.right = right
		self.data = data
		
	def inorderTraverse(self,sentList=[]):
		''' Inorder Traversal of the tree '''
		
		if self.left != None: 
			self.left.inorderTraverse(sentList)
		if self.data !=None:
			sentList.append( self.data )
		if self.right != None  :
			self.right.inorderTraverse(sentList)
	
	def replaceNode(self,data):
		if self.data !=None :
			self.data = data
		
		 
		

class TemplateToTree:
	
	def __init__(self):
		self.topic = ""
		self.condition = ""
		self.syntacticTree = Tree()
	
	def readTemplateFile(self):
		fi = open('templates/template.txt','r')
		data = fi.read()
		data = str(data)
		grm = data.split('<eol>')
		
		while grm.count('') > 0:
			try:
				grm.remove('')
			except ValueError:
				pass
		return grm

	def removeStopList(self,listItem,listItemPurged):
		''' Remove listItemPurged from listItem '''
		return list(set(listItem)-set(listItemPurged))

	def buildTree(self,topic='Defination',condition='cond1'):
		
		''' Build the template tree '''
		
		grm = self.readTemplateFile()		
	
		self.topic = topic
		self.condition = condition

		for ge in grm :
			gelist = ge.split(':')
			if gelist[1] == topic :
				sent = gelist[2].split('\n')
				indices = ['>','']
				sent = self.removeStopList(sent,indices)
				sentIndexSelected = int(re.findall('\d+',condition)[0])-1
				sentString = sent[sentIndexSelected]
				sentString = sentString.split('//')
				
				nodeLeft = Tree()
				nodeLeft.createTree(None,sentString[1],None)
				nodeRight = Tree()
				nodeRight.createTree(None,sentString[3],None)


				self.syntacticTree.createTree(nodeLeft,sentString[2],nodeRight)

	def generateSentence(self) :
				sentList=[]
				self.syntacticTree.inorderTraverse(sentList)
				return ' '.join(sentList)
				
#obj = TemplateToTree()
#obj.buildTree()
	

class generator:
	def generate (self,allTopics,allTemplates):
		topicFinished = False 
		
		docManipulationObj = dm.docManipulation('Defination')
		docManipulationObj.docToSentList()
		sentenceList=docManipulationObj.docListOfList()

		syl = ['Mobile System']
		for topic in allTopics:	
		    for Sent in sentenceList:				
			templateSelected = TemplateToTree()
			templateSelected.buildTree(topic)
			templateSelected.generateSentence()
			
			
			if templateSelected.syntacticTree.left.data == '$hsent':
				templateSelected.syntacticTree.left.replaceNode(syl[0])				
			if templateSelected.syntacticTree.right.data == '$sent':
				templateSelected.syntacticTree.right.replaceNode(' '.join(Sent))
			print templateSelected.generateSentence()



obj = generator()
obj.generate(['Defination'],['Definition','Listing'])



			
		
	

