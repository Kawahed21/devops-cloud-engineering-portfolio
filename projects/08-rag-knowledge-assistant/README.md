# 08 — RAG Knowledge Assistant

## Objective
A retrieval-augmented generation pipeline with chunking, an embedding abstraction, cosine-similarity retrieval, top-k context selection, grounded answer generation and source attribution. Optional OpenAI adapters provide real embeddings and generation while the tests remain deterministic.

## Data flow
1. Ingest a text document and split it into overlapping chunks.
2. Generate an embedding for each chunk.
3. Store chunk text, source identifier and vector.
4. Embed a user question and rank chunks by cosine similarity.
5. Pass top-k context to the generator with an instruction to treat retrieved text as untrusted reference data.
6. Return the answer and source identifiers.

## Run tests
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

## Optional OpenAI integration
Set `OPENAI_API_KEY` in the environment, then construct `OpenAIEmbedder` and `OpenAIGenerator` from `rag.openai_adapters`. The embedding adapter defaults to `text-embedding-3-small`; generation defaults to `gpt-4.1-mini`. API calls can incur charges. CI tests mock HTTP responses and never require credentials or call a paid endpoint.

## Production hardening checklist
- [ ] Use a persistent vector store with tenant-level access controls.
- [ ] Add document parsing, MIME/type validation, malware scanning and size limits.
- [ ] Encrypt source documents and embeddings at rest and in transit.
- [ ] Treat retrieved text as untrusted data; never allow it to override system instructions.
- [ ] Enforce authorization before retrieval; do not rely on vector similarity for access control.
- [ ] Evaluate retrieval precision/recall, groundedness, citation correctness and latency.
- [ ] Add deletion propagation when a source document is removed.
- [ ] Add rate limits, token budgets, retries and provider timeouts.

## Limitations
The included vector index is in-memory and intended for demonstration, not persistence or horizontal scale. Document ingestion currently accepts text strings; PDF/Office parsing, a production vector database and evaluation datasets are separate follow-up work.
