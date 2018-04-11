#!/usr/bin/env python3

from __future__ import print_function
import httplib2
import os
import json

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

except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/tasks.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Report for finished Google Tasks'


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
    return credentials


def outputToConsole(finishedTasksAsList, deadlineDate):
    """Reporting the finished tasks as console output
    """
    if not finishedTasksAsList:
        print('No finished tasks were found.')
    else:
        print()
        dateString = deadlineDate.date().strftime("%d.%m.%Y")
        print('Übersicht abgeschlossener Tasks in den letzten {0} Tagen (seit dem {1}):'
                .format(numberOfDays, dateString))
        for currentTask in finishedTasksAsList:
            completedDateTime = getCompletionDateTime(currentTask)
            print ('"{0}" wurde am {1} abgeschlossen.'.format(currentTask['title'],
                completedDateTime.date().strftime("%d.%m.%Y")))
        print('Es wurden {0} abgeschlossene Tasks gefunden.'.format(len(finishedTasksAsList)))
        print()


def outputToJson(finishedTasksAsList):
    """Writes all the content of the given dictionary to a JSON-file
    """
    if not finishedTasksAsList:
        print('No taskslists were found so none were written.')
    else:
        ts_now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        with open('myTasks_{0}.json'.format(ts_now), "w") as file:
            json.dump(finishedTasksAsList, file, indent=4 * ' ')
        file.close()
        print('All found tasks written to: {0}'.format(file.name))


        print('Es wurden {0} abgeschlossene Tasks gefunden.'.format(len(finishedTasksAsList)))
        

def getCompletionDateTime(task):
    """Determine a dateTime-Object from a given String
    """
    completedDateTime = datetime.strptime(task['completed'], '%Y-%m-%dT%H:%M:%S.%fZ')
    return completedDateTime


def getDeadlineDate():
    today = datetime.today()
    deadlineDate = today - timedelta(days=numberOfDays)
    return deadlineDate


def filterFinishedTasks(tasks_dict, deadlineDate):
    """Iterates over the tasklists in the dict to filter out the finished tasks
    during the last days (given as parameter!).
    """
    finished_tasks = []

    if not tasks_dict:
        print('No task lists found.')

    else:
        for taskList in tasks_dict.values():
            for currentTask in taskList:
                if currentTask['status'] == 'completed':
                    completedDateTime = getCompletionDateTime(currentTask)
                    if (completedDateTime > deadlineDate):
                        finished_tasks.append(currentTask)
    return finished_tasks


def determineAllTasks(taskService):
    """Requests through the Google Tasks API the available task lists,
    iterates over them to determine all the tasks and returns all as a dictionary
    """
    dict_of_tasklists = {}
    results = taskService.tasklists().list().execute()
    taskLists = results.get('items', [])

    if not taskLists:
        print('No task lists found.')
    else:
        number_of_tasks = 0

        for taskList in taskLists:
            currentTaskList = taskService.tasks().list(tasklist=taskList['id'],
                    showCompleted='true').execute()
            dict_of_tasklists[taskList['id']] =  currentTaskList['items']
            number_of_tasks += len(currentTaskList['items'])

        print('Es wurden insgesamt {0} Aufgaben in {1} Listen gefunden.'
                .format(number_of_tasks, len(dict_of_tasklists)))
        return dict_of_tasklists


def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    taskService = discovery.build('tasks', 'v1', http=http)
    dictTasklists = determineAllTasks(taskService)
    deadlineDate = getDeadlineDate()
    finishedTasks = filterFinishedTasks(dictTasklists, deadlineDate)
    outputToConsole(finishedTasks, deadlineDate)
    outputToJson(finishedTasks)


if __name__ == '__main__':
    main()
