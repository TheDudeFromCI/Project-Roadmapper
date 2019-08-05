#!/usr/bin/python
import uuid

class TaskException(Exception):
    """
    Base class for all exceptions involving task manipulation.
    """

    """
    Creates a new task exception.

    Attributes:
        message -- The error message.
    """
    def __init__(self, message):
        self.message = message

class Task():
    """
    A task is the most basic building block for a project. It
    represents a single step, often built from many smaller steps
    which can be completed to accomplish a goal.
    """
    
    """
    Create a new task with the given name. The task is
    also given a randomly generated id.

    Attributes:
        name -- The name of the task.
        description -- The description of the task. Defaults to an empty
            string.
    """
    def __init__(self, name, description = ''):
        self.name = name
        self.description = description
        self.id = uuid.uuid4().hex
        self.dependencies = []
        self.parent = None
        self.steps = []
        self.complete = False

    """
    Sets this task to depend on another task. The other task
    must be completed first to finish this task. The other
    task does not need to be a decendent of this task, but
    cannot be an ancestor or create circular dependency
    references.

    Attributes:
        task -- The task this task should depend on.
    """
    def dependsOn(self, task):
        if task == None or task in self.dependencies:
            return
        
        self.dependencies.append(task)
        
        # TODO: Check for circular dependencies

    '''
    Assigns another task as a child of this task. If the
    task already has a parent, it is removed from that parent.
    If a circular recursion is detected, an error is thrown.

    Attributes:
        task -- The task which should be a subtask for this task.
    '''
    def hasStep(self, task):
        if task == None or task in self.steps:
            return

        p = task
        while p.parent != None:
            if p == self:
                raise TaskException('Subtask cannot be a parent of this task!')
            p = p.parent
        
        if task.parent != None:
            task.parent.steps.remove(task)

        task.parent = self
        self.steps.append(task)

class Timeline():
    """
    The timeline is the main project space in which all
    tasks live. A timeline may only have one root object,
    and all tasks must stem from it.
    """

    """
    Creates a new timeline instance.
    """
    def __init__(self):
        self.tasks = []

    """
    Checks if a task with the given name or id exists within this
    timeline. Here, either name or id can be used, but not both.
    If neither are given or both are, false is always returned.

    Attributes:
        name -- The name of the task to look for. (Optional)
        id -- The id of the task to look for. (Optional)
    """
    def hasTask(self, name = '', id = ''):
        if name == '' and id == '':
            return False
        if name != '' and id != '':
            return False

        for t in self.tasks:
            if (name != '' and t.name == name) or (id != '' and t.id == id):
                return True
        return False

    """
    Finds a task within this timeline by its name. If multiple
    tasks have the same name, the first task is returned. If
    this timeline does not contain a task with the given name,
    a new task is created and return

    Attributes:
        name -- The name of the task to look for.
    """
    def getTaskByName(self, name):
        for t in self.tasks:
            if t.name == name:
                return t

        t = Task(name)
        self.tasks.append(t)
        return t

    """
    Finds a task within this timeline by its id. If there
    is no task with the given id, None is returned.

    Attributes:
        id -- The id of the task to look for.
    """
    def getTaskById(self, id):
        for t in self.tasks:
            if t.id == id:
                return t
        return None

    """
    Deletes a task and all subtasks for that task. All
    references to the task within the timeline are also
    removed.

    Attributes:
        task -- The task to delete.
    """
    def delete(self, task):
        if task == None:
            return

        if task in self.tasks:
            self.tasks.remove(task)

        for t in self.tasks:
            if task in s.steps:
                s.steps.remove(task)
            if task in t.dependencies:
                t.dependencies.remove(task)

        for t in task.steps:
            self.delete(t)
