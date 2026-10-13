# citeshine-audit

**Open-source AI visibility (GEO) audit CLI** by [Citeshine 引耀](https://citeshine.com) · MIT · [中文说明](#中文说明)

Ask AI engines the questions your buyers ask, and measure whether they mention, rank, and cite your brand versus competitors. Each answer is stored with its timestamp, engine, model and prompt, so a run can be reproduced and re-analyzed.

## What it measures
- **Mention rate**: share of answers that mention the brand (name, aliases, domain), per engine and per prompt.
- **Position**: order of first mention among tracked entities, plus rank inside a numbered or bulleted list.
- **Share of voice**: how many answers mention each tracked brand or competitor.
- **Cited sources**: domains the engine cites (when the engine exposes citations) and whether your own domain is cited.
- **Accuracy / sentiment notes**: every answer that mentions the brand is quoted for human review. There is no automatic sentiment score.

All figures are raw counts with sample sizes, and the tool never extrapolates. Answers vary, so run each prompt several times (`-n`).

## Engines
**API engines** (recommended; set env vars): `openai` (Responses API + web search) `OPENAI_API_KEY` · `perplexity` `PERPLEXITY_API_KEY` · `deepseek` `DEEPSEEK_API_KEY` · `kimi` `MOONSHOT_API_KEY` · `grok` `XAI_API_KEY` · `claude` (web search) `ANTHROPIC_API_KEY` · `gemini` (Search grounding) `GEMINI_API_KEY`.

**Web-UI engines** (experimental): `chatgpt-web`, `perplexity-web`, `kimi-web`. They drive a Chrome you already run with `--remote-debugging-port` (set `CITESHINE_CDP`, default `http://127.0.0.1:9226`) and use whatever session you are logged in with. Pacing is human-like: one tab, typed input, 20–40 s gaps between prompts. A run stops at the first captcha or login wall. Selectors break when sites change. Respect each site's terms and keep volume low. Requires `pip install playwright`.

## Usage
```bash
python3 -m citeshine_audit --list-engines
python3 -m citeshine_audit configs/citeshine.json -n 3                       # all API engines with keys
python3 -m citeshine_audit configs/citeshine.json --engines deepseek,perplexity:sonar-pro -o runs/x
python3 -m citeshine_audit configs/citeshine.json --engines chatgpt-web -n 1 --prompts zh01,en01
python3 -m citeshine_audit configs/citeshine.json -o runs/x --report-only     # rebuild report from raw.jsonl
python3 -m unittest tests/test_basic.py
```
Output goes to `runs/<brand>-<time>/`: `raw.jsonl`, `report.md` and `report.html`. A config is JSON with `brand` (name, aliases, domain, category), `competitors` and `prompts` (id, lang, text); see `configs/citeshine.json`.

## Example
[docs/examples/citeshine-chatgpt-web-2026-10-13.md](docs/examples/citeshine-chatgpt-web-2026-10-13.md) is a real audit of our own brand: ChatGPT web, logged out, n=1, 13 prompts. Citeshine was not mentioned in any of the 11 generic buyer questions. Asked by name, ChatGPT confused citeshine.com with an unrelated older web shop. That is the honest day-0 baseline.

## Methodology and limits
- Brand matching is case-insensitive substring matching on names and aliases. Choose aliases that can't match ordinary words.
- Logged-out web answers differ from API answers and from logged-in or personalized answers. Always report engine, mode, date and n.
- The ChatGPT web UI shows sources as chips, so `chatgpt-web` usually records no cited URLs.
- Small n means high variance. Compare runs that use the same prompts and engines.

---

## 中文说明
**citeshine-audit** 是 [引耀 Citeshine](https://citeshine.com) 开源的 AI 可见度（GEO）体检工具。它用买家真实会问的问题去问各个 AI 引擎，统计品牌和竞品被提及的情况：

- **提及率**
- **排名位置**
- **声量占比**
- **引用来源**：被引用的域名，以及有没有引用到你的官网
- **准确性备注**：提到品牌的回答原文，留给人工核对

每条回答都保存时间、引擎、模型和问题，结果可以复现。所有数字都是原始计数，附带样本量，不做外推。

- **API 引擎**：设置对应的环境变量即可，支持 OpenAI、Perplexity、DeepSeek、Kimi、Grok、Claude、Gemini。
- **网页引擎（实验性）**：通过 CDP 连接你本机已登录的 Chrome，单标签页、按人的节奏操作，遇到验证码或登录墙就停止。请遵守各网站的条款，控制频率。
- **示例**：见 `docs/examples/`。这是对引耀自己做的真实体检（ChatGPT 网页版，未登录，n=1），通用问题的提及率是 0/11，这就是起点。

需要专业 GEO 服务？先做免费 AI 可见度体检，再按效果付费：[citeshine.com](https://citeshine.com)。

MIT License.
