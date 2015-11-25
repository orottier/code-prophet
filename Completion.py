class Completion(object):

    def __init__(self, name, description, score = 0):
        self.mode = None

        self.name = name
        self.score = score
        self.realScore = (1. * score / len(name)) if len(name) else 0
        self.description = description + " (" + str(round(self.realScore, 3)) + ")"

        self.line = 12
        self.column = 4
        self.module_path = ""

    def matches(self, query):
        return query in self.name

    def toJson(self):
        return {
            'name': self.name,
            'description': self.description,
            'docstring': self.description,
            'line': self.line,
            'column': self.column,
            'module_path': self.module_path
        }

class CompletionBuilder:
    def __init__(self, query, maxItems = 50, minTokenLength = 4):
        self.query = query
        self.maxItems = maxItems
        self.completions = []
        self.extraTokens = {}
        self.minTokenLength = minTokenLength

    def add(self, completion, skipMaxCheck = False):
        if skipMaxCheck or len(self.completions) < self.maxItems and completion.matches(self.query):
            self.completions.append(completion)

            if completion.mode == "line":
                tokens = completion.name.split()
                if len(tokens) > 1 and len(tokens[0]) >= self.minTokenLength:
                    token = tokens[0]
                    if not token in self.extraTokens:
                        self.extraTokens[token] = 0
                    self.extraTokens[token] += completion.score


    def addMany(self, completions, skipMaxCheck = False):
        if skipMaxCheck or len(self.completions) < self.maxItems:
            for completion in completions:
                self.add(completion, skipMaxCheck)

    def getCompletions(self):
        self.addMany([TokenCompletion(token, "sub", count) for (token, count) in self.extraTokens.items()], True)
        self.completions.sort(key=lambda x: x.realScore, reverse=True)
        return [completion.toJson() for completion in self.completions]

class LineCompletion(Completion):

    def __init__(self, *args):
        super(LineCompletion, self).__init__(*args)
        self.mode = "line"

class TokenCompletion(Completion):

    def __init__(self, *args):
        super(TokenCompletion, self).__init__(*args)
        self.mode = "token"
