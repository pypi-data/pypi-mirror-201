# Copyright 2018-2022 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st

st.set_page_config(
    page_title="🧠",
    page_icon="🧠",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    # 智能应用 👋
    
    ## 语音
    - 语音识别：支持【实时语音识别】，【端到端识别】，【音频文件识别】三种模式
    - 语音合成：支持【流式合成】与【端到端合成】两种方式
    - 语音聊天：语音识别能力+语音合成能力，对话部分基于NLP的闲聊功能
    - 语音指令：语音识别 + NLP的信息抽取，实现通信费的智能报销
    - 声纹识别

"""
)

st.image('/Users/yuanjie/Desktop/ai.jpeg', width=256)
