
class Topic:
	
	def __init__(self):
		self.topicname = ""
		self.subtopics = []
		self.level = -1
		self.urls = []
		self.docs=[]
		self.images=[]
		self.finalText=""
	


class Syllabus:
	
	def readFile(self):
		f=open("static/topic.txt")
		lines=f.readlines()
		f.close()

		topics = []
		

		for line in lines:
			line=line.lstrip()
			line=line.rstrip('\n')
			topics.append(line)
		
	
		return topics
			
	
	def addSubTopic(self,parent,line,level,pos):
		child= Topic()
		child.topicname = line
		child.level = level
		parent.subtopics.insert(pos,child)
			
	def makeObject(self):
		syllabus = self.readFile()
		
		sylObject = Topic()
		sylObject.topicname = syllabus[0]
		sylObject.level=0
		
                for i in range(1,len(syllabus)): 
			if (syllabus[i] !=''):
				line = syllabus[i]
				position = line.partition(' ')[0]
				line = line.partition(' ')[2]
				count = position.count('.')
				values = position.split('.')
				obj = sylObject
				
				for j in range(0,count): 
					pos = int(values[j])
					obj = obj.subtopics[pos-1]
			
		        
				self.addSubTopic(obj,line,(count+1),int(values[count]))
			
		return sylObject
