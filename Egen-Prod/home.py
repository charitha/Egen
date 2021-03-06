"""
GUI-For Ebook display 

"""
"""configuration file"""
CONFIG='config.cfg'

import os.path
import cherrypy
import sys
import debug

from cherrypy.lib.static import serve_file

class EbookGUI:
	def index(self):
		return serve_file(os.path.join(current_dir, "index.html"))
	index.exposed = True



if __name__ == '__main__':
	current_dir = os.path.dirname(os.path.abspath(__file__))
	conf = os.path.join(current_dir, CONFIG)	
	cherrypy.quickstart(EbookGUI(), config=conf)
else:
	cherrypy.tree.mount(EbookGUI(), config=tutconf)
