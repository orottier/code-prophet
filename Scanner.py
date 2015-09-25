import fnmatch
import os

class Scanner:

	def __init__(self, path, pattern):
		self.path = path
		self.pattern = pattern

	def scan(self):
		matches = []
		for root, dirNames, fileNames in os.walk(self.path):
			for fileName in fnmatch.filter(fileNames, self.pattern):
				matches.append(os.path.join(root, fileName))

		fileDict = {}

		for fileName in matches:
			with open(fileName) as f:
				lines = []
				for line in f:
					line = line.strip()
					if line:
						lines.append(line)
			if lines:
				fileDict[fileName] = lines

		return fileDict
