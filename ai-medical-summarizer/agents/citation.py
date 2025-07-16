import logging
logger = logging.getLogger(__name__)

def build_citation(doc: dict) -> dict:
    doc["citation"] = f"[{doc['title']}]({doc['link']})"
    return doc

def citation_node(state: dict) -> dict:
    docs = state["docs"]
    state["docs"] = [build_citation(doc) for doc in docs]
    return state
