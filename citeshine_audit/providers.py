"""Pluggable AI engine providers. Official APIs only; no web-UI scraping."""
import json, os, urllib.request

def _post(url, headers, body, timeout=120):
    req = urllib.request.Request(url, json.dumps(body).encode(), {**headers, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())

class Provider:
    name = ""; env = ""; default_model = ""
    def __init__(self, model=None): self.model = model or self.default_model
    @classmethod
    def available(cls): return bool(os.environ.get(cls.env))
    def key(self): return os.environ[self.env]
    def ask(self, prompt):  # -> {"text": str, "citations": [url], "raw": dict}
        raise NotImplementedError

class OpenAIChatCompat(Provider):
    base = ""
    def ask(self, prompt):
        d = _post(self.base + "/chat/completions", {"Authorization": f"Bearer {self.key()}"},
                  {"model": self.model, "messages": [{"role": "user", "content": prompt}]})
        cites = d.get("citations") or [r.get("url") for r in d.get("search_results", []) if r.get("url")]
        return {"text": d["choices"][0]["message"]["content"], "citations": cites, "raw": d}

class OpenAI(Provider):
    name, env, default_model = "openai", "OPENAI_API_KEY", "gpt-4o-mini"
    def ask(self, prompt):  # Responses API with web search tool
        d = _post("https://api.openai.com/v1/responses", {"Authorization": f"Bearer {self.key()}"},
                  {"model": self.model, "input": prompt, "tools": [{"type": "web_search"}]})
        text, cites = [], []
        for o in d.get("output", []):
            for c in o.get("content", []) or []:
                if c.get("type") == "output_text":
                    text.append(c.get("text", ""))
                    cites += [a["url"] for a in c.get("annotations", []) if a.get("url")]
        return {"text": "\n".join(text), "citations": cites, "raw": d}

class Perplexity(OpenAIChatCompat):
    name, env, default_model, base = "perplexity", "PERPLEXITY_API_KEY", "sonar", "https://api.perplexity.ai"
class DeepSeek(OpenAIChatCompat):
    name, env, default_model, base = "deepseek", "DEEPSEEK_API_KEY", "deepseek-chat", "https://api.deepseek.com"
class Moonshot(OpenAIChatCompat):
    name, env, default_model, base = "kimi", "MOONSHOT_API_KEY", "moonshot-v1-8k", "https://api.moonshot.cn/v1"
class XAI(OpenAIChatCompat):
    name, env, default_model, base = "grok", "XAI_API_KEY", "grok-3-mini", "https://api.x.ai/v1"

class Anthropic(Provider):
    name, env, default_model = "claude", "ANTHROPIC_API_KEY", "claude-sonnet-4-5"
    def ask(self, prompt):
        d = _post("https://api.anthropic.com/v1/messages", {"x-api-key": self.key(), "anthropic-version": "2023-06-01"},
                  {"model": self.model, "max_tokens": 1500, "messages": [{"role": "user", "content": prompt}],
                   "tools": [{"type": "web_search_20250305", "name": "web_search", "max_uses": 3}]})
        text, cites = [], []
        for b in d.get("content", []):
            if b.get("type") == "text":
                text.append(b["text"]); cites += [c["url"] for c in b.get("citations") or [] if c.get("url")]
        return {"text": "\n".join(text), "citations": cites, "raw": d}

class Gemini(Provider):
    name, env, default_model = "gemini", "GEMINI_API_KEY", "gemini-2.5-flash"
    def ask(self, prompt):
        d = _post(f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.key()}", {},
                  {"contents": [{"parts": [{"text": prompt}]}], "tools": [{"google_search": {}}]})
        c = d["candidates"][0]
        text = "".join(p.get("text", "") for p in c["content"]["parts"])
        cites = [ch["web"]["uri"] for ch in c.get("groundingMetadata", {}).get("groundingChunks", []) if "web" in ch]
        return {"text": text, "citations": cites, "raw": d}

class Fake(Provider):
    """Offline provider for tests only. Never used in real audits unless explicitly requested."""
    name, env, default_model = "fake", "", "fake"
    @classmethod
    def available(cls): return False
    def ask(self, prompt):
        return {"text": "1. Profound\n2. Otterly.AI\n3. Peec AI", "citations": ["https://example.com/a"], "raw": {}}

REGISTRY = {p.name: p for p in [OpenAI, Perplexity, DeepSeek, Moonshot, XAI, Anthropic, Gemini, Fake]}

from .web import SITES as _WEB, WebProvider as _WP
for _n in _WEB:
    REGISTRY[_n] = type(_n, (), {"name": _n, "env": "(web session)", "available": classmethod(lambda c: False),
                                 "__new__": (lambda n: lambda cls, model=None: _WP(n, model))(_n)})
