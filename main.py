from todoist_api_python.api import TodoistAPI
from notion_client import Client
from env import *
from books import Book
from audiovisual import Audiovisual


class App():
    def __init__(self):
        self.todoistAPI = TodoistAPI(token=TODOIST_API_TOKEN)
        self.notionAPI = Client(auth=NOTION_INTEGRATION_SECRET)
        self.tasks = []
        self.books = []
        self.audiovisuals = []
        self.loadTasks()
        self.listBooks()
        self.listAudiovisuals()
        # self.insertBooks()
        self.insertAudiovisuals()

    def loadTasks(self):
        try:
            tasks = self.todoistAPI.get_tasks(project_id=TODOIST_INBOX_ID)
            for task in tasks:
                if task.section_id == TODOIST_WAITLIST_ID and len(task.labels) > 0:
                    label = task.labels[0]
                    if task.content == "Titulo":
                        continue
                    if label == "Libro":
                        self.books.append(Book(task))
                    elif label == "Pelicula":
                        self.audiovisuals.append(Audiovisual(task, "Movie"))
        except Exception as e:
            print(f"Error al cargar tareas: {e}")

    def listBooks(self):
        for book in self.books:
            print(book)

    def insertBooks(self):
        for book in self.books:
            try:
                properties = {
                    "Name": {
                        "title": [
                            {
                                "text": {
                                    "content": book.title
                                }
                            }
                        ]
                    },
                    "Author": {
                        "multi_select": [
                            {"name": author} for author in book.platform
                        ]
                    }
                }

                if book.amazonUrl:
                    properties["Amazon"] = {
                        "url": book.amazonUrl
                    }

                self.notionAPI.pages.create(
                    parent={"database_id": NOTION_BOOK_DATABASE_ID},
                    properties=properties,
                )

                self.todoistAPI.close_task(book.originalTaskId)
                print(f"Libro '{book.title}' insertado en Notion.")

            except Exception as e:
                print(f"Error al procesar el libro '{book.title}': {e}")

    def listAudiovisuals(self):
        for av in self.audiovisuals:
            print(av)

    def insertAudiovisuals(self):
        for av in self.audiovisuals:
            try:
                properties = {
                    "Name": {"title": [{"text": {"content": av.title}}]},
                    "Where to watch": {"select": {"name": av.platform}},
                    "Type": {"select": {"name": av.type}},
                }

                if av.justWatchUrl:
                    properties["JustWatch"] = {"url": av.justWatchUrl}

                self.notionAPI.pages.create(
                    parent={"database_id": NOTION_AV_DATABASE_ID},
                    properties=properties,
                )

                self.todoistAPI.close_task(av.originalTaskId)
                print(f"Audiovisual '{av.title}' insertado en Notion.")
            except Exception as e:
                print(f"Error al procesar el audiovisual '{av.title}': {e}")


app = App()
