# -*- coding: utf-8 -*-
"""电报腔扫描：<p>内纯叙述段（无引号）中，
A=[；。]后跟"1-4字，1-5字。"电报句；B=≤10字独立短段。doc-quote/journal豁免。"""
import io, re, sys

def scan(path):
    t = io.open(path, encoding='utf-8').read()
    t = re.sub(r'<div class="doc-quote">.*?</div>\s*', '', t, flags=re.S)
    t = re.sub(r'<div class="journal".*?</div>\n</div>\s*', '', t, flags=re.S)  # 章末日志整体豁免
    paras = re.findall(r'<p[^>]*>(.*?)</p>', t, flags=re.S)
    raw_ps = re.findall(r'<p[^>]*>', t)
    a_hits, b_hits = [], []
    for tag, p in zip(raw_ps, paras):
        if 'section-en' in tag:
            continue  # 英文副题不是叙述
        text = re.sub(r'<[^>]+>', '', p).strip()
        if not text or '"' in text:
            continue  # 纯叙述段才计
        # 段首也算：段首电报句同样无主语
        padded = '。' + text
        for m in re.finditer(r'[；。]([^，。；！？\s]{1,4})，([^。；！？\s]{1,5})。', padded):
            frag = m.group(1) + '，' + m.group(2) + '。'
            a_hits.append((frag, text))
        if len(text) <= 10:
            b_hits.append(text)
    return a_hits, b_hits

if __name__ == '__main__':
    total = 0
    for path in sys.argv[1:]:
        a, b = scan(path)
        print(f'== {path}  A(电报句):{len(a)}  B(短段):{len(b)}  合计:{len(a)+len(b)}')
        for frag, ctx in a:
            print(f'  A [{frag}]  <<{ctx[:40]}>>')
        for s in b:
            print(f'  B [{s}]')
        total += len(a) + len(b)
    sys.exit(0)
