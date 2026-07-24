#!/usr/bin/env bash
# The Bridge — standing verification. Run from anywhere: ./verify.sh
# Turns the CONTEXT.md checklist into an executable check: counts are COMPUTED,
# not typed; links/math are machine-checked; the two prose scans are surfaced
# for an eyeball. Exits non-zero on any hard failure.
set -u
cd "$(dirname "$0")"
fail=0

echo "== count sync (computed, not typed) =="
files=$(ls chapters/*.html 2>/dev/null | wc -l | tr -d ' ')
links=$(grep -oE 'href="chapters/[0-9][^"]*\.html"' index.html | sort -u | wc -l | tr -d ' ')
echo "  $files chapter files on disk; $links distinct chapter links on the contents page"
if [ "$files" != "$links" ]; then echo "  FAIL: contents page ($links) != chapter files ($files)"; fail=1; fi

echo "== links resolve + math delimiters balance =="
python3 - <<'PY' || fail=1
import re,os,glob,sys
bad=0
for f in glob.glob("*.html")+glob.glob("chapters/*.html"):
    base=os.path.dirname(f); t=open(f).read()
    dd=t.count("$$"); s=t.count("$")-2*dd
    if dd%2 or s%2: print(f"  MATH imbalance {f}: $$={dd} inline$={s}"); bad+=1
    for m in re.findall(r'(?:href|src)="([^"]+)"', t):
        if m.startswith("http") or m.startswith("#"): continue
        if not os.path.exists(os.path.normpath(os.path.join(base, m.split('#')[0]))):
            print(f"  BROKEN link {f} -> {m}"); bad+=1
print("  OK" if not bad else f"  {bad} problem(s)")
sys.exit(1 if bad else 0)
PY

echo "== prev/next chain contiguity (a link resolving != the chain being right) =="
python3 - <<'PY' || fail=1
import re,os,sys
idx=open("index.html").read()
order=re.findall(r'href="chapters/([0-9][^"#]*\.html)"', idx)
seen=set(); order=[x for x in order if not (x in seen or seen.add(x))]
CONTENTS="../index.html"
def norm(h):
    if not h: return None
    return "CONTENTS" if h.endswith("index.html") else os.path.basename(h)
prob=0
for i,name in enumerate(order):
    p=os.path.join("chapters",name)
    if not os.path.exists(p): print(f"  {name}: listed on contents but file missing"); prob+=1; continue
    m=re.search(r'<nav class="chapter-nav">(.*?)</nav>', open(p).read(), re.S)
    if not m: print(f"  {name}: no chapter-nav"); prob+=1; continue
    nav=m.group(1)
    nx=re.search(r'<a class="next" href="([^"]+)"', nav)
    nxh=nx.group(1) if nx else None
    pvh=next((a for a in re.findall(r'<a[^>]*href="([^"]+)"', nav) if a!=nxh), None)
    exp_prev = order[i-1] if i>0 else CONTENTS
    exp_next = order[i+1] if i<len(order)-1 else CONTENTS
    if norm(pvh)!=norm(exp_prev): print(f"  {name}: prev={pvh}  expected {exp_prev}"); prob+=1
    if norm(nxh)!=norm(exp_next): print(f"  {name}: next={nxh}  expected {exp_next}"); prob+=1
print(f"  {len(order)} essays in contents order, chain contiguous" if not prob else f"  {prob} chain problem(s)")
sys.exit(1 if prob else 0)
PY

echo "== quotation scan (no reproduced source prose) =="
grep -rn "<blockquote>" chapters/*.html >/dev/null && echo "  (read each <blockquote> by eye — curly-quote regex is unreliable)"
lifted=$(grep -rIn "Many introductions\|augmented by unitary operations\|coarse way\|without in any way disturbing\|element of physical reality corresponding" chapters/ 2>/dev/null)
if [ -n "$lifted" ]; then echo "  FAIL lifted source prose:"; echo "$lifted"; fail=1; else echo "  no known lifted phrases"; fi

echo "== self-assessment scan (essay must not grade itself) =="
hits=$(grep -rniE "cleanest|clearest|sharpest|in the whole book|of its thesis|worth saying|fails because .* succeeds" chapters/*.html)
if [ -n "$hits" ]; then echo "  triage (physics superlative = ok; verdict about the essay = fix):"; echo "$hits"; else echo "  none"; fi

echo "== no copyrighted PDFs tracked by git =="
tracked=$(git ls-files '*.pdf' 2>/dev/null)
if [ -n "$tracked" ]; then echo "  FAIL: PDF tracked: $tracked"; fail=1; else echo "  none tracked"; fi

echo "----------"
if [ "$fail" = 0 ]; then echo "VERIFY: PASS"; else echo "VERIFY: FAIL"; fi
exit $fail
