"""
GUI-For Ebook display 

"""
"""configuration file"""
CONFIG='config.cfg'

import os.path
import cherrypy
import sys
import logging 
import mylogger as log
import informationRetreival
#import documentSimilarity
#import LSA


from cherrypy.lib.static import serve_file

class EbookGUI:
	def index(self):
	  	log.lgr.warn('loaded index')
		return serve_file(os.path.join(current_dir, "home.html"))
	index.exposed = True
	
	
	def readfile(self,syllabus):
			structuredSyllabus = syllabus.file.read(8192)
			log.lgr.warn('STATUS: '+structuredSyllabus)
			f=open('static/file.txt','w')
			f.write(structuredSyllabus)
			f.close()
			obj=informationRetreival.InformationRetreival()
			obj.infoRetreive("not")
			#return serve_file(os.path.join(current_dir, "home.html"))
	readfile.exposed=True


	def debug(self):
		log.lgr.warn('loaded debug')
		return serve_file(os.path.join(current_dir, "debug.html"))
	debug.exposed=True

if __name__ == '__main__':
	current_dir = os.path.dirname(os.path.abspath(__file__))
	conf = os.path.join(current_dir, CONFIG)
	root = EbookGUI()
	root.debug = root.debug()
	cherrypy.quickstart(root, config=conf)


if __name__ == '__main__':
	current_dir = os.path.dirname(os.path.abspath(__file__))
	conf = os.path.join(current_dir, CONFIG)	
	cherrypy.quickstart(EbookGUI(), config=conf)
