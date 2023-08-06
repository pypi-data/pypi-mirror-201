#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : Python.
# @File         : c
# @Time         : 2023/3/7 上午9:57
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from jina import Client, DocumentArray

c = Client(port=12345)
r = c.post('/', DocumentArray.empty(10))
print(r.texts)