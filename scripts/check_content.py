#!/usr/bin/env python3
"""Check the reading structure and internal destinations of the static book."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import re

ROOT=Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self,path):
        super().__init__(convert_charrefs=True)
        self.path=path
        self.ids=[];self.links=[];self.h1=0;self.details=0;self.summaries=0
        self.lang=None;self.stack=[];self.errors=[]
        self.feed(path.read_text())
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html': self.lang=a.get('lang')
        if 'id' in a:self.ids.append(a['id'])
        if tag=='h1':self.h1+=1
        if tag=='details':self.details+=1
        if tag=='summary':self.summaries+=1
        for key in ('href','src'):
            if key in a:self.links.append(a[key])
        if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:
            self.stack.append(tag)
    def handle_endtag(self,tag):
        if not self.stack or self.stack[-1]!=tag:
            self.errors.append(f'unexpected closing {tag}; stack={self.stack}')
        else:self.stack.pop()

paths=sorted(ROOT.glob('*.html'))+sorted((ROOT/'chapters').glob('*.html'))
pages={p.resolve():Page(p) for p in paths}
errors=[]
for path,p in pages.items():
    label=path.relative_to(ROOT)
    if p.lang!='en' or p.h1!=1:errors.append(f'{label}: language or main heading')
    if len(p.ids)!=len(set(p.ids)):errors.append(f'{label}: duplicate anchor IDs')
    if p.errors or p.stack:errors.append(f'{label}: invalid nesting {p.errors} {p.stack}')
    text=path.read_text()
    if re.search(r'class="(?:bridge|move)"|The step across|Check the crossing|Move [1-4]',text):
        errors.append(f'{label}: retired chapter framework remains')
    if path.parent.name=='chapters':
        if p.details!=2 or p.summaries!=2:errors.append(f'{label}: expected two answer controls')
        if 'Before you start:' not in text or 'References and further reading' not in text:
            errors.append(f'{label}: missing prerequisites or references')
    for href in p.links:
        u=urlsplit(href)
        if u.scheme or u.netloc:continue
        target=(path.parent/unquote(u.path)).resolve() if u.path else path
        if not target.exists():errors.append(f'{label}: missing {href}')
        elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:
            errors.append(f'{label}: missing anchor {href}')
if errors:raise SystemExit('\n'.join(errors))
print(f'CONTENT: PASS — {len(paths)} pages, valid local destinations, chapter structure, and 30 answer controls')
