from numpy import zeros
from scipy.linalg import svd
from math import log
from numpy import asarray, sum
from nltk.corpus import stopwords
import docManipulation as dm
import re

class LSA(object):
    def __init__(self):
        self.stopwords = stopwords.words('english')
        self.ignorechars = ''',:'!'''
        self.wdict = {}
        self.dcount = 0        
    def parse(self, doc):
        words = doc.split();
	
        for w in words:
            w = w.lower().translate(None, self.ignorechars)
            if w in self.stopwords:
                continue
            elif w in self.wdict:
                self.wdict[w].append(self.dcount)
            else:
                self.wdict[w] = [self.dcount]

	
        self.dcount += 1 
     
    def build(self):
        self.keys = [k for k in self.wdict.keys() if len(self.wdict[k]) > 1]
	print "keys:"+str(self.keys)
        self.keys.sort()
        self.A = zeros([len(self.keys), self.dcount])
	print "A"
	print self.A
        for i, k in enumerate(self.keys):
            for d in self.wdict[k]:
                self.A[i,d] += 1
	print self.printA()
    def calc(self):
        self.U, self.S, self.Vt = svd(self.A)
	print "U"
	print self.printU()
	print "S"
	print self.S
	print "Vt"
	print self.printVt()
	
    def TFIDF(self):
        WordsPerDoc = sum(self.A, axis=0)        
        DocsPerWord = sum(asarray(self.A > 0, 'i'), axis=1)
        rows, cols = self.A.shape
        for i in range(rows):
            for j in range(cols):
                self.A[i,j] = (self.A[i,j] / WordsPerDoc[j]) * log(float(cols) / DocsPerWord[i])
    def printA(self):
        return self.A
    def printS(self):
        return self.S
    def printU(self):
	return self.U
    def printVt(self):
        return self.Vt
    
    def removeStopList(self,listItem,listItemPurged):
		''' Remove listItemPurged from listItem '''
		return list(set(listItem)-set(listItemPurged))
    
    def readData(self):
        fd = open('doc3.txt','r')
        data = fd.read()
        fd.close()
        data = data.replace('\n','')
	
        doc = str(data).split('.')
        doc = self.removeStopList(doc,[' '])
	
        lsaObj=LSA()
        for sent in doc:
            sent.replace('\n','')
            lsaObj.parse(sent)
            lsaObj.build()
            lsaObj.calc()
            matS=lsaObj.printS()
            matU=lsaObj.printU()
            matVt=lsaObj.printVt()

obj = LSA();
obj.readData()

