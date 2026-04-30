from __future__ import annotations
from pathlib import Path
from typing import List, Dict
import json
import re


def _tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z0-9_-]+", text.lower()))


class SimpleKeywordRetriever:
    def __init__(self, knowledge_root: str):
        self.knowledge_root = Path(knowledge_root)
        self.docs = self._load_docs()

    def _load_docs(self) -> List[Dict]:
        docs = []

        for p in (self.knowledge_root / "manuals").glob("*.md"):
            text = p.read_text(encoding="utf-8")
            docs.append({"source": "manual", "title": p.stem, "text": text, "path": str(p)})

        for p in (self.knowledge_root / "sop").glob("*.md"):
            text = p.read_text(encoding="utf-8")
            docs.append({"source": "sop", "title": p.stem, "text": text, "path": str(p)})

        case_file = self.knowledge_root / "cases" / "historical_cases.json"
        if case_file.exists():
            data = json.loads(case_file.read_text(encoding="utf-8"))
            for item in data:
                docs.append({
                    "source": "case",
                    "title": item["case_id"],
                    "text": json.dumps(item, ensure_ascii=False),
                    "path": str(case_file),
                })
        return docs

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        q = _tokenize(query)
        results = []
        for doc in self.docs:
            d = _tokenize(doc["text"] + " " + doc["title"])
            if not d:
                continue
            overlap = len(q & d)
            if overlap == 0:
                continue
            score = overlap / max(len(q), 1)
            snippet = doc["text"][:400].replace("\n", " ")
            results.append({
                "source": doc["source"],
                "title": doc["title"],
                "snippet": snippet,
                "score": round(score, 3),
                "metadata": {"path": doc["path"]},
            })
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
