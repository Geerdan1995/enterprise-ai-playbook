# -*- coding: utf-8 -*-
r"""manuscript/ 目录 md 稿 ↔ fragments/ html 片段 双向转换器

作者改 md（事实源），compile 生成 fragments 供 build.js 使用。
用法：
  python tools/manuscript.py export    # fragments -> manuscript/*.md（迁移用，日常不跑）
  python tools/manuscript.py compile   # manuscript/*.md -> fragments/*.html（构建第一步）
  python tools/manuscript.py verify    # 逐文件 round-trip 校验（md 编译回 html 须与现件逐字节一致）

md 方言（转换器只认这些构造，其余文字原样保留）：
  # 01 章题          章/附录标题（编号与题间一个空格；紧随其后的 *English* 行＝英文副题）
  ## 小节题 {#id}    三级标题（{#id} 可选，附录G六问用它）
  ### 小节题         四级标题      #### 小节题  五级标题
  空行分段；段落内回车＝段内换行
  **加粗**  *斜体*    行内样式
  1. 条目            有序列表       - 条目  无序列表
  * * *              分场线
  > 引导段           灰底引导段（section-intro）
  ![图题](../assets/illustrations/shots/xx.png)   插图（图题即 alt 文字）
  <!--表宽:16%,14%,-,--->                        表格列宽注释（紧贴表格上方，别删）
  | 表头 | 表头 |                                 GFM 表格；单元格内换行写 <br/>
  | --- | --- |
  | 内容 | 内容 |
  :::题记 … :::      章首题记；内部以——开头的行＝署名行
  :::文书 标题 … :::  书中文书块；":::文书"后不带标题＝无题文书；行尾加 \ ＝行内强制换行
  :::日志 日期 … :::  章末工作日志；内部：普通段落＋"- "列表，空行原样保留
  :::流程 … :::      流程图：条目行＋箭头行（→）交替
  :::对照 … :::      正反对照块：内部"好：…"行与"坏：…"行
  :::提示 … :::      提示块（tip）
  ```html … ```      原样 HTML（无表头表格等机器格式，勿手改）
"""
import html
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRAG = os.path.join(ROOT, 'fragments')
MD = os.path.join(ROOT, 'manuscript')

# fragment 文件名 -> [(md 文件名, h2 id), ...]（多 md 共属一个 fragment 时按书序拆分）
FILES = [
    ('02-editor-note.html', [('00-编者按.md', 'editor-note')]),
    ('part1-ch1.html', [('第01章-三月十七号，四个坏消息.md', 'ch1')]),
    ('part1-ch2.html', [('第02章-试出来的难处.md', 'ch2')]),
    ('part2-ch3.html', [('第03章-档案馆里的老人.md', 'ch3')]),
    ('part2-ch4.html', [('第04章-两万三千份文件.md', 'ch4')]),
    ('part2-ch5.html', [('第05章-五百个节点的图.md', 'ch5')]),
    ('part2-ch6.html', [('第06章-老唐的失眠夜.md', 'ch6')]),
    ('part2-ch7.html', [('第07章-六月三十号.md', 'ch7')]),
    ('part3-ch8.html', [('第08章-许曼的表.md', 'ch8')]),
    ('part3-ch9.html', [('第09章-段兴的背包.md', 'ch9')]),
    ('part3-ch10.html', [('第10章-一张报价单.md', 'ch10')]),
    ('part3-ch11.html', [('第11章-看不见的订单.md', 'ch11')]),
    ('part3-ch12.html', [('第12章-数人头的.md', 'ch12')]),
    ('part3-ch13.html', [('第13章-墙.md', 'ch13')]),
    ('part3-ch14.html', [('第14章-各自为战.md', 'ch14')]),
    ('part4-ch15.html', [('第15章-审核通知.md', 'ch15')]),
    ('part4-ch16.html', [('第16章-董事会的账.md', 'ch16')]),
    ('part4-ch17.html', [('第17章-叶老的图纸.md', 'ch17')]),
    ('part5-ch18.html', [('第18章-开工.md', 'ch18')]),
    ('part5-ch19.html', [('第19章-五个名字的供应商.md', 'ch19')]),
    ('part5-ch20.html', [('第20章-灰区.md', 'ch20')]),
    ('part5-ch21.html', [('第21章-审核日.md', 'ch21')]),
    ('part5-ch22.html', [('第22章-老唐退休那天.md', 'ch22')]),
    ('interlude-1.html', [('间章一-八月的会.md', 'interlude1')]),
    ('interlude-2.html', [('间章二-来客.md', 'interlude2')]),
    ('appendix.html', [
        ('附录A-一张图看懂知识图谱与本体论.md', 'appA'),
        ('附录B-本体论小辞典.md', 'appB'),
        ('附录C-情节与真实案例对照表.md', 'appC'),
        ('附录D-延伸阅读.md', 'appD'),
        ('附录E-把AI用起来——写给企业里的人.md', 'appE'),
        ('附录F-AI用起来之后——一个实践者的方法论笔记.md', 'appF'),
        ('附录G-二十四家，六个问题——一本案例集的横读.md', 'appG'),
        ('附录H-AI应用落地工作法.md', 'appH'),
        ('附录K-解决方案工具箱.md', 'appK'),
    ]),
    ('98-afterword.html', [('99-后记-青山没打的七仗.md', 'afterword')]),
]
BY_MD = {m: (f, i) for f, mds in FILES for (m, i) in mds}
BY_FRAG = {f: mds for f, mds in FILES}

RE_H2 = re.compile(r'^<h2 class="section-title page-break" id="([^"]+)"><span class="num">([^<]*)</span>([^<]*)</h2>$')
RE_H3 = re.compile(r'^<h3(?: id="([^"]+)")?>([^<]*)</h3>$')
RE_H4 = re.compile(r'^<h4>([^<]*)</h4>$')
RE_H5 = re.compile(r'^<h5>([^<]*)</h5>$')
RE_P = re.compile(r'^<p>(.*)</p>$')
RE_PEN = re.compile(r'^<p class="section-en">(.*)</p>$')
RE_PINTRO = re.compile(r'^<p class="section-intro">(.*)</p>$')
RE_FIG = re.compile(r'^<div class="figure"><img src="([^"]+)" alt="([^"]*)"><div class="figcap">([^<]*)</div></div>$')
RE_WHO = re.compile(r'^<span class="who">(.*)</span>$')
RE_LI = re.compile(r'^<li>(.*)</li>$')
RE_DOCQ = re.compile(r'^<div class="doc-quote">$')
RE_DOCT = re.compile(r'^<div class="doc-title">(.*)</div>$')
RE_JOUR = re.compile(r'^<div class="journal" data-date="([^"]*)">$')
RE_FLOWITEM = re.compile(r'^<div class="flow-item">(.*)</div>$')
RE_FLOWARROW = re.compile(r'^<div class="flow-arrow">(.*)</div>$')
RE_CMP = re.compile(r'^<div class="compare-(good|bad)">(.*)</div>$')
ARROWS = set('→↓←↑↔⇒')

# 图形区收集器的"已知构造"终止线：命中即停止收集（这些走各自的转换分支）
_KNOWN_STARTS = ('<h2', '<div class="chapter-epigraph">', '<div class="scene-break"></div>',
                 '<div class="figure">', '<div class="journal', '<div class="doc-quote">',
                 '<div class="flow">', '<div class="compare">', '<div class="tip">',
                 '<ul>', '<ol>', '<table>', '<p class=')


def _known_line(s):
    return bool(RE_H2.match(s) or RE_H3.match(s) or RE_H4.match(s) or RE_H5.match(s)
                or RE_P.match(s) or RE_PEN.match(s) or RE_FIG.match(s) or RE_DOCQ.match(s)
                or RE_JOUR.match(s) or s.startswith(_KNOWN_STARTS))


class X(Exception):
    pass


TAGWARN = []


def to_inline(s, keep_br=False):
    """html 行内文本 -> md 行内（strong→**，em→*，实体还原；keep_br 时 <br/> 原样保留）"""
    if s.count('<strong>') != s.count('</strong>') or s.count('<em>') != s.count('</em>'):
        raise X('行内标签不配对: ' + s[:60])
    s = (s.replace('<strong>', '\x00').replace('</strong>', '\x01')
          .replace('<em>', '\x02').replace('</em>', '\x03'))
    t = html.unescape(s)
    if not keep_br:
        t = t.replace('<br/>', '\n')
    t = t.replace('\x00', '**').replace('\x01', '**').replace('\x02', '*').replace('\x03', '*')
    if t.count('**') % 2:
        raise X('** 不配对: ' + t[:60])
    return t


def from_inline(s, keep_br=False):
    """md 行内 -> html 行内文本（**→strong，*→em；其余原样直通不转义，
    疑似 HTML 标签的文本记入 TAGWARN 只警告不拦截；keep_br 时 \n 不转 <br/>）"""
    if s.count('**') % 2:
        raise X('** 不配对（加粗没合上？）: ' + s[:60])
    out = []
    for k, part in enumerate(s.split('**')):
        segs = part.split('*')
        if len(segs) % 2 == 0:
            raise X('* 不配对（斜体没合上？）: ' + s[:60])
        p2 = ''
        for j2, seg in enumerate(segs):
            if k % 2 == 0 and j2 % 2 == 0:
                m = re.search(r'</?[a-zA-Z][a-zA-Z0-9]*(\s[^<>]*)?>', seg)
                if m and m.group(0) not in ('<br/>', '<br>', '<p>', '</p>'):
                    TAGWARN.append((m.group(0), s[:50]))
            p2 += (('<em>' if j2 % 2 else '') + seg + ('</em>' if j2 % 2 else ''))
        out.append(('<strong>' if k % 2 else '') + p2 + ('</strong>' if k % 2 else ''))
    t = ''.join(out)
    return t if keep_br else t.replace('\n', '<br/>')


def html_seg_to_md_lines(seg):
    """一段 html 行内文本 -> md 行列表：<br/> 拆续行（行尾 \\），strong/em 转 **//*"""
    parts = [to_inline(x) for x in seg.split('<br/>')]
    return [p + '\\' for p in parts[:-1]] + [parts[-1]]


def fence_html_to_lines(html_lines):
    """fence 内部 html 行 -> md 行：每个 html 行一行；行内 <br/> 拆为以 \\ 结尾的续行"""
    out = []
    for l in html_lines:
        segs = l.split('<br/>')
        for k, seg in enumerate(segs):
            out.append(html.unescape(seg) + ('\\' if k < len(segs) - 1 else ''))
    return out


def fence_lines_to_html(md_lines):
    r"""fence 内部 md 行 -> html 行：行尾 \ 表示与下一行同属一行（<br/> 连接）"""
    groups, pending = [], None
    for l in md_lines:
        cont = l.endswith('\\')
        text = l[:-1] if cont else l
        if pending is None:
            pending = [text]
        else:
            pending.append(text)
        if not cont:
            groups.append(pending)
            pending = None
    if pending is not None:
        groups.append(pending)
    return ['<br/>'.join(from_inline(x) for x in g) for g in groups]


# ---------------- export：fragments -> md ----------------

def export_frag(fname):
    lines = io.open(os.path.join(FRAG, fname), encoding='utf-8').read().split('\n')
    blocks, i, n = [], 0, len(lines)

    while i < n:
        s = lines[i].strip()
        if s == '<div class="content">' or s == '':
            i += 1
            continue
        if s == '</div>' and i >= n - 2:
            break
        m = RE_H2.match(s)
        if m:
            mds = BY_FRAG[fname]
            if m.group(1) != mds[0][1] and m.group(1) not in [x[1] for x in mds]:
                raise X('%s h2 id=%s 不在映射中' % (fname, m.group(1)))
            blocks.append(('raw', '# %s %s' % (m.group(2), m.group(3).strip())))
            i += 1
            continue
        m = RE_PEN.match(s)
        if m:
            prev = blocks[-1] if blocks else None
            if prev and prev[0] == 'raw' and isinstance(prev[1], str) and prev[1].startswith('# '):
                blocks[-1] = ('lines', [prev[1], '*' + to_inline(m.group(1)) + '*'])
            else:
                raise X('%s 英文副题不在章标题后: %s' % (fname, s[:60]))
            i += 1
            continue
        m = RE_H3.match(s)
        if m:
            blocks.append(('raw', '## ' + to_inline(m.group(2)) + (' {#%s}' % m.group(1) if m.group(1) else '')))
            i += 1
            continue
        m = RE_H4.match(s)
        if m:
            blocks.append(('raw', '### ' + to_inline(m.group(1))))
            i += 1
            continue
        m = RE_H5.match(s)
        if m:
            blocks.append(('raw', '#### ' + to_inline(m.group(1))))
            i += 1
            continue
        if s == '<div class="chapter-epigraph">':
            i += 1
            inner = []
            while lines[i].strip() != '</div>':
                inner.append(lines[i].strip())
                i += 1
            i += 1
            body = []
            for t in inner:
                wm = RE_WHO.match(t)
                if wm:
                    if '<br/>' in wm.group(1):
                        raise X('%s 题记署名含换行，需人工处理: %s' % (fname, t[:60]))
                    body.append(to_inline(wm.group(1)))
                else:
                    body.extend(html_seg_to_md_lines(t))
            blocks.append(('fence', '题记', '', body))
            continue
        # 单行紧凑文书块（G附录词典词条形态）：<div class="doc-quote">[<div class="doc-title">T</div>]<p>…</p>[<p>…</p>]</div>
        if s.startswith('<div class="doc-quote">') and s != '<div class="doc-quote">' and s.endswith('</div>'):
            inner = s[len('<div class="doc-quote">'):-len('</div>')]
            title = ''
            tm = re.match(r'^<div class="doc-title">(.*)</div>(.*)$', inner)
            if tm:
                title, inner = tm.group(1), tm.group(2)
            body = []
            pos = 0
            for pm in re.finditer(r'<p>(.*?)</p>', inner):
                if inner[pos:pm.start()].strip():
                    raise X('%s 文书块内 p 外有散落文本: %r' % (fname, inner[pos:pm.start()][:60]))
                seg = html_seg_to_md_lines(pm.group(1))
                seg[0] = '<p>' + seg[0]
                seg[-1] = seg[-1] + '</p>'
                body.extend(seg)
                pos = pm.end()
            if inner[pos:].strip():
                raise X('%s 文书块尾部有散落文本: %r' % (fname, inner[pos:][:60]))
            blocks.append(('fence', '文书', to_inline(title), body))
            i += 1
            continue
        if s == '<div class="scene-break"></div>':
            blocks.append(('raw', '* * *'))
            i += 1
            continue
        m = RE_FIG.match(s)
        if m:
            if m.group(2) != m.group(3):
                raise X('%s 插图 alt 与图题不一致: %s' % (fname, s[:70]))
            blocks.append(('raw', '![%s](%s)' % (to_inline(m.group(2)), m.group(1))))
            i += 1
            continue
        if RE_DOCQ.match(s):
            i += 1
            arg = ''
            tm = RE_DOCT.match(lines[i].strip())
            if tm:
                arg = to_inline(tm.group(1))
                i += 1
            inner = []
            while lines[i].strip() != '</div>':
                inner.append(lines[i].strip())
                i += 1
            i += 1
            body = []
            for t in inner:
                body.extend(html_seg_to_md_lines(t))
            blocks.append(('fence', '文书', arg, body))
            continue
        m = RE_JOUR.match(s)
        if m:
            i += 1
            inner = []
            while lines[i].strip() != '</div>':
                inner.append(lines[i])
                i += 1
            i += 1
            body = []
            for l in inner:
                t = l.strip()
                if t == '':
                    body.append('')
                elif t == '<ul>' or t == '</ul>':
                    continue
                else:
                    lm = RE_LI.match(t)
                    if lm:
                        body.append('- ' + to_inline(lm.group(1)))
                    else:
                        pm = RE_P.match(t)
                        if not pm:
                            raise X('%s journal 内不认识的行: %r' % (fname, t[:60]))
                        body.extend(fence_html_to_lines([pm.group(1)]))
            blocks.append(('fence', '日志', m.group(1), body))
            continue
        if s == '<div class="flow">':
            j = i + 1
            body, ok = [], True
            while lines[j].strip() != '</div>':
                t = lines[j].strip()
                mi, ma = RE_FLOWITEM.match(t), RE_FLOWARROW.match(t)
                if mi:
                    body.append(to_inline(mi.group(1)))
                elif ma:
                    body.append(ma.group(1))
                else:
                    ok = False
                j += 1
            j += 1
            if ok:
                blocks.append(('fence', '流程', '', body))
            else:
                blocks.append(('lines', ['```html'] + lines[i:j] + ['```']))
            i = j
            continue
        if s == '<div class="compare">':
            i += 1
            body = []
            while lines[i].strip() != '</div>':
                t = lines[i].strip()
                mc = RE_CMP.match(t)
                if not mc:
                    raise X('%s compare 内不认识的行: %r' % (fname, t[:60]))
                body.append(('好：' if mc.group(1) == 'good' else '坏：') + to_inline(mc.group(2)))
                i += 1
            i += 1
            blocks.append(('fence', '对照', '', body))
            continue
        if s.startswith('<div class="tip">'):
            tm = re.match(r'^<div class="tip">(.*)</div>$', s)
            if not tm:
                raise X('%s tip 跨行: %s' % (fname, s[:60]))
            blocks.append(('fence', '提示', '', [to_inline(tm.group(1))]))
            i += 1
            continue
        if s in ('<ul>', '<ol>'):
            ordered = (s == '<ol>')
            i += 1
            items = []
            closer = '</ol>' if ordered else '</ul>'
            while lines[i].strip() != closer:
                lm = RE_LI.match(lines[i].strip())
                if not lm:
                    raise X('%s %s 内非 li 行: %r' % (fname, s, lines[i][:60]))
                items.append(to_inline(lm.group(1)))
                i += 1
            i += 1
            if ordered:
                blocks.append(('lines', ['%d. %s' % (k + 1, it) for k, it in enumerate(items)]))
            else:
                blocks.append(('lines', ['- ' + it for it in items]))
            continue
        if s == '<table>':
            j = i + 1
            tb = []
            while lines[j].strip() != '</table>':
                tb.append(lines[j].strip())
                j += 1
            endj = j
            i_next = j + 1
            thead_cells, widths, rows = None, [], []
            k = 0
            if tb and tb[0].startswith('<thead>'):
                mh = re.match(r'^<thead><tr>(.*)</tr></thead>$', tb[0])
                if not mh:
                    raise X('%s thead 跨行需人工处理: %s' % (fname, tb[0][:60]))
                thead_cells = re.findall(r'<th(?:\s[^>]*)?>(.*?)</th>', mh.group(1))
                widths = re.findall(r'<th(?:\s+style="width:([^"]*)")?>', mh.group(1))
                k = 1
            if thead_cells is None:
                blocks.append(('lines', ['```html'] + lines[i:endj + 1] + ['```']))
                i = i_next
                continue
            if k < len(tb) and tb[k] == '<tbody>':
                k += 1
                while tb[k] != '</tbody>':
                    rows.append(tb[k])
                    k += 1
                k += 1
            out_lines = []
            if any(w for w in widths):
                out_lines.append('<!--表宽:' + ','.join(w or '-' for w in widths) + '-->')
            out_lines.append('| ' + ' | '.join(to_inline(c, keep_br=True) for c in thead_cells) + ' |')
            out_lines.append('|' + ''.join(' --- |' for _ in thead_cells))
            for tr in rows:
                m2 = re.match(r'^<tr>(.*)</tr>$', tr)
                if not m2:
                    raise X('%s 表格行不认识: %r' % (fname, tr[:60]))
                cells = re.findall(r'<td(?:\s[^>]*)?>(.*?)</td>', m2.group(1))
                if len(cells) != len(thead_cells):
                    raise X('%s 表格列数与表头不齐: %r' % (fname, tr[:60]))
                out_lines.append('| ' + ' | '.join(to_inline(c, keep_br=True) for c in cells) + ' |')
            blocks.append(('lines', out_lines))
            i = i_next
            continue
        m = RE_P.match(s)
        if m:
            blocks.append(('raw', to_inline(m.group(1))))
            i += 1
            continue
        m = RE_PINTRO.match(s)
        if m:
            blocks.append(('lines', ['> ' + to_inline(m.group(1))]))
            i += 1
            continue
        if s.startswith('<p '):
            blocks.append(('lines', ['```html', lines[i], '```']))
            i += 1
            continue
        # 内联样式图形区（如附录A三层楼图）：机器排版，整体原样栅栏保真
        if s.startswith('<div style=') or s.startswith('<!--'):
            j = i
            region = []
            while j < n:
                t = lines[j].strip()
                if t == '</div>' and j >= n - 3:
                    break
                if t == '':
                    region.append('')
                    j += 1
                    continue
                if t.startswith('<') and not _known_line(t):
                    region.append(lines[j])
                    j += 1
                    continue
                break
            while region and region[-1] == '':
                region.pop()
            if not region:
                raise X('%s L%d 空图形区' % (fname, i + 1))
            blocks.append(('lines', ['```html'] + region + ['```']))
            i = j
            continue
        raise X('%s L%d 不认识的行: %r' % (fname, i + 1, s[:80]))

    return blocks


def ser_block(b):
    if b[0] in ('raw', 'lines'):
        return '\n'.join(b[1] if isinstance(b[1], list) else [b[1]])
    return '\n'.join([':::%s%s' % (b[1], (' ' + b[2]) if b[2] else '')] + b[3] + [':::'])


def export():
    os.makedirs(MD, exist_ok=True)
    for fname, mds in FILES:
        blocks = export_frag(fname)
        if len(mds) == 1:
            parts = [blocks]
        else:
            # 多 md：按 h2（块首行以 '# ' 开头）切分，前导块并入第一片
            def is_h2(b):
                first = b[1][0] if (b[0] == 'lines' and isinstance(b[1], list)) else b[1]
                return isinstance(first, str) and first.startswith('# ')
            starts = [k for k, b in enumerate(blocks) if is_h2(b)]
            if len(starts) != len(mds):
                raise X('%s h2 数(%d)与 md 文件数(%d)不符' % (fname, len(starts), len(mds)))
            bounds = starts + [len(blocks)]
            parts = [blocks[bounds[k]:bounds[k + 1]] for k in range(len(mds))]
        for (mname, _), part in zip(mds, parts):
            if not part:
                raise X('%s 切出空文件 %s' % (fname, mname))
            text = '\n\n'.join(ser_block(b) for b in part)
            with io.open(os.path.join(MD, mname), 'w', encoding='utf-8', newline='\n') as f:
                f.write(text + '\n')
            print('导出', mname)


# ---------------- compile：md -> fragments ----------------

def split_blocks(mlines, mname):
    """md 行 -> 顶层块。kind: h1/h3/h4/h5/para/list/olist/fence/scene/img/gtable/quote/table"""
    blocks, i, n = [], 0, len(mlines)
    stop = lambda s: (s == '' or s.startswith('- ') or s.startswith(':::') or s.startswith('#')
                      or s.startswith('> ') or s.startswith('|') or s.startswith('<!--')
                      or s in ('```html', ':::', '* * *', '***') or s.startswith('![')
                      or re.match(r'\d+\. ', s) is not None)
    while i < n:
        s = mlines[i].strip()
        if s == '':
            i += 1
            continue
        if s in ('* * *', '***'):
            blocks.append(('scene',))
            i += 1
            continue
        if s.startswith('#### '):
            blocks.append(('h5', s[5:]))
            i += 1
            continue
        if s.startswith('### '):
            blocks.append(('h4', s[4:]))
            i += 1
            continue
        if s.startswith('## '):
            blocks.append(('h3', s[3:]))
            i += 1
            continue
        if s.startswith('# '):
            blocks.append(('h1', s[2:]))
            i += 1
            continue
        if s == '```html':
            i += 1
            buf = []
            while i < n and mlines[i].strip() != '```':
                buf.append(mlines[i])
                i += 1
            if i >= n:
                raise X('%s html fence 未闭合' % mname)
            i += 1
            blocks.append(('table', buf))
            continue
        if s.startswith('<!--表宽:') or s.startswith('|'):
            widths = None
            if s.startswith('<!--表宽:'):
                widths = s[len('<!--表宽:'):-len('-->')].split(',')
                i += 1
                if i >= n:
                    raise X('%s 表宽注释后没有表格' % mname)
                s = mlines[i].strip()
                if not s.startswith('|'):
                    raise X('%s 表宽注释后必须紧跟表格' % mname)
            rows = []
            while i < n and mlines[i].strip().startswith('|'):
                rows.append(mlines[i].strip())
                i += 1
            blocks.append(('gtable', widths, rows))
            continue
        if s.startswith('> '):
            buf = []
            while i < n and mlines[i].strip().startswith('> '):
                buf.append(mlines[i].strip()[2:])
                i += 1
            blocks.append(('quote', buf))
            continue
        if s.startswith(':::'):
            body = s[3:].strip()
            if body == '':
                raise X('%s 孤立的收尾 ::: （缺块头或多了收尾）' % mname)
            kind = body.split(' ', 1)[0]
            arg = body[len(kind):].strip()
            if kind not in ('题记', '文书', '日志', '流程', '对照', '提示'):
                raise X('%s 不认识的块类型: %r（只认 题记/文书/日志/流程/对照/提示）' % (mname, kind))
            if kind == '日志' and arg == '':
                raise X('%s :::日志 缺日期参数（如 :::日志 2026年6月15日夜）' % mname)
            i += 1
            buf = []
            while i < n and mlines[i].strip() != ':::':
                buf.append(mlines[i])
                i += 1
            if i >= n:
                raise X('%s :::%s 未闭合（缺收尾 :::）' % (mname, kind))
            i += 1
            blocks.append(('fence', kind, arg, buf))
            continue
        im = re.match(r'^!\[([^]]*)\]\(([^)]+)\)$', s)
        if im:
            blocks.append(('img', im.group(1), im.group(2)))
            i += 1
            continue
        if s.startswith('- '):
            items = []
            while i < n and mlines[i].strip().startswith('- '):
                items.append(mlines[i].strip()[2:])
                i += 1
            blocks.append(('list', items))
            continue
        if re.match(r'\d+\. ', s):
            items = []
            while i < n and re.match(r'\d+\. ', mlines[i].strip()):
                items.append(re.sub(r'^\d+\. ', '', mlines[i].strip()))
                i += 1
            blocks.append(('olist', items))
            continue
        buf = []
        while i < n and not stop(mlines[i].strip()):
            buf.append(mlines[i])
            i += 1
        blocks.append(('para', buf))
    return blocks


def cells_of(row):
    if not (row.startswith('|') and row.endswith('|')):
        raise X('表格行必须以 | 开头结尾: %r' % row[:60])
    return [c.strip() for c in row[1:-1].split('|')]


def compile_frag(fname):
    mds = BY_FRAG[fname]
    out = ['<div class="content">', '']
    for k, (mname, fid) in enumerate(mds):
        path = os.path.join(MD, mname)
        if not os.path.exists(path):
            raise X('找不到 %s（manuscript 目录缺文件，对照 tools/manuscript.py 的 FILES 清单）' % mname)
        mlines = io.open(path, encoding='utf-8').read().split('\n')
        if mlines and mlines[-1] == '':
            mlines = mlines[:-1]
        blocks = split_blocks(mlines, mname)
        prev_kind = None
        for b in blocks:
            kind = b[0]
            en = (kind == 'para' and len(b[1]) == 1 and prev_kind == 'h1'
                  and re.fullmatch(r'\*[^*]+\*', b[1][0].strip()))
            if prev_kind is not None and not en:
                out.append('')
            if kind == 'h1':
                parts = b[1].split(' ', 1)
                if len(parts) != 2 or not parts[1].strip():
                    raise X('%s 章标题应为"# 编号 题目": %r' % (mname, b[1]))
                out.append('<h2 class="section-title page-break" id="%s"><span class="num">%s</span> %s</h2>'
                           % (fid, parts[0], from_inline(parts[1].strip())))
            elif kind == 'h3':
                m = re.search(r'\s*\{#([A-Za-z0-9_-]+)\}$', b[1])
                txt, h3id = (b[1][:m.start()], m.group(1)) if m else (b[1], None)
                out.append('<h3%s>%s</h3>' % ((' id="%s"' % h3id) if h3id else '', from_inline(txt)))
            elif kind == 'h4':
                out.append('<h4>%s</h4>' % from_inline(b[1]))
            elif kind == 'h5':
                out.append('<h5>%s</h5>' % from_inline(b[1]))
            elif kind == 'scene':
                out.append('<div class="scene-break"></div>')
            elif kind == 'img':
                out.append('<div class="figure"><img src="%s" alt="%s"><div class="figcap">%s</div></div>'
                           % (b[2], from_inline(b[1]), from_inline(b[1])))
            elif kind == 'quote':
                out.append('<p class="section-intro">%s</p>' % from_inline('\n'.join(b[1])))
            elif kind == 'para':
                if en:
                    out.append('<p class="section-en">%s</p>' % from_inline(b[1][0].strip()[1:-1]))
                else:
                    out.append('<p>%s</p>' % from_inline('\n'.join(b[1])))
            elif kind == 'list':
                out.append('<ul>')
                for it in b[1]:
                    out.append('<li>%s</li>' % from_inline(it))
                out.append('</ul>')
            elif kind == 'olist':
                out.append('<ol>')
                for it in b[1]:
                    out.append('<li>%s</li>' % from_inline(it))
                out.append('</ol>')
            elif kind == 'table':
                out.extend(b[1])
            elif kind == 'gtable':
                widths, rows = b[1], b[2]
                if len(rows) < 3:
                    raise X('%s 表格至少要表头、| --- | 分隔线、一行内容' % mname)
                header = cells_of(rows[0])
                sep = cells_of(rows[1])
                if not all(re.fullmatch(r':?-{3,}:?', c) for c in sep):
                    raise X('%s 表格第二行必须是 | --- | --- | 分隔线: %r' % (mname, rows[1][:60]))
                if widths and len(widths) != len(header):
                    raise X('%s 表宽注释列数与表头不符' % mname)
                ths = ''
                for ci, c in enumerate(header):
                    w = widths[ci] if widths else '-'
                    ths += ('<th style="width:%s">%s</th>' % (w, from_inline(c, keep_br=True))) if w != '-' \
                        else ('<th>%s</th>' % from_inline(c, keep_br=True))
                out.append('<table>')
                out.append('<thead><tr>' + ths + '</tr></thead>')
                out.append('<tbody>')
                for r in rows[2:]:
                    tds = cells_of(r)
                    if len(tds) != len(header):
                        raise X('%s 表格行列数与表头不齐: %r' % (mname, r[:60]))
                    out.append('<tr>' + ''.join('<td>%s</td>' % from_inline(c, keep_br=True) for c in tds) + '</tr>')
                out.append('</tbody>')
                out.append('</table>')
            elif kind == 'fence':
                fkind, arg, buf = b[1], b[2], b[3]
                if fkind == '题记':
                    out.append('<div class="chapter-epigraph">')
                    for l in fence_lines_to_html(buf):
                        out.append(('<span class="who">%s</span>' % l) if l.startswith('——') else l)
                    out.append('</div>')
                elif fkind == '文书':
                    out.append('<div class="doc-quote">')
                    if arg:
                        out.append('<div class="doc-title">%s</div>' % from_inline(arg))
                    # 带 <p>…</p> 包裹的行＝带段距词条（G附录形态），原样透传；裸行＝紧凑行
                    out.extend(fence_lines_to_html(buf))
                    out.append('</div>')
                elif fkind == '日志':
                    out.append('<div class="journal" data-date="%s">' % arg)
                    i2, n2 = 0, len(buf)
                    while i2 < n2:
                        t = buf[i2].strip()
                        if t == '':
                            out.append('')
                            i2 += 1
                        elif t.startswith('- '):
                            out.append('<ul>')
                            while i2 < n2 and buf[i2].strip().startswith('- '):
                                out.append('<li>%s</li>' % from_inline(buf[i2].strip()[2:]))
                                i2 += 1
                            out.append('</ul>')
                        else:
                            run = []
                            while i2 < n2 and buf[i2].strip() != '' and not buf[i2].strip().startswith('- '):
                                run.append(buf[i2])
                                i2 += 1
                            out.extend('<p>%s</p>' % x for x in fence_lines_to_html(run))
                    out.append('</div>')
                elif fkind == '流程':
                    out.append('<div class="flow">')
                    for l in buf:
                        t = l.strip()
                        if t and all(ch in ARROWS for ch in t):
                            out.append('<div class="flow-arrow">%s</div>' % t)
                        else:
                            out.append('<div class="flow-item">%s</div>' % from_inline(l))
                    out.append('</div>')
                elif fkind == '对照':
                    out.append('<div class="compare">')
                    for l in buf:
                        if l.startswith('好：'):
                            out.append('<div class="compare-good">%s</div>' % from_inline(l[len('好：'):]))
                        elif l.startswith('坏：'):
                            out.append('<div class="compare-bad">%s</div>' % from_inline(l[len('坏：'):]))
                        else:
                            raise X('%s :::对照 内每行必须以"好："或"坏："开头: %r' % (mname, l[:40]))
                    out.append('</div>')
                else:
                    out.append('<div class="tip">%s</div>' % '<br/>'.join(fence_lines_to_html(buf)))
            prev_kind = kind
    out.append('')
    out.append('</div>')
    return '\n'.join(out) + '\n'


def compile_cmd():
    for fname, mds in FILES:
        text = compile_frag(fname)
        with io.open(os.path.join(FRAG, fname), 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
        print('编译', ' + '.join(m for m, _ in mds), '->', fname)
    for tag, ctx in TAGWARN:
        print('⚠ 正文含疑似 HTML 标签文本（原样进书，请确认是有意为之）: %r @ %s' % (tag, ctx))


def verify():
    bad = 0
    for fname, mds in FILES:
        orig = io.open(os.path.join(FRAG, fname), encoding='utf-8').read()
        try:
            built = compile_frag(fname)
        except X as e:
            print('❌', ' + '.join(m for m, _ in mds), '编译失败:', e)
            bad += 1
            continue
        if built != orig:
            a = [l.strip() for l in orig.split('\n') if l.strip()]
            b = [l.strip() for l in built.split('\n') if l.strip()]
            if a == b:
                print('○', ' + '.join(m for m, _ in mds)[:40], '仅空行位置不同（先跑 compile 规范化）')
                continue
            print('❌', ' + '.join(m for m, _ in mds)[:40], '内容有差异，第一处:')
            for k in range(max(len(a), len(b))):
                x = a[k] if k < len(a) else '<EOF>'
                y = b[k] if k < len(b) else '<EOF>'
                if x != y:
                    print('   L%d 原: %r' % (k + 1, x[:90]))
                    print('   L%d 编: %r' % (k + 1, y[:90]))
                    break
            bad += 1
        else:
            print('✓', ' + '.join(m for m, _ in mds)[:40])
    print('---', ('全部 %d 个 fragment 验证通过' % len(FILES)) if not bad else ('%d 个 fragment 内容有差异' % bad))
    return bad


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'verify'
    if cmd == 'export':
        export()
    elif cmd == 'compile':
        compile_cmd()
    elif cmd == 'verify':
        sys.exit(1 if verify() else 0)
    else:
        print(__doc__)
