from sys import path
path.append('')

import model

def addTask(title, description):
    title = str(title)
    title = title.strip()

    description = str(description)
    description = description.strip()

    task = model.Task(title, description, None, None)
    task.add()

    return task.task_index


def setDone(task_index):
    task_index = int(task_index)
    task = find(task_index)
    task.setDone()
    return task

def getAllTasks():
    tasks_data = model.getAllTasks()
    if tasks_data[0][3]== 0:
        return 0

    tasks = []

    for task in tasks_data:
        task_in_list = model.Task(*task)
        tasks.append(task_in_list)
    return tasks


def find(task_index):
    task_index = int(task_index)
    return model.find(task_index)


def delete(task):
    task.delete()
