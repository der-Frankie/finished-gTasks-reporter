#!/usr/bin/env python3

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from datetime import datetime
from datetime import timedelta

try:
    import argparse
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    parser.add_argument('integers', metavar='N', type=int, nargs='?', default=7,
                        help='Number of days for retrospected intervall')

    flags = parser.parse_args()

    numberOfDays = flags.integers
    #print ('Eingabe: {0}'.format(numberOfDays))
    
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/tasks.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Weekly Report for finished Google Tasks'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, CLIENT_SECRET_FILE)
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        #print('Storing credentials to ' + credential_path)
    return credentials


def outputToConsole(finishedTasksDict, dateString):    
    taskCounter = 0

    # checken, ob len(finishedTasksDict > 0)
    if not finishedTasksDict:
        print('No finished tasks were found.')
    else:
        print()
        print('Übersicht abgeschlossener Tasks in den letzten {0} Tagen (seit dem {1}):'
                .format(numberOfDays, dateString))    
        print()
     
        '''Iteration über die Aufgaben'''
        for task in finishedTasksDict.values():
            print ('"{0}" (Liste: "{1}") wurde am {2} abgeschlossen.'
                .format(task[0], task[1], task[2]))            
            taskCounter += 1
        print('Es wurden {0} abgeschlossene Tasks gefunden.'.format(taskCounter))
        print()


def determineFinishedTasks(taskService):
    """Requests via the Google Tasks API the available task lists 
    (limited through the value of 'maxNumberOfTaskLists')
    and iterates over them to determine the finished tasks during the
    last days (given as parameter!) and reporting them as console output.
    """
    maxNumberOfTaskLists = 10
    today = datetime.today()
    dateSomeDaysAgo = today - timedelta(days=numberOfDays)

    results = taskService.tasklists().list(maxResults=maxNumberOfTaskLists).execute()
    taskLists = results.get('items', [])
    
    if not taskLists:
        skip
        #print('No task lists found.')
    else:
        tasks = {}
        dateString = dateSomeDaysAgo.date().strftime("%d.%m.%Y")
        
        for taskList in taskLists:
            currentTaskList = taskService.tasks().list(tasklist=taskList['id'],
                    showCompleted='true').execute()
            currentTaskList_items =  currentTaskList['items']
            for task in currentTaskList_items:
                if task['status'] == 'completed':
                    completedDateTime = datetime.strptime(task['completed'],
                            '%Y-%m-%dT%H:%M:%S.%fZ')
                    if (completedDateTime > dateSomeDaysAgo):
                        task = {task['id'] : (task['title'], taskList['title'], 
                                    completedDateTime.date().strftime("%d.%m.%Y"))}
                        tasks.update(task)
    
    outputToConsole(tasks, dateString)


def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    taskService = discovery.build('tasks', 'v1', http=http)
    determineFinishedTasks(taskService)


if __name__ == '__main__':
    main()
