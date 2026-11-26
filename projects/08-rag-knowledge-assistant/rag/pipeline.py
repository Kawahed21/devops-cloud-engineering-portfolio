from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Protocol, Sequence


class Embedder(Protocol):
    def embed(self, text: str) -> Sequence[float]: ...


class Generator(Protocol):
    def answer(self, question: str, context: list[str]) -> str: ...


@dataclass(frozen=True)
class Chunk:
    source: str
    text: str
    vector: tuple[float, ...]


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right) or not left:
        raise ValueError("vectors must have the same non-zero dimension")
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)


def split_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    if chunk_size < 1 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("require chunk_size > overlap >= 0")
    words = text.split()
    chunks: list[str] = []
    step = chunk_size - overlap
    for start in range(0, len(words), step):
        chunk = " ".join(words[start : start + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks


class RagPipeline:
    def __init__(self, embedder: Embedder, generator: Generator) -> None:
        self.embedder = embedder
        self.generator = generator
        self.chunks: list[Chunk] = []

    def ingest(self, source: str, text: str, *, chunk_size: int = 500, overlap: int = 50) -> int:
        if not source.strip() or not text.strip():
            raise ValueError("source and text must not be empty")
        pieces = split_text(text, chunk_size, overlap)
        self.chunks.extend(
            Chunk(source, piece, tuple(self.embedder.embed(piece))) for piece in pieces
        )
        return len(pieces)

    def retrieve(self, question: str, *, top_k: int = 3) -> list[Chunk]:
        if not question.strip():
            raise ValueError("question must not be empty")
        if top_k < 1:
            raise ValueError("top_k must be positive")
        query_vector = self.embedder.embed(question)
        ranked = sorted(
            self.chunks,
            key=lambda item: cosine_similarity(query_vector, item.vector),
            reverse=True,
        )
        return ranked[:top_k]

    def ask(self, question: str, *, top_k: int = 3) -> dict[str, object]:
        matches = self.retrieve(question, top_k=top_k)
        context = [item.text for item in matches]
        return {
            "answer": self.generator.answer(question, context),
            "sources": sorted({item.source for item in matches}),
            "retrieved_chunks": len(matches),
        }
