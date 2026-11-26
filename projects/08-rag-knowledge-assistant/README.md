# 08 — RAG Knowledge Assistant

## Objective
A provider-agnostic retrieval-augmented generation (RAG) pipeline with chunking, embedding abstraction, cosine-similarity retrieval, top-k context selection, answer generation and source attribution.

## Data flow
1. Ingest a text document and split it into overlapping chunks.
2. Generate an embedding for each chunk through the Embedder interface.
3. Store chunk text, source identifier and vector.
4. Embed a user question and rank chunks by cosine similarity.
5. Pass the top-k retrieved context to a Generator.
6. Return the generated answer and source identifiers.

## Run tests
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

## Provider integration
The tests use deterministic fake embedder and generator implementations, so CI needs no API key and makes no paid requests. A production adapter can implement the Embedder and Generator protocols using an approved embedding/model provider and replace the in-memory list with a vector database (pgvector, OpenSearch or a managed vector service).

## Production hardening checklist
- [ ] Use a persistent vector store with tenant-level access controls.
- [ ] Add document parsing, MIME/type validation, malware scanning and size limits.
- [ ] Encrypt source documents and embeddings at rest and in transit.
- [ ] Add prompt-injection defenses: retrieved text is untrusted data, never system instructions.
- [ ] Enforce authorization before retrieval; do not rely on vector similarity for access control.
- [ ] Evaluate retrieval precision/recall, groundedness, citation correctness and latency.
- [ ] Add deletion propagation when a source document is removed.

## Limitations
This is a tested RAG core, not a deployed chatbot. The in-memory vector index is for demonstration and is not persistent or horizontally scalable. Provider adapters and cloud hosting are separate projects.
