from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from data.doc_cache_utils import hash_doc_content, get_cached_doc, store_doc

import logging
logger = logging.getLogger(__name__)


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def summarize_document(doc: dict) -> dict:
    content = doc["content"][:3000]
    doc_type = doc.get("type", "research paper")
    
    prompt = [
        SystemMessage(content=f"You are a medical summarizer. Summarize this {doc_type} with key findings, methods, and limitations if any. You give the top 3 to top 5 research papers which are most recent. These papers are closely related to the question. You never hallucinate. You are the best medical researcher."),
        HumanMessage(content=content)
    ]
    summary = llm(prompt).content.strip()
    doc["summary"] = summary
    return doc

def summarizer_node(state: dict):
    docs = state["docs"]
    summarized = []

    for doc in docs:
        doc_hash = hash_doc_content(doc)
        cached = get_cached_doc(doc_hash)

        if cached and "summary" in cached:
            logger.info("[Classifier] Cache hit for document")
            doc["summary"] = cached["summary"]
        else:
            # Summarize using LLM
            content = doc["content"][:3000]
            doc_type = doc.get("type", "research paper")
            prompt = [
                SystemMessage(content=f"You are a medical summarizer. Summarize this {doc_type} with key findings, methods, and limitations."),
                HumanMessage(content=content)
            ]
            summary = llm(prompt).content.strip()
            doc["summary"] = summary

            # Store in cache
            store_doc(doc_hash, {
                "type": doc.get("type", ""),
                "summary": summary
            })

        summarized.append(doc)

    state["docs"] = summarized
    logger.info("Stored the simmarized information to state['docs']")
    return state

