# -*- coding: utf-8 -*-
"""
style-report.py —— 风格量化指纹报告（风格圣经 v2.0 第一节指纹的测量器）

对照《理想之城》基准值（38.3 万字全书）：
  对话标签 "说："      34.26/万字（说道/笑道/问道≈0）
  台词长度             中位 14 字，≤10 字占 35.7%
  叙述句长             均值 35 字，P90=64，短句(<10字)仅 5%
  对话占比             均值 41.4%，带宽 21.6%-59.8%
  感叹号 vs 问号       ！33 vs ？2205
  比喻标记             约 4-5 处/万字
  章均字数             6700（4400-10100）

用法：
  python tools/style-report.py <file.html> [file2 ...]     # 单/多文件，逐文件一行表
说明：只测不改；台词语料取自成对引号“……”内的文本；标签统计含对白与叙述行。
"""
import sys, re, html


def load_text(path):
    raw = open(path, encoding='utf-8').read()
    raw = re.sub(r'<div class="figure">.*?</div>', '', raw, flags=re.S)
    raw = html.unescape(re.sub(r'<[^>]+>', '', raw))
    return raw


def analyze(path):
    raw = load_text(path)
    lines = [l.strip() for l in raw.split('\n') if l.strip()]
    text = '\n'.join(lines)

    # ---- 字数（中日韩字符计） ----
    cjk = len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', text))
    wan = cjk / 10000.0 if cjk else 1.0

    # ---- 对白语料（成对"……"直引号；兼容弯引号） ----
    dialogues = re.findall(r'"([^"]*)"', text) + re.findall(r'“([^”]*)”', text)
    dlg_chars = sum(len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', d)) for d in dialogues)
    dlg_ratio = dlg_chars / cjk * 100 if cjk else 0
    turns = [len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', d)) for d in dialogues]
    turns_sorted = sorted(turns)
    med = turns_sorted[len(turns_sorted) // 2] if turns_sorted else 0
    short_pct = sum(1 for t in turns if t <= 10) / len(turns) * 100 if turns else 0

    # ---- 光杆连发（连续引号块之间无叙述句隔断的轮数） ----
    # 按段落扫描：引号连续出现、中间只有空白的算连拍
    bare_runs, run = [], 0
    for para in lines:
        # 剥掉引号内容后若段内只剩标点/空白/标签词，视为纯对白段
        stripped = re.sub(r'"[^"]*"', '', para)
        stripped = re.sub(r'“[^”]*”', '', stripped)
        stripped = re.sub(r'[，。！？；：、\s a-zA-Z0-9"“”—…·（）《》]', '', stripped)
        if not stripped:
            run += len(re.findall(r'"[^"]*"', para)) + len(re.findall(r'“[^”]*”', para))
        else:
            if run >= 4:
                bare_runs.append(run)
            run = 0
    if run >= 4:
        bare_runs.append(run)

    # ---- 叙述句长（全文本剥对白后按句切） ----
    narr = text
    narr = re.sub(r'"[^"]*"', '', narr)
    narr = re.sub(r'“[^”]*”', '', narr)
    sents = [s for s in re.split(r'[。！？]', narr) if re.search(r'[\u4e00-\u9fff]', s)]
    slens = [len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', s)) for s in sents]
    if slens:
        sl_sorted = sorted(slens)
        mean_len = sum(slens) / len(slens)
        p90 = sl_sorted[int(len(sl_sorted) * 0.9) - 1 if len(sl_sorted) >= 10 else -1]
        short_narr_pct = sum(1 for l in slens if l < 10) / len(slens) * 100
    else:
        mean_len = p90 = short_narr_pct = 0

    # ---- 标签谱（全角/半角冒号都认） ----
    tags = {'说：': 0, '说道': 0, '笑道': 0, '问道': 0, '答道': 0, '冷笑道': 0, '叹道': 0}
    tags['说：'] = text.count('说：') + text.count('说:')
    for t in ('说道', '笑道', '问道', '答道', '冷笑道', '叹道'):
        tags[t] = text.count(t)

    # ---- 感叹号/问号 ----
    excla = text.count('！')
    quest = text.count('？')

    # ---- 比喻标记（叙述+对白合计，同圣经口径） ----
    sim_marks = ['像', '如同', '仿佛', '好比', '一样', '似的']
    sim_count = sum(text.count(m) for m in sim_marks)

    return {
        'path': path.split('/')[-1].split('\\')[-1],
        'chars': cjk, 'dlg_ratio': dlg_ratio,
        'turns': len(dialogues), 'med': med, 'short_pct': short_pct,
        'bare': len(bare_runs), 'bare_max': max(bare_runs) if bare_runs else 0,
        'mean_len': mean_len, 'p90': p90, 'short_narr': short_narr_pct,
        'shuo': tags['说：'] / wan, 'dao': sum(v for k, v in tags.items() if k != '说：'),
        'excla': excla, 'quest': quest,
        'sim': sim_count / wan,
    }


def main():
    print('%-22s %6s %7s %5s %5s %6s %5s %6s %5s %8s %5s %6s %5s' % (
        '文件', '字数', '对话%', '轮次', '台词中位', '≤10字%', '光杆≥4', '最长连拍',
        '叙述均长', '叙述P90', '短句%', '说:/万', '道系'))
    for p in sys.argv[1:]:
        r = analyze(p)
        print('%-22s %6d %6.1f%% %5d %7d %5.1f%% %5d %7d %8.1f %7d %6.1f%% %6.1f %5d' % (
            r['path'], r['chars'], r['dlg_ratio'], r['turns'], r['med'], r['short_pct'],
            r['bare'], r['bare_max'], r['mean_len'], r['p90'], r['short_narr'],
            r['shuo'], r['dao']))
    print('\n比喻标记/万字：', end='')
    for p in sys.argv[1:]:
        r = analyze(p)
        print(' %s=%.1f' % (r['path'].replace('part', '').replace('interlude', '间').replace('.html', ''), r['sim']), end='')
    print('\n！/？：', end='')
    for p in sys.argv[1:]:
        r = analyze(p)
        print(' %s=%d/%d' % (r['path'].replace('part', '').replace('interlude', '间').replace('.html', ''), r['excla'], r['quest']), end='')
    print()


if __name__ == '__main__':
    main()
