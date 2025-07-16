import os
import json
import hashlib

DOC_CACHE_PATH = "data/doc_cache.json"

def load_doc_cache():
    if not os.path.exists(DOC_CACHE_PATH):
        return {}
    try:
        with open(DOC_CACHE_PATH, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # File is empty or corrupt
        return {}

def save_doc_cache(cache: dict):
    with open(DOC_CACHE_PATH, "w") as f:
        json.dump(cache, f, indent=2)

def hash_doc_content(doc: dict) -> str:
    content = doc.get("content", "").strip().lower()
    return hashlib.sha256(content.encode()).hexdigest()

def get_cached_doc(doc_hash: str):
    cache = load_doc_cache()
    return cache.get(doc_hash, None)

def store_doc(doc_hash: str, result: dict):
    cache = load_doc_cache()
    cache[doc_hash] = result
    save_doc_cache(cache)
