#!/usr/bin/python

import os.path
from tasks import Timeline
from tasks import Task

"""
This function will save a timeline to a file which can
be loaded from at a later point in time.

Attributes:
    timeline -- The timeline to save.
    path -- The path of the file to save to.
"""
def save(timeline, path):
    file = open(path, 'w')
    
    for task in timeline.tasks:
        file.write('t:' + task.id + '\n')
        file.write('name=' + task.name + '\n')
        file.write('description=' + task.description + '\n')
        file.write('dependencies=[' + ', '.join(x.id for x in task.dependencies) + ']\n')
        file.write('steps=[' + ', '.join(x.id for x in task.steps) + ']\n')
        file.write('complete=' + str(task.complete) + '\n')

    file.close()

"""
This function will load a timeline from the given path,
if the path exists. If the path does not exist or an error
is thrown while opening it, an empty timeline is returned
instead.

Attributes:
    path -- The path of the file to load.
"""
def load(path):
    try:
        file = open(path, 'r')
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        file.close()
    except:
        lines = []
    
    timeline = Timeline()

    for line in lines:
        if line.startswith('t:'):
            task = timeline.getTaskById(line[2:])
            
        elif line.startswith('name='):
            task.name = line[5:]
            
        elif line.startswith('description='):
            task.description = line[12:]

        elif line.startswith('dependencies='):
            if line[14:-1] != '':
                list = line[14:-1].split(', ')
                for id in list:
                    dep = timeline.getTaskById(id)
                    task.dependencies.append(dep)

        elif line.startswith('steps='):
            if line[7:-1] != '':
                list = line[7:-1].split(', ')
                for id in list:
                    step = timeline.getTaskById(id)
                    task.steps.append(step)
                    step.parent = task

        elif line.startswith('complete='):
            task.complete = bool(line[9:])
                
    return timeline
