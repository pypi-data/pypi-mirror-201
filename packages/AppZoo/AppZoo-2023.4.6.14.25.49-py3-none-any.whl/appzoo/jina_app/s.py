#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : Python.
# @File         : s
# @Time         : 2023/3/7 上午9:57
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from jina import DocumentArray, Executor, Flow, requests


class FooExec(Executor):
    @requests
    async def add_text(self, docs: DocumentArray, **kwargs):
        for d in docs:
            d.text += 'hello, world!'


class BarExec(Executor):
    @requests
    async def add_text(self, docs: DocumentArray, **kwargs):
        for d in docs:
            d.text += 'goodbye!'


f = Flow(port=12345).add(uses=FooExec, replicas=3).add(uses=BarExec, replicas=2)

with f:
    f.block()