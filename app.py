# built in modules
import logging
import requests
import random
import time
import json
import os 

from api import rag_api
from api import llm_chat

from responses.rag_res import RagResponse


# 3rd party imports
import streamlit as st

API_URL = "http://209.38.157.244:8000"

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
prompt = st.chat_input("Ask anything...", disabled=st.session_state.is_streaming)

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
    st.session_state.conversation.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        documents = rag_api({"prompt": prompt, "top_k": 3})

        ctx = get_context_from_docs(documents)

        full_prompt = f"""you are an expert in blockchain develpment\n\n only answer questions related to blockchain or the context provided, answer the user question using the following context:\n\n{ctx}\n\n user question: {prompt}"""
        
        body = {"prompt": full_prompt, "model": 'deepseek-chat'}
        stream = llm_chat(body)
        response = st.write_stream(stream)
        
        # stream = llm_chat()

    st.session_state.conversation.append({"role": "assistant", "content": response})
    st.rerun()

# first mirror user input
if prompt:
    on_user_prompt(prompt)




# if prompt and not st.session_state.is_streaming:
#     st.session_state.conversation.append({"role": "user", "content": prompt})

#     with st.chat_message("user"):
#         st.markdown(prompt)

#     try:
#         body = {"prompt": prompt, "top_k": 3}
#         context = ""
#         response = requests.post(f"{API_URL}/rag/context", json=body)  # GET contexto
#         if response.status_code == 200:
#             documents = response.json()  # 🔥 Parseamos los documentos

#             docs = []
#             for i, doc in enumerate(documents):
#                 header = f"---- chunk {i+1} ----"
#                 name = doc.get("name", "")
#                 source = doc.get("source", "")
#                 cosine_similarity = doc.get("distance", 0)
#                 text = doc.get("text", "")



#                 s = f"{header}\n\n**Name**: {name}\n\n**Source**: {source}\n\n**Cosine Similarity**: {cosine_similarity}\n\n**Text**: {text}"
#                 docs.append(s)
        
#             context = "\n\n".join(docs)
#         else:
#             print(f"Failed to fetch context, status: {response.status_code}")
#     except Exception as e:
#         print(f"Error fetching context: {e}")


#     answer_format = f"source: <source>\n\n response <response>"


#     # 🔥 Formatear el prompt con el contexto
#     full_prompt = f"""you are an expert in blockchain develpment\n\n only anser questions related to blockchain or the context provided, answer the user question using the following context:\n\n{context}\n\n user question: {prompt}"""

#     body = {"prompt": full_prompt}
#     with st.chat_message("assistant"):
#         def stream_response():
#             st.session_state.is_streaming = True
#             with requests.post(f"{API_URL}/llm/chat", json=body, stream=True) as stream:
#                 for chunk in stream.iter_lines():
#                     if chunk:
#                         try:
#                             chunk_decoded = chunk.decode("utf-8").strip()
                            
#                             # Ensure only valid JSON chunks are processed
#                             if chunk_decoded.startswith("data: "):
#                                 chunk_decoded = chunk_decoded[6:]  # Remove "data: "
                            
#                             json_chunk = json.loads(chunk_decoded)  # Convert to JSON
#                             message = json_chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")

#                             if message:
#                                 yield message  # Send incremental updates
#                         except json.JSONDecodeError as e:
#                             print(f"JSON Decode Error: {e}, Raw Chunk: {chunk_decoded}")  # Debugging info

#         response_text = st.write_stream(stream_response())  # Stream messages dynamically

#     st.session_state.conversation.append({"role": "assistant", "content": response_text})

#     st.session_state.is_streaming = False
#     st.rerun()  # Refresh UI for next input

