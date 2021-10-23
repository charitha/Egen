import centeringTheory as ct
import docManipulation as dm

class SentenceOrdering:
	def __init__(self):
		self.finalDoc=[]

	def demo(self):
		self.documentMerge(documents)
		
	def documentMerge(self,documents):
		if len(documents)>1:
			while (len(documents)!=1):
				self.finalDoc=[]
				doc1 = documents.pop(0)
				doc2 = documents.pop(0)
				dmObj = dm.docManipulation("")
				doc1 =	dmObj.docToSentList(doc1)
				if len(doc1) > 5:
					doc1 = doc1[0:5]
				doc2 = dmObj.docToSentList(doc2)
				if len(doc2) > 5:
					doc2=doc2[0:5]
				self.mergeDocSentences(doc1,doc2)
				documents.insert(0,'.'.join(self.finalDoc))

		return documents[0]
				
	def mergeDocSentences(self,sentList1,sentList2):
		obj = ct.CenteringTheory()
		merged = []
		merged.append(sentList1.pop(0))
		try:
			sentList1 = [sent for sent in sentList1 if sent != '' and sent !=u' ' and len(sent) >5 and obj.isValidSentence(sent)]
			sentList2 = [sent for sent in sentList2 if sent != '' and sent !=u' ' and len(sent) >5 and obj.isValidSentence(sent)]
			
		except:
			pass		

		while len(sentList1) and len(sentList2):
			a = merged[len(merged)-1]
						
			b = a+"."+sentList1[0]+"."
		        

			if obj.isValid(b)=="TRUE":
				val1 = obj.parse(b)
			else:
				val1=-1
	
			b = a+"."+sentList2[0]+"."
			

			if obj.isValid(b) == "TRUE":
				val2=obj.parse(b)
			else:
				val2 = -1

	
			if val1 > 0 or val2 >0 :
				if val1 >= val2:
					merged.append(sentList1.pop(0))
				else:		
					merged.append(sentList2.pop(0))

			elif val1==0 and val2==0:
				self.mergeDocSentences(sentList1,sentList2)

			else:
				if val1 < 0:
					sentList1.pop(0)
		
				if val2 < 0:
					sentList2.pop(0)

		if len(sentList1):
			merged += sentList1
			sentList1 = []
			
	
		if len(sentList2):
			merged += sentList2
			sentList2 = []
		
			
		self.finalDoc =merged + self.finalDoc
		 
	
#documents = ["A microprocessor incorporates the functions of a computer's central processing unit (CPU) on a single integrated circuit (IC),[1] or at most a few integrated circuits.All modern CPUs are microprocessors making the micro- prefix redundant. The microprocessor is a multipurpose, programmable device that accepts digital data as input, processes it according to instructions stored in its memory, and provides results as output.The internal arrangement of a microprocessor varies depending on the age of the design and the intended purposes of the processor. The complexity of an integrated circuit is bounded by physical limitations of the number of transistors that can be put onto one chip, the number of package terminations that can connect the processor to other parts of the system, the number of interconnections it is possible to make on the chip, and the heat that the chip can dissipate.","The internal arrangement of a microprocessor varies depending on the age of the design and the intended purposes of the processor. The complexity of an integrated circuit is bounded by physical limitations of the number of transistors that can be put onto one chip, the number of package terminations that can connect the processor to other parts of the system, the number of interconnections it is possible to make on the chip, and the heat that the chip can dissipate.","As integrated circuit technology advanced, it was feasible to manufacture more and more complex processors on a single chip. The size of data objects became larger; allowing more transistors on a chip allowed word sizes to increase from 4- and 8-bit words up to today's 64-bit words."]
#obj = SentenceOrdering()
#obj.demo()
