# Positioning copy review (2026-10-13)

Scope: all uncommitted changes in this repo. That means `README.md` and `README.zh-CN.md`, 4 hunks each. There were no untracked files. Nothing was committed, pushed or published.

Fact sources checked: `runs/citeshine-web-20261013/` (`raw.jsonl`, `report.md`) and `docs/examples/citeshine-chatgpt-web-2026-10-13.md`.

## Verified, no change needed

- **0 / 11 generic questions.** The run has 13 prompts with n=1. Citeshine was mentioned 2/13 times, and both mentions were the by-name prompts zh07 and en06. That leaves 0/11 generic. Engine: ChatGPT web, logged out, 2026-10-13. ✔
- **Mistaken identity.** Both by-name answers call citeshine.com a Shopify store (registered Dec 2021) that sold phone cases or accessories, and both cite Merchant Genius. ✔
- **Pricing (both languages).** Free audit, a monthly base fee, and a bonus only when a re-test meets a target agreed in writing. ✔
- **No 出海, 代理, proxy or residential IP in the changed copy.** The only 出海 in the repo is the verbatim audit question zh03 (in `configs/citeshine.json` and the example report), which is an allowed exception. ✔
- **No invented customers, testimonials, star counts or competitor claims.** ✔

## Changes made

| # | File | Before | After | Reason |
|---|---|---|---|---|
| 1 | README.md L7 (headline) | Find out what ChatGPT, Perplexity, DeepSeek & co. say about your product: whether they recommend you, and whether they get you right. | Find out whether ChatGPT recommends your product or your competitors, and read exactly what it says about you. | The tool only has a working `chatgpt-web` engine, so the headline should not suggest it already measures Perplexity or DeepSeek. "Whether they get you right" also overclaims: accuracy is checked by hand from excerpts, and automatic accuracy flags are still on the roadmap. |
| 2 | README.md L32 | …publish every result against this day-0 run… | …publish each result next to this day-0 run… | More natural English. "Against this run" read like a benchmark. |
| 3 | README.md L123 (service) | …find and fix what AI gets wrong about them. The service covers overseas AIs (ChatGPT, Perplexity, Gemini) and Chinese AIs (DeepSeek, Doubao, Kimi); logged-in web support for the Chinese ones is on this tool's roadmap. | …get recommended by AI, and fixes what AI gets wrong about them. Our service tests ChatGPT, Perplexity and Gemini, plus DeepSeek, Doubao and Kimi. In this open-source tool, only `chatgpt-web` has produced a published report so far; logged-in web engines for DeepSeek, Doubao, Kimi and Perplexity are on the [roadmap](#roadmap). | (a) Saying only the Chinese engines are "on the roadmap" implied the tool already measures ChatGPT, Perplexity and Gemini. The new wording keeps the six-engine service claim, which is approved, and is accurate about the tool. The roadmap list matches the README's Roadmap section; Gemini is not on it, so it is left out. (b) "Overseas AIs" is unnatural English. (c) "Find and fix" alone dropped the core offer (being recommended) that the section heading and pricing are about. |
| 4 | README.zh-CN.md L7 (headline) | ChatGPT、Perplexity、DeepSeek 推荐的是你还是竞品？把你说对了没有？一条命令查清。 | ChatGPT 推荐的是你还是竞品？它怎么介绍你？一条命令查清。 | Same reason as #1. "把你说对了没有" has no subject and reads awkwardly. It also claims one command can judge accuracy, which the tool cannot do yet. |
| 5 | README.zh-CN.md L23 | 更糟的是 AI 可能把你说错：… | 更糟的是，AI 可能把你说错：… | Added the missing pause comma (full-width). |
| 6 | README.zh-CN.md L32 | 差距就摆在这里。这是我们的起点。我们公开构建：之后用同一组问题复测引耀，每次结果都对照第 0 天公开，变好变坏都发。 | 差距就摆在这里，这也是我们的起点。之后我们会用同一组问题复测引耀，每次结果都和第 0 天对照公开，变好变坏都发。 | "公开构建" is a literal translation of "build in public" and does not read as natural Chinese. The sentence already says the results will be published, so it was removed and the choppy sentences were merged. |
| 7 | README.zh-CN.md L117 (service) | 引耀帮面向海外的中国 SaaS 与 AI 工具团队，找出并纠正 AI 对产品的错误描述。服务覆盖海外的 ChatGPT、Perplexity、Gemini 和国产的 DeepSeek、豆包、Kimi；国产引擎的登录网页版支持在本工具的路线图里。 | 引耀服务做海外市场的中国 SaaS 和 AI 工具团队：让 AI 推荐你，也纠正 AI 对你的错误描述。服务测试 ChatGPT、Perplexity、Gemini，也测试 DeepSeek、豆包、Kimi。本开源工具目前只有 `chatgpt-web` 跑出过公开报告；DeepSeek、豆包、Kimi、Perplexity 的登录网页版已列入[路线图](#路线图)。 | Same as #3. The original also stacked a long modifier in front of the noun ("帮面向海外的…团队，找出并纠正…"); it is now split into short sentences. |

The EN line L23 ("Worse, the engine may describe you wrongly: an old product, a previous owner of your domain, a stale complaint.") was kept. It is phrased as a possibility ("may"), and the domain case is backed by our own run.

## Unresolved (outside the changed lines, not edited)

1. **Supported engines table (EN L50–60, ZH L50–54) and the How it works diagram.** These lines are unchanged but still label the 7 API engines "Implemented, bring your own key" and list them as working paths. That contradicts the premise that only `chatgpt-web` currently works. The owner should choose one of two options: verify those engines end to end, or change their status to something like "Code present, not yet verified".
2. **Brand assets.** `BRAND.md` section 9, the Tencent bio (≤50 chars), the Product Hunt headline (≤40) and the X bio (≤160) are not in this repo and not in the diff. A `BRAND.md` exists at `/workspace/citeshine/docs/brand/BRAND.md` in a different repo, but it had no uncommitted changes in scope here, so none of these could be checked.
3. **Earlier review note.** `docs/README-REVIEW.md` (committed earlier) is a previous review note. It is not part of this diff and was left as is.

## 2026-10-13 follow-up edits (resolves Unresolved item 1)

| # | File | Change |
|---|---|---|
| 1 | README.md, Supported engines | Status of the 7 API engines: "Implemented, bring your own key" → "Implemented, untested end to end; bring your own key". `chatgpt-web` status: "Used for the sample report" → "The only engine used in public reports". Added a line under the table: "Only `chatgpt-web` is used in our public reports. The API engines are implemented but have not been fully tested end to end." |
| 2 | README.zh-CN.md, 支持的引擎 | API 引擎状态：“已实现，自备 Key” → “已实现，未完整验证；自备 Key”。`chatgpt-web`：“示例报告就靠它跑出” → “公开报告只用这个引擎”。表格下加一句：“我们的公开报告只用 `chatgpt-web`。API 引擎代码已经写好，但还没有完整跑通验证。” |

All other text, including the How it works diagram, is unchanged. Item 2 (brand bios) was checked in the citeshine repo: all within limits, no 出海. Nothing was committed, pushed or published.
