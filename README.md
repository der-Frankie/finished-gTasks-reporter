# finished-gTasks-reporter

Short script for reporting finished tasks (from Google Tasks) in the last couple of days.

## Description

The code is based on the "quickstart.py" from the [Google Tasks API-Dokumentations](https://developers.google.com/google-apps/tasks/quickstart/python).
My goal was to have a nice little report of the thing's I finished the the last couple of days.
because from my point of view there's a lack of "easy" possible ways (e.g. via apps) to take a look on finished tasks. I think that could be helpful even as a feedback for somebody's self-assurance to get a feeling especially for the time with many personal/private project's (without the need of charging anyone for the time I spend).


## Requirements & Installation

It is highly recommanded to take a closer look at the 'Prerequisites'-Sektion of the [Google Tasks API-Dokumentations](https://developers.google.com/google-apps/tasks/quickstart/python) (so I don't have to write all the steps here).


## Usage

For help, use `-h` option.

```
$ finishedTasksReporter.py -h
usage: finishedTasksReporter.py [-h] [--auth_host_name AUTH_HOST_NAME]
                                   [--noauth_local_webserver]
                                   [--auth_host_port [AUTH_HOST_PORT [AUTH_HOST_PORT ...]]]
                                   [--logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                                   [N]

positional arguments:
  N                     Number of days for retrospected intervall

optional arguments:
  -h, --help            show this help message and exit
  --auth_host_name AUTH_HOST_NAME
                        Hostname when running a local web server.
  --noauth_local_webserver
                        Do not run a local web server.
  --auth_host_port [AUTH_HOST_PORT [AUTH_HOST_PORT ...]]
                        Port web server should listen on.
  --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set the logging level of detail.
```
