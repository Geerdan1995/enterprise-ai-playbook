# -*- coding: utf-8 -*-
"""
style-scan.py —— 《理想之城式》改稿的风格纪律机械闸门（风格圣经 v1.x 配套）

检查项（对应圣经条款）：
  1. 概念术语入叙述 / 术语比喻        R4 AI味判别①②
  2. "不是A，是B"式定性句（叙述）      R4 判别③ + 禁金句律
  3. 双拍对仗收尾（叙述段尾句）        R4 判别④
  4. 四连排比                          禁金句律机械扫描
  5. 预叙句登记 + 演示骨架复用检测     R3 + R3 防填空
  6. 议论候选句登记（配额人工核对）    R4 计数判据
  7. 对话标签违规（道/笑道/问道系）    R8
  8. 感叹号配额（叙述 vs 对白分开）    R13
  9. AI 禁词                           现行机械扫描
  10. 数字等式点睛                       R4增量检验（一个X压着Y斤式）
  11. 伪分析从句/吹捧/模糊归因            no-ai-slop 吸收（2026-09-20，查叙述轨）
用法：
  python tools/style-scan.py <file.md|file.html> [--keep-lists]
说明：扫描器只报嫌疑，不下死刑；每条命中需人工裁决（术语在事实性叙述中合法）。
"""
import sys, re, html

IT_TERMS = ['存储介质', '备份', '接口', '端口', '带宽', '算力', '颗粒度', '底层逻辑',
            '维度', '闭环', '赋能', '抓手', '对齐', '拉通', '沉淀', '复用', '解耦', '心智']
SIM_MARKS = ['像', '如同', '仿佛', '好比', '一样', '似的']
AI_WORDS = ['值得注意的是', '总的来说', '极大地', '赋能', '抓手', '众所周知',
            '不言而喻', '毋庸置疑', '显而易见', '死线']
PSEUDO_WORDS = ['体现了', '彰显', '标志着', '展现了', '见证了', '充分体现', '有力证明',
                '研究表明', '业内人士', '普遍认为']
PSEUDO_VERB = re.compile(r'(发挥|起到|起着)[了着]?[^。！？，；,;]{0,10}作用')
TAGS = ['说道', '笑道', '问道', '冷笑道', '答道', '叹道']
YILUN = re.compile(r'(这就是|所谓|无非|永远|从来都|显然|自然不|向来|向来是)')


def load_text(path, keep_lists):
    raw = open(path, encoding='utf-8').read()
    # 图块整段抹空但保留换行数，使行号与源文件物理行号一致
    raw = re.sub(r'<div class="figure">.*?</div>', lambda m: '\n' * m.group(0).count('\n'), raw, flags=re.S)
    raw = html.unescape(re.sub(r'<[^>]+>', '', raw))
    if not keep_lists:
        raw = re.sub(r'### 【守则使用清单[\s\S]*?(?=\n---\n|\n## |\Z)', '', raw)
    return [(n, l) for n, l in enumerate(raw.split('\n'), 1) if l.strip()]


def strip_dialog(line):
    line = re.sub(r'“[^”]*”', '', line)
    return re.sub(r'"[^"]*"', '', line)


def segs_of(sent):
    return [s for s in re.split(r'[，；,;]', sent) if s.strip()]


def main():
    path, keep = sys.argv[1], '--keep-lists' in sys.argv
    lines = load_text(path, keep)
    rep = {k: [] for k in ['term_sim', 'term_narr', 'notAisB', 'double', 'parallel',
                           'foreshadow_tpl', 'foreshadow', 'yilun', 'tags', 'aiword', 'numpun',
                           'pseudo']}
    excla_n = excla_d = 0
    for n, line in lines:
        i = n  # 报告行号＝源文件物理行号
        narr = strip_dialog(line)
        # 感叹号分轨
        excla_d += line.count('！') - narr.count('！')
        excla_n += narr.count('！')
        # 1. 术语：比喻语境（硬嫌疑）与叙述在场（复核）
        for t in IT_TERMS:
            for m in re.finditer('[^。！？]*' + t + '[^。！？]*[。！？]?', narr):
                s = m.group(0).strip()
                if any(k in s for k in SIM_MARKS):
                    rep['term_sim'].append((i, s[:60]))
                else:
                    rep['term_narr'].append((i, s[:60]))
        # 2. 不是A是B（叙述）
        for m in re.finditer(r'[^。！？]*不是[^。！？]{1,20}[，,][^。！？]{0,8}(而是|是在|是)[^。！？]*[。！？]?', narr):
            rep['notAisB'].append((i, m.group(0).strip()[:60]))
        # 3. 双拍对仗收尾：叙述行末句最后两段等长
        sents = [s for s in re.split(r'[。！？]', narr) if s.strip()]
        if sents:
            tail = segs_of(sents[-1])
            if len(tail) >= 2:
                a, b = tail[-2].strip(), tail[-1].strip()
                ye1 = b[:1] in '也还又都' and 4 <= len(b) <= 14 and len(a) <= 14 and ('不' in a or '没' in a)
                ye2 = b[:1] in '也还又都' and 4 <= len(b) <= 12 and len(a) <= 12
                if ye1 or ye2:
                    rep['double'].append((i, (a + '，' + b)[:60]))
        # 4. 四连排比
        for s in sents:
            ss = segs_of(s)
            for k in range(len(ss) - 3):
                quad = [x.strip() for x in ss[k:k + 4]]
                if all(len(q) >= 2 for q in quad) and (
                        len({q[:2] for q in quad}) == 1 or len({q[-2:] for q in quad}) == 1):
                    rep['parallel'].append((i, '，'.join(quad)[:60]))
        # 5. 预叙
        if '还不知道' in narr or '很久以后' in narr or '多年以后' in narr:
            rep['foreshadow'].append((i, narr.strip()[:60]))
            if re.search(r'那个时候.{0,20}还不知道', narr) and '息息相关' in narr:
                rep['foreshadow_tpl'].append((i, narr.strip()[:60]))
        # 6. 议论候选
        for m in YILUN.finditer(narr):
            s = re.split(r'[。！？]', narr)
            hit = [x for x in s if YILUN.search(x)]
            for h in hit:
                rep['yilun'].append((i, h.strip()[:56]))
            break
        # 7. 标签
        for t in TAGS:
            if t in line:
                rep['tags'].append((i, line.strip()[:60]))
        # 9. AI禁词
        for w in AI_WORDS:
            if w in line:
                rep['aiword'].append((i, line.strip()[:60]))
        # 11. 伪分析从句/吹捧/模糊归因（no-ai-slop 吸收；查叙述轨，对白豁免）
        for w in PSEUDO_WORDS:
            if w in narr:
                rep['pseudo'].append((i, narr.strip()[:60]))
        for m in PSEUDO_VERB.finditer(narr):
            rep['pseudo'].append((i, m.group(0)))
        # 10. 数字等式点睛（R4增量检验：一个X压着Y斤式）
        for m in re.finditer(r'[^。！？]*一个[字词句纸][^。！？]*[。！？]?', narr):
            s = m.group(0)
            if re.search(r'压着?|顶着?|抵得上|值得上|重过', s) and re.search(r'[一二两三四五六七八九十百千万\d]+[多几余]?(斤|吨|钧|万)', s):
                rep['numpun'].append((i, s.strip()[:60]))
    print('=== style-scan 报告：%s ===' % path)
    print('行数 %d ｜ 叙述感叹号 %d ｜ 对白感叹号 %d' % (len(lines), excla_n, excla_d))
    names = {'term_sim': '①术语比喻（硬嫌疑）', 'term_narr': '①叙述含术语（人工复核）',
             'notAisB': '②不是A是B定性句', 'double': '③双拍对仗收尾嫌疑',
             'parallel': '④四连排比', 'foreshadow_tpl': '⑤预叙骨架复用（硬嫌疑）',
             'foreshadow': '⑤预叙句登记', 'yilun': '⑥议论候选（配额核对）',
             'tags': '⑦标签违规', 'aiword': '⑨AI禁词', 'numpun': '⑩数字等式点睛（增量检验）',
             'pseudo': '⑪伪分析从句/吹捧/模糊归因（no-ai-slop）'}
    for k, label in names.items():
        print('\n[%s] %d 处' % (label, len(rep[k])))
        for ln, s in rep[k][:6]:
            print('  L%-4d %s' % (ln, s))
        if len(rep[k]) > 6:
            print('  …… 另 %d 处' % (len(rep[k]) - 6))


if __name__ == '__main__':
    main()
