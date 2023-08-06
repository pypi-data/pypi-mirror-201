#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : main
# @Time         : 2022/6/14 下午2:01
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from fastapi import FastAPI, File, UploadFile, Request

from meutils.pipe import *
from appzoo import App

app = App()
app_ = app.app


# app.add_route('/get', lambda **kwargs: kwargs, method="GET", result_key="GetResult")
# app.add_route('/post', lambda **kwargs: kwargs, method="POST", result_key="PostResult")
#
# app.add_route_plus('/post_test', lambda **kwargs: kwargs, method="POST")
#
# from fastapi import FastAPI, Form, Depends, File, UploadFile, Body, Request, Path
#
# def proxy_app_(kwargs: dict):
#     logger.info(kwargs)
#     print(kwargs)
#     r = requests.request(**kwargs)
#     return r.json()
#
#
# app.add_route_plus(proxy_app_, methods=["GET", "POST"], data=None)

# def file_uploader(kwargs):
#     bio = kwargs['files'][0]
#     return bio.read()
#
# app.add_route_plus(file_uploader, methods="POST")


@app.post('/a')
async def file_uploader(file: UploadFile = File(...)):
    logger.debug(file)
    df = pd.read_excel(await file.read())
    logger.debug(df)


@app.post('/b')
def file_uploader(file: bytes = File(...)):
    logger.debug(file)
    df = pd.read_excel(file)
    logger.debug(df)


if __name__ == '__main__':
    app.run(app.app_from(__file__), port=9955, debug=True)

    # app.gunicorn_run()
