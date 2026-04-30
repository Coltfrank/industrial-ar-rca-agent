from app.core.models import ActionPlan


class ActionAgent:
    def __init__(self, max_auto_retry: int = 1):
        self.max_auto_retry = max_auto_retry

    def plan(self, root_cause_result, signal_context: dict):
        top = root_cause_result.top_cause
        title = top.title.lower()

        if "jam" in title:
            return ActionPlan(
                severity="NEED_OPERATOR_CONFIRMATION",
                rationale="Likely mechanical jam. A blind reset may worsen equipment risk.",
                steps=[
                    "Confirm transfer zone has no jammed workpiece",
                    "Clear obstruction under lockout/tagout policy if required",
                    "Clean sensor PE_14 and confirm indicator changes correctly",
                    "Reset alarm and retry one cycle only",
                    "Escalate maintenance if alarm recurs",
                ],
                escalation="Escalate to maintenance if repeated within 3 cycles",
                auto_reset_allowed=False,
            )

        if "sensor" in title:
            return ActionPlan(
                severity="AUTO_RECOVERABLE",
                rationale="Sensor contamination can often be resolved quickly after inspection.",
                steps=[
                    "Inspect and clean PE_14",
                    "Verify IO input transition in HMI/PLC diagnostics",
                    f"Allow up to {self.max_auto_retry} reset attempt after confirmation",
                ],
                escalation="Escalate to electrical technician if no input change",
                auto_reset_allowed=True,
            )

        return ActionPlan(
            severity="REQUIRE_STOPPAGE",
            rationale="Cause confidence is low or safety-related conditions are present.",
            steps=[
                "Stop affected station",
                "Verify safety interlocks, pressure, and actuator status",
                "Call maintenance engineer for on-site inspection",
            ],
            escalation="Immediate maintenance intervention required",
            auto_reset_allowed=False,
        )
