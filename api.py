import requests
import json

from dto.rag_dto import RagDto
from responses.rag_res import RagResponse

from dto.llm_dto import LlmChatDto
from constants import API_URL


api = {
    'rag': {
        'get_context': f'{API_URL}/rag/context',
    }
}


def rag_api(dto: RagDto) -> list[RagResponse]:
    # TODO use async aiohttp to avoid blocking the main thread
    response =  requests.post(api['rag']['get_context'], json=dto)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch context, status: {response.status_code}")
    
def llm_chat(dto: LlmChatDto):
    with requests.post(f"{API_URL}/llm/chat", json=dto, stream=True) as stream:
        for chunk in stream.iter_lines():    
            if chunk:
                try:
                    chunk_decoded = chunk.decode("utf-8").strip()

                    if chunk_decoded.startswith("[DONE]"):
                        break
                    
                    # Ensure only valid JSON chunks are processed
                    if chunk_decoded.startswith("data: "):
                        chunk_decoded = chunk_decoded[6:]  # Remove "data: "
                    
                    json_chunk = json.loads(chunk_decoded)  # Convert to JSON
                    message = json_chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")

                    if message:
                        yield message  # Send incremental updates

                except json.JSONDecodeError as e:
                    print(f"JSON Decode Error: {e}, Raw Chunk: {chunk_decoded}")  # Debugging info
    

def get_instructions():
    try:
        res = requests.get(f"{API_URL}/files/instructions.md")
        res.raise_for_status()
        return res
    except Exception as e:
        return f"Failed to load instructions: {e}"
    
def upload_instrunctions(file):
    try:
        files = [('files', ('instructions.md', file.getvalue(), 'text/markdown'))]
        res = requests.post(f"{API_URL}/files", files=files)
        res.raise_for_status()
        return True, "File uploaded successfully!"
    except Exception as e:
        return False, f"Upload failed: {e}"
