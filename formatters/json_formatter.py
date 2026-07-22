"""Default JSON response formatter."""

from core.contracts import OutputFormatter
from core.registry import register_plugin


@register_plugin("formatters", "default_json")
class DefaultJSONFormatter(OutputFormatter):
    def format(self, answer: str, context_chunks: list[str]) -> dict:
        return {"answer": answer, "context": context_chunks}

