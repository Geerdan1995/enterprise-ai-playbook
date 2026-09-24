// 全书目录：与 scripts/build.js 的 FRAGMENT_ORDER 同源（封面/目录/封底三个印刷件不入网）。
// 附录 A–K 在书稿里同属一个 fragment（appendix.html），网上按 sectionId 锚点拆成单页。
export interface TocEntry {
  slug: string;
  fragment: string;
  md: string;
  num: string;
  title: string;
  teaser?: string;
  /** 附录拆页用：该篇在 fragment 内的 h2 锚点 id */
  sectionId?: string;
}

export interface TocPart {
  name: string;
  entries: TocEntry[];
}

const GH = 'https://github.com/Geerdan1995/enterprise-ai-playbook/blob/main/manuscript/';

const e = (
  slug: string,
  fragment: string,
  md: string,
  num: string,
  title: string,
  teaser?: string,
  sectionId?: string,
): TocEntry => ({ slug, fragment, md: GH + md, num, title, teaser, sectionId });

export const parts: TocPart[] = [
  {
    name: '卷首',
    entries: [
      e('editor-note', '02-editor-note.html', '00-编者按.md', '卷首', '编者按',
        '这本书讲什么、怎么读、人物是谁'),
    ],
  },
  {
    name: '第一幕 · 多事之春',
    entries: [
      e('ch1', 'part1-ch1.html', '第01章-三月十七号，四个坏消息.md', '01', '三月十七号，四个坏消息',
        '四个坏消息，凑在同一个早上找上门'),
      e('ch2', 'part1-ch2.html', '第02章-试出来的难处.md', '02', '试出来的难处',
        '数字办的白板上写了四个字：怎么自救'),
    ],
  },
  {
    name: '第二幕 · 点火与速胜',
    entries: [
      e('ch3', 'part2-ch3.html', '第03章-档案馆里的老人.md', '03', '档案馆里的老人',
        '负一层的档案馆，和一个守在那儿的老人'),
      e('ch4', 'part2-ch4.html', '第04章-两万三千份文件.md', '04', '两万三千份文件',
        'AI 要吃的第一口饭，是两万三千份旧文件'),
      e('ch5', 'part2-ch5.html', '第05章-五百个节点的图.md', '05', '五百个节点的图',
        '一张折成四折的 A3 纸铺上桌：五百个节点'),
      e('ch6', 'part2-ch6.html', '第06章-老唐的失眠夜.md', '06', '老唐的失眠夜',
        '老客户的电话打进技术部；那阵子老唐夜里睡不好'),
      e('ch7', 'part2-ch7.html', '第07章-六月三十号.md', '07', '六月三十号',
        '前面几个月的活儿，都要在这一天当众过一遍'),
    ],
  },
  {
    name: '第三幕 · 星火',
    entries: [
      e('ch8', 'part3-ch8.html', '第08章-许曼的表.md', '08', '许曼的表', '六月的账，对到第三天'),
      e('interlude-1', 'interlude-1.html', '间章一-八月的会.md', '间一', '八月的会',
        '头一班高铁，陈临和小夏出门去开会'),
      e('ch9', 'part3-ch9.html', '第09章-段兴的背包.md', '09', '段兴的背包',
        '售后的段兴回厂五天，背来一个军绿双肩包'),
      e('ch10', 'part3-ch10.html', '第10章-一张报价单.md', '10', '一张报价单',
        '一张报价单从销售部发了出去'),
      e('interlude-2', 'interlude-2.html', '间章二-来客.md', '间二', '来客',
        '门房递出访客登记本：省城那家咨询公司的顾问又来了'),
      e('ch11', 'part3-ch11.html', '第11章-看不见的订单.md', '11', '看不见的订单',
        '月度经营分析会开到第五页，董事长把笔搁下了'),
      e('ch12', 'part3-ch12.html', '第12章-数人头的.md', '12', '数人头的',
        '「数字办要替人」的说法，从装配车间三班的夜班上传开'),
      e('ch13', 'part3-ch13.html', '第13章-墙.md', '13', '墙',
        '三页 2019 年的内部接口文档，摊在赵峰桌上'),
      e('ch14', 'part3-ch14.html', '第14章-各自为战.md', '14', '各自为战',
        '一月盘去年的账：账不动，数字办的人跟着录'),
    ],
  },
  {
    name: '第四幕 · 大考',
    entries: [
      e('ch15', 'part4-ch15.html', '第15章-审核通知.md', '15', '审核通知',
        '节后上班头一天，审核通知到了'),
      e('ch16', 'part4-ch16.html', '第16章-董事会的账.md', '16', '董事会的账',
        '董事会要算账，陈临先下了一趟负一层'),
      e('ch17', 'part4-ch17.html', '第17章-叶老的图纸.md', '17', '叶老的图纸',
        '路线之争吵到散会，叶老的那一课总算开讲'),
    ],
  },
  {
    name: '第五幕 · 终局与传承',
    entries: [
      e('ch18', 'part5-ch18.html', '第18章-开工.md', '18', '开工', '三月头一个星期二，项目开工'),
      e('ch19', 'part5-ch19.html', '第19章-五个名字的供应商.md', '19', '五个名字的供应商',
        '同一家供应商，在系统里挂了五个名字'),
      e('ch20', 'part5-ch20.html', '第20章-灰区.md', '20', '灰区',
        '一柜子旧账啃完，剩下的叫灰区'),
      e('ch21', 'part5-ch21.html', '第21章-审核日.md', '21', '审核日',
        '五月九号下午四点，一辆灰色商务车开进厂区'),
      e('ch22', 'part5-ch22.html', '第22章-老唐退休那天.md', '22', '老唐退休那天',
        '这一年走完，到了老唐退休的那天'),
    ],
  },
  {
    name: '附录',
    entries: [
      e('appendix-a', 'appendix.html', '附录A-一张图看懂知识图谱与本体论.md', '附录A',
        '一张图看懂知识图谱与本体论', '一页图，把全书的技术主线画明白', 'appA'),
      e('appendix-b', 'appendix.html', '附录B-本体论小辞典.md', '附录B',
        '本体论小辞典', '名词看不懂，随手查', 'appB'),
      e('appendix-c', 'appendix.html', '附录C-情节与真实案例对照表.md', '附录C',
        '情节与真实案例对照表', '书里哪件事对应哪个真实案例，逐条对账', 'appC'),
      e('appendix-d', 'appendix.html', '附录D-延伸阅读.md', '附录D',
        '延伸阅读', '想再深入，往哪儿走', 'appD'),
      e('appendix-e', 'appendix.html', '附录E-把AI用起来——写给企业里的人.md', '附录E',
        '把AI用起来——写给企业里的人', '企业把 AI 用起来的顺序：八段路', 'appE'),
      e('appendix-f', 'appendix.html', '附录F-AI用起来之后——一个实践者的方法论笔记.md', '附录F',
        'AI用起来之后——一个实践者的方法论笔记', '用起来之后的事：个人撞组织，流程撞部门墙，工具撞账本', 'appF'),
      e('appendix-g', 'appendix.html', '附录G-二十四家，六个问题——一本案例集的横读.md', '附录G',
        '二十四家，六个问题——一本案例集的横读', '二十四家企业的案例横着读，读出六个问题', 'appG'),
      e('appendix-h', 'appendix.html', '附录H-AI应用落地工作法.md', '附录H',
        'AI应用落地工作法', '从书里长出来的落地工作法', 'appH'),
      e('appendix-k', 'appendix.html', '附录K-解决方案工具箱.md', '附录K',
        '解决方案工具箱', '三十五个案例的解法速查，按解法分九类', 'appK'),
    ],
  },
  {
    name: '后记',
    entries: [
      e('afterword', '98-afterword.html', '99-后记-青山没打的七仗.md', '尾声',
        '青山没打的七仗', '故事讲完，账还没算完的部分'),
    ],
  },
];

export const entries: TocEntry[] = parts.flatMap((p) => p.entries);

export const enabledEntries = entries;

export function findEntry(slug: string): TocEntry | undefined {
  return entries.find((x) => x.slug === slug);
}

/** 阅读顺序里的上一篇／下一篇 */
export function neighbors(slug: string): { prev?: TocEntry; next?: TocEntry } {
  const i = entries.findIndex((x) => x.slug === slug);
  if (i < 0) return {};
  return { prev: entries[i - 1], next: entries[i + 1] };
}
