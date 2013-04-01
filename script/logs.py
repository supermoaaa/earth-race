import logging

def initLogs():
	logger = logging.getLogger()
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
	fh = logging.FileHandler('earth-race.log')
	fh.setLevel(logging.DEBUG) # niveau de log du fichier
	fh.setFormatter(formatter)
	logger.addHandler(fh)
	sh = logging.StreamHandler()
	sh.setLevel(logging.DEBUG) # niveau de log de la console
	sh.setFormatter(formatter)
	logger.addHandler(sh)
	#~ les niveaux de log sont dans l'ordre DEBUG, INFO, WARNING, ERROR, CRITICAL

def log(level, message):
	logger = logging.getLogger()
	if level=="debug":
		logger.debug(message)
	elif level=="info":
		logger.info(message)
	elif level=="warning":
		logger.warning(message)
	elif level=="error":
		logger.error(message)
	elif level=="critical":
		logger.critical(message)
	else:
		logger.debug(message) # si on ne reconnais pas le level on le met en niveau debug
