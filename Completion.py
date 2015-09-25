class Completion:

    def __init__(self, name, description):
        self.name = name
        self.description = description

        self.line = 12
        self.column = 4
        self.module_path = ""

    def toJson(self):
        return {
            'name': self.name,
            'description': self.description,
            'docstring': self.description,
            'line': self.line,
            'column': self.column,
            'module_path': self.module_path
        }

