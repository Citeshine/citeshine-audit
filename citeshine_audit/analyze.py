import re
from urllib.parse import urlparse

def find_pos(text, names):
    t = text.lower(); hits = [t.find(n.lower()) for n in names if n and t.find(n.lower()) >= 0]
    return min(hits) if hits else -1

def list_rank(text, names):
    """Rank in a numbered/bulleted list if the brand appears in one, else None."""
    items = [l for l in text.splitlines() if re.match(r"\s*(\d+[.)、]|[-*•])\s+", l)]
    for i, l in enumerate(items, 1):
        if find_pos(l, names) >= 0: return i
    return None

def analyze_answer(text, citations, brand, competitors, brand_domain):
    entities = {"__brand__": [brand["name"], *brand.get("aliases", []), brand_domain]}
    for c in competitors: entities[c["name"]] = [c["name"], *c.get("aliases", [])]
    found = {k: find_pos(text, v) for k, v in entities.items()}
    mentioned = [k for k, p in sorted(found.items(), key=lambda x: x[1]) if p >= 0]
    domains = [urlparse(u).netloc.removeprefix("www.") for u in citations if u]
    return {"brand_mentioned": found["__brand__"] >= 0,
            "brand_order": (mentioned.index("__brand__") + 1) if "__brand__" in mentioned else None,
            "brand_list_rank": list_rank(text, entities["__brand__"]),
            "mentioned": mentioned, "cited_domains": domains,
            "brand_domain_cited": any(brand_domain in d for d in domains)}
