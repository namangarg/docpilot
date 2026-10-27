import asyncio
from collections.abc import AsyncIterator
from typing import Protocol

from app.services.retrieval import Hit


class LLMProvider(Protocol):
    def stream_answer(self, question: str, context: list[Hit]) -> AsyncIterator[str]: ...


class FakeLLM:
    """Streams an extractive 'answer' built from the best chunk, word by word."""

    def __init__(self, delay: float = 0.0) -> None:
        self._delay = delay

    async def stream_answer(self, question: str, context: list[Hit]) -> AsyncIterator[str]:
        if not context:
            answer = "I couldn't find anything relevant in your documents."
        else:
            best = context[0]
            answer = f"Based on '{best.document_title}': {best.text}"
        for word in answer.split():
            if self._delay:
                await asyncio.sleep(self._delay)
            yield word + " "