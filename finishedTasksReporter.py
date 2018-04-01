#!/usr/bin/env python3

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from datetime import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
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
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Requests via the Google Tasks API the available task lists (max. 10)
    and iterates over them to determine the finished tasks during the
    last 7 days and reporting them as console output.
    """

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    taskService = discovery.build('tasks', 'v1', http=http)

    numberOfDays = 7
    today = datetime.today()
    sevenDaysAgo = today.replace(day = today.day - numberOfDays)
    overallTasks = 0

    results = taskService.tasklists().list(maxResults=10).execute()
    taskLists = results.get('items', [])
    if not taskLists:
        print('No task lists found.')
    else:
        print()
        print('Übersicht abgeschlossener Tasks seit dem {0} (letzte {1} Tage):'
                .format(sevenDaysAgo.date().strftime("%d.%m.%Y"), numberOfDays))    
        print()
        
        for taskList in taskLists:
            currentListItems = 0

            tasks_allg = taskService.tasks().list(tasklist=taskList['id'],
                    showCompleted='true').execute()
            tasks_allg_items =  tasks_allg['items']
            for task in tasks_allg_items:
                if task['status'] == 'completed':
                    completedDateTime = datetime.strptime(task['completed'],
                            '%Y-%m-%dT%H:%M:%S.%fZ')

                    '''print ('    {0}'.format(completedDateTime)'''

                    if (completedDateTime > sevenDaysAgo):
                        print ('+  "{0}" (Liste: "{1}") wurde am {2} abgeschlossen.'
                                .format(task['title'], taskList['title'], 
                                    completedDateTime.date().strftime("%d.%m.%Y")))
                        print ()
                        currentListItems += 1

            if currentListItems == 0:
                print('-  Keine abgeschlossene Aufgabe auf der Liste "{0}".'
                        .format(taskList['title']))            
                print ()                
            overallTasks += currentListItems

    print('Es wurden {0} abgeschlossene Tasks gefunden.'.format(overallTasks))
    print()

if __name__ == '__main__':
    main()
