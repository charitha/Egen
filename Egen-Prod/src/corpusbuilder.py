class corpusbuilder(object):
	noMix = False
	__tag=""
	def __init__(self):
		self.documents1 = {}
		self.documents2 = {}
		self.IDs = []
		self.corpus = {}
		self.mixedcorpus = {}
		self.mixedIDs = []
	def calcsimscore(self,index):
		"""Get simscore for document pair at index.
		Some heuristic could be inserted here.
		Default is to assume complete similarity.
		Overload this function to add granularity.
		"""
		return 1.0
	def scoreCorpus(self):
		"""Get pairs of annotated sentences with their 			similarity score.
		"""
		annotTuples = {}
		for ID in self.IDs:
			annotTuples[ID] = (self.documents1[ID],self.documents2[ID], self.calcsimscore(ID))
		return annotTuples
	def generatemixed(self,tag,quantity=None):
		if self.noMix:
			return
		if quantity is None:
			quantity = len(self.corpus)
		global globalindex
		counter = 0
		keys1 = self.corpus.keys() # get corpus keys
		keys2 = keys1[:] # create copy
		while counter < quantity:
			random1 = random.randint(0,len(keys1)-1)
			random2 = random.randint(0,len(keys1)-1)
	
			key1 = keys1[random1]
			key2 = keys2[random2]
			if key1 == key2: continue
			ID = tag+str(globalindex)
			self.mixedIDs.append(ID)
			self.mixedcorpus[ID] = (self.corpus[key1][0],
			self.corpus[key2][1], 0.0)
			del keys1[random1], keys2[random2]
			globalindex += 1
			counter += 1
