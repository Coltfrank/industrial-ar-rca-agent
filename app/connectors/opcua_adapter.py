class OPCUAAdapter:
    """Stub adapter for future integration.

    Replace with a real OPC UA client in production.
    """

    def read_snapshot(self, endpoint: str, tags: list[str]) -> dict:
        return {tag: "N/A" for tag in tags}
