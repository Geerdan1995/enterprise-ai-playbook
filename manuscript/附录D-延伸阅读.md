# 附录D 延伸阅读
*Appendix D: Further Reading*

> 分四组：书、论文与标准、开源与开放资源，最后是本书调研信源的诚实说明。所选条目只收正文提过或与青山做法直接相关的，不是一张求全的书单。

## 一、书

- 王昊奋、漆桂林、陈华钧：《知识图谱：方法、实践与应用》，电子工业出版社。中文系统专著，构建流程、表示学习、行业应用俱全。
- Noy, McGuinness：《Ontology Development 101》，斯坦福大学，2001。小夏那门课的葡萄酒本体作业出自这里（第17章），也是"先圈范围、小步迭代"方法的源头。
- Arp, Smith, Spear：《Building Ontologies with Basic Formal Ontology》，MIT Press，2015。顶层本体BFO的配套教材，想往深里走再读。
- 阿耐：《大江东去》。本书对话写法的底本——短句入对话、开口前先做小动作、争执钉在实物上，这些规矩是从这部书里学来的。
- Goldratt：《目标》；Gene Kim等：《凤凰项目》。用工厂小说讲管理方法的两条老路，本书叙事结构的参照。

## 二、论文与标准

- Gruber：《Toward Principles for the Design of Ontologies Used for Knowledge Sharing》，KSL 93-04，斯坦福，1993（期刊版见International Journal of Human-Computer Studies，1995）。第17章小夏念的那句定义的出处。
- Studer, Benjamins, Fensel：《Knowledge Engineering: Principles and Methods》，1998。给Gruber定义添上"形式化的、共享的"两个词。
- Hogan等：《Knowledge Graphs》，ACM Computing Surveys，2021。知识图谱的系统综述，谱系讲得清楚。
- Berners-Lee, Hendler, Lassila：《The Semantic Web》，Scientific American，2001。语义网宣言，图谱技术的直系前史。
- IATF 16949:2016 汽车质量管理体系。第15章审核条款的行业底盘，尤其8.5.2"标识和可追溯性"。
- W3C标准：RDF 1.1（2014）、OWL 2（2009）、SPARQL 1.1（2013）。总目装进机器后，机器读的那套文法。
- ISO/IEC 21838-2:2021。顶层本体BFO的国际标准。
- Pereira, Graylin, Lin, Brynjolfsson：《The Enterprise AI Playbook：Lessons from 51 Successful Deployments》，斯坦福大学 Digital Economy Lab。51 个企业 AI 落地案例的访谈调研：77% 最难的挑战在人、流程与治理；61% 的成功之前有失败；附录C"补强信源"三条出自此处。
- Erik Brynjolfsson, Bharat Chandar, Ruyu Chen：《Canaries in the Coal Mine? Six Facts about the Recent Employment Effects of AI》，斯坦福大学 Digital Economy Lab 工作论文，2025。基于 ADP 千万级工资单数据：AI 暴露岗位上，22-25 岁早期职业者就业相对下降 16%——对应书中"徒弟带不住"的那条暗线。
- Erik Brynjolfsson, Daniel Rock, Chad Syverson：《The Productivity J-Curve》，《American Economic Journal: Macroeconomics》13卷1期，2021。生产力J曲线：通用目的技术的生产率增长，早期被系统性低估、后期被高估——因为真正的投入是流程重设计、人的本事和组织重构，这些账不在报表上。电力化的四十年，AI正在重走。
- Paul A. David：《The Dynamo and the Computer: An Historical Perspective on the Modern Productivity Paradox》，《American Economic Review》80卷2期，1990。经济史名文：电站建成之后约四十年，美国制造业的生产率才起来——"化"字要等多久、等的是什么，电力给过一个完整的答案。附录B"通用目的技术"词条的出处。
- Bresnahan & Trajtenberg：《General Purpose Technologies "Engines of Growth"?》，《Journal of Econometrics》65卷1期，1995。"通用目的技术"一词的学术出处。

## 三、开源与开放资源

- Neo4j（社区版）——第5章赵峰在淘汰机器上装的那个图数据库，免费、单机。
- NebulaGraph——国产分布式图数据库，Apache 2.0协议，信创环境可选。
- Wikidata——开放事实库，1.23亿条目，CC0协议；谷歌知识面板的数据底座之一。
- OpenKG——中文开放知识图谱社区，国内领域的入口。
- Gene Ontology——第17章叶老讲的那个词表：细胞组分、分子功能、生物过程三大类，四万四千多条术语，制药行业绕不开。
- DBpedia、Schema.org——从维基百科和网页标注里长出来的两个大规模开放图谱。
- GraphRAG（微软，2024年开源）——附录B"GraphRAG"词条的出处，把语料先抽成图再做检索。
- Protégé——斯坦福的本体编辑器，免费；小夏们画图的工具。

## 四、本书调研信源说明

诚实声明：本书写作基于六份专题调研文档与Datawhale《FDE案例100》（其中24案进入素材库，去向见附录C）。虚构的只是青山传动这层壳和壳里的人；情节的做法、路径与效果量级皆有真实原型，检索核验过的专业细节（齿轮测绘、银行对账、供应商审核、叙词表史料等）在写作档案中逐条存有信源。效果表述守一条口径：能证明什么、还证明不了什么，都写清楚；证明不了的，不编数。

- 调研1：知识图谱技术体系（三元组、图数据库、构建流程、七大坑，36条信源）
- 调研2：本体论（哲学到信息科学、Gruber定义链、方法论、GO/SNOMED/FIBO，50条信源）
- 调研3：行业应用案例（Google、金融、医疗、制造、GraphRAG、失败清单）
- 调研4：叙事型技术书籍写作方法（《目标》《凤凰项目》《大话设计模式》逐本分析）
- 调研5：概念辨析与通俗类比（六组辨析、四大误解、类比及其边界）
- 调研6：去AI味中文写作（AI味特征与28条写作守则）
