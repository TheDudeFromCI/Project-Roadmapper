#!/usr/bin/python

import shlex
from tasks import Task
from tasks import Timeline
from tasks import TaskException

def parseCommand(command):
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
                
                task = timeline.getTaskByName(words[1])
                subtask = timeline.getTaskByName(words[2])
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
                task = timeline.getTaskByName(words[1])
                subtask = timeline.getTaskByName(words[2])
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
                task = timeline.getTaskByName(words[1])
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
                if timeline.hasTask(name = words[1]):
                    task = timeline.getTaskByName(words[1])
                    timeline.delete(task)

                    print(task.name + ' has been deleted.')
                    return True
                else:
                    print('There is no task with that name!')
                    return False
            
            except TaskException as e:
                print('Failed to execute task!')
                print('  ' + e.message)
                return False

        print('Unknown command: ' + words[0])
        return False
    
    except:
        print('Failed to parse command!')
        return False

if __name__ == '__main__':
    global timeline
    timeline = Timeline()

    # Parse Raw Input
    while True:
        line = input('> ')

        if line == 'exit':
            break
        
        parseCommand(line)
