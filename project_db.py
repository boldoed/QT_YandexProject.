import sqlite3


class ProjectDB:
    def __init__(self):
        self.connection = sqlite3.connect('QT_Project_db.db')
        self.cursor = self.connection.cursor()





