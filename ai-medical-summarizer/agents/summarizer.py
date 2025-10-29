from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from data.doc_cache_utils import hash_doc_content, get_cached_doc, store_doc

import json
import logging
logger = logging.getLogger(__name__)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def summarize_document(doc: dict) -> dict:
    content = doc["content"][:3000]
    doc_type = doc.get("type", "research paper")

    prompt = [
        SystemMessage(content="You are a medical research summarizer."),
        HumanMessage(content=f"""
Summarize the following {doc_type} in the following example JSON format ONLY:

{{
  "type": "<restate the document type>",
  "causes": ["cause 1", "cause 2"]
  "key_findings": ["point 1", "point 2", "point 3"],
  "common treatment methods": [["method 1":"approach of the method"], ["method 2":"approach of the method"]],
  "limitations of certain treatments": ["limitation 1":"what is the alternate treatment", "limitation 2":"what is the alternate treatment"],
  "latest treatments": ["treatment 1":["proposed institution":"Mayo Clinic", "year of proposal":2019, approved_for_use:"Approved/ Under Trials", "treatment approach":"the treatment uses abc method..."], "treatment 2":["proposed institution":"Mayo Clinic", "year of proposal":2019, approved_for_use:"Approved/ Under Trials", "treatment approach":"the treatment uses abc method..."]]
  
}}

- Return **only valid JSON** (no markdown or commentary).
- Give a 250 words explanation for each key finding.
- 
- Each list should contain a max of 5 concise points.
- No field should be blank.
- Do NOT repeat content or headers.
- Do NOT include any citation in this response.
- Include at least 3 latest treatment if mentioned.
- Include up to 3 recent paper titles with links if available.
- do not hallucinate.
- every method, treatment type or whatever it is, must appear only once.
- generate answers only if there is a source available. do not make up treatments or any other methods

Document:
\"\"\"{content}\"\"\"
""")
    ]

    response = llm(prompt).content.strip()

    try:
        parsed = json.loads(response)
        doc["summary_json"] = parsed
    except json.JSONDecodeError:
        logger.warning("❌ Failed to parse JSON. Storing fallback raw text.")
        doc["summary_json"] = {
            "type": doc_type,
            "key_findings": [],
            "methods": [],
            "limitations": [],
            
            "raw": response
        }

    return doc

def summarizer_node(state: dict):
    docs = state["docs"]
    summarized = []

    for doc in docs:
        doc_hash = hash_doc_content(doc)
        cached = get_cached_doc(doc_hash)

        if cached and "summary_json" in cached:
            logger.info(f"[Summarizer] Cache hit: SHA={doc_hash}")
            doc["summary_json"] = cached["summary_json"]
        else:
            logger.info(f"[Summarizer] Generating summary: SHA={doc_hash}")
            doc = summarize_document(doc)

            store_doc(doc_hash, {
                "type": doc.get("type", ""),
                "summary_json": doc["summary_json"]
            })

        summarized.append(doc)

    state["docs"] = summarized
    logger.info("[SUCCESS] Stored all summaries in state['docs']")
    return state
