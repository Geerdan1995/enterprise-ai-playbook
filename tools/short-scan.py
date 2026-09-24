# -*- coding: utf-8 -*-
"""短句候选扫描：把 md 稿里 N 字以下的叙述轨句子逐条列出，供金句病判读。

用法：python tools/short-scan.py <md文件...> [-n 10]

口径（与判读文档一致）：
- 句子以 。！？… 收尾，引号内的句末标点不切句（引语是对白的，不归叙述管）
- 候选＝句子的叙述骨架（剥掉引文）≤N 字，且句内引文合计 ≤3 字
  （"容忍区间"这类 4 字以上的引语句属引语承载，不按短句判；"化""客户"这类嵌词不算引文）
- 段末无标点残句算一句；冒号/引号引导的前缀碎片（"老蔡问："）不算
- md 方言：空行＝分段，单换行＝段内换行——单换行独占一行的单句标"独行"档（独行拍）
- 段首加粗章名/人名剥离后再计字数（**8｜许曼的表**——财务对账。 按"财务对账"计）
- 跳过：标题、表格、插图、代码块、分场线、::: 栅栏（题记/文书/日志/流程/对照/提示）、全斜体副题
- 已知边界：—— 与 ； 不切句，从句级顿拍不在射程内
- 输出分档：独立成段 > 独行 > 段末 > 段内（首/中）> 列表项/引导段
"""
import argparse
import io
import re
import sys

SENT_CHARS = '。！？…'


COMMENT = re.compile(r'<!--.*?-->|\{#[^}]*\}')
BOLD = re.compile(r'\*\*(.+?)\*\*')
ITALIC = re.compile(r'\*(.+?)\*')
LEAD_BOLD = re.compile(r'^\*\*[^*]+\*\*')
LIST_UL = re.compile(r'^[-*+]\s+')
LIST_OL = re.compile(r'^\d+[.、]\s+')
SUBTITLE = re.compile(r'^\*[^*|]+\*$')
CORE = re.compile(r'[^\w]')
QUOTE_SPAN = re.compile(r'[“"]([^“”"]*)[”"]')

CAT_ORDER = ['独立成段', '独行', '段末', '段内', '列表项', '引导段']


def core_len(s):
    return len(CORE.sub('', s))


def clean_inline(s):
    s = COMMENT.sub('', s)
    s = BOLD.sub(r'\1', s)
    s = ITALIC.sub(r'\1', s)
    return s


def split_sentences(text):
    """按引号外的 。！？… 切句。返回 [(整句原文, 是否有句末标点)]。"""
    sents, buf, in_q = [], [], False
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c == '“':
            in_q, buf = True, buf + [c]
        elif c == '”':
            in_q, buf = False, buf + [c]
        elif c == '"':
            in_q, buf = not in_q, buf + [c]
        elif c in SENT_CHARS and not in_q:
            j = i
            while j < n and text[j] in SENT_CHARS:
                j += 1
            buf.append(text[i:j])
            sents.append((''.join(buf), True))
            buf = []
            i = j
            continue
        else:
            buf.append(c)
        i += 1
    if ''.join(buf).strip():
        sents.append((''.join(buf), False))
    return sents


def skeleton(sent):
    """返回（叙述骨架, 引文字数）。"""
    qlen = sum(len(m.group(1)) for m in QUOTE_SPAN.finditer(sent))
    return QUOTE_SPAN.sub('', sent), qlen


def scan(path, limit):
    lines = io.open(path, encoding='utf-8').read().split('\n')
    items = []
    fence = code = False
    para = []

    def flush():
        if not para:
            return
        block, para[:] = para[:], []
        first = block[0][1].strip()
        if first.startswith('#') or first.startswith('![') or first == '* * *':
            return
        if SUBTITLE.match(first):
            return
        if any(l.strip().startswith('|') for _, l in block):
            return
        cat_prefix = ''
        if first.startswith('>'):
            cat_prefix = '引导段'
            preps = [re.sub(r'^\s*>\s?', '', l).strip() for _, l in block]
        elif LIST_UL.match(first) or LIST_OL.match(first):
            cat_prefix = '列表项'
            preps = [LIST_UL.sub('', LIST_OL.sub('', l.strip(), 1), 1).strip() for _, l in block]
        else:
            preps = [l.strip() for _, l in block]
        preps[0] = LEAD_BOLD.sub('', preps[0])
        seq = []  # 每句：text/terminated/len/qlen/alone
        for t in preps:
            t = clean_inline(t)
            if not t:
                continue
            line_sents = []
            for stext, term in split_sentences(t):
                skel, qlen = skeleton(stext)
                if not skel.strip():
                    continue
                line_sents.append({'text': stext.strip(), 'term': term,
                                   'len': core_len(skel), 'qlen': qlen})
            for s in line_sents:
                s['alone'] = len(line_sents) == 1
            seq.extend(line_sents)
        if not seq:
            return
        # 引导碎片丢弃：未收尾且非段末
        alive = [s for s in seq if s['term'] or s is seq[-1]]
        for i, s in enumerate(alive):
            if not 1 <= s['len'] <= limit or s['qlen'] > 3:
                continue
            if cat_prefix:
                cat = cat_prefix
            elif len(alive) == 1 and s['alone'] and s['qlen'] == 0 and len(preps) == 1:
                cat = '独立成段'
            elif s['alone'] and s['qlen'] == 0 and len(preps) > 1:
                cat = '独行'
            elif i == len(alive) - 1:
                cat = '段末'
            else:
                cat = '段内'
            items.append({
                'line': block[0][0], 'cat': cat, 'text': s['text'],
                'prev': alive[i - 1]['text'] if i > 0 else None,
                'next': alive[i + 1]['text'] if i + 1 < len(alive) else None,
            })

    for ln, raw in enumerate(lines, 1):
        s = raw.strip()
        if code:
            if s.startswith('```'):
                code = False
            continue
        if s.startswith('```'):
            flush()
            code = True
            continue
        if fence:
            if s.startswith(':::'):
                fence = False
            continue
        if s.startswith(':::'):
            flush()
            fence = True
            continue
        if not s:
            flush()
            continue
        para.append((ln, raw))
    flush()
    return items


def ctx(s, tail=False):
    if s is None:
        return '—'
    t = re.sub(r'\s+', '', s)
    if len(t) <= 18:
        return t
    return ('…' + t[-18:]) if tail else (t[:18] + '…')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('files', nargs='+')
    ap.add_argument('-n', type=int, default=10, help='字数上限（默认10）')
    a = ap.parse_args()
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    for path in a.files:
        items = scan(path, a.n)
        name = path.replace('\\', '/').split('/')[-1]
        print(f'===== {name}  阈值≤{a.n}字  候选 {len(items)} 条 =====')
        for cat in CAT_ORDER:
            group = [it for it in items if it['cat'] == cat]
            if not group:
                continue
            print(f'\n【{cat}】{len(group)} 条')
            for it in group:
                print(f"L{it['line']:03d} ◆{it['text']}")
                print(f"      上:{ctx(it['prev'], tail=True)}  下:{ctx(it['next'])}")
        print()


if __name__ == '__main__':
    main()
