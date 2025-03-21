from api import rag_api
from api import llm_chat

from responses.rag_res import RagResponse

import enum

import streamlit as st
from pages.instructions_page import instructions
from pages.main import main_page 

pages = {
    "Chat": [st.Page(main_page, default=True, icon="🤖", title="PWR Assistant")],
    "Instructions": [st.Page(instructions, url_path="instructions", icon="📄", title="Instructions")]
}

pg = st.navigation(pages, position="hidden")
pg.run()
