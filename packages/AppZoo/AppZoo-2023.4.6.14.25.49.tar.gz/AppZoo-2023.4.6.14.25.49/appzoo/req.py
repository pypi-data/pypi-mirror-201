#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : Python.
# @File         : req
# @Time         : 2022/10/27 下午1:40
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *

print(requests.post('http://0.0.0.0:9955/file-uploader',
                    files={'files': open('./main.py')}, json={}
                    ).json())