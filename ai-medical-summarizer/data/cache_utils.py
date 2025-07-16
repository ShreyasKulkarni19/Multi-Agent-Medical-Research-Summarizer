import os
import json
import hashlib

CACHE_PATH = "data/cached_docs.json"

def load_cache():
    if not os.path.exists(CACHE_PATH):
        return {}
    try:
        with open(CACHE_PATH, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # File is empty or corrupt
        return {}


def save_cache(cache: dict):
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f, indent=2)

def hash_query(query: str) -> str:
    return hashlib.sha256(query.strip().lower().encode()).hexdigest()

def get_cached_result(query: str):
    cache = load_cache()
    qhash = hash_query(query)
    return cache.get(qhash, None)

def store_result_in_cache(query: str, state: dict):
    cache = load_cache()
    qhash = hash_query(query)
    # Save only relevant parts
    cache[qhash] = {
        "query": query,
        "docs": state.get("docs", []),
        "final_output": state.get("final_output", "")
    }
    save_cache(cache)
