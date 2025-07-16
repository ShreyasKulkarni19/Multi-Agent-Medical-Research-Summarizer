from graph_config import compiled
from data.cache_utils import get_cached_result, store_result_in_cache

from logging_config import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)


def run_pipeline(query: str):
    logger.info(f"Running pipeline for query: {query}")
    cached = get_cached_result(query)

    if cached:
        
        logger.info(f"[CACHE] Query hit: {query}")
        print(f"[🧠] Loaded cached result for query: {query}")
        print(cached["final_output"])
        return cached["final_output"]

    logger.info(f"[GRAPH] Running full pipeline for query: {query}")
    print(f"[+] Running graph for new query: {query}")
    initial_state = {"query": query}
    result = compiled.invoke(initial_state)

    logger.info("storing result in cache...")
    store_result_in_cache(query, result)
    print(result["final_output"])
    
    logger.info("stored result in cache")
    return result["final_output"]

if __name__ == "__main__":
    run_pipeline("What are the latest treatments for Alzheimer's?")
