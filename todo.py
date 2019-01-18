#!/usr/bin/python
import sys, getopt
import json
import os

# Define data
# data = {'title':'Todo - cli', 
#        'description': 'desc',
#        'todos': [
#                {'id':1, 'todo':'todo1', 'priority': 0},
#                {'id':2, 'todo':'todo2', 'priority': 1}
#                ]
#        } 
#

def writeJson(data):
    with open('todo.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False)

def readJson():
    with open('todo.json') as data_file:
        return json.load(data_file)

def readAll():
    data_loaded = readJson()
    
    title = data_loaded['title']
    description = data_loaded['description']
    
    print('---------------------\n{0} - {1}\n---------------------'.format(title, description))
    
    todos = data_loaded['todos']
    for t in todos:
        id = t['id']
        todo = t['todo']
        priority = t['priority']
        print('{0:3} [{2}]: {1}'.format(id, todo, priority))

def lastId(todos):
    maxId = -1
    for t in todos:
        id = t['id']
        if (maxId < id):
            maxId = id
    return maxId

def verifyPriority(priority):
    try:
        priority = int(priority)
    except ValueError:
        print('Alert: Priority range 0-9')
        exit()
        
    if not ((priority >= 0) and (priority <= 9)):
        print('Alert: Priority range 0-9')
        exit()
    return priority

def saveTodo(todo, priority):
    data_loaded = readJson()
    
    title = data_loaded['title']
    description = data_loaded['description']
    todos = data_loaded['todos']
    todos.append({'id':lastId(todos)+1, 'todo':todo, 'priority': priority})
    
    data = {'title':title, 
            'description': description,
            'todos': todos
        }
    writeJson(data)

def checkFileJson(fileJson):
    return os.path.isfile(fileJson)

def deleteTodo(did):
    data_loaded = readJson()
    
    title = data_loaded['title']
    description = data_loaded['description']
    todos = data_loaded['todos']
    todosDeleted = []
    
    for t in todos:
        id = t['id']
        todo = t['todo']
        priority = t['priority']
        if not(str(did)==str(id)):
            todosDeleted.append({'id':id, 'todo':todo, 'priority': priority})
        
    data = {'title':title, 
            'description': description,
            'todos': todosDeleted
        }
    writeJson(data)

def main(argv):
    if not (checkFileJson('todo.json')):
        # Set title and decription
        print("New Todo list")
        title = input("Title: ")
        description = input("Description: ")
        todos = []
        data = {'title':title, 
            'description': description,
            'todos': todos
        }
        writeJson(data)
    action = ''
    todo = ''
    priority = 0
    help = 'python todo.py \n Add todo \t -a <todo description> \n Set Priority \t -p <priority 0-9> \n Delete \t -d <id>'
    try:
        opts, args = getopt.getopt(argv,"ha:p:d:",["atodo=","ppriority=","did="])
    except getopt.GetoptError:
        print(help)
        sys.exit(2)
    for opt, arg in opts:
        if ((opt == '-h') or (opt == '-help')):
            print(help)
            sys.exit()
        elif opt in ("-a", "--ttodo"):
            action = 'add'
            todo = arg
        elif opt in ("-p", "--ppriority"):
            priority = arg
        elif opt in ("-d", "--did"):
            action = 'delete'
            did = arg
          
    if (action=='add'):
        if not todo=='':
            priority = verifyPriority(priority)
            saveTodo(str(todo), priority)
    elif (action=='delete'):
        deleteTodo(did)
         
    readAll()
   
if __name__ == "__main__":
   main(sys.argv[1:])