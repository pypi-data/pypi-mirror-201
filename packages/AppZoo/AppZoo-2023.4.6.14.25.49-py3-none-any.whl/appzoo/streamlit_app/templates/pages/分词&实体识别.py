#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : Python.
# @File         : 分词
# @Time         : 2022/12/7 上午8:46
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :


from meutils.pipe import *
from appzoo.streamlit_app import Page

import streamlit as st

from LAC import LAC as _LAC

LAC = st.experimental_singleton(_LAC, show_spinner=False)
LAC()  # 初始化

ner2name = {
    'n': '普通名词',
    'f': '方位名词',
    's': '处所名词',
    't': '时间',
    'nr': '人名',
    'ns': '地名',
    'nt': '机构名',
    'nw': '作品名',
    'nz': '其他专名',
    'v': '普通动词',
    'vd': '动副词',
    'vn': '名动词',
    'a': '形容词',
    'ad': '副形词',
    'an': '名形词',
    'd': '副词',
    'm': '数量词',
    'q': '量词',
    'r': '代词',
    'p': '介词',
    'c': '连词',
    'u': '助词',
    'xc': '其他虚词',
    'w': '标点符号',
    'PER': '人名',
    'LOC': '地名',
    'ORG': '机构名',
    'TIME': '时间'
}


@ttl_cache(key=str)
@disk_cache()
def tokenizer(texts):
    return LAC().run(texts) | xmap_(lambda r: list(zip(r[0], map(ner2name.get, r[1]))))


class MyPage(Page):

    def main(self):
        with st.form("Coding"):

            texts = st.text_area("输入文本", ["永远相信美好的事情即将发生"] * 3 | xjoin('\n')).split("\n")

            if st.form_submit_button('开始转换'):
                _ = tokenizer(texts)

                from annotated_text import annotated_text, annotation

                for w2n_list in _:
                    annotated_text(*w2n_list)

                with st.expander('详情'):
                    st.dataframe(pd.DataFrame(_))


if __name__ == '__main__':
    app_title = f"# {Path(__file__).name.split('.')[0]}"
    app_info = ""
    MyPage(
        app_title=app_title,
        app_info=app_info,
        layout="wide",
        initial_sidebar_state="collapsed"
    ).main()
