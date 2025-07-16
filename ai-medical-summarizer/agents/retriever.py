from tavily import TavilyClient
import os
from dotenv import load_dotenv
load_dotenv()

import logging
logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

def retriever_node(state: dict) -> dict:
    query = state["query"]
    results = client.search(query=query, include_raw_content=True, max_results=3)
    
    documents = []
    for item in results["results"]:
        documents.append({
            "title": item["title"],
            "link": item["url"],
            "content": item.get("content", ""),
            "source": item["url"]
        })
    
    state["docs"] = documents
    logger.info("Stored documents to state['docs]")
    return state

