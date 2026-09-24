# -*- coding: utf-8 -*-
"""节奏诊断：全书每章对照第一幕基线。用法 py tools/rhythm-check.py [章文件名...]"""
import io, re, sys, glob, os

BASE = {'time': 24, 'short': 0.28, 'para': 55}  # 基线上限：时间词24/短句28%/段均长55字（±容差）

def check(path):
    t = io.open(path, encoding='utf-8').read()
    t = re.sub(r'<div class="doc-quote">.*?</div>', '', t, flags=re.S)  # 系统推送/文件引文为不可动件
    text = re.sub(r'<[^>]+>', '', t)
    narr = ''.join(text.split('"')[::2])
    sents = [s.strip() for s in re.split(r'[。！？]', narr) if len(s.strip()) >= 2]
    lens = [len(s) for s in sents]
    avg = sum(lens)/len(lens) if lens else 0
    short = sum(1 for l in lens if l <= 12)/len(lens) if lens else 0
    time = len(re.findall(r'\d{1,2}月\d{1,2}日|星期[一二三四五六日天]|凌晨|早上|上午|下午|傍晚|夜里', text))
    # 数据串豁免：叙述中"词+日期"连排（看板九宫格"询价9月22日，报价9月23日…"）属剧情载核
    seq = re.compile(r'\d{1,2}月\d{1,2}日(?:[，、]?\s*[一-龥]{1,6}\d{1,2}月\d{1,2}日){2,}')
    data_dates = sum(len(re.findall(r'\d{1,2}月\d{1,2}日', m.group(0))) for m in seq.finditer(narr))
    time -= data_dates
    paras = [p for p in text.split('\n') if len(p.strip()) > 10]
    pav = sum(len(p) for p in paras)/len(paras) if paras else 0
    flags = []
    if time > BASE['time']: flags.append(f'时间词超标({time}>{BASE["time"]})')
    if short > BASE['short']: flags.append(f'短句超标({short:.0%})')
    if pav < BASE['para']: flags.append(f'段落偏碎({pav:.0f}字)')
    tag = '⚠ ' + '；'.join(flags) if flags else '✓'
    print(f'{os.path.basename(path):20} 时间词:{time:3d} 句均:{avg:4.1f} 短句:{short:4.0%} 段均:{pav:4.0f}字  {tag}')
    return not flags

if __name__ == '__main__':
    args = sys.argv[1:] or sorted(glob.glob('fragments/part*.html'))
    bad = [f for f in args if not check(f)]
    sys.exit(1 if bad else 0)
