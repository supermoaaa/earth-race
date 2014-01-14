import logging
import sys
import traceback


def initLogs():
	rotateLog()
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


def rotateLog():
	with open("earth-race.log.old", "w+") as outFile, \
			open("earth-race.log", "r") as inFile:
		outFile.write(inFile.read())


def log(level, *allMessages):
	message = " ".join([str(m) for m in allMessages])
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
