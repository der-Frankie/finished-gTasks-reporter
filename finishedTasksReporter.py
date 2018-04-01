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

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/tasks-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/tasks.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Tasks API Python Quickstart'


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
    credential_path = os.path.join(credential_dir,
                                   'tasks-python-quickstart.json')
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
    """Shows basic usage of the Google Tasks API.

    Creates a Google Tasks API service object and outputs the first 10
    task lists.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    taskService = discovery.build('tasks', 'v1', http=http)

    today = datetime.today()
    sevenDaysAgo = today.replace(day=today.day - 7)

    results = taskService.tasklists().list(maxResults=10).execute()
    tasklists = results.get('items', [])
    if not tasklists:
        print('No task lists found.')
    else:
        print()
        taskList =  taskService.tasklists().get(tasklist='MDUwNjMxMTAzMzk3NDE2MjYzNTg6MDow').execute()
        print('Task list: ' + taskList['title'])

        tasks_allg = taskService.tasks().list(tasklist='MDUwNjMxMTAzMzk3NDE2MjYzNTg6MDow',
                showCompleted='true').execute()
        anzahl = 0
        tasks_allg_items =  tasks_allg['items']
        for task in tasks_allg_items:
            if task['status'] == 'completed':
                completedDateTime = datetime.strptime(task['completed'], '%Y-%m-%dT%H:%M:%S.%fZ')
                '''print ('    {0}'.format(completedDateTime)'''

                if (completedDateTime > sevenDaysAgo):
                    print ('Task:' + task['title'])
                    print ('    {0}'.format(task['completed']))
                    print ()
                    anzahl += 1

        print(' Es wurden {0} Tasks gefunden.'.format(anzahl))
        print(' Datum 7 Tage zurück lautet {0}.'.format(sevenDaysAgo))    
        print()

if __name__ == '__main__':
    main()
