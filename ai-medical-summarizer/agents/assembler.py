import logging
logger = logging.getLogger(__name__)


def assemble(docs: list, query: str) -> str:
    output = f"# 🔍 Query: {query}\n\n"
    for i, doc in enumerate(docs, 1):
        output += f"### 🧾 Paper {i}: {doc['title']}\n"
        output += f"**Type**: {doc.get('type')}\n\n"
        output += f"{doc.get('summary', 'No summary available')}\n\n"
        output += f"**Citation**: {doc['citation']}\n\n---\n\n"
    return output

def assembler_node(state: dict) -> dict:
    docs = state["docs"]
    query = state["query"]
    final = assemble(docs, query)
    state["final_output"] = final
    return state
