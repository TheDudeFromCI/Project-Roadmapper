#!/usr/bin/python

import os
import shlex
from tasks import Task
from tasks import Timeline
from tasks import TaskException
from projectfile import save
from projectfile import load

def log(output, line):
    output.append(line)
    print(line)

def parseCommand(main, command):
    output = []
    try:
        command = command.strip()
        if command == '':
            return False, output
        
        words = shlex.split(command)

        if words[0] == 'step': # Step
            
            if len(words) != 3:
                log(output, 'Unknown number of arguments!')
                return False, output

            try:
                task = main.timeline.getTaskByName(words[1])
                subtask = main.timeline.getTaskByName(words[2])
                task.hasStep(subtask)

                log(output, subtask.name + ' is now a subtask of ' + task.name)
                return True, output
            
            except TaskException as e:
                log(output, 'Failed to execute task!')
                log(output, '  ' + e.message)
                return False, output
            
        elif words[0] == 'dep': # Depends
            
            if len(words) != 3:
                log(output, 'Unknown number of arguments!')
                return False, output

            try:
                task = main.timeline.getTaskByName(words[1])
                subtask = main.timeline.getTaskByName(words[2])
                task.dependsOn(subtask)
                
                log(output, task.name + ' now depends on ' + subtask.name)
                return True, output
            
            except TaskException as e:
                log(output, 'Failed to execute task!')
                log(output, '  ' + e.message)
                return False, output

        elif words[0] == 'rn': # Rename
            
            if len(words) != 3:
                log(output, 'Unknown number of arguments!')
                return False, output

            try:
                task = main.timeline.getTaskByName(words[1])
                task.name = words[2]

                log(output, words[1] + ' has been renamed to ' + task.name)
                return True, output
            
            except TaskException as e:
                log(output, 'Failed to execute task!')
                log(output, '  ' + e.message)
                return False, output

        elif words[0] == 'del': # Delete
            
            if len(words) != 2:
                log(output, 'Unknown number of arguments!')
                return False, output

            try:
                if main.timeline.hasTask(name = words[1]):
                    task = main.timeline.getTaskByName(words[1])
                    main.timeline.delete(task)

                    log(output, task.name + ' has been deleted.')
                    return True, output
                
                else:
                    log(output, 'There is no task with that name!')
                    return False, output
            
            except TaskException as e:
                log(output, 'Failed to execute task!')
                log(output, '  ' + e.message)
                return False, output

        elif words[0] == 'save': # Save
            if len(words) != 2:
                log(output, 'Unknown number of arguments!')
                return False, output

            try:
                path = '../projects/' + words[1] + '.rmapp'
                save(main.timeline, path)
                
                log(output, 'Project saved to ' + path)
                return True, output
                
            except Exception as e:
                log(output, 'Failed to save timeline!')
                log(output, '  ' + str(e))
                return False, output
                
        elif words[0] == 'load': # Load
            if len(words) != 2:
                log(output, 'Unknown number of arguments!')
                return False, output

            try:
                path = '../projects/' + words[1] + '.rmapp'
                main.timeline = load(path)

                log(output, 'Timeline loaded from ' + path)
                return True, output
                
            except Exception as e:
                log(output, 'Failed to load timeline!')
                log(output, '  ' + str(e))
                return False, output

        elif words[0] == 'print': # Print
            if len(words) != 1:
                log(output, 'Unknown number of arguments!')
                return False, output

            try:
                log(output, 'Project Hierarchy:')
                printSceneRecursive(output, main.timeline.getRoot(), 0)

                return True, output
            
            except Exception as e:
                log(output, 'Failed to print timeline!')
                log(output, '  ' + str(e))
                return False, output

        elif words[0] == 'clear': # Clear
            if len(words) != 1:
                log(output, 'Unknown number of arguments!')
                return False, output

            try:
                main.console.clear()

                return True, output
            
            except Exception as e:
                log(output, 'Failed to clear console!')
                log(output, '  ' + str(e))
                return False, output

        log(output, 'Unknown command: ' + words[0])
        return False, output
    
    except Exception as e:
        log(output, 'Failed to parse command!')
        log(output, '  ' + str(e))
        return False, output

def printSceneRecursive(output, task, depth):
    if task == None:
        return
    
    log(output, '  ' * depth + task.name)

    for step in task.steps:
        printSceneRecursive(output, step, depth + 1)
