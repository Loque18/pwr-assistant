import streamlit as st
import requests
from api import get_instructions, upload_instrunctions
import bcrypt

def instructions():

    password = st.secrets["password"]

    # chec if queryparams contains p param
    param = st.query_params.get("p")

    if not param or not bcrypt.checkpw(param.encode(), password.encode()):
        st.error("You are not authorized to view this page. Please contact the administrator.")
        return


    # if not st.query_params["p"] and not st.query_params["p"] == "instructions":
    #     st.error("You are not authorized to view this page. Please contact the administrator.")
    #     return

    st.set_page_config(page_title="Instructions", layout="centered")
    st.title("📄 Pwr assistant intructions")

    # Function to fetch and display markdown from server
    def load_markdown():
        try:
            response = get_instructions()
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Failed to load markdown: {e}")

    # Upload new markdown file
    uploaded_file = st.file_uploader("Upload your Markdown file", type=["md", "txt"])



    def upload_to_server():
        with st.spinner("Uploading file..."):
            success, message = upload_instrunctions(uploaded_file)
            if success:
                st.success(message)
            else:
                st.error(message)
            


    upload = st.button("Upload", on_click=upload_to_server)


    st.subheader("📖 Currenct instructions")
    load_markdown()