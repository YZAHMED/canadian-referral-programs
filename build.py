#!/usr/bin/env python3
"""Generate index.html from carrier-referral-programs.json.

The page is generated rather than hand-written so it cannot drift from the data
it describes — the same reason every figure in this dataset carries the date it
was read. Run after any edit to the JSON:

    python3 build.py && git add -A && git commit
"""

import json
import html
from pathlib import Path

ROOT = Path(__file__).parent
DATA = json.loads((ROOT / "carrier-referral-programs.json").read_text())
SITE = "https://yzahmed.github.io/canadian-referral-programs/"
REPO = "https://github.com/YZAHMED/canadian-referral-programs"
# This repo's default branch is master, not main — raw/ URLs 404 on the wrong one.
BRANCH = "master"
GUIDE = "https://mobilereferrals.ca/carrier-referral-programs/"

e = html.escape


def rows():
    out = []
    for p in DATA["programs"]:
        live = p.get("live")
        status = (
            '<span class="tag live">live</span>'
            if live
            else f'<span class="tag ended">ended</span>'
        )
        ended = "" if live else f'<div class="sub">{e(p.get("endedOn", p.get("ended", "")))}</div>'
        note = f'<div class="sub">{e(p["refereeNote"])}</div>' if p.get("refereeNote") else ""
        checked = f'<div class="sub">re-checked {e(p["lastChecked"])}</div>' if p.get("lastChecked") else ""
        out.append(
            "<tr>"
            f'<th scope="row">{e(p["carrier"])}<div class="sub">{e(p["parent"])}</div></th>'
            f"<td>{status}{ended}</td>"
            f'<td>{e(p.get("referee") or "—")}{note}{checked}</td>'
            f'<td>{e(p.get("referrer") or "—")}</td>'
            f'<td><a href="{e(p["source"])}" rel="nofollow noopener">source</a></td>'
            "</tr>"
        )
    return "\n".join(out)


live_n = sum(1 for p in DATA["programs"] if p.get("live"))
total_n = len(DATA["programs"])
ended_n = total_n - live_n

jsonld = {
    "@context": "https://schema.org",
    "@type": "Dataset",
    "name": "Canadian carrier referral programs",
    "alternateName": "Canadian refer-a-friend programme dataset",
    "description": (
        "Every major Canadian mobile carrier's refer-a-friend programme, read from the carrier's "
        f"own website and published with the date it was checked. {total_n} carriers, {live_n} live, "
        f"{ended_n} discontinued. Each record carries the source URL it was read from; contradictions "
        "between a carrier's own pages are recorded rather than resolved."
    ),
    "url": SITE,
    "sameAs": REPO,
    "license": "https://creativecommons.org/licenses/by/4.0/",
    "isAccessibleForFree": True,
    "dateModified": DATA["checked"],
    "keywords": [
        "referral program", "refer a friend", "mobile carrier", "Canada",
        "telecommunications", "Fizz", "Koodo", "Public Mobile", "Freedom Mobile",
    ],
    "spatialCoverage": {"@type": "Place", "name": "Canada"},
    "creator": {
        "@type": "Organization",
        "name": "MobileReferrals.ca",
        "url": "https://mobilereferrals.ca/",
    },
    "distribution": [
        {
            "@type": "DataDownload",
            "encodingFormat": "application/json",
            "contentUrl": f"{REPO}/raw/{BRANCH}/carrier-referral-programs.json",
        },
        {
            "@type": "DataDownload",
            "encodingFormat": "text/csv",
            "contentUrl": f"{REPO}/raw/{BRANCH}/carrier-referral-programs.csv",
        },
    ],
}

HTML = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Canadian carrier referral programs — an open, dated dataset</title>
<meta name="description" content="Open dataset: every Canadian mobile carrier's refer-a-friend programme, read from the carrier's own site and dated. {total_n} carriers, {live_n} live, {ended_n} discontinued. JSON and CSV, CC BY 4.0.">
<link rel="canonical" href="{SITE}">
<meta property="og:title" content="Canadian carrier referral programs — an open, dated dataset">
<meta property="og:description" content="{total_n} Canadian carriers' refer-a-friend programmes, each read from the carrier's own website and published with the date it was checked.">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}">
<script type="application/ld+json">
{json.dumps(jsonld, indent=2, ensure_ascii=False)}
</script>
<style>
  :root {{
    --ground:#fbfcfb; --surface:#fff; --ink:#12201b; --soft:#4d5f57; --mute:#7d8d85;
    --line:#dde5e0; --accent:#0f6b47; --live:#0f6b47; --live-bg:#e0efe8;
    --ended:#9c3520; --ended-bg:#f6e6e1;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --ground:#0c1310; --surface:#111a16; --ink:#e6efea; --soft:#a4b4ac; --mute:#7a8a82;
      --line:#213029; --accent:#3fc78d; --live:#3fc78d; --live-bg:#0f2c20;
      --ended:#e8836a; --ended-bg:#2c1611;
    }}
  }}
  * {{ box-sizing:border-box; }}
  body {{
    margin:0; background:var(--ground); color:var(--ink);
    font:15px/1.6 ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
    -webkit-font-smoothing:antialiased;
  }}
  .wrap {{ max-width:920px; margin:0 auto; padding:48px 22px 80px; }}
  a {{ color:var(--accent); text-underline-offset:2px; }}
  h1 {{ font-size:clamp(26px,4vw,36px); line-height:1.15; letter-spacing:-.015em; margin:0 0 12px; }}
  h2 {{ font-size:19px; letter-spacing:-.01em; margin:44px 0 10px; }}
  .lede {{ font-size:17px; color:var(--soft); max-width:62ch; margin:0 0 20px; }}
  .meta {{
    font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:12px;
    letter-spacing:.04em; color:var(--mute); text-transform:uppercase; margin:0 0 26px;
  }}
  .scroll {{ overflow-x:auto; border:1px solid var(--line); border-radius:4px; background:var(--surface); }}
  table {{ border-collapse:collapse; width:100%; font-size:14px; min-width:720px; }}
  th,td {{ text-align:left; padding:12px 14px; border-bottom:1px solid var(--line); vertical-align:top; }}
  thead th {{
    font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:11px; font-weight:500;
    letter-spacing:.08em; text-transform:uppercase; color:var(--mute);
  }}
  tbody tr:last-child th, tbody tr:last-child td {{ border-bottom:0; }}
  tbody th {{ font-weight:600; white-space:nowrap; }}
  .sub {{ font-size:12.5px; color:var(--mute); font-weight:400; margin-top:3px; line-height:1.45; }}
  .tag {{
    display:inline-block; font-family:ui-monospace,SFMono-Regular,Menlo,monospace;
    font-size:11px; padding:2px 8px; border-radius:20px; white-space:nowrap;
  }}
  .tag.live {{ background:var(--live-bg); color:var(--live); }}
  .tag.ended {{ background:var(--ended-bg); color:var(--ended); }}
  .files {{ display:flex; flex-wrap:wrap; gap:10px; margin:14px 0 0; padding:0; list-style:none; }}
  .files a {{
    display:inline-block; border:1px solid var(--line); background:var(--surface);
    padding:9px 14px; border-radius:4px; text-decoration:none;
    font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:13px;
  }}
  .files a:hover {{ border-color:var(--accent); }}
  ol,ul {{ max-width:66ch; color:var(--soft); }}
  li {{ margin:7px 0; }}
  p {{ max-width:66ch; color:var(--soft); }}
  strong {{ color:var(--ink); }}
  footer {{ margin-top:52px; padding-top:20px; border-top:1px solid var(--line); font-size:13.5px; color:var(--mute); }}
</style>
</head>
<body>
<div class="wrap">

<h1>Canadian carrier referral programs</h1>
<p class="lede">
  Every major Canadian mobile carrier's refer-a-friend programme, read from the carrier's own
  website and published with the date it was checked.
</p>
<p class="meta">
  {total_n} carriers &middot; {live_n} live &middot; {ended_n} discontinued &middot; checked {DATA["checked"]} &middot; CC BY 4.0
</p>

<h2>Why this exists</h2>
<p>
  Referral-code aggregators routinely publish programmes that no longer exist. At the time of
  writing, several still advertise Virgin Plus and Fido referral offers &mdash;
  <strong>both ended in 2024&ndash;2025</strong>. Nobody maintained a dated, sourced record, so
  this is one.
</p>
<p>
  The finding worth noting is that <strong>half the industry has left</strong>. Bell closed both of
  its flanker programmes on the same day. Rogers closed both of its own, earlier and separately.
  Every surviving programme belongs to TELUS or Quebecor.
</p>

<h2>The data</h2>
<div class="scroll">
<table>
  <thead>
    <tr><th>Carrier</th><th>Status</th><th>New customer</th><th>Referrer</th><th>Source</th></tr>
  </thead>
  <tbody>
{rows()}
  </tbody>
</table>
</div>

<ul class="files">
  <li><a href="{REPO}/raw/{BRANCH}/carrier-referral-programs.json">carrier-referral-programs.json</a></li>
  <li><a href="{REPO}/raw/{BRANCH}/carrier-referral-programs.csv">carrier-referral-programs.csv</a></li>
  <li><a href="{REPO}">repository</a></li>
</ul>

<h2>Method</h2>
<ol>
  <li>Amounts are read from <strong>the carrier's own</strong> website or support documentation.
      Never from a coupon site or a referral aggregator.</li>
  <li>Every record carries the <code>source</code> URL it was read from.</li>
  <li>Where a carrier's own pages contradict each other, that is recorded rather than resolved.
      Fizz is the live example: its programme page says $25 in every region while its plan pages
      advertise $40 outside Quebec.</li>
  <li>Anything that could not be confirmed is left blank.
      <strong>A blank cell is publishable; a plausible guess is not.</strong></li>
</ol>
<p>
  Figures are re-checked in a real browser rather than by fetching raw HTML, because several
  carriers ship every regional variant of a page and delete the non-matching ones in the browser
  &mdash; a check that reads the raw markup reports amounts no visitor can see.
</p>

<h2>Known limits</h2>
<ul>
  <li><strong>Amounts change without notice.</strong> Check the carrier's own page before acting.</li>
  <li>Public Mobile's referrer reward is 1 Public Point per 30 days. The commonly quoted
      &ldquo;1 point = $1&rdquo; appears on <strong>no current Public Mobile page</strong> &mdash; its
      only source is a staff forum post from January 2022, so the dollar value is deliberately not
      asserted here.</li>
  <li>Freedom Mobile has <strong>no shareable referral code</strong>. Its programme is invite-only and
      its terms permit referring only &ldquo;individuals with whom you have a personal
      relationship&rdquo;, so it cannot be used the way the others can.</li>
</ul>

<h2>Corrections</h2>
<p>
  Open an <a href="{REPO}/issues">issue</a>, or email
  <a href="mailto:hello@mobilereferrals.ca">hello@mobilereferrals.ca</a>. Corrections get fixed and
  logged with a date rather than quietly edited.
</p>

<footer>
  <p>
    Licensed <a href="https://creativecommons.org/licenses/by/4.0/" rel="license">CC BY 4.0</a> &mdash;
    use it freely, credit <a href="{GUIDE}">MobileReferrals.ca</a>.
  </p>
  <p>
    Maintained by <a href="https://mobilereferrals.ca/">MobileReferrals.ca</a>, an independent site
    that publishes guides to these programmes and shares referral codes for two of them. Not
    affiliated with, endorsed by, or sponsored by any carrier. The dataset states what each carrier
    publishes, including for programmes it earns nothing from.
  </p>
</footer>

</div>
</body>
</html>
"""

(ROOT / "index.html").write_text(HTML)
(ROOT / ".nojekyll").write_text("")
print(f"index.html written — {total_n} carriers, {live_n} live, {ended_n} ended")
