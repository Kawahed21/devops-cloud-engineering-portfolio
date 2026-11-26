import pytest

from rag.pipeline import RagPipeline, cosine_similarity, split_text


class TinyEmbedder:
    def embed(self, text):
        lower = text.lower()
        return [float("cloud" in lower), float("database" in lower), 1.0]


class EchoGenerator:
    def answer(self, question, context):
        return f"Question: {question}; context: {' | '.join(context)}"


def build_pipeline():
    return RagPipeline(TinyEmbedder(), EchoGenerator())


def test_split_text_overlap_and_validation():
    assert split_text("a b c d e", chunk_size=3, overlap=1) == ["a b c", "c d e"]
    with pytest.raises(ValueError):
        split_text("x", chunk_size=2, overlap=2)


def test_ingest_retrieve_and_answer_with_sources():
    rag = build_pipeline()
    rag.ingest("cloud-guide.md", "Cloud networking uses VPC and subnets.", chunk_size=20, overlap=5)
    rag.ingest("db-guide.md", "Database backups should be encrypted.", chunk_size=20)
    result = rag.ask("cloud networking", top_k=1)
    assert result["sources"] == ["cloud-guide.md"]
    assert result["retrieved_chunks"] == 1
    assert "Cloud networking" in result["answer"]


def test_cosine_rejects_dimension_mismatch():
    with pytest.raises(ValueError):
        cosine_similarity([1, 2], [1])


def test_empty_question_rejected():
    with pytest.raises(ValueError):
        build_pipeline().retrieve(" ")
