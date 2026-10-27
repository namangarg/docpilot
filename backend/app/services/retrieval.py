import math
import re
from collections import Counter
from dataclasses import dataclass

_TOKEN = re.compile(r"[a-z0-9]+") 
_STOPWORDS = {"a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "he", "in", "is", "it", "its", "of", "on", "that", "the", "to", "was", "were", "will", "with"}


def tokenize(text: str) -> list[str]:
    return [t for t in _TOKEN.findall(text.lower()) if t not in _STOPWORDS]

@dataclass
class Hit:
    document_id: str
    document_title:str
    chunk_index: int
    text: str
    score:float

def search(docs: list[dict], query:str, top_k:int) -> list[Hit]:
    q_terms = set(tokenize(query))
    entries = [
        (doc, i, chunk, Counter(tokenize(chunk)))
         for doc in docs
         for i, chunk in enumerate(doc["chunks"])
    ]

    # entries [
        #   ({'title': 'A', 'chunks': ['red red blue', 'green']}, 0, 'red red blue', Counter({'red': 2, 'blue': 1})),
    #   ({'title': 'A', 'chunks': ['red red blue', 'green']}, 1, 'green', Counter({'green': 1})),
        # ]


    if not q_terms or not entries:
        return []   

    n = len(entries)
    df = Counter()
    for *_, tf in entries:
        df.update(set(tf) & q_terms)

    print("q_terms:", q_terms)
    print("entries:", len(entries))
    print("df:", df)
    hits = []
    for doc, idx , text , tf in entries:
        score = sum(
                    (1 + math.log(tf[t])) * (math.log((n + 1) / (df[t] + 1)) + 1)
                    for t in q_terms
                    if tf[t]
                )
        if score > 0:
            hits.append(Hit(doc["id"], doc["title"], idx, text, round(score, 4)))

    hits.sort(key=lambda h: h.score, reverse=True)
    return hits[:top_k]
