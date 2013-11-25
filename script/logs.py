from os import path, rename, remove
import logging

def initLogs():
	#~ try:
		#~ with open('earth-race.log', 'w') as file:
			#~ file.close()
	#~ except:
		#~ pass
	if path.isfile('earth-race.log'):
		try:
			rename('earth-race.log','earth-race.log.old')
		except:
			remove('earth-race.log.old')
			rename('earth-race.log','earth-race.log.old')
	logger = logging.getLogger('earth-race')
	logger.setLevel(logging.DEBUG) # niveau max de log que peuvent prendre le log ou la console
	fh = logging.FileHandler('earth-race.log')
	fh.setLevel(logging.DEBUG) # niveau de log du fichier
	fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
	logger.addHandler(fh)
	sh = logging.StreamHandler()
	sh.setLevel(logging.ERROR) # niveau de log de la console
	sh.setFormatter(logging.Formatter('%(levelname)s : %(message)s'))
	logger.addHandler(sh)
	logger.debug("start")
	#~ les niveaux de log sont dans l'ordre DEBUG, INFO, WARNING, ERROR, CRITICAL

def log(level, message):
	logger = logging.getLogger('earth-race')
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
