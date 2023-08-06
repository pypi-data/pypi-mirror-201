#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : page
# @Time         : 2022/9/22 下午2:19
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://zhuanlan.zhihu.com/p/547200679


import streamlit as st
from appzoo.streamlit_app.utils import hide_st_style


class Page(object):

    def __init__(self, app_title="# App Title",
                 app_info="",
                 page_title="AI",  # "Page Title",
                 page_icon='🔥',
                 menu_items=None,
                 layout="centered",  # wide
                 initial_sidebar_state="auto",  # "auto" or "expanded" or "collapsed"
                 footer_content="Made with Betterme"
                 ):
        # 前面不允许有 streamlit 指令
        st.set_page_config(
            page_title=page_title,
            page_icon=page_icon,
            menu_items=menu_items,
            layout=layout,
            initial_sidebar_state=initial_sidebar_state,
        )

        # 隐藏streamlit默认格式信息 https://discuss.streamlit.io/t/st-footer/6447/11
        if hide_st_style: hide_st_style(footer_content)
        if app_title: st.markdown(app_title)
        if app_info: st.markdown(app_info)

    def main(self):
        raise NotImplementedError('Method not implemented!')


if __name__ == '__main__':
    class SPage(Page):

        def main(self):
            st.markdown("这是个`main`函数")


    SPage().main()
