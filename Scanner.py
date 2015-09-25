import fnmatch
import os

class Scanner:

	def __init__(self, path, pattern):
		self.path = path
		self.pattern = pattern
		self.files = 0
		self.lines = 0

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
						self.lines += 1
						lines.append(line)
			if lines:
				self.files += 1
				fileDict[fileName] = lines

		return fileDict