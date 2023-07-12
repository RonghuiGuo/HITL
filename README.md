
演示记录:

Please generate a web page with a random roll call function.


Problems:

model由gpt-3.5-turbo改成gpt-3.5-turbo-0613后结果会发生很大的变化


ERROR:

可能是此bug导致log框输出不了

https://github.com/gradio-app/gradio/issues/2290
https://github.com/gradio-app/gradio/issues/2261
https://github.com/gradio-app/gradio/issues/4061

future: <Task finished name='oqhjdrbdel_15' coro=<Queue.process_events() done, defined at /home/user/.local/lib/python3.10/site-packages/gradio/queueing.py:342> exception=ValueError('[<gradio.queueing.Event object at 0x7febc752c820>] is not in list')>
Traceback (most recent call last):
  File "/home/user/.local/lib/python3.10/site-packages/gradio/queueing.py", line 369, in process_events
    while response.json.get("is_generating", False):
  File "/home/user/.local/lib/python3.10/site-packages/gradio/utils.py", line 543, in json
    return self._json_response_data
AttributeError: 'AsyncRequest' object has no attribute '_json_response_data'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/user/.local/lib/python3.10/site-packages/gradio/queueing.py", line 424, in process_events
    self.active_jobs[self.active_jobs.index(events)] = None
ValueError: [<gradio.queueing.Event object at 0x7febc752c820>] is not in list



/home/user/.local/lib/python3.10/site-packages/gradio/queueing.py

line 425

change

"""
self.active_jobs[self.active_jobs.index(events)] = None
"""

to

"""
try:
    self.active_jobs[self.active_jobs.index(events)] = None
except Exception:
    pass
"""



