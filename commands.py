#!/usr/bin/python

import shlex
from tasks import Task
from tasks import Timeline
from tasks import TaskException
from projectfile import save
from projectfile import load

def parseCommand(main, command):
    try:
        command = command.strip()
        if command == '':
            return False
        
        words = shlex.split(command)

        if words[0] == 'stp': # Step
            
            if len(words) != 3:
                print('Unknown number of arguments!')
                return False

            try:
                task = main.timeline.getTaskByName(words[1])
                subtask = main.timeline.getTaskByName(words[2])
                task.hasStep(subtask)

                print(subtask.name + ' is now a subtask of ' + task.name)
                return True
            
            except TaskException as e:
                print('Failed to execute task!')
                print('  ' + e.message)
                return False
            
        elif words[0] == 'dep': # Depends
            
            if len(words) != 3:
                print('Unknown number of arguments!')
                return False

            try:
                task = main.timeline.getTaskByName(words[1])
                subtask = main.timeline.getTaskByName(words[2])
                task.dependsOn(subtask)
                
                print(task.name + ' now depends on ' + subtask.name)
                return True
            
            except TaskException as e:
                print('Failed to execute task!')
                print('  ' + e.message)
                return False

        elif words[0] == 'ren': # Rename
            
            if len(words) != 3:
                print('Unknown number of arguments!')
                return False

            try:
                task = main.timeline.getTaskByName(words[1])
                task.name = words[2]

                print(words[1] + ' has been renamed to ' + task.name)
                return True
            
            except TaskException as e:
                print('Failed to execute task!')
                print('  ' + e.message)
                return False

        elif words[0] == 'del': # Delete
            
            if len(words) != 2:
                print('Unknown number of arguments!')
                return False

            try:
                if main.timeline.hasTask(name = words[1]):
                    task = main.timeline.getTaskByName(words[1])
                    main.timeline.delete(task)

                    print(task.name + ' has been deleted.')
                    return True
                
                else:
                    print('There is no task with that name!')
                    return False
            
            except TaskException as e:
                print('Failed to execute task!')
                print('  ' + e.message)
                return False

        elif words[0] == 'save': # Save
            if len(words) != 2:
                print('Unknown number of arguments!')
                return False

            try:
                path = words[1] + '.rmapp'
                save(main.timeline, path)
                
                print('Project saved to ' + path)
                return True
                
            except Exception as e:
                print('Failed to save timeline!')
                print('  ' + str(e))
                return False
                
        elif words[0] == 'load': # Load
            if len(words) != 2:
                print('Unknown number of arguments!')
                return False

            try:
                path = words[1] + '.rmapp'
                main.timeline = load(path)

                print('Timeline loaded from ' + path)
                return True
                
            except Exception as e:
                print('Failed to load timeline!')
                print('  ' + str(e))
                return False

        elif words[0] == 'print': # Print
            if len(words) != 1:
                print('Unknown number of arguments!')
                return False

            try:
                print('Project Hierarchy:')
                printSceneRecursive(main.timeline.getRoot(), 0)

                return True
            
            except Exception as e:
                print('Failed to print timeline!')
                print('  ' + str(e))
                return False

        print('Unknown command: ' + words[0])
        return False
    
    except Exception as e:
        print('Failed to parse command!')
        print('  ' + str(e))
        return False

def printSceneRecursive(task, depth):
    if task == None:
        return
    
    print('  ' * depth + task.name)

    for step in task.steps:
        printSceneRecursive(step, depth + 1)
