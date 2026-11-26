import json

from rag.openai_adapters import OpenAIEmbedder, OpenAIGenerator


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return json.dumps(self.payload).encode()


def test_embedding_adapter(monkeypatch):
    def fake_urlopen(request, timeout):
        assert request.full_url.endswith("/v1/embeddings")
        assert request.get_header("Authorization") == "Bearer test"
        return FakeResponse({"data": [{"embedding": [0.1, 0.2]}]})

    monkeypatch.setattr("rag.openai_adapters.urlopen", fake_urlopen)
    assert OpenAIEmbedder(api_key="test").embed("hello") == [0.1, 0.2]


def test_generator_adapter(monkeypatch):
    def fake_urlopen(request, timeout):
        assert request.full_url.endswith("/v1/responses")
        return FakeResponse({
            "output": [{"content": [{"type": "output_text", "text": "Grounded answer"}]}]
        })

    monkeypatch.setattr("rag.openai_adapters.urlopen", fake_urlopen)
    assert OpenAIGenerator(api_key="test").answer("Q?", ["Context"]) == "Grounded answer"
