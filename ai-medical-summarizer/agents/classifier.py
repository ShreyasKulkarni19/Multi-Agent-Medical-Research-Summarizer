from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from data.doc_cache_utils import hash_doc_content, get_cached_doc, store_doc

import logging
logger = logging.getLogger(__name__)


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def classify_document(doc: dict) -> dict:
    content = doc["content"][:2000]
    prompt = [
        SystemMessage(content="You are a medical paper classifier. You give the top 3 to top 5 research papers which are most recent. These papers are closely related to the question."),
        HumanMessage(content=f"Classify the following as clinical trial, meta-analysis, review, or case study:\n\n{content}")
    ]
    result = llm(prompt).content.lower().strip()
    doc["type"] = result
    return doc



def classifier_node(state: dict):
    docs = state["docs"]
    classified = []

    for doc in docs:
        doc_hash = hash_doc_content(doc)
        cached = get_cached_doc(doc_hash)

        if cached and "type" in cached:
            doc["type"] = cached["type"]
        else:
            # Classify using LLM
            content = doc["content"][:2000]
            prompt = [
                SystemMessage(content="You are a medical research classifier."),
                HumanMessage(content=f"Classify this document:\n{content}")
            ]
            result = llm(prompt).content.lower().strip()
            doc["type"] = result

            store_doc(doc_hash, {"type": result})

        classified.append(doc)

    state["docs"] = classified
    return state

