#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : test
# @Time         : 2022/3/25 下午4:36
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :



from fastapi import FastAPI, File, UploadFile, Request

from meutils.pipe import *
from meutils.decorators import backend

from appzoo import App

app = App()
app_ = app.app

task_result = {}

def do_task(s=3):
    logger.info(f'Task created')
    time.sleep(s)
    return s

@backend
def create_task(kwargs):
    task_id = kwargs.get('task_id', 1)
    s = int(kwargs.get('s', 1))
    task_result[task_id] = do_task(s)



def get_task_result(kwargs):
    return task_result

app.add_route_plus(create_task)
app.add_route_plus(get_task_result)


if __name__ == '__main__':

    # app.run()
    from paddlenlp import Taskflow

    ner = Taskflow('ner', entity_only=True)

    disk_cache(ner)