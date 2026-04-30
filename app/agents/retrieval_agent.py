from app.utils.retriever import SimpleKeywordRetriever
from app.core.models import RetrievedDoc


class RetrievalAgent:
    def __init__(self, knowledge_root: str):
        self.retriever = SimpleKeywordRetriever(knowledge_root)

    def retrieve(self, signal_context: dict):
        query_parts = [
            signal_context.get("alarm_code", ""),
            signal_context.get("alarm_message", ""),
            signal_context.get("station", ""),
            " ".join(signal_context.get("plc_map", {}).keys()),
            " ".join([a["action"] for a in signal_context.get("recent_actions", [])]),
        ]
        query = " ".join([x for x in query_parts if x])
        docs = self.retriever.search(query, top_k=6)
        return [RetrievedDoc(**d) for d in docs]
