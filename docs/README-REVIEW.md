# README review log (2026-10-13)

Scope: rewrite `README.zh-CN.md` as native Chinese marketing copy; light flow and accuracy pass on `README.md`.

Fixed constraints, checked for both files:

- Facts and numbers unchanged and consistent with `docs/examples/citeshine-chatgpt-web-2026-10-13.md`: 0/11 generic buyer questions, 13 prompts, n=1, logged-out ChatGPT web, citeshine.com described as an old Shopify phone-case store, Merchant Genius as the source.
- No new customers, testimonials, metrics or star counts. No mention of proxies. The word 出海 does not appear.
- All commands, code blocks, image paths and links unchanged and working. Badge anchors point at existing headings (`#快速上手`, `#测什么`).
- CTA and pricing structure unchanged: free audit → monthly base fee → results bonus paid only when a re-test meets a target agreed in writing. CTA link text unchanged in both languages.

## README.zh-CN.md

Rewritten from scratch in the voice of a Chinese founder: short sentences, fewer 的, no English-style long clauses. GEO, CLI, API and engine names kept as-is.

Structural changes for parity with the English README:

- Added the GEO badge (links to `#测什么`).
- Added the missing quickstart command `--engines deepseek,perplexity:sonar-pro -o runs/x`, with the same blank-line grouping as the English version.
- API engine row now notes that `--list-engines` shows each engine's environment variable.

Before / after examples:

| Before | After |
|---|---|
| 一条命令，查清 ChatGPT、Perplexity、DeepSeek 这些 AI 推荐的是你，还是你的竞品。 | ChatGPT、Perplexity、DeepSeek 推荐的是你，还是你的竞品？一条命令查清。 |
| 买家不再搜索了，他们直接问 AI | 买家不搜了，直接问 AI |
| 大多数团队根本不知道 AI 是怎么介绍自己的。 | AI 怎么介绍你？多数团队心里没底。 |
| 这就是这个工具能帮你看见的差距，也是我们自己的起点。之后的复测结果也会公开。 | 差距就摆在这里。这是我们的起点，之后的复测结果也会对照它公开。 |
| 品牌匹配是对名称和别名做不区分大小写的子串匹配，别名不要选容易撞上普通词的。 | 品牌匹配：对名称和别名做不区分大小写的子串匹配。别名别选容易撞上常用词的。 |
| 想出现在 AI 的答案里？ | 想进 AI 的推荐名单？ |

## README.md

Light edits only. Two of the three fix accuracy problems found by checking the code:

| Before | After | Why |
|---|---|---|
| Answers that mention you are quoted in full so a person can check them for accuracy. | Answers that mention you are excerpted in the report so a person can check them for accuracy; the full text stays in `raw.jsonl`. | Accuracy: `cli.py` writes the first 300 characters of each answer to the report, not the full text. |
| `--list-engines  # shows which engines have keys/sessions` | `--list-engines  # lists engines and whether their API key is set` | Accuracy: web engines always print as unavailable, so the command does not detect sessions. Command unchanged. |
| "Which tool should I use for X?" now goes to ChatGPT, … | Questions like "Which tool should I use for X?" now go to ChatGPT, … | Flow and grammar. |

The Chinese README carries the same two accuracy fixes (摘录原文 + 完整原文都在 `raw.jsonl`; 看 API Key 是否就绪).
