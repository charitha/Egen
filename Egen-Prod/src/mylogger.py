import logging
# create logger
lgr = logging.getLogger('Egen')
lgr.setLevel(logging.INFO)
# add a file handler
fh = logging.FileHandler('server1.log')
fh.setLevel(logging.INFO)
# create a formatter and set the formatter for the handler.
frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(frmt)
# add the Handler to the logger
lgr.addHandler(fh)
