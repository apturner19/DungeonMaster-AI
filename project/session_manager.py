import os, sys, json, d20
from pathlib import Path
from typing import List, Dict, Any
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

import ollama
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter

from util.llm_utils import TemplateChat

def track_tools(fn):
    calls = defaultdict(list)
    def wrapper(*args, **kwargs):
        out = fn(*args, **kwargs)
        calls[fn.__name__].append({
          "args": args, "kwargs": kwargs, "result": out
        })
        print(f"[TOOL] {fn.__name__} → {out}")
        return out
    return wrapper

@track_tools
def roll_dice(notation: str, **kwargs) -> dict:
    # Roll the given dice notation and return the result
    result = d20.roll(notation)
    return {
        "notation": notation,
        "total": result.total,
        "detail": str(result)
    }

class KnowledgeBase:
    # Split a text file into chunks and index them
    def __init__(self, chunks: List[Dict[str, Any]], collection_name="RAG_context"):
        self.client = chromadb.Client()
        try:
            self.client.delete_collection(collection_name)
        except:
            pass
        self.coll = self.client.create_collection(
            name=collection_name,
            embedding_function=OllamaEmbeddingFn("nomic-embed-text")
        )
        self.coll.add(
            ids=[c["id"] for c in chunks],
            documents=[c["text"] for c in chunks],
            metadatas=[c["metadata"] for c in chunks]
        )

    def query(self, question: str, top_k: int = 3) -> List[str]:
        res = self.coll.query(query_texts=[question], n_results=top_k)
        return res.get("documents", [[]])[0]

def ingest_RAG_context(path: str, chunk_size=400, overlap=50) -> List[Dict[str,Any]]:
    # Split a .txt into smaller pieces for embeddings
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    text = open(path, encoding="utf-8").read()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=overlap, length_function=len
    )
    chunks = []
    for i, piece in enumerate(splitter.split_text(text)):
        chunks.append({
          "id": f"{os.path.basename(path)}_part_{i}",
          "text": piece,
          "metadata": {"source": os.path.basename(path), "part": i}
        })
    print(f"[RAG] {len(chunks)} chunks from {path}")
    return chunks

class OllamaEmbeddingFn:
    def __init__(self, model_name: str = "nomic-embed-text"):
        self.model_name = model_name

    def __call__(self, input: List[str]) -> List[List[float]]:
        resp = ollama.embed(model=self.model_name, input=input)
        return resp.embeddings


def run_session(
    template_file: str,
    session_id: str,
    RAG_path: str = None
):
    # Load LLM template
    chat = TemplateChat.from_file(template_file, sign=session_id)

    # Build RAG index
    kb = None
    if RAG_path:
        chunks = ingest_RAG_context(RAG_path)
        kb = KnowledgeBase(chunks)

    # Start conversation
    msg = chat.start_chat()
    print("DM:", msg)

    # Main loop
    while True:
        user_in = input("You: ")
        if user_in.lower() in ("/exit","/quit"):
            print("Session ended.")
            break

        # Prepend RAG context
        if kb:
            ctx = kb.query(user_in)
            user_in = "\n\n".join(ctx) + "\n\nPlayer: " + user_in

        # Send to LLM
        chat.messages.append({'role':'user','content':user_in})
        response = chat.chat_turn()
        message = response['message']

        # Handle any tool calls
        calls = getattr(message, "tool_calls", []) or []
        if calls:
            for call in calls:
                fn_name = call.function.name
                args = call.function.arguments
                result = globals()[fn_name](**args)
                # insert tool result
                chat.messages.append({
                    "role": "tool",
                    "name": fn_name,
                    "content": json.dumps(result)
                })
            # get follow up from LLM after tool output
            follow = chat.chat_turn()
            message = follow['message']

        # Print reply
        print("DM:", message.content)

if __name__ == "__main__":
    here = os.path.dirname(__file__)
    run_session(
        template_file=os.path.join(here, "dm_config.json"),
        session_id="DnD_DM",
        RAG_path=os.path.join(here, "classes_info.txt")
    )
