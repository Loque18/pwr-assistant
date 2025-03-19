from api import rag_api
from api import llm_chat

from responses.rag_res import RagResponse

import enum

import streamlit as st

st.markdown(
    r"""
    <style>
    .stDeployButton {
            visibility: hidden;
        }
    </style>
    """, unsafe_allow_html=True
)

class ModelEnum(enum.Enum):
    DEEPSEEK_CHAT = "deepseek-chat"
    DEEPSEEK_R1 = "deepseek-reasoner"

# 3rd party imports

API_URL = "https://pwragent-api.pwrlabs.io"

# set app title
st.title("PWR Assistant")


# chat history
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "is_streaming" not in st.session_state:
    st.session_state.is_streaming = False

# display messages
for message in st.session_state.conversation:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# user input

prompt = st.chat_input("Ask anything...")

def get_context_from_docs(documents: list[RagResponse]):

    docs = []
    for i, doc in enumerate(documents):
        header = f"---- chunk {i+1} ----"
        name = doc.get("name", "")
        source = doc.get("source", "")
        cosine_similarity = doc.get("distance", 0)
        text = doc.get("text", "")

        s = f"{header}\n\n**Name**: {name}\n\n**Source**: {source}\n\n**Cosine Similarity**: {cosine_similarity}\n\n**Text**: {text}"
        docs.append(s)
    
    return "\n\n".join(docs)

def on_user_prompt(prompt: str):
    st.session_state.is_streaming = True
    st.session_state.conversation.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                documents = rag_api({"prompt": prompt, "top_k": 3})

                ctx = get_context_from_docs(documents)

                full_prompt = f"""you are an expert in blockchain develpment\n\n only answer questions related to blockchain or the context provided, answer the user question using the following context:\n\n{ctx}\n\n user question: {prompt}"""

                body = {"prompt": full_prompt, "model": "deepseek-reasoner"}
                stream = llm_chat(body)
                response = st.write_stream(stream)

            except Exception as e:
                print('error')
                response = f"There was an error processing your request: {e}"
            finally:
                st.session_state.is_streaming = False
        
        # stream = llm_chat()

    st.session_state.conversation.append({"role": "assistant", "content": response})
    st.rerun()

# first mirror user input
if prompt:
    on_user_prompt(prompt)

