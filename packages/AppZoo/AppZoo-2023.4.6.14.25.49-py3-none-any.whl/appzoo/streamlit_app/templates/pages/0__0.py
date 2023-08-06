import streamlit as st

from appzoo.streamlit_app import Page

from meutils.pipe import *

class SPage(Page):

    def main(self):
        uploaded_file = st.sidebar.file_uploader("请上传一张图片")


        Path('a.png').write_bytes(uploaded_file.read())


SPage(menu_items={'about': "hi"}).main()
