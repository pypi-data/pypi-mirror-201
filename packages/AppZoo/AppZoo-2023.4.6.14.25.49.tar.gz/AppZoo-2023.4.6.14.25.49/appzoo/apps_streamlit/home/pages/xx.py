import streamlit as st
from streamlit.hello.utils import show_code
import inspect
import textwrap


class Page(object):

    def __init__(self, app_title="# App Title",
                 app_info="> App Info",
                 sidebar_title="## Sidebar Title",
                 page_title="Page Title",
                 page_icon='🔥',
                 menu_items=None,
                 show_code=False
                 ):
        st.set_page_config(
            page_title=page_title,
            page_icon=page_icon,
            initial_sidebar_state='auto',
            menu_items=menu_items
        )

        if app_title: st.markdown(app_title)
        if app_info: st.markdown(app_info)
        if sidebar_title: st.sidebar.markdown(sidebar_title)

        if sidebar_title and show_code: self.show_code(self.main)

    def main(self):
        raise NotImplementedError('Method not implemented!')

    def show_code(self, demo):
        """Showing the code of the demo."""
        _ = st.sidebar.checkbox("Show code", False)
        if _:
            # Showing the code of the demo.
            st.markdown("---")
            st.markdown("## Main Code")
            sourcelines, _ = inspect.getsourcelines(demo)
            st.code(textwrap.dedent("".join(sourcelines[1:])))
            st.markdown("---")



class SPage(Page):

    def main(self):
        st.markdown("这是个`main`函数")


SPage(sidebar_title='').main()
