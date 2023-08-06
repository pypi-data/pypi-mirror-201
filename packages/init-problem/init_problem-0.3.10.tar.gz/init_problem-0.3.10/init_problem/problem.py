import sqlite3
import time
import os

from sqlite3 import Error
from .chapters import chapters, modules


class Problem:
    def __init__(self, problem_format, chapter, parent_path):
        '''
        problem_format -> ['JEE', 'NEET', 'IIT-JEE', 'BOOK', 'MINE']
        chapter -> kinematics, projectile ...
        parent_path -> '/Users/vaibhavblayer/10xphysics'
        '''

        self.problem_format = problem_format
        self.chapter = chapter
        self.parent_path = parent_path


    def path_problem_format(self):
        '''
        returns the path for respective problem format
        '''

        if self.chapter in chapters[0]:
            return f'{self.parent_path}/{modules[0]}/{self.chapter}/problems/{self.problem_format}'
        elif self.chapter in chapters[1]:
            return f'{self.parent_path}/{modules[1]}/{self.chapter}/problems/{self.problem_format}'
        elif self.chapter in chapters[2]:
            return f'{self.parent_path}/{modules[2]}/{self.chapter}/problems/{self.problem_format}'
        elif self.chapter in chapters[3]:
            return f'{self.parent_path}/{modules[3]}/{self.chapter}/problems/{self.problem_format}'




    def create_connection(self):
        '''
        creates connection with sqlite database at given path.
        '''

        db_file = f'{self.path_problem_format()}/problem_{self.problem_format}.db'
        try:
            conn = sqlite3.connect(db_file)
        except:
            os.makedirs(self.path_problem_format())

        return conn


    def create_database(self):
        '''
        creates the database according to init params in the respective directory
        '''
        database = self.create_connection()
        try:
            database.execute(
                """ CREATE TABLE IF NOT EXISTS problem(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chapter TEXT NOT NULL,
                    date TEXT
                ); """
                )
        except Error as e:
            print(e)

        database.close()


    def get_data(self, n):
        try:
            database = self.create_connection()
            cursor = database.cursor()
            execute_statement = f'SELECT * FROM problem ORDER BY id DESC LIMIT {n};'
            output = cursor.execute(execute_statement)
            return output.fetchmany(n)
            database.close()
        except:
            self.create_database()


    def insert_data(self):
        try:
            database = self.create_connection()
            cursor = database.cursor()
            time_date = f'{int(time.strftime("%H%M%S%d%m%Y")):14}'
            execute_statement = f'INSERT INTO problem(chapter, date) VALUES("{self.chapter}", "{time_date}");'
            cursor.execute(execute_statement)
            database.commit()
            database.close()
        except Error as e:
            print(e)




