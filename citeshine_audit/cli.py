import argparse, collections, datetime, html, json, os, sys, time
from pathlib import Path
from . import providers
from .analyze import analyze_answer

def load(p):
    t = Path(p).read_text(encoding="utf-8")
    if p.endswith((".yaml", ".yml")):
        import yaml; return yaml.safe_load(t)
    return json.loads(t)

def run(cfg, engines, n, out):
    out.mkdir(parents=True, exist_ok=True)
    raw = out / "raw.jsonl"
    with raw.open("a", encoding="utf-8") as f:
        for eng in engines:
            name, _, model = eng.partition(":")
            prov = providers.REGISTRY[name](model or None); walled = False
            for p in cfg["prompts"]:
                for i in range(n):
                    rec = {"ts": datetime.datetime.now(datetime.timezone.utc).isoformat(), "engine": name,
                           "model": prov.model, "prompt_id": p["id"], "lang": p["lang"], "prompt": p["text"], "run": i}
                    if walled: break
                    try:
                        r = prov.ask(p["text"]); rec.update(text=r["text"], citations=r["citations"], error=None)
                        rec["response_model"] = r["raw"].get("model"); rec["page_url"] = r["raw"].get("url")
                    except Exception as e:
                        from .web import WallError
                        if isinstance(e, WallError):
                            rec.update(text="", citations=[], error=f"WALL: {e}"); f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                            print(f"[{name}] stopped: {e}", file=sys.stderr); walled = True; break
                        rec.update(text="", citations=[], error=f"{type(e).__name__}: {str(e)[:200]}")
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n"); f.flush()
                    print(f"[{name}] {p['id']} #{i} {'ERR '+rec['error'] if rec['error'] else 'ok'}", file=sys.stderr)
    return raw

def report(cfg, raw, out):
    recs = [json.loads(l) for l in raw.read_text(encoding="utf-8").splitlines() if l.strip()]
    ok = [r for r in recs if not r.get("error")]
    b, comps = cfg["brand"], cfg.get("competitors", [])
    for r in ok: r["a"] = analyze_answer(r["text"], r["citations"], b, comps, b["domain"])
    L = [f"# AI Visibility Audit: {b['name']}", "",
         f"Generated {datetime.datetime.now().isoformat(timespec='minutes')}. Raw answers: `{raw.name}`.",
         f"Total calls: {len(recs)}, successful: {len(ok)}, errors: {len(recs)-len(ok)}.",
         "All figures are raw counts from this sample; no extrapolation.", ""]
    if not ok:
        L += ["**No successful engine responses — no results to report.**", ""]
    by_eng = collections.defaultdict(list)
    for r in ok: by_eng[f"{r['engine']} ({r['model']})"].append(r)
    L += ["## Mention rate by engine", "", "| Engine | Answers | Brand mentioned | Brand domain cited |", "|---|---|---|---|"]
    for e, rs in by_eng.items():
        m = sum(r["a"]["brand_mentioned"] for r in rs); c = sum(r["a"]["brand_domain_cited"] for r in rs)
        L.append(f"| {e} | {len(rs)} | {m}/{len(rs)} | {c}/{len(rs)} |")
    sov = collections.Counter(k for r in ok for k in r["a"]["mentioned"])
    tot = sum(sov.values()) or 1
    L += ["", "## Share of voice (answers mentioning each entity)", "", "| Entity | Answers | Share of mentions |", "|---|---|---|"]
    for k, v in sov.most_common():
        L.append(f"| {b['name'] if k=='__brand__' else k} | {v}/{len(ok)} | {v}/{tot} |")
    L += ["", "## Per prompt", "", "| Prompt | Lang | Answers | Brand mentioned | Brand order (when mentioned) |", "|---|---|---|---|---|"]
    for p in cfg["prompts"]:
        rs = [r for r in ok if r["prompt_id"] == p["id"]]
        ords = [r["a"]["brand_order"] for r in rs if r["a"]["brand_order"]]
        L.append(f"| {p['text']} | {p['lang']} | {len(rs)} | {sum(r['a']['brand_mentioned'] for r in rs)}/{len(rs)} | {ords or '-'} |")
    dom = collections.Counter(d for r in ok for d in set(r["a"]["cited_domains"]))
    L += ["", "## Most cited domains", "", "| Domain | Answers citing |", "|---|---|"]
    L += [f"| {d} | {c} |" for d, c in dom.most_common(25)] or ["| (none) | |"]
    L += ["", "## Accuracy / sentiment notes", "", "Answers that mention the brand (manual review needed):", ""]
    for r in ok:
        if r["a"]["brand_mentioned"]:
            L.append(f"- [{r['engine']}] {r['prompt_id']}: {r['text'][:300].replace(chr(10),' ')}")
    md = "\n".join(L) + "\n"
    (out / "report.md").write_text(md, encoding="utf-8")
    try:
        import markdown; body = markdown.markdown(md, extensions=["tables"])
    except ImportError:
        body = f"<pre>{html.escape(md)}</pre>"
    (out / "report.html").write_text(f"<!doctype html><meta charset=utf-8><title>Audit</title><style>body{{font-family:sans-serif;max-width:960px;margin:auto}}table{{border-collapse:collapse}}td,th{{border:1px solid #ccc;padding:4px}}</style>{body}", encoding="utf-8")
    return out / "report.md"

def main():
    ap = argparse.ArgumentParser("citeshine-audit")
    ap.add_argument("config", nargs="?"); ap.add_argument("--engines", help="comma list, e.g. openai,perplexity:sonar-pro (default: all with keys)")
    ap.add_argument("-n", "--runs", type=int, default=3); ap.add_argument("-o", "--out", default=None)
    ap.add_argument("--report-only", action="store_true", help="rebuild report from existing raw.jsonl")
    ap.add_argument("--list-engines", action="store_true")
    ap.add_argument("--prompts", help="comma list of prompt ids to run (smoke tests)")
    a = ap.parse_args()
    if a.list_engines:
        for k, p in providers.REGISTRY.items():
            if k != "fake": print(f"{k:12} {p.env:20} {'available' if p.available() else 'missing key'}")
        return
    cfg = load(a.config)
    if a.prompts: cfg["prompts"] = [p for p in cfg["prompts"] if p["id"] in a.prompts.split(",")]
    out = Path(a.out or f"runs/{cfg['brand']['name']}-{time.strftime('%Y%m%d-%H%M%S')}")
    if not a.report_only:
        engines = a.engines.split(",") if a.engines else [k for k, p in providers.REGISTRY.items() if p.available()]
        if not engines: sys.exit("No engines available: set at least one API key (see --list-engines).")
        run(cfg, engines, a.runs, out)
    print(report(cfg, out / "raw.jsonl", out))

if __name__ == "__main__": main()
