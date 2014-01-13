from os import path, rename, remove
import logging
import sys
import traceback


def initLogs():
	#~ try:
		#~ with open('earth-race.log', 'w') as file:
			#~ file.close()
	#~ except:
		#~ pass
	if path.isfile('earth-race.log'):
		try:
			remove('earth-race.log.old')
		except:
			pass
		rename('earth-race.log', 'earth-race.log.old')
	logger = logging.getLogger('earth-race')
	# niveau max de log que peuvent prendre le log ou la console
	logger.setLevel(logging.DEBUG)
	fh = logging.FileHandler('earth-race.log')
	fh.setLevel(logging.DEBUG)  # niveau de log du fichier
	fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
	logger.addHandler(fh)
	sh = logging.StreamHandler()
	sh.setLevel(logging.ERROR)  # niveau de log de la console
	sh.setFormatter(logging.Formatter('%(levelname)s : %(message)s'))
	logger.addHandler(sh)
	logger.debug("start")
	#~ les niveaux de log sont dans l'ordre DEBUG, INFO, WARNING, ERROR, CRITICAL

	def log_uncaught_exceptions(ex_cls, ex, tb):
		logger.critical(''.join(traceback.format_tb(tb)))
		logger.critical('{0}: {1}'.format(ex_cls, ex))

	sys.excepthook = log_uncaught_exceptions  # log uncaught exception


def log(level, message):
	logger = logging.getLogger('earth-race')
	if level == "debug":
		logger.debug(message)
	elif level == "info":
		logger.info(message)
	elif level == "warning":
		logger.warning(message)
	elif level == "error":
		logger.error(message)
	elif level == "critical":
		logger.critical(message)
	else:
		# si on ne reconnais pas le level on le met en niveau debug
		logger.debug(message)
