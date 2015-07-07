from __future__ import absolute_import
import os, gameglobals, puzzlelevels
from io import open

fileName = u"save.dat"

class SaveData(object):
	def __init__(self):
		#-1 represents uncleared/unplayed
		self.initialiseDefault()

	def initialiseDefault(self):
		self.standardScores = [-1]*4 # 10000 * %cleared. 10000 for clear. (integer only!)
		self.endlessScores = [-1]*3 #Highest achieved score.
		self.puzzleScores = [-1]*puzzlelevels.numPuzzles #Lowest rotations scored.

	def serialize(self):
		builders = []
		builder = []
		for score in self.standardScores:
			builder.append(unicode(score))
		builders.append(u".".join(builder))

		builder = []
		for score in self.endlessScores:
			builder.append(unicode(score))
		builders.append(u".".join(builder))

		builder = []
		for score in self.puzzleScores:
			builder.append(unicode(score))
		builders.append(u".".join(builder))

		return u"@".join(builders)

	def unserialize(self, data): #set variables
		builder = data.split(u"@")
		success = self.readIntoArray(builder[0], self.standardScores,
							lambda value : self.standardCheck(value)) and \
				self.readIntoArray(builder[1], self.endlessScores,
							lambda value : self.endlessCheck(value)) and \
				self.readIntoArray(builder[2], self.puzzleScores,
							lambda value : self.puzzleCheck(value))
		if not success:
			self.initialiseDefault()

	def standardCheck(self, value):
		return value >= -1 and value <= 10000

	def endlessCheck(self, value):
		return value >= -1

	def puzzleCheck(self, value):
		return value >= -1

	def readIntoArray(self, data, array, meetsCondition):
		builder = data.split(u".")
		if len(builder) != len(array):
			return False
		for i in xrange(0,len(builder)):
			value = int(builder[i])
			if meetsCondition(value):
				array[i] = value
			else:
				return False
		return True

	def tryUpdateStandard(self, index, value):
		if self.standardScores[index] == -1 or value > self.standardScores[index]:
			self.standardScores[index] = value
			saveData()

	def tryUpdateEndless(self, index, value):
		if self.endlessScores[index] == -1 or value > self.endlessScores[index]:
			self.endlessScores[index] = value
			saveData()

	def tryUpdatePuzzle(self, index, value):
		if self.puzzleScores[index] == -1 or value < self.puzzleScores[index]:
			self.puzzleScores[index] = value
			saveData()



def startupInitialise():
	gameglobals.saveData = SaveData()
	read(gameglobals.saveData)


def saveData():
	write(gameglobals.saveData)


def write(saveData):
	data = saveData.serialize()
	data = encrypt(data)
	global fileName
	f = open(fileName, u'w+', encoding=u'utf-8')
	f.write(data)

def read(saveData):
	global fileName
	if os.path.isfile(fileName):
		f = open(fileName, u'r', encoding=u'utf-8')
		data = f.read()
		data = decrypt(data)
		saveData.unserialize(data)


def encrypt(input):
	arr = []
	for i in input:
		arr.append(ord(i))
	for i in xrange(1,len(arr)):
		arr[i] += arr[i-1]
		arr[i] %= 256
		if arr[i] < 0: arr[i] += 256
	for i in xrange(len(arr)-2,-1,-1):
		arr[i] += arr[i+1]
		arr[i] %= 256
		if arr[i] < 0: arr[i] += 256
	for i in xrange(0,len(arr)):
		arr[i] += (177*i)%256
		arr[i] %= 256
		if arr[i] < 0: arr[i] += 256

	for i in xrange(0,len(arr)):
		arr[i] += 32
		#print(arr[i])
	for i in xrange(0,len(arr)):
		arr[i] = unichr(arr[i])
	return u"".join(arr)

def decrypt(input):
	arr = []
	for i in input:
		arr.append(ord(i))
	for i in xrange(0,len(arr)):
		arr[i] -= 32

	for i in xrange(0,len(arr)):
		arr[i] -= (177*i)%256
		arr[i] %= 256
		if arr[i] < 0: arr[i] += 256
	for i in xrange(0,len(arr)-1):
		arr[i] -= arr[i+1]
		arr[i] %= 256
		if arr[i] < 0: arr[i] += 256
	for i in xrange(len(arr)-1,0,-1):
		arr[i] -= arr[i-1]
		arr[i] %= 256
		if arr[i] < 0: arr[i] += 256

	for i in xrange(0,len(arr)):
		arr[i] = unichr(arr[i])
	return u"".join(arr)