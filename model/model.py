import sqlite3

db = sqlite3.connect('agenda.db')
db_cursor = db.cursor()
db_cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (
                     TaskTitle TEXT NOT NULL,
                     TaskDescription TEXT NOT NULL,
                     TaskIndex INTEGER NOT NULL DEFAULT 0,
                     TaskStatus TEXT NOT NULL DEFAULT 'Невыполнена',
                     PRIMARY KEY (TaskIndex));
                     """)

class Task:
    task_title = ""
    task_description = ""
    task_index = 0
    task_status = "Невыполнена"

    def __init__(self, title, description, taskindex, status):
        self.task_title = title
        self.task_description = description
        if taskindex == None and status == None:
            self.task_index = db_cursor.execute("SELECT MAX(TaskIndex) FROM tasks;").fetchone()[0]+1
        else:
            self.task_index = taskindex
            self.task_status = status

    def add(self):
        db_cursor.execute("INSERT INTO tasks VALUES (?,?,?,?);", (self.task_title, self.task_description, self.task_index, self.task_status))
        db.commit()

    def setDone(self):
        self.status = "Выполнена"
        db_cursor.execute("UPDATE tasks SET TaskStatus='Выполнена' WHERE TaskIndex=:index;", {"index":self.task_index})
        db.commit()

    def delete(self):
        db_cursor.execute("DELETE FROM tasks WHERE TaskIndex=:index;", {"index":self.task_index})
        db.commit()


def find(task_index):
    db_cursor.execute("SELECT * FROM tasks WHERE TaskIndex=:index", {"index":task_index})
    task_data = db_cursor.fetchone()
    return Task(task_data[0],task_data[1],task_data[2],task_data[3])


def getAllTasks():
    db_cursor.execute("SELECT * FROM tasks")
    return db_cursor.fetchall()
