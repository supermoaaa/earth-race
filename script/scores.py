from operator import itemgetter

class Scores:
	def __init__(self, mapName):
		self.mapName=mapName;
		self.scores={};
		self.lastScores=[];

	def __json__(self, request):
		return dict(
			mapName=self.mapName,
			scores=self.scores,
			)

	def newScore(self, playerName, duration):
		if playerName not in self.scores:
			self.scores[playerName]=[]
		self.scores[playerName].append(duration)
		self.scores[playerName].sort()
		self.scores[playerName]=self.scores[playerName][0:4]
		self.lastScores.append([playerName, duration, gl.nbLaps])

	def getLastScores(self):
		return sorted(self.lastScores, key=itemgetter(1))

	def getBestScores(self):
		orderedScores = self.__sortScores(self.scores.items())[:8]
		bestScores = []
		for key, listValues in orderedScores:
			for value in listValues:
				bestScores.append([key,value])
		return self.__sortScores(bestScores)[:8]

	def getPlayerBestScores(self, playerName):
		return self.scores.get(playerName, [])

	def __sortScores(self, scores):
		return sorted(scores, key=lambda x: x[1][0]/x[1][1])
