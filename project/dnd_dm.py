import os
from session_manager import run_session

def start_dm():
    base = os.path.dirname(__file__)
    config = os.path.join(base, "dm_config.json")
    RAG_txt = os.path.join(base, "classes_info.txt")

    run_session(
        template_file = config,
        session_id = "DnD_DM",
        RAG_path = RAG_txt
    )

if __name__ == "__main__":
    start_dm()
