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
		self.lastScores.append([playerName, duration])

	def getLastScores(self):
		return sorted(self.lastScores, key=lambda x:x[1])

	def getBestScores(self):
		orderedScores = sorted(self.scores.items(), key=lambda x: x[1])[:8]
		bestScores = []
		for key, listValues in orderedScores:
			for value in listValues:
				bestScores.append([key,value])
		orderedBestScores = sorted(bestScores, key=lambda x: x[1])
		return orderedBestScores[:8]

	def getPlayerBestScores(self, playerName):
		return self.scores.get(playerName, [])
