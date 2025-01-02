import re


class Audiovisual():
    def __init__(self, task, type):
        self.originalTaskId = task.id
        self.setTitle(task.content)
        self.platform = task.description
        self.type = type

    def setTitle(self, content):
        if "[" in content and "]" in content:
            match = re.search(r'\[(.*?)\]\((.*?)\)', content)
            if match:
                self.title = match.group(1)
                self.justWatchUrl = match.group(2)
            else:
                self.title = content
                self.justWatchUrl = ""
        else:
            self.title = content
            self.justWatchUrl = ""

    def __str__(self):
        return f"{self.title} - {self.platform}"
