"""Web-UI engines: drive the box Chrome (already routed through the box proxy) over CDP.
One tab, human-like pacing, low volume. Raises WallError on captcha/login walls."""
import asyncio, os, random, re
CDP = os.environ.get("CITESHINE_CDP", "http://127.0.0.1:9226")

class WallError(Exception): pass

SITES = {
 "chatgpt-web": dict(url="https://chatgpt.com/", input="#prompt-textarea:visible, textarea:visible, [contenteditable=true]:visible",
     answer="[data-message-author-role=assistant]", stop="[data-testid=stop-button]",
     exclude=r"chatgpt\.com|openai\.com", send="button[aria-label='Send message']:visible",
     tail=["ChatGPT is AI and can make mistakes", "Chat with ChatGPT"]),
 "perplexity-web": dict(url="https://www.perplexity.ai/", input="#ask-input, [contenteditable=true], textarea",
     answer=".prose", stop="button[aria-label*=Stop]", exclude=r"perplexity\.ai"),
 "kimi-web": dict(url="https://www.kimi.com/", input=".chat-input-editor:visible, [contenteditable=true]:visible, textarea:visible",
     answer=".segment-assistant, .markdown", stop=".stop-message-btn, [class*=stop]", exclude=r"kimi\.com|moonshot"),
}
WALL = re.compile(r"verify you are human|captcha|are you a robot|unusual activity|人机验证|安全验证|请完成验证|Log in to continue|too many requests|Sign up and repeat|注册并重复|WeChat QR login|Send code", re.I)

async def _ask(name, prompt):
    from playwright.async_api import async_playwright
    s = SITES[name]
    async with async_playwright() as p:
        b = await p.chromium.connect_over_cdp(CDP)
        pg = await b.contexts[0].new_page()
        try:
            await pg.goto(s["url"], timeout=60000); await pg.wait_for_timeout(random.randint(4000, 7000))
            body = await pg.inner_text("body")
            if WALL.search(body[:3000]) or "sign_in" in pg.url or "login" in pg.url:
                raise WallError(f"wall at {pg.url}: {body[:150]!r}")
            inp = pg.locator(s["input"]).first
            await inp.click(); await pg.wait_for_timeout(random.randint(500, 1200))
            await pg.keyboard.press("Control+A"); await pg.keyboard.press("Backspace")  # clear any saved draft
            await pg.keyboard.type(prompt, delay=random.randint(25, 60))
            await pg.wait_for_timeout(random.randint(600, 1500)); 
            await pg.wait_for_timeout(1500)
            await pg.keyboard.press("Enter"); await pg.wait_for_timeout(4000)
            if s.get("send") and await pg.locator(s["send"]).count(): await pg.locator(s["send"]).first.click()
            else: await pg.keyboard.press("Enter")
            last, stable = "", 0
            for _ in range(100):
                await pg.wait_for_timeout(3000)
                a = pg.locator(s["answer"])
                txt = (await a.last.inner_text()) if await a.count() else ""
                if not txt and s.get("tail"):  # fallback: page text after the prompt, minus footer
                    body = await pg.inner_text("body"); i = body.rfind(prompt[:40])
                    txt = body[i + len(prompt):] if i >= 0 else ""
                    for t in s["tail"]: txt = txt.split(t)[0]
                    txt = txt.strip()
                stopping = await pg.locator(s["stop"]).count() > 0
                if len(txt) > 40 and txt == last and not stopping:
                    stable += 1
                    if stable >= 3: break
                else: stable = 0
                last = txt
            if not last:
                body = await pg.inner_text("body")
                raise WallError(f"no answer at {pg.url}: {body[:200]!r}") if WALL.search(body) else RuntimeError(f"no answer at {pg.url}: {body[-300:]!r}")
            if WALL.search(last) or WALL.search((await pg.inner_text("body"))[-800:]):
                raise WallError(f"login/signup wall after submit at {pg.url}: {last[:120]!r}")
            links = await pg.eval_on_selector_all("main a[href], a[href]", "es=>es.map(e=>e.href)")
            cites = list(dict.fromkeys(u for u in links if u.startswith("http") and not re.search(s["exclude"], u)))
            logged_in = not re.search(r"\bLog in\b|Sign In|登录", (await pg.inner_text("body"))[:1500])
            return {"text": last, "citations": cites, "raw": {"model": f"{name} (web UI, {'logged-in' if logged_in else 'logged-out'})", "url": pg.url}}
        finally:
            await pg.close()
            await asyncio.sleep(random.uniform(20, 40))  # human-like gap between prompts

class WebProvider:
    def __init__(self, name, model=None): self.name = name; self.model = name + " web"
    def ask(self, prompt): return asyncio.run(_ask(self.name, prompt))
