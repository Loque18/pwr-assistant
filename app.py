from api import rag_api
from api import llm_chat

from responses.rag_res import RagResponse

import enum

import streamlit as st
from pages.instructions import instructions_page as instructions_page 
from pages.main import main_page as chat_page

pages = {
    "Chat": [chat_page],
    "Instructions": [instructions_page]
}

pg = st.navigation(pages, position="hidden")
pg.run()
