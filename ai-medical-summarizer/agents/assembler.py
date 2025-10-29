import logging
logger = logging.getLogger(__name__)


import logging
logger = logging.getLogger(__name__)

def assemble_json(docs: list, query: str) -> dict:
    return {
        "query": query,
        "papers": [
            {
                "title": doc["title"],
                "link": doc["link"],
                "type": doc.get("type", ""),
                "summary": doc.get("summary_json", {}),
                "citation": doc.get("citation", "")
            } for doc in docs
        ]
    }



def assembler_node(state: dict) -> dict:
    docs = state["docs"]
    query = state["query"]
    final = assemble_json(docs, query)
    state["final_output"] = final
    return state

