import json
import time
from threading import Lock

import urllib3

authUrl = "https://autosolve-dashboard-api.aycd.io/api/v1/auth/generate-token"
apiUrl = "https://autosolve-api.aycd.io/api/v1"
tasksUrl = apiUrl + "/tasks"
tasksCreateUrl = tasksUrl + "/create"
tasksCancelUrl = tasksUrl + "/cancel"

Success = "success"
Cancelled = "cancelled"

ReCaptchaV2Checkbox = 0
ReCaptchaV2Invisible = 1
ReCaptchaV3 = 2
HCaptchaCheckbox = 3
HCaptchaInvisible = 4
GeeTest = 5
ReCaptchaV3Enterprise = 6
ReCaptchaV2Enterprise = 7
FunCaptcha = 8
GeeTestV4 = 9
TextImageCaptcha = 10

http = urllib3.PoolManager()
session_map = {}
session_map_lock = Lock()


class Session:
    def __init__(self, api_key):
        self.api_key = api_key
        self.debug = False
        self.auth_lock = Lock()
        self.token_expires_at = 0
        self.token = None
        self.tasks = {}
        self.tasks_lock = Lock()
        self.tasks_fetch_at = 0

    def enable_debug(self):
        self.debug = True

    def disable_debug(self):
        self.debug = False

    def solve(self, task_req, timeout):
        if self.__send(task_req, tasksCreateUrl):
            return self.__wait_for_task(task_req["taskId"], timeout)
        else:
            return None

    def cancel_many_tasks(self, task_ids):
        cancel_req = {"taskIds": task_ids}
        return self.__send(cancel_req, tasksCancelUrl)

    def cancel_all_tasks(self):
        cancel_req = {}
        return self.__send(cancel_req, tasksCancelUrl)

    def __send(self, obj, url):
        body = json.dumps(obj)
        resp = self.__do('POST', url, body)
        if resp is None or not is_status_2xx(resp.status):
            return False
        return True

    def __do(self, method, url, body):
        self.auth_lock.acquire()
        try:
            if self.token_expires_at <= time.time():
                self.__log("new auth token is required.")
                self.__refresh_auth_token()
        except Exception as e:
            self.token_expires_at = time.time() + 60
            self.__log("failed to send request: " + str(e))
        finally:
            self.auth_lock.release()
        if self.token is None:
            self.__log("auth token is not available.")
            return None
        headers = {'Authorization': 'Token ' + self.token}
        if body is not None:
            headers['Content-Type'] = 'application/json'
        return http.request(method, url, body=body, headers=headers)

    def __log(self, msg):
        if self.debug:
            print(msg)

    def __refresh_auth_token(self):
        self.__log("refreshing auth token...")
        url = authUrl + "?apiKey=" + self.api_key
        resp = http.request('GET', url)
        if not is_status_2xx(resp.status):
            raise Exception("failed to get auth token")
        data = json.loads(resp.data.decode('utf-8'))
        self.token = data["token"]
        self.token_expires_at = data['expiresAt']
        self.__log("new auth token is generated with expires_at: " + str(self.token_expires_at))

    def __wait_for_task(self, task_id, timeout):
        start_time = time.time()
        time.sleep(5)
        delay = 5
        while True:
            try:
                delay = self.__fetch_tasks()
                if task_id in self.tasks:
                    task_resp = self.tasks[task_id]
                    self.tasks[task_id] = None
                    return task_resp
            except Exception as e:
                self.__log("failed to fetch tasks: " + str(e))
            if time.time() - start_time > timeout:
                if not self.cancel_many_tasks([task_id]):
                    self.__log("failed to cancel task: " + task_id)
                return None
            time.sleep(delay)

    def __fetch_tasks(self):
        self.tasks_lock.acquire()
        next_fetch_delay = 5
        try:
            if self.tasks_fetch_at <= time.time():
                resp = self.__do('GET', tasksUrl, None)
                if resp is None:
                    self.__log("failed to fetch tasks")
                elif is_status_2xx(resp.status):
                    data = json.loads(resp.data.decode('utf-8'))
                    for task in data:
                        self.tasks[task["taskId"]] = task
                    if len(data) >= 100:
                        next_fetch_delay = 1
                    self.tasks_fetch_at = time.time() + next_fetch_delay
                    self.__log("fetched tasks: " + str(len(data)) + " with next fetch delay: " + str(next_fetch_delay))
                else:
                    self.__log("failed to fetch tasks with status: " + str(resp.status))
        except Exception as e:
            self.__log("failed to fetch tasks: " + str(e))
        finally:
            self.tasks_lock.release()
        return next_fetch_delay


def new_session(api_key):
    session_map_lock.acquire()
    try:
        if api_key in session_map:
            return session_map[api_key]
        session = Session(api_key)
        session_map[api_key] = session
        return session
    finally:
        session_map_lock.release()


def is_status_2xx(status):
    return 200 <= status < 300
