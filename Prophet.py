import operator
from itertools import ifilter
from Completion import Completion
from Script import Script

class Prophet:

    def __init__(self, fileDict):

        """word separators for tokenizer: " ./\\()\"'-:,.;<>~!@#$%^&*|+=[]{}`~?",  """

        """ first line context """
        firstLines = {}
        for key,lines in fileDict.items():
            first = lines[0]
            if not first in firstLines:
                firstLines[first] = 0
            firstLines[first] += 1
        self.firstLines = sorted(firstLines.items(), key=operator.itemgetter(1), reverse=True)

        """ no context """
        allLines = {}
        for key,lines in fileDict.items():
            for line in lines:
                if not line in allLines:
                    allLines[line] = 0
                allLines[line] += 1
        self.allLines = sorted(allLines.items(), key=operator.itemgetter(1), reverse=True)

        """ prev line context """
        prevLines = {}
        for key,lines in fileDict.items():
            prev = None;
            for line in lines:
                if prev:
                    if not prev in prevLines:
                        prevLines[prev] = {}
                    if not line in prevLines[prev]:
                        prevLines[prev][line] = 0
                    prevLines[prev][line] += 1
                prev = line
        for key,nextValues in prevLines.items():
            prevLines[key] = sorted(prevLines[key].items(), key=operator.itemgetter(1), reverse=True)
        self.prevLines = prevLines


    def speak(self, script):
        chunks = set(script['contents'][0].split())
        # full line suggest
        if int(script['column'][0]) == 0:
            # first line
            if int(script['line'][0]) == 0:
                return [Completion(text, str(count)).toJson() for (text, count) in self.firstLines]
            # else:
            #     return [Completion(text, str(count)).toJson() for (text, count) in self.prevLines[...]]
            return [Completion(text, str(count)).toJson() for (text, count) in self.allLines]
        else:
            return [Completion(text, "identifier").toJson() for text in chunks]

