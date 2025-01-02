import re

class Book():
    def __init__(self, task):
        self.originalTaskId = task.id
        self.setTitle(task.content)
        self.setAuthor(task.description)

    def setTitle(self, content):
        if "[" in content and "]" in content:
            match = re.search(r'\[(.*?)\]\((.*?)\)', content)
            if match:
                self.title = match.group(1)
                self.amazonUrl = match.group(2)
            else:
                self.title = content
                self.amazonUrl = ""
        else:
            self.title = content
            self.amazonUrl = ""

    def setAuthor(self, author):
        if " y " in author:
            authors = [author.strip() for author in author.split(" y ")]
        else:
            authors = [author.strip()]
        self.author = authors

    def __str__(self):
        return f"{self.title} - {self.author}"