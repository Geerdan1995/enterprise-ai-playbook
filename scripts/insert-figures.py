# -*- coding: utf-8 -*-
"""v1.4.0 进书脚本：把 29 张插图按锚点插入 fragments，全书统一"图 N"编号。
锚点模式：
  after_text:<text>   在含该文本的 </p> 之后插入（段落末尾）
  before_text:<text>  在该文本之前插入
  before_journal      在该文件首个 <div class="journal" 之前插入
幂等：已含同名图片引用的文件跳过。
"""
import io, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
FRAG = os.path.join(ROOT, '..', 'fragments')
IMG = '../assets/illustrations/shots/'

# (fragment, 模式锚点, 图文件, 图题)
FIGS = [
 ('02-editor-note.html', 'before_text:<h3>五幕各讲什么</h3>', 'c28-卷首-时间轴.png', '图 1｜五幕一年：2026.3.17 → 2027.5.31（卷首）'),
 ('part1-ch1.html', 'after_text:他在白板前站了二十分钟。最后什么线也没拉', 'v2-b01-白板孤词机制.png', '图 2｜白板上的孤词：一条线也拉不出来（第1章）'),
 ('part1-ch1.html', 'after_text:散会的时候，人事老总在走廊里拍了拍陈临的肩膀', 'c02-ch1-口径册.png', '图 3｜387 对 462：差的 75 家没有格子可放（第1章）'),
 ('part1-ch1.html', 'after_text:他想起郑敏傍晚说的，全厂就这么一个本子', 'c16-ch1-苦役路线.png', '图 4｜一个本子串四个系统（第1章）'),
 ('part1-ch2.html', 'before_journal', 'v2-b03-三条路机制.png', '图 5｜三次试验，断点各在哪（第2章）'),
 ('part2-ch3.html', 'before_journal', 'c04-ch3-词卡实物.png', '图 6｜一张 1986 年的词卡（第3章）'),
 ('part2-ch4.html', 'before_journal', 'c17-ch4-分拣台.png', '图 7｜两万三千份文件，三岔分拣（第4章）'),
 ('part2-ch4.html', 'after_fig:图 7｜', 'c18-ch4-门票.png', '图 8｜有效目录是闸门，答案出门带出处（第4章）'),
 ('part2-ch5.html', 'before_journal', 'c05-ch5-双管道.png', '图 9｜同一道题，两条管（第5章）'),
 ('part2-ch6.html', 'before_journal', 'c19-ch6-路牌.html'[:-5] + '.png', '图 10｜指路的是它，走路的得是我们（第6章）'),
 ('part3-ch8.html', 'before_journal', 'c06-ch8-筛网漏斗.png', '图 11｜对账四道筛网：1653 → 58 → 252 笔（第8章）'),
 ('part3-ch9.html', 'before_journal', 'c20-ch9-三层台阶.png', '图 12｜知识三层台阶，最窄那层最值钱（第9章）'),
 ('part3-ch10.html', 'before_journal', 'c07-ch10-流水线.png', '图 13｜一把梭翻车，五段流水线（第10章）'),
 ('part3-ch11.html', 'before_journal', 'c21-ch11-九格环链.png', '图 14｜九格订单环链，红牌提前亮（第11章）'),
 ('part3-ch11.html', 'after_fig:图 14｜', 'c22-ch11-缝里捞单.png', '图 15｜缝里的单子：4980 对 5000（第11章）'),
 ('part3-ch13.html', 'before_journal', 'c08-ch13-六本账.png', '图 16｜六本账，断桥相望（第13章）'),
 ('part4-ch14.html', 'before_journal', 'c23-ch14-断链.png', '图 17｜段段都有，接不起来（第14章）'),
 ('part4-ch14.html', 'after_fig:图 17｜', 'c24-ch14-规模面积.png', '图 18｜追溯规模：285 / 4216 / 13000 台（第14章）'),
 ('part4-ch16.html', 'after_text:东西还是那个东西，名目换了', 'c25-ch16-名目换了.png', '图 19｜旧词卡走进屏幕：名目换了（第16章）'),
 ('part4-ch16.html', 'before_journal', 'c09-ch16-柜子三态.html'[:-5] + '.png', '图 20｜合卡两回：1985 黄，1986 成，2027 得名（第16章）'),
 ('part5-ch17.html', 'before_journal', 'c10-ch17-闸机.png', '图 21｜词要背着题进总目（第17章）'),
 ('part5-ch18.html', 'before_journal', 'c11-ch18-牌子分堆.png', '图 22｜五个名字分三堆：章说了算（第18章）'),
 ('part5-ch19.html', 'before_journal', 'c26-ch19-联动灯板.png', '图 23｜改一个词，六格联动签收（第19章）'),
 ('part5-ch20.html', 'before_journal', 'c12-ch20-单据链.png', '图 24｜单据链：笔尖停在试车单（第20章）'),
 ('part5-ch21.html', 'before_journal', 'c13-ch21-声波挂绳.png', '图 25｜条目卡底下挂着一根声波（第21章）'),
 ('part5-ch21.html', 'after_fig:图 25｜', 'c27-ch21-四源汇聚.png', '图 26｜四条道都通到一台机器（第21章）'),
 ('appendix.html', 'after_text:按这段话画下来，是上下三层', 'b00-附录A-三层总图.png', '图 27｜总目在上，卡在中间，应用在下（附录A）'),
 ('appendix.html', 'before_text:<h3>二、概念：总目在上', 'c14-附录A-六词山路.png', '图 28｜一年，六个词（附录A）'),
 ('98-afterword.html', 'before_journal', 'c29-后记-七扇门.png', '图 29｜走廊里七扇门（后记）'),
]

def insert_after_paragraph(t, anchor):
    i = t.find(anchor)
    if i < 0: return None
    j = t.find('</p>', i)
    if j < 0: return None
    return j + 4

def insert_before_text(t, anchor):
    i = t.find(anchor)
    if i < 0: return None
    return i

def insert_before_journal(t):
    i = t.find('<div class="journal"')
    if i < 0: return None
    return i

def main():
    applied = 0
    skipped = 0
    for frag, mode, png, cap in FIGS:
        path = os.path.join(FRAG, frag)
        t = io.open(path, encoding='utf-8').read()
        if IMG + png in t:
            skipped += 1
            continue
        if mode == 'before_journal':
            pos = insert_before_journal(t)
        elif mode.startswith('after_text:'):
            pos = insert_after_paragraph(t, mode[len('after_text:'):])
        elif mode.startswith('before_text:'):
            pos = insert_before_text(t, mode[len('before_text:'):])
        elif mode.startswith('after_fig:'):
            capref = mode[len('after_fig:'):]
            i = t.find(capref)
            if i < 0: pos = None
            else:
                # 找该图 figure 的闭合 </div>（figcap 之后）
                j = t.find('</div>', i)
                pos = j + 6 if j >= 0 else None
        else:
            pos = None
        if pos is None:
            print(f'❌ 锚点未命中: {frag} :: {mode[:40]}')
            sys.exit(1)
        block = f'\n<div class="figure"><img src="{IMG}{png}" alt="{cap}"><div class="figcap">{cap}</div></div>\n'
        t = t[:pos] + block + t[pos:]
        io.open(path, 'w', encoding='utf-8').write(t)
        applied += 1
        print(f'✅ 图入 {frag} :: {cap}')
    print(f'\n插入 {applied} 张，跳过（已存在）{skipped} 张')

if __name__ == '__main__':
    main()
