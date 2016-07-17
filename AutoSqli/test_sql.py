

import sys
import os
import requests
import json
import time


class AutoSqlmapAPI(object):

    def __init__(self):
        self.headers = {
                'Content-Type': 'application/json'
                }
        self.server = 'http://127.0.0.1:8775'


    def new_task(self):

        new_task = '/task/new'
        url = self.server + new_task

        try:
            response = json.loads(requests.get(url).text)
            if response and response['success'] == True:
                print time.strftime('%Y-%m-%d %H:%M:%S') + ' new task successfully...'
                return response['taskid']

        except Exception, ex:
            print ex

        return False


    def set_options(self, taskid):

        data = {
                'url': 'http://www.chinesetest.cn/gosign.do?id=1&lid=0',
                'level':3
                }

        url = self.server + '/option/{taskid}/set'.format(taskid=taskid)
        try:
            response = requests.post(url, data=json.dumps(data), headers=self.headers)
            if response:
                response = json.loads(response.text)
            return response['success']
        except Exception, ex:
            print ex

    def get_options(self, taskid):

        url = self.server + '/option/{taskid}/list'.format(taskid=taskid)
        # response = requests.post(url, data=json.dumps({}), headers=self.headers)
        response = requests.get(url)#, data=json.dumps({}), headers=self.headers)

        response = json.loads(response.text)
        print response



    def start_task(self, taskid):

        if self.set_options(taskid):

            url = self.server + '/scan/{taskid}/start'.format(taskid=taskid)
            response = requests.post(url, data=json.dumps({}), headers=self.headers)
            # print response.text


    def task_status(self, taskid):

        url = self.server + '/scan/{taskid}/status'.format(taskid=taskid)
        # url = self.server + '/scan/{taskid}/log'.format(taskid=taskid)
        while True:
            response = requests.get(url)
            print response.text
            time.sleep(10)


def main():
    autoapi = AutoSqlmapAPI()
    # taskid = autoapi.new_task()
    # autoapi.start_task(taskid)
    # autoapi.task_status(taskid)
    taskid='eb631f8b0e88d628'
    # autoapi.task_status(taskid)
    autoapi.get_options(taskid)


if __name__ == '__main__':
    os.system('clear')

    main()
