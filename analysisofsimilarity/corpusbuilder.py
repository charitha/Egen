from __future__ import division
import re
from nltk import clean_html
import urllib2
import glob
import sys, os
from subprocess import call
import random
from nltk.corpus import brown
try:
	import psyco
	psyco.full()
except ImportError:
	pass
globalindex = 1

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
class lapatacorp(corpusbuilder):
	"""Class for generating sections derived from Lapata corpus.
	"""
	__annotations_A = {}
	__annotations_C = {}
	tokens1 = {}
	tokens2 = {}
	def __init__(self,rawfile1,rawfile2,fileA,fileC,tag=""):
		corpusbuilder.__init__(self)
		if (rawfile1 == None) or (rawfile2 == None) or \
		(fileA == None) or (fileC == None):
			raise Exception, "Missing filenames in constructor args."
		if len(tag)>0: self.__tag = "Paraphrase-"+tag
		else: self.__tag = "Paraphrase"
		# store tokens for each sentence one of the paraphrase
		self.documents1, self.documents2, self.IDs, self.tokens1, self.tokens2 \
		= self.getdocs(rawfile1,rawfile2)
		# store alignment annotations for annotators
		self.__annotations_A, self.__annotations_C = \
		self.annotparser(fileA, fileC, self.IDs)
		self.corpus = self.scoreCorpus()
		self.generatemixed(self.__tag)
	def getdocs(self, rawfile1, rawfile2):
		global globalindex
		rawdocs1, rawIDs = self.rawparser(rawfile1)
		rawdocs2 = self.rawparser(rawfile2)[0]
		docs1 = {}
		docs2 = {}
		tokens1 = {}
		tokens2 = {}
		IDs = []
		for ID in rawIDs:
			newID = self.__tag+str(globalindex)
			tokens1[newID] = rawdocs1[ID]
			tokens2[newID] = rawdocs2[ID]
			docs1[newID] = " ".join(rawdocs1[ID])
			docs2[newID] = " ".join(rawdocs2[ID])
			IDs.append(self.__tag+str(globalindex))
			globalindex += 1
		return docs1, docs2, IDs, tokens1, tokens2
	def rawparser(self,rawfile):
		sentences = {}
		orderedIDs = []
		rawfile.seek(0)
		for line in rawfile:
			#group up tags and raw sentence
			parts = re.search(r"(<s snum=[0-9]+>) ([^<]*) (</s>)",line)
			#strip away tags
			sentence = parts.group(2)
			# extract id number from leading <s...> tag
			id = int(re.search(r"[0-9]+",parts.group(1)).group(0))
			orderedIDs.append(id)
			sentences[id] = sentence.split()
		return (sentences,orderedIDs)

	def annotparser(self,fileA,fileC,IDs):
		annotA = {}
		annotC = {}
		fileA.seek(0)
		fileC.seek(0)
		for line in fileA:
			parts = re.search(r"([0-9]+) ([0-9]+) ([0-9]+) ([SP])",line)
			key = IDs[int(parts.group(1))]
			align1 = int(parts.group(2))
			align2 = int(parts.group(3))
			note = parts.group(4)
			try:
				annotA[key][(align1,align2)] = note
			except KeyError:
				annotA[key] = {(align1,align2):note}
		for line in fileC:
			parts = re.search(r"([0-9]+) ([0-9]+) ([0-9]+) ([SP])",line)
			key = IDs[int(parts.group(1))]
			align1 = int(parts.group(2))
			align2 = int(parts.group(3))
			note = parts.group(4)
			try:
				annotC[key][(align1,align2)] = note

			except KeyError:
				annotC[key] = {(align1,align2):note}
		for id in IDs:
			for alignpair in annotA[id]:
				if alignpair not in annotC[id]: annotC[id][alignpair] ='-'
			for alignpair in annotC[id]:
				if alignpair not in annotA[id]: annotA[id][alignpair] ='-'
		return (annotA,annotC)
	def calcsimscore(self,index):
		""" Returns the F-measure of inter-annotator agreement.
		"""
		As = 0
		Cs = 0
		AsIntCp = 0
		ApIntCs = 0
		for pair in self.__annotations_A[index]:
			word1index, word2index = pair
			noteA = self.__annotations_A[index][pair]
			noteC = self.__annotations_C[index][pair]
			word1 = self.tokens1[index][word1index-1].lower()
			word2 = self.tokens2[index][word2index-1].lower()
			if not word1 == word2:
				if noteA == 'S':
					As += 1
					if (noteC == 'P') or (noteC == 'S'):
						AsIntCp += 1
			if noteC == 'S':
				Cs += 1
				if (noteA == 'P') or (noteA == 'S'):
					ApIntCs += 1
		if As > 0: prec = AsIntCp / As
		else: prec = 1
		if Cs > 0: rec = ApIntCs / Cs
		else: rec = 1
		if prec+rec > 0: return (2*prec*rec)/(prec+rec)
		else: return 0


class wikicorp(corpusbuilder):
	def __init__(self, urllist,tag=""):
		corpusbuilder.__init__(self)
		global globalindex
		if len(tag)>0: self.__tag = "Wikipedia-"+tag
		else: self.__tag = "Wikipedia"
		urllist.seek(0)
		for url in urllist:
			try:
				if url.find(r"&printable=yes"):
					html_eng = self.getHTML(self.getprintURL(url))
				else:
					html_eng = self.getHTML(url)
			except:
				sys.stderr.write("Couldn't retrieve "+url+"\nSkipping...\n")
				continue
			try:
				simplepatt = r'(http://simple\.wikipedia\.org/'+ r'wiki/[^/<>\s"]+[/]{0,1})'
				urlsimple = re.search(simplepatt,html_eng).group(0).strip('\n')
			except AttributeError:
				sys.stderr.write("No Simple English version of "+ \
			url+"\nSkipping...\n")
				continue
			try:
				html_simp = self.getHTML(self.getprintURL(urlsimple))
			except:
				sys.stderr.write("Couldn't retrieve "+ \
			urlsimple+"\nSkipping...\n")
				continue
			try:
				text_eng = clean_html(html_eng)
				text_simp = clean_html(html_simp)
				self.documents1[self.__tag+str(globalindex)] = \
					self.getarticlebody(text_eng)
				self.documents2[self.__tag+str(globalindex)] = \
					self.getarticlebody(text_simp)
			except:
				sys.stderr.write("Problem came up while cleaning up "+ \
			url+"\nSkipping...\n")
				continue
			self.IDs.append(self.__tag+str(globalindex))
			globalindex +=1
		self.corpus = self.scoreCorpus()
		self.generatemixed(self.__tag)

	def getHTML(self, url):
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		infile = opener.open(url)
		page = infile.read()
		return page

	def getprintURL(self, url):
		parts = re.search(r"(http://)([a-zA-Z]+)(.wikipedia.org/wiki/)(.*)",url)
		formattedurl = "http://"+parts.group(2)+ \
		".wikipedia.org/w/index.php?title="+ \
		parts.group(4)+"&printable=yes"
		return formattedurl

	def getarticlebody(self,raw):
		# find start of boilerplate text
		boilerplate = raw.find(r'Retrieved from "http://')
		# remove boilerplate text
		cleantext = raw[:boilerplate]
		# remove large chunks of whitespace
		cleantext = re.sub(r"[ \t]{2}[ \t]*"," ",cleantext)
		# bunch up newlines
		cleantext = re.sub(r"[ \t]+\n","\n",cleantext)
		# reduce large chunks of newlines
		cleantext = re.sub(r"\n\n\n+","\n\n",cleantext)
		return cleantext

class papercorp(corpusbuilder):
	def __init__(self,folder,tag=""):
		corpusbuilder.__init__(self)
		global globalindex
		rawpdfs = []
		if len(tag)>0: self.__tag = "Abstracts-"+tag
		else: self.__tag = "Abstracts"
		# These get absolute path (computationally cheap, so let's skip checks)
		folder = os.path.expanduser(folder)
		folder = os.path.expandvars(folder)
		folder = os.path.abspath(folder)

		if not os.path.exists(folder):
			raise Exception, folder+" does not exist!"

		pdflist = glob.glob(folder+"/*.pdf")
		for pdf in pdflist:
			try:
				raw = self.getrawtxt(pdf)
			except:
				sys.stderr.write("\nSomething went wrong while trying to " + \
						"open "+pdf+". Perhaps it is write "+ \
						"protected? Skipping...\n")
				continue
			rawpdfs.append(raw)

		for rawtext in rawpdfs:
			try:
				abstract, body = self.chopabstract(rawtext)
			except:
				sys.stderr.write("\nSomething went wrong trying to chop up "+ \
						"document.\nHere is a "+ \
						"sample of the first few lines:\n"+ \
						"=============\n" + rawtext[:250]+ \
						"\n=============\nSkipping...\n")
				continue
			self.documents1[self.__tag+str(globalindex)] = abstract
			self.documents2[self.__tag+str(globalindex)] = body
			self.IDs.append(self.__tag+str(globalindex))
			globalindex += 1
		self.corpus = self.scoreCorpus()
		self.generatemixed(self.__tag)

	def getrawtxt(self,pdf):
		textFN = pdf[:pdf.find('.pdf')]+".txt"
		retcode = call(["/usr/local/bin/pdftotext", "-nopgbrk", \
		"-raw",pdf,textFN])
		if retcode is not 0: # pdftotxt failed to process pdf
			raise Exception # This will be handled in __init__
		try:
			textfile = open(textFN)
		except:
			sys.stderr.write("Something went really wrong. Check pdftotext.\n")
			sys.stderr.write("Problem happened with "+pdf+"\nSkipping...\n")
			sys.exit()
		try:
			raw = "".join(textfile.readlines())
		except:
			raise Exception # This will be handled in __init__
		finally: # to avoid potential memory leaks if this messes up
			textfile.close()
			os.remove(textFN) # clean up generated text file
		return raw
	
	def chopabstract(self,raw):
		if "introduction" in raw[:2500].lower():
			regex = r"(abstract.*?)(introduction.*)"
		elif "keyword" in raw[:2500].lower():
			regex = r"(keyword.*?)(introduction.*)"
		else: raise Exception # introduction/keywords not found
		slicer = re.compile(regex, re.I|re.DOTALL)
		parts = slicer.search(raw)
		if parts is None:
			regex = regex = r"(.*?)(introduction.*)"
			slicer = re.compile(regex, re.I|re.DOTALL)
			parts = slicer.search(raw)
		abstract = self.cleantext(parts.group(1))
		body = self.cleantext(parts.group(2))
		return abstract, body
	
	def cleantext(self,text):
		cleantext = text.replace('-\n ','') # fix split words
		cleantext = cleantext.replace('-\n','') # ditto
		# remove newlines in the middle of sentences
		cleantext = re.sub(r"(?<=[\w:.,-?!;()])\n(?=[\w])", ' ', cleantext)
		return cleantext

class editcorp(corpusbuilder):
	noMix = True
	def __init__(self,startindex=0,size=500):
		corpusbuilder.__init__(self)
		global globalindex
		self.sentences = brown.sents()[startindex:startindex+size]
		for sentence in self.sentences:
			sent1 = " ".join(sentence)
			sent2, edits = self.randomedits(sent1)
			score = 1 - (edits/len(sent1))
			ID = "Edits" + str(globalindex)
			self.IDs.append(ID)
			self.corpus[ID] = (sent1, sent2, score)
			globalindex += 1	

	def randomedits(self,sentence):
		edits = 0
		randindex = lambda x: random.randint(0,len(x)-1)
		maxchanges = randindex(sentence)

		for i in range(0,maxchanges):
			edit_type = random.randint(1,3)
			try: edit_loc = randindex(sentence)
			except:
				print sentence
				sys.exit()
			if edit_type is 1:
				sentence = self.morph(sentence,edit_loc)
			elif edit_type is 2:
				sentence = self.delete(sentence,edit_loc)
			elif edit_type is 3:
				destination = randindex(sentence)
				while destination is edit_loc:
					destination = randindex(sentence)
				sentence = self.move(sentence,edit_loc,destination)
			edits += 1
		return (sentence,edits)
	
	def morph(self,sent,loc):
		target = "1234567890abcdefghijklmnopqrstuvw"\
	"xyzABCDEFGHIJKLMNOPQRSTUVWXYZ,.;:?!"
		original = sent[loc]
		change = target[random.randint(0,len(target)-1)]
		while change is original:
			change = target[random.randint(0,len	(target)-1)]
		return sent[:loc]+change+sent[loc+1:]

	def delete(self,sent,loc):
		return sent[:loc]+sent[loc+1:]

	def move(self,sent,loc,dest):
		character = sent[loc]
		sent = self.delete(sent, loc)
		if dest > loc: dest -= 1
		return sent[:dest]+character+sent[dest:]

class themecorp(corpusbuilder):
	noMix = True
	text_chunks = {}
	cats =['adventure','editorial','romance','religion','science_fiction']
	dualcats = {'adventure':'editorial',
'editorial':'romance',
'romance':'science_fiction',
'religion':'adventure',
'science_fiction':'religion'}

	def __init__(self,startindex=0,set_size=3,set_no=50):
		corpusbuilder.__init__(self)
		self.__tag = "Themes"
		global globalindex
		for category in self.cats:
			index = startindex
			self.text_chunks[category] = []
			while index-startindex < (set_no*set_size*2):
				chunk = ""
				for i in range (0,set_size):
					para = " ".join(reduce(lambda x,y:x+y,
						brown.paras(categories=category)[index+i]))
					chunk += para
				self.text_chunks[category].append(chunk)
				index += set_size

			for category in self.cats:
				for i in range(0,len(self.text_chunks[category]),2):
					sent1 = self.text_chunks[category][i]
					sent2 = self.text_chunks[category][i+1]
					ID = self.__tag+str(globalindex)
					self.IDs.append(ID)
					self.corpus[ID] = (sent1,sent2,1.0)
					globalindex += 1

			for category in self.cats:
				for i in range(0,set_no):
					sent1 = self.text_chunks[category][i]
					sent2 = self.text_chunks[self.dualcats[category]][i]
					ID = self.__tag+str(globalindex)+"m"
					self.mixedIDs.append(ID)
					self.mixedcorpus[ID] = (sent1,sent2,0.0)
					globalindex += 1

class POSswitchcorp(corpusbuilder):
	def __init__(self,startindex=1500,size=500):
		corpusbuilder.__init__(self)
		global globalindex
		self.__tag = "POSswitch"		
		self.tagged_sents = brown.tagged_sents()[startindex:startindex+size]
		POScatwords = {}
		for pair in reduce(lambda x,y:x+y, self.tagged_sents):
			word, tag = pair
			try: POScatwords[tag].append(word)
			except: POScatwords[tag] = [word]
		for tag in POScatwords:
			POScatwords[tag] = list(set(POScatwords[tag]))
		for tagged_sent in self.tagged_sents:
			dual_sent = tagged_sent[:] # create working copy
			for i in range(0,random.randint(1,len(tagged_sent))):
				loc = random.randint(0,len(tagged_sent)-1)
				type = dual_sent[loc][1]
				wordlist = POScatwords[type]
				subs_word = wordlist[random.randint(0,len(wordlist)-1)]
				if dual_sent[loc][0].islower():
					subs_word = subs_word[0].lower() + subs_word[1:]
				else: subs_word = subs_word[0].upper() + subs_word[1:]
				dual_sent[loc] = (subs_word,type)
			tagged_sent = " ".join(map(lambda x:x[0],tagged_sent))
			dual_sent = " ".join(map(lambda x:x[0],dual_sent))
			ID = self.__tag+str(globalindex)
			self.IDs.append(ID)
			self.documents1[ID] = tagged_sent
			self.documents2[ID] = dual_sent
			globalindex += 1
		self.corpus = self.scoreCorpus()
		self.generatemixed(self.__tag)
