from pathlib import Path
from app.agents.signal_agent import SignalAgent
from app.agents.retrieval_agent import RetrievalAgent
from app.agents.reasoning_agent import ReasoningAgent
from app.agents.action_agent import ActionAgent
from app.agents.postmortem_agent import PostmortemAgent
from app.core.models import DiagnosisResponse
from app.core.config import settings


class DiagnosisOrchestrator:
    def __init__(self):
        knowledge_root = str(Path(__file__).resolve().parents[1] / "knowledge")
        self.signal_agent = SignalAgent()
        self.retrieval_agent = RetrievalAgent(knowledge_root)
        self.reasoning_agent = ReasoningAgent(knowledge_root)
        self.action_agent = ActionAgent(max_auto_retry=settings.auto_reset_max_retry)
        self.postmortem_agent = PostmortemAgent()

    def run(self, event):
        signal_context = self.signal_agent.collect(event)
        docs = self.retrieval_agent.retrieve(signal_context)
        root_cause = self.reasoning_agent.infer(signal_context, docs)
        action_plan = self.action_agent.plan(root_cause, signal_context)
        report = self.postmortem_agent.generate(event, root_cause, action_plan)

        return DiagnosisResponse(
            alarm_code=root_cause.alarm_code,
            alarm_message=root_cause.alarm_message,
            root_cause=root_cause.top_cause.model_dump(),
            alternatives=[c.model_dump() for c in root_cause.alternatives],
            severity=action_plan.severity,
            recommended_actions=action_plan.steps,
            report_id=report.report_id,
            retrieved_knowledge=[d.model_dump() for d in root_cause.evidence_docs],
        )
