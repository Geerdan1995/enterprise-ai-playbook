# 附录A 一张图看懂知识图谱与本体论
*Appendix A: The Whole Map*

> 写给第一次接触这些词的读者：RAG、知识库、知识图谱、本体论。不用任何数学，用一座档案馆把四个概念一次讲透；阅读顺序即理解顺序，全部图示为手绘示意。

## 01｜先别背定义：四个词，其实是一座档案馆的四个角色

这四个词之所以容易混，是因为它们描述的不是同一类东西——有的是**仓库**，有的是**组织方式**，有的是**规则**，有的是**工作流程**。

想象一家公司刚建了一座**档案馆**，要把散落各处的合同、会议纪要、培训视频、产品手册都收进来，让员工（以及 AI 助手）随时能查。这座馆里自然出现了四个角色：

```html
<div class="figure">
<svg width="100%" viewBox="0 0 820 330" xmlns="http://www.w3.org/2000/svg" font-family="PingFang SC, Microsoft YaHei, sans-serif">
  <!-- 档案馆外框 -->
  <rect x="30" y="30" width="760" height="270" rx="14" fill="none" stroke="#22201C" stroke-width="2.5"/>
  <rect x="330" y="16" width="160" height="30" rx="4" fill="#F7F4EE" stroke="#22201C" stroke-width="2.5"/>
  <text x="410" y="37" text-anchor="middle" font-size="15" font-weight="700" fill="#22201C">档案馆</text>
  <text x="410" y="62" text-anchor="middle" font-size="12.5" fill="#5C564C">= 知识库（Knowledge Base）：存放知识的仓库</text>
  <!-- 区1 老师傅 -->
  <rect x="60" y="90" width="220" height="180" rx="10" fill="#FBF6F1" stroke="#C24A20" stroke-width="1.6" stroke-dasharray="6 4"/>
  <text x="170" y="118" text-anchor="middle" font-size="14" font-weight="700" fill="#C24A20">「凭感觉」找资料的老师傅</text>
  <circle cx="140" cy="165" r="14" fill="none" stroke="#C24A20" stroke-width="2"/>
  <path d="M150 175 L168 193" stroke="#C24A20" stroke-width="3" stroke-linecap="round"/>
  <text x="170" y="222" text-anchor="middle" font-size="12.5" fill="#5C564C">= 向量检索 / Embedding</text>
  <text x="170" y="244" text-anchor="middle" font-size="12.5" fill="#5C564C">按「意思像不像」找</text>
  <!-- 区2 关系网 -->
  <rect x="300" y="90" width="220" height="180" rx="10" fill="#F2F5F1" stroke="#3D5A45" stroke-width="1.6" stroke-dasharray="6 4"/>
  <text x="410" y="118" text-anchor="middle" font-size="14" font-weight="700" fill="#3D5A45">一面「关系网」墙</text>
  <circle cx="360" cy="160" r="9" fill="#3D5A45"/><circle cx="460" cy="155" r="9" fill="#3D5A45"/><circle cx="415" cy="205" r="9" fill="#3D5A45"/>
  <line x1="369" y1="160" x2="451" y2="156" stroke="#3D5A45" stroke-width="1.8"/><line x1="366" y1="168" x2="410" y2="197" stroke="#3D5A45" stroke-width="1.8"/><line x1="455" y1="164" x2="422" y2="197" stroke="#3D5A45" stroke-width="1.8"/>
  <text x="410" y="240" text-anchor="middle" font-size="12.5" fill="#5C564C">= 知识图谱：谁和谁有什么关系</text>
  <!-- 区3 规则手册 -->
  <rect x="540" y="90" width="220" height="180" rx="10" fill="#F7F3E8" stroke="#B98A2F" stroke-width="1.6" stroke-dasharray="6 4"/>
  <text x="650" y="118" text-anchor="middle" font-size="14" font-weight="700" fill="#B98A2F">一本《编目规则手册》</text>
  <rect x="615" y="140" width="70" height="52" rx="4" fill="#fff" stroke="#B98A2F" stroke-width="2"/>
  <line x1="625" y1="156" x2="675" y2="156" stroke="#B98A2F" stroke-width="1.6"/><line x1="625" y1="170" x2="668" y2="170" stroke="#B98A2F" stroke-width="1.6"/><line x1="625" y1="182" x2="670" y2="182" stroke="#B98A2F" stroke-width="1.6"/>
  <text x="650" y="222" text-anchor="middle" font-size="12.5" fill="#5C564C">= 本体论：先规定好</text>
  <text x="650" y="244" text-anchor="middle" font-size="12.5" fill="#5C564C">有哪些概念、允许什么关系</text>
</svg>
<div class="figcap">图 28｜一座档案馆的四个角色（附录A）</div>
</div>
```

<!--表宽:18%,30%,--->
| 词 | 在档案馆里是… | 它回答什么问题 |
| --- | --- | --- |
| **知识库** | 整座档案馆 | 「知识放在哪？」——**仓库** |
| **RAG** | 借阅服务流程 | 「怎么把资料交给 AI 让它照着答？」——**工作流程** |
| **知识图谱** | 关系网墙 | 「谁和谁、有什么关系？」——**组织方式** |
| **本体论** | 编目规则手册 | 「知识该按什么规则来描述？」——**规则** |

接下来按「先有库 → 再会查 → 查得更准」的顺序，逐个讲清楚（图里这些名词先混个脸熟就好，每一节都会展开）。你会发现它们是一层一层长出来的。

## 02｜知识库：先有个地方放知识

最朴素的概念：**知识库 = 存放知识的地方，外加一套管理制度。**

你的网盘是知识库吗？是「文件库」，但不算好的知识库——因为一万份 PDF 堆在一起，和一座有分类、有索引、有目录卡的档案馆，差别在于**能不能被高效使用**。

所以现代「知识库」这个词，实际指的不只是存储，而是一条**加工流水线**：

```html
<div class="figure">
<svg width="100%" viewBox="0 0 820 130" xmlns="http://www.w3.org/2000/svg" font-family="PingFang SC, Microsoft YaHei, sans-serif">
  <defs><marker id="ar" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#5C564C"/></marker></defs>
  <g font-size="14" font-weight="600">
    <rect x="20"  y="35" width="120" height="60" rx="10" fill="#EFEAE0" stroke="#22201C" stroke-width="1.5"/><text x="80"  y="62" text-anchor="middle">原始资料</text><text x="80" y="82" text-anchor="middle" font-size="11.5" fill="#5C564C" font-weight="400">PDF/视频/音频</text>
    <rect x="185" y="35" width="120" height="60" rx="10" fill="#EFEAE0" stroke="#22201C" stroke-width="1.5"/><text x="245" y="62" text-anchor="middle">解析</text><text x="245" y="82" text-anchor="middle" font-size="11.5" fill="#5C564C" font-weight="400">变成干净文本</text>
    <rect x="350" y="35" width="120" height="60" rx="10" fill="#EFEAE0" stroke="#22201C" stroke-width="1.5"/><text x="410" y="62" text-anchor="middle">切块</text><text x="410" y="82" text-anchor="middle" font-size="11.5" fill="#5C564C" font-weight="400">长文切成小段</text>
    <rect x="515" y="35" width="120" height="60" rx="10" fill="#EFEAE0" stroke="#22201C" stroke-width="1.5"/><text x="575" y="62" text-anchor="middle">建索引</text><text x="575" y="82" text-anchor="middle" font-size="11.5" fill="#5C564C" font-weight="400">向量 / 图谱</text>
    <rect x="680" y="35" width="120" height="60" rx="10" fill="#C24A20"/><text x="740" y="62" text-anchor="middle" fill="#fff">可查询的知识库</text><text x="740" y="82" text-anchor="middle" font-size="11.5" fill="#F5E3D8" font-weight="400">能被检索、被引用</text>
    <line x1="140" y1="65" x2="183" y2="65" stroke="#5C564C" stroke-width="2" marker-end="url(#ar)"/>
    <line x1="305" y1="65" x2="348" y2="65" stroke="#5C564C" stroke-width="2" marker-end="url(#ar)"/>
    <line x1="470" y1="65" x2="513" y2="65" stroke="#5C564C" stroke-width="2" marker-end="url(#ar)"/>
    <line x1="635" y1="65" x2="678" y2="65" stroke="#5C564C" stroke-width="2" marker-end="url(#ar)"/>
  </g>
</svg>
<div class="figcap">图 29｜知识库是一条加工流水线（附录A）</div>
</div>
```

### 多讲一步：切块（Chunking）——最容易被忽视的质量开关

流水线里那格「切块」看着不起眼，实际直接决定检索质量：**长文档要先切成一段一段的「块」，检索和 Embedding（下一节的主角，先把名字混个脸熟）都以块为单位。**块切小了，定位精准但上下文碎——搜到半句话，答不出完整政策；块切大了，上下文完整但重点被稀释，嵌入也跟着变「糊」。没有标准答案，只能按文档类型调：开源知识引擎 Jonex（第 08 节的主角）默认每块 1200 字符。

```html
<div class="figure">
<svg width="100%" viewBox="0 0 820 230" xmlns="http://www.w3.org/2000/svg" font-family="PingFang SC, Microsoft YaHei, sans-serif">
  <rect x="50" y="24" width="330" height="182" rx="10" fill="#FBF6F1" stroke="#C24A20" stroke-width="1.5"/>
  <text x="215" y="52" text-anchor="middle" font-size="14.5" font-weight="700" fill="#C24A20">小块（如 200 字）→ 40 块</text>
  <g fill="#E8C9B8" stroke="#C24A20" stroke-width="1">
    <rect x="78" y="68" width="58" height="16" rx="3"/><rect x="144" y="68" width="58" height="16" rx="3"/><rect x="210" y="68" width="58" height="16" rx="3"/><rect x="276" y="68" width="58" height="16" rx="3"/>
    <rect x="78" y="92" width="58" height="16" rx="3"/><rect x="144" y="92" width="58" height="16" rx="3"/><rect x="210" y="92" width="58" height="16" rx="3"/><rect x="276" y="92" width="58" height="16" rx="3"/>
    <rect x="78" y="116" width="58" height="16" rx="3"/><rect x="144" y="116" width="58" height="16" rx="3"/><rect x="210" y="116" width="58" height="16" rx="3"/><rect x="276" y="116" width="58" height="16" rx="3"/>
    <rect x="78" y="140" width="58" height="16" rx="3"/><rect x="144" y="140" width="58" height="16" rx="3"/><rect x="210" y="140" width="58" height="16" rx="3"/><rect x="276" y="140" width="58" height="16" rx="3"/>
  </g>
  <text x="215" y="178" text-anchor="middle" font-size="12.5" fill="#3D5A45" font-weight="600">✔ 定位准：一搜就中要害</text>
  <text x="215" y="198" text-anchor="middle" font-size="12.5" fill="#B4441C" font-weight="600">✘ 上下文碎：找到半句，答不完整</text>
  <rect x="440" y="24" width="330" height="182" rx="10" fill="#F2F5F1" stroke="#3D5A45" stroke-width="1.5"/>
  <text x="605" y="52" text-anchor="middle" font-size="14.5" font-weight="700" fill="#3D5A45">大块（如 1200 字）→ 7 块</text>
  <g fill="#C9D6CB" stroke="#3D5A45" stroke-width="1">
    <rect x="468" y="66" width="130" height="42" rx="4"/><rect x="610" y="66" width="130" height="42" rx="4"/>
    <rect x="468" y="118" width="130" height="42" rx="4"/><rect x="610" y="118" width="130" height="42" rx="4"/>
  </g>
  <text x="605" y="178" text-anchor="middle" font-size="12.5" fill="#3D5A45" font-weight="600">✔ 上下文完整：政策全貌都在</text>
  <text x="605" y="198" text-anchor="middle" font-size="12.5" fill="#B4441C" font-weight="600">✘ 重点稀释：无关内容把答案带偏</text>
</svg>
<div class="figcap">图 30｜切块大小决定检索粒度（附录A）</div>
</div>
```

:::提示
**常见误解澄清：**「知识库 ≠ 知识图谱」。图谱只是索引的一种形态（下一节和第 05 节都会看到，另一种索引是向量）。就像档案馆里既有按「意思相近」排列的检索卡，也有一面关系网墙。
:::

### 那知识库到底「是」个什么东西？——厨房类比

看到这里你可能冒出一个疑问：向量检索有向量数据库，知识图谱有图数据库，那知识库是啥？是包含这两种数据库的某个软件吗？**都不是——知识库不是某一件软件或某一个数据库，它是「整套系统」的功能性称呼**，就像「厨房」。

你不会指着冰箱或灶台问「厨房是哪个电器」——厨房根本不是电器，它是房间、设备和流程组成的整体。少了哪样都不完整，但哪一样都不等于它。知识库同理，由一排零件拼成：

| 厨房里 | 知识库里的零件 | 分工 |
| --- | --- | --- |
| 冰箱（存食材） | 对象存储（如 MinIO） | 存原始 PDF、视频文件 |
| 食材台账本 | 元数据库（如 PostgreSQL） | 记「哪个文档、什么状态、属于谁」 |
| 灶台 A | 向量数据库（如 Milvus） | 一种找法：按「意思近」找 |
| 灶台 B | 图数据库（如 Neo4j） | 另一种找法：按「关系」找 |
| 备菜流程 | 解析流水线 | 把原料加工成可检索的形态 |
| 服务员 | 检索服务 / API | 接单上菜：把结果交给用户和 AI |

分清两个视角就不会再绕晕：**向量库、图数据库是工程师视角的词**——具体的软件零件，回答「用什么实现」；**「知识库」是使用者视角的词**——回答「这套东西整体上干什么」：存放知识、组织知识、供人查、供 AI 引用。所以只有向量、没有图谱的简化系统也叫知识库，连只有关键词搜索的老式文档系统都常自称知识库——**配几种索引是配置问题，不是定义问题**。

一句话记住：**向量库和图数据库是两个「灶台」，知识库是整座厨房**——第 07 节全景图里从解析、索引到检索的那一大片设施加起来，才是「一个知识库」。

## 03｜RAG：让 AI 从「闭卷考试」变成「开卷考试」

RAG = Retrieval-Augmented Generation，检索增强生成。**一句话：先查资料，再回答。**

### 为什么需要它？

大语言模型（LLM，比如 ChatGPT 背后的模型）有两个天生的毛病：

**① 知识会过期。**模型的知识来自训练时「读」过的资料，训练完就定格了。你公司的内部制度它从来没读过。
**② 会一本正经地编造。**也就是「幻觉」——没读过的东西它也能编得像模像样，还特别自信。

怎么办？让它**开卷考试**：回答问题之前，先从知识库里把相关资料检索出来（Retrieval），夹在题目后面一起递给模型，命令它「只准根据这些资料回答」（Augmented），最后生成（Generation）一段带出处的答案。

```html
<div class="figure">
<svg width="100%" viewBox="0 0 820 400" xmlns="http://www.w3.org/2000/svg" font-family="PingFang SC, Microsoft YaHei, sans-serif">
  <defs><marker id="ar2" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#5C564C"/></marker></defs>
  <!-- 闭卷 -->
  <rect x="30" y="20" width="340" height="130" rx="10" fill="#fff" stroke="#22201C" stroke-width="1.5"/>
  <text x="200" y="48" text-anchor="middle" font-size="15" font-weight="700">✘ 闭卷考试（纯 LLM）</text>
  <rect x="120" y="66" width="160" height="34" rx="17" fill="#EFEAE0" stroke="#5C564C"/>
  <text x="200" y="88" text-anchor="middle" font-size="13">「我们退货要几天？」</text>
  <line x1="200" y1="106" x2="200" y2="124" stroke="#5C564C" stroke-width="2" marker-end="url(#ar2)"/>
  <text x="200" y="142" text-anchor="middle" font-size="13" fill="#B4441C" font-weight="600">模型凭记忆硬答 → 可能编造</text>
  <!-- 开卷 -->
  <rect x="440" y="20" width="350" height="130" rx="10" fill="#fff" stroke="#3D5A45" stroke-width="2"/>
  <text x="615" y="48" text-anchor="middle" font-size="15" font-weight="700" fill="#3D5A45">✔ 开卷考试（RAG）</text>
  <rect x="470" y="66" width="140" height="34" rx="17" fill="#E4EBE4" stroke="#3D5A45"/>
  <text x="540" y="88" text-anchor="middle" font-size="13">同一个问题</text>
  <line x1="614" y1="83" x2="646" y2="83" stroke="#3D5A45" stroke-width="2" marker-end="url(#ar2)"/>
  <rect x="650" y="66" width="118" height="34" rx="17" fill="#3D5A45"/>
  <text x="709" y="88" text-anchor="middle" font-size="13" fill="#fff">资料 + 出处</text>
  <text x="615" y="130" text-anchor="middle" font-size="13" fill="#3D5A45" font-weight="600">照着资料答 → 可溯源</text>
  <!-- RAG 流程 -->
  <text x="410" y="196" text-anchor="middle" font-size="15" font-weight="700">RAG 完整流程（四步）</text>
  <g font-size="14" font-weight="600">
    <rect x="20" y="220" width="176" height="120" rx="10" fill="#FBF6F1" stroke="#C24A20" stroke-width="1.5"/>
    <text x="108" y="250" text-anchor="middle" fill="#C24A20">① 提出问题</text>
    <text x="108" y="278" text-anchor="middle" font-size="12" fill="#5C564C" font-weight="400">「退货要几天？」</text>
    <text x="108" y="298" text-anchor="middle" font-size="12" fill="#5C564C" font-weight="400">问题也被转成向量</text>

    <rect x="216" y="220" width="176" height="120" rx="10" fill="#F2F5F1" stroke="#3D5A45" stroke-width="1.5"/>
    <text x="304" y="250" text-anchor="middle" fill="#3D5A45">② 检索</text>
    <text x="304" y="278" text-anchor="middle" font-size="12" fill="#5C564C" font-weight="400">去向量库找「意思近」的</text>
    <text x="304" y="298" text-anchor="middle" font-size="12" fill="#5C564C" font-weight="400">去图谱找「逻辑相关」的</text>
    <text x="304" y="324" text-anchor="middle" font-size="10.5" fill="#8B857A" font-weight="400">（「向量」是什么？下一节拆开讲）</text>

    <rect x="412" y="220" width="176" height="120" rx="10" fill="#EFEAE0" stroke="#22201C" stroke-width="1.5"/>
    <text x="500" y="250" text-anchor="middle">③ 交给 LLM</text>
    <text x="500" y="278" text-anchor="middle" font-size="12" fill="#5C564C" font-weight="400">「问题+找到的资料片段」</text>
    <text x="500" y="298" text-anchor="middle" font-size="12" fill="#5C564C" font-weight="400">拼成一份「开卷考卷」</text>

    <rect x="608" y="220" width="176" height="120" rx="10" fill="#22201C"/>
    <text x="696" y="250" text-anchor="middle" fill="#F4EFE6">④ 生成答案</text>
    <text x="696" y="278" text-anchor="middle" font-size="12" fill="#B8B0A0" font-weight="400">「7 天（见《售后制度》</text>
    <text x="696" y="298" text-anchor="middle" font-size="12" fill="#B8B0A0" font-weight="400">第 3 条）」← 带引用</text>

    <line x1="196" y1="280" x2="214" y2="280" stroke="#5C564C" stroke-width="2" marker-end="url(#ar2)"/>
    <line x1="392" y1="280" x2="410" y2="280" stroke="#5C564C" stroke-width="2" marker-end="url(#ar2)"/>
    <line x1="588" y1="280" x2="606" y2="280" stroke="#5C564C" stroke-width="2" marker-end="url(#ar2)"/>
  </g>
</svg>
<div class="figcap">图 31｜闭卷与开卷：RAG 的完整流程（附录A）</div>
</div>
```

注意第②步里那行小字——检索可以走两条路：**按「意思相近」找（向量检索）**，或者**按「逻辑相关」找（知识图谱）**。这正是接下来两节的内容，也是整个知识工程最核心的两条腿。

顺带学会一个常见词：**重排（Rerank）**。检索常常分两步——先用快而糙的方式「粗召回」一批可能相关的片段（比如 50 条），再由一个更挑剔但更慢的模型逐条精读、重新排序，只留最相关的几条交给 LLM。相当于老师傅先抱来一摞大概沾边的卷宗，资深馆员再一页页挑出真正有用的三份。

:::提示
**RAG 不是万能药——它治「没资料」，治不了下面这些：**① 库里根本没有相关内容时，模型多半照样硬答（检索空手 ≠ 拒答）；② 引用可能张冠李戴——片段找对了，出处标错了；③ 粗召回的片段里混进无关内容，把答案带偏。其中「逻辑型问题答不准」这个病根，正是第 05、06 节的图谱与本体要来补的。
:::

## 04｜Embedding：把文字变成坐标，「老师傅」靠它找资料

向量检索的全部秘密：**意思相近的文字，变成数字后距离也相近。**

Embedding 模型干的事很单纯：吃进一段文字，吐出一串数字（比如 1024 个数），这串数字叫**向量**。神奇之处在于——它是从数十亿字的海量文本里「悟」出来的，**意思越近的两段话，向量距离越近**。

```html
<div class="figure">
<svg width="100%" viewBox="0 0 820 330" xmlns="http://www.w3.org/2000/svg" font-family="PingFang SC, Microsoft YaHei, sans-serif">
  <!-- 坐标 -->
  <line x1="70" y1="280" x2="770" y2="280" stroke="#B8B0A0" stroke-width="1.5"/>
  <line x1="70" y1="280" x2="70" y2="30" stroke="#B8B0A0" stroke-width="1.5"/>
  <text x="70" y="318" text-anchor="start" font-size="12" fill="#8B857A">（想象这是 1024 维空间压平后的样子）</text>
  <!-- 簇1 售后 -->
  <circle cx="200" cy="90" r="7" fill="#C24A20"/><circle cx="230" cy="105" r="7" fill="#C24A20"/><circle cx="215" cy="70" r="7" fill="#C24A20"/><circle cx="245" cy="82" r="7" fill="#C24A20"/>
  <ellipse cx="222" cy="88" rx="62" ry="52" fill="none" stroke="#C24A20" stroke-width="1.4" stroke-dasharray="5 4"/>
  <text x="222" y="165" text-anchor="middle" font-size="13.5" fill="#C24A20" font-weight="600">「如何退货」</text>
  <text x="222" y="185" text-anchor="middle" font-size="13.5" fill="#C24A20" font-weight="600">「退款流程是什么」</text>
  <text x="222" y="205" text-anchor="middle" font-size="11.5" fill="#8B857A">字面几乎不同，意思却近 → 距离近</text>
  <!-- 簇2 物流 -->
  <circle cx="560" cy="220" r="7" fill="#3D5A45"/><circle cx="590" cy="235" r="7" fill="#3D5A45"/><circle cx="575" cy="205" r="7" fill="#3D5A45"/>
  <ellipse cx="577" cy="221" rx="52" ry="42" fill="none" stroke="#3D5A45" stroke-width="1.4" stroke-dasharray="5 4"/>
  <text x="577" y="296" text-anchor="middle" font-size="13.5" fill="#3D5A45" font-weight="600">「快递几天到」「运费谁出」</text>
  <!-- 簇3 闲聊 -->
  <circle cx="640" cy="80" r="7" fill="#8B857A"/><circle cx="668" cy="95" r="7" fill="#8B857A"/><circle cx="650" cy="60" r="7" fill="#8B857A"/>
  <ellipse cx="653" cy="79" rx="46" ry="40" fill="none" stroke="#8B857A" stroke-width="1.4" stroke-dasharray="5 4"/>
  <text x="653" y="145" text-anchor="middle" font-size="13.5" fill="#8B857A" font-weight="600">「今天天气不错」</text>
  <!-- 查询星 -->
  <path d="M 420 150 l 4.5 12 12.5 1 -9.5 8.3 3 12.2 -10.5 -6.6 -10.5 6.6 3 -12.2 -9.5 -8.3 12.5 -1 z" fill="#B98A2F"/>
  <text x="420" y="205" text-anchor="middle" font-size="12.5" fill="#B98A2F" font-weight="600">你的问题落在这里</text>
  <line x1="420" y1="150" x2="268" y2="100" stroke="#B98A2F" stroke-width="1.6" stroke-dasharray="4 4"/>
  <line x1="438" y1="152" x2="545" y2="207" stroke="#B98A2F" stroke-width="1.6" stroke-dasharray="4 4"/>
  <text x="335" y="112" font-size="11.5" fill="#B98A2F">近 → 优先召回</text>
  <text x="510" y="168" font-size="11.5" fill="#B98A2F">也相关 → 召回</text>
</svg>
<div class="figcap">图 32｜在「意思的空间」里找邻居（附录A）</div>
</div>
```

**它强在哪：**模糊、口语、没见过的说法都能对上。「家父是何人」这种文言文，规则表里没有，但老师傅凭感觉知道它≈「我爸爸是谁」。
**它弱在哪：**只懂「像」，不懂「对」。问「小明的爷爷是谁」，资料里只写了「张三是小明爸爸、李四是张三爸爸」——靠相似度只能捞回一堆「和小明家人有关」的片段，**推不出**李四就是爷爷（就算片段都捞回来了，能不能串对也全靠模型临场发挥，没有任何机制保证）。这种严格的多步逻辑，要靠下一节的知识图谱。

:::提示
**一个容易踩的坑：**换 Embedding 模型 = 换了整个坐标系，新旧向量没法互相比较，整个索引必须推倒重建。所以工程上 Embedding 模型总是最先定、最不轻易换的那一个。顺带认识一位仓库管理员：专门存向量的数据库（如 Milvus）优化的就是「高维空间找邻居」这一件事——第 08 节实战表里会再遇到它。
:::

## 05｜知识图谱：把知识织成一张「关系网」

向量管「感觉像」，图谱管**「事实和逻辑」**。它的最小单元叫三元组。

知识图谱存知识的方式非常朴素——一条一条的「主语、谓语、宾语」：（张三，任职于，腾讯）、（腾讯，开发了，微信）、（腾讯，总部位于，深圳）。

把成千上万条三元组画出来，就是一张网：**节点**是实体（张三、腾讯、微信、深圳），**边**是关系（任职于、开发了、位于）。

```html
<div class="figure">
<svg width="100%" viewBox="0 0 820 300" xmlns="http://www.w3.org/2000/svg" font-family="PingFang SC, Microsoft YaHei, sans-serif">
  <defs><marker id="ar3" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="#5C564C"/></marker></defs>
  <!-- 边 -->
  <line x1="185" y1="150" x2="352" y2="150" stroke="#5C564C" stroke-width="2" marker-end="url(#ar3)"/>
  <text x="257" y="171" text-anchor="middle" font-size="13" fill="#5C564C" font-style="italic">任职于</text>
  <line x1="447" y1="139" x2="608" y2="84" stroke="#5C564C" stroke-width="2" marker-end="url(#ar3)"/>
  <text x="540" y="92" text-anchor="middle" font-size="13" fill="#5C564C" font-style="italic">开发了</text>
  <line x1="446" y1="165" x2="610" y2="217" stroke="#5C564C" stroke-width="2" marker-end="url(#ar3)"/>
  <text x="545" y="215" text-anchor="middle" font-size="13" fill="#5C564C" font-style="italic">总部位于</text>
  <line x1="166" y1="81" x2="350" y2="172" stroke="#B98A2F" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#ar3)"/>
  <text x="244" y="100" text-anchor="middle" font-size="13" fill="#B98A2F" font-style="italic">任职于</text>
  <!-- 节点 -->
  <g font-weight="700">
    <circle cx="160" cy="150" r="42" fill="#FBF6F1" stroke="#C24A20" stroke-width="2.5"/><text x="160" y="148" text-anchor="middle" font-size="15">张三</text><text x="160" y="166" text-anchor="middle" font-size="10.5" fill="#8B857A" font-weight="400">人</text>
    <circle cx="130" cy="70" r="38" fill="#FBF6F1" stroke="#C24A20" stroke-width="2.5"/><text x="130" y="68" text-anchor="middle" font-size="15">李四</text><text x="130" y="85" text-anchor="middle" font-size="10.5" fill="#8B857A" font-weight="400">人</text>
    <circle cx="400" cy="150" r="48" fill="#F2F5F1" stroke="#3D5A45" stroke-width="2.5"/><text x="400" y="148" text-anchor="middle" font-size="15">腾讯</text><text x="400" y="166" text-anchor="middle" font-size="10.5" fill="#8B857A" font-weight="400">公司</text>
    <circle cx="648" cy="72" r="42" fill="#F7F3E8" stroke="#B98A2F" stroke-width="2.5"/><text x="648" y="70" text-anchor="middle" font-size="15">微信</text><text x="648" y="87" text-anchor="middle" font-size="10.5" fill="#8B857A" font-weight="400">产品</text>
    <circle cx="650" cy="230" r="42" fill="#EFEAE0" stroke="#22201C" stroke-width="2.5"/><text x="650" y="228" text-anchor="middle" font-size="15">深圳</text><text x="650" y="245" text-anchor="middle" font-size="10.5" fill="#8B857A" font-weight="400">城市</text>
  </g>
  <text x="410" y="285" text-anchor="middle" font-size="12.5" fill="#8B857A">节点 = 实体（带类型）　·　带箭头的边 = 关系　·　整张网 = 知识图谱</text>
</svg>
<div class="figcap">图 33｜实体是点，关系是边（附录A）</div>
</div>
```

注意上图里每个节点都标了类型（人/公司/产品/城市）——这个「类型」从哪来？答案在第 06 节。

### 图谱的杀手锏：多跳推理

问：「李四的同事所在的公司总部在哪？」人脑会走：**李四 →（任职于）→ 腾讯 →（总部位于）→ 深圳**。沿着边走两步，答案就出来了。这种「走两三步才到答案」的问题（也叫多跳问题），向量检索基本无能为力，图谱却是天然擅长。专门存这种网的数据库叫图数据库（如 Neo4j）——它优化的就是「顺着边走」这件事。

| | 向量检索（老师傅） | 知识图谱（关系网） |
| --- | --- | --- |
| 擅长 | 模糊、口语化、没见过的说法 | 精确事实、多步逻辑、关系推理 |
| 短板 | 推不出「爷爷=爸爸的爸爸」 | 规则和事实都要人（或 AI）先建好 |
| 比喻 | 凭语感找相似 | 顺着线头找关联 |

现代知识引擎（比如开源项目 Jonex）几乎都是**两路一起召回**：向量捞「感觉像的」，图谱查「逻辑相关的」，合并后交给 LLM。这类用图谱增强检索的系统，常被统称为 **GraphRAG**。（检索领域另有一个「混合检索」，指向量+关键词双路召回，是另一回事，别混淆。）

## 06｜本体论：给知识定「语法规则」的手册

最后一块拼图。哲学里它研究「存在什么」；信息科学里它是一份**明确写下来的概念清单 + 关系规则**。

### 为什么图谱需要一本「手册」？

假设没有规则，大家随便往图谱里存东西：（张三，任职于，腾讯）、（张三，就职于，腾讯公司）、（张三，属于，TX）——三条说的是同一件事，但机器看起来是三个不同的关系。图谱越大越乱，最后没人说得清「任职于」和「就职于」是不是一回事。**本体就是事先立好的规矩**：概念叫什么名、允许哪些属性、什么类型之间允许什么关系、同义词算谁。

但规矩只是本体的一半：**一份完整的本体 = 规则 + 按规则登记的事实**。知识表示领域给这两半各起了名字——理解了这对术语，本体这个词就再也不会拆散：

```html
<div class="figure">
<svg width="100%" viewBox="0 0 820 300" xmlns="http://www.w3.org/2000/svg" font-family="PingFang SC, Microsoft YaHei, sans-serif">
  <defs><marker id="ar4" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="#B98A2F"/></marker></defs>
  <!-- TBox -->
  <rect x="40" y="30" width="340" height="240" rx="12" fill="#F7F3E8" stroke="#B98A2F" stroke-width="2"/>
  <text x="210" y="60" text-anchor="middle" font-size="16" font-weight="700" fill="#B98A2F">TBox：概念层（手册）</text>
  <g font-size="13.5">
    <rect x="80" y="85" width="110" height="40" rx="8" fill="#fff" stroke="#B98A2F" stroke-width="1.8"/><text x="135" y="110" text-anchor="middle">类型：人</text>
    <rect x="240" y="85" width="110" height="40" rx="8" fill="#fff" stroke="#B98A2F" stroke-width="1.8"/><text x="295" y="110" text-anchor="middle">类型：公司</text>
    <line x1="190" y1="105" x2="238" y2="105" stroke="#B98A2F" stroke-width="1.8" marker-end="url(#ar4)"/>
    <text x="215" y="97" text-anchor="middle" font-size="11.5" fill="#8B857A">任职于</text>
    <text x="210" y="165" text-anchor="middle" fill="#5C564C">人可以有：姓名、入职日期</text>
    <text x="210" y="192" text-anchor="middle" fill="#5C564C">公司可以有：法人、注册地</text>
    <text x="210" y="219" text-anchor="middle" fill="#5C564C">「公司」的别名：企业/机构</text>
    <text x="210" y="252" text-anchor="middle" font-size="12.5" fill="#B98A2F" font-weight="600">≈ 数据库的表结构（CREATE TABLE）</text>
  </g>
  <!-- 箭头 -->
  <line x1="385" y1="150" x2="435" y2="150" stroke="#B98A2F" stroke-width="2.5" marker-end="url(#ar4)"/>
  <text x="410" y="132" text-anchor="middle" font-size="12" fill="#B98A2F">约束</text>
  <!-- ABox -->
  <rect x="440" y="30" width="340" height="240" rx="12" fill="#F2F5F1" stroke="#3D5A45" stroke-width="2"/>
  <text x="610" y="60" text-anchor="middle" font-size="16" font-weight="700" fill="#3D5A45">ABox：事实层（数据）</text>
  <g font-size="13.5">
    <circle cx="530" cy="120" r="10" fill="#C24A20"/><text x="530" y="152" text-anchor="middle" font-size="13">张三</text>
    <circle cx="700" cy="120" r="10" fill="#3D5A45"/><text x="700" y="152" text-anchor="middle" font-size="13">腾讯</text>
    <line x1="540" y1="120" x2="688" y2="120" stroke="#5C564C" stroke-width="1.8" marker-end="url(#ar4)"/>
    <text x="615" y="112" text-anchor="middle" font-size="11.5" fill="#8B857A">任职于</text>
    <circle cx="615" cy="200" r="10" fill="#B98A2F"/><text x="615" y="232" text-anchor="middle" font-size="13">深圳</text>
    <line x1="708" y1="128" x2="628" y2="192" stroke="#5C564C" stroke-width="1.8" marker-end="url(#ar4)"/>
    <text x="688" y="175" text-anchor="middle" font-size="11.5" fill="#8B857A">总部位于</text>
    <text x="610" y="252" text-anchor="middle" font-size="12.5" fill="#3D5A45" font-weight="600">≈ 表里一行一行的数据（INSERT）</text>
  </g>
</svg>
<div class="figcap">图 34｜TBox 定规则，ABox 装事实（附录A）</div>
</div>
```

再送一个更完整的类比——把本体想成**一个 Excel 工作簿**：

| 工作簿里 | 本体里 |
| --- | --- |
| 所有 sheet 的名字、全部表头、每列的数据验证规则、跨表引用的约定 | **TBox**（结构层） |
| 所有 sheet 里填的数据行，加上行与行之间的引用 | **ABox**（数据层） |

有两块信息是「表头」装不下的，恰好是本体的精髓：**① sheet 的名字本身**——有哪些类型，是 TBox 定的第一件事；**② 跨 sheet 的关联规则**——「人」表可以有一列指向「公司」表。普通表格想引用就引用、填错没人拦，而本体在结构上就规定死了允许哪些关系。另外 ABox 那半也别只想着行：**行与行之间的连线同样是 ABox 的数据**——「张三任职于腾讯」这条引用，和行内的姓名、日期平级。

### 「YAML 本体」vs「OWL 本体」：轻量版和完全体

讲完本体的内容结构（TBox + ABox），还剩一个独立的选择：**TBox 用哪种格式写**——这就是「YAML 本体」「OWL 本体」两个词的全部含义，跟上面的内容结构是两个互不干扰的维度。（ABox 那半怎么生产、存在哪，本节末尾两小节专门讲。）

写 TBox 的「笔」有两种。Jonex 用的 **YAML**，是给人看的极简格式——下面这段代码不是新东西，就是图 34 左边那份 TBox 用 YAML 写出来的样子：

```html
<pre style="font-family:Consolas,'Courier New',monospace; font-size:8.5pt; line-height:1.75; background:#F6F5F2; border:1px solid #E7E5E4; border-radius:8px; padding:14px 18px; margin:18px 0; white-space:pre; page-break-inside:avoid;"># ── 一份极简本体（依 Jonex 的 YAML TBox 扩充的示意版）──
# 整份文件只回答三个问题：
#   ① 有哪些实体类型？                → entity_types
#   ② 每个类型长什么样（别名+属性）？  → aliases / attributes
#   ③ 类型之间允许什么关系？           → relation_types

entity_types:              # ── 第一部分：实体类型清单（= 工作簿里所有 sheet 的名字）──
  - name: Person           # 类型一：人
    aliases: ["员工", "职员"]   # 别名：文档里写「员工」「职员」都算 Person
    attributes:            # 属性清单（= 这张 sheet 的列 + 数据验证规则）
      - { name: name,      type: string }  # 姓名：必须是文字
      - { name: hire_date, type: date }    # 入职日期：必须是日期
      - { name: level, type: enum, values: ["P1","P2","P3","P4","P5"] }
                                    # ↑ 级别：只能五选一（Excel 下拉框）

  - name: Organization     # 类型二：机构
    aliases: ["公司", "企业", "机构"]  # 中文别名：抽到「企业」也算这类
    attributes:
      - { name: legal_name, type: string }  # 法人名：文字
      - { name: founded_on, type: date }    # 成立日期：日期

relation_types:            # ── 第二部分：关系类型清单（= 跨表引用规则）──
  - name: BELONGS_TO       # 关系：「隶属于」
    source: Person         # 起点只能是人
    target: Organization   # 终点只能是机构
    # ↑（张三 → 腾讯）合法；（腾讯 → 李四）方向反了，直接违规</pre>
```

对照工作簿类比读一遍：<code>entity_types</code> 是 sheet 名单，<code>attributes</code> 是每张 sheet 的列和数据验证（enum 那行就是下拉框），<code>relation_types</code> 是跨表引用约定——source/target 一旦写死，方向装反的登记就进不了库。

再把这份代码登记出来的数据，真的画成工作簿的样子——两张 sheet、各自的表头和数据行、还有跨表引用列，每一项都能在代码里找到出处：

#### Sheet 1《Person》人

| name<br/>（姓名） | hire_date<br/>（入职日期） | level<br/>（级别·五选一） | 所属机构（BELONGS_TO）<br/>→ 只能引用《Organization》的行 |
| --- | --- | --- | --- |
| 张三 | 2024-03-01 | P3 | 腾讯（跨表引用 ↓） |
| 李四 | 2021-07-15 | P2 | 腾讯（跨表引用 ↓） |

#### Sheet 2《Organization》机构

| legal_name<br/>（法人名） | founded_on<br/>（成立日期） |
| --- | --- |
| 腾讯 | 1998-11-11 |

逐项指认：两张 sheet 的**名字**来自 <code>entity_types</code>，每张表的**表头和验证规则**来自 <code>attributes</code>（level 列就是那个五选一下拉框），Sheet 1 最后一列的**引用规则**来自 <code>relation_types</code>——这一列只能填《Organization》里的行。反过来，不合规的数据进不了表：李四的 level 若填成 M2，整行被下拉框拦下；（腾讯，BELONGS_TO，李四）方向装反，引用直接被拒。放行的行最终写进图数据库——这就是「schema 约束的抽取」的全貌。

而学术正统用 **OWL**（W3C 标准），表达力强得多——能声明「公司是一种机构」的**子类继承**，也能把某个关系声明为**传递的**（如「上游供应商」：A 供 B、B 供 C ⇒ 机器自动推出 A 供 C），还能据此**自动推理**出新事实。代价是门槛高，没受过训练的人写不了。（跑大型 OWL 本体的老牌实例：把维基百科结构化的 DBpedia、基因学界的标准词汇 Gene Ontology。）

| 能力 | YAML 本体（务实派，如 Jonex） | OWL 本体（学院派，如 DBpedia、Gene Ontology） |
| --- | --- | --- |
| 定义类型、属性、关系 | ✔ | ✔ |
| 中文别名对齐 | ✔ 一行搞定 | △ 用 SKOS 标签体系，啰嗦 |
| 子类继承推理 | ✘ | ✔ |
| 传递关系（A属B、B属C ⇒ A从属C） | ✘ | ✔ |
| 逻辑一致性校验 | ✘ | ✔ |
| 上手难度 | 十分钟 | 要学一套标准 |

这是一道经典的工程取舍题：**砍掉推理能力，换来人人能写。**公平地补两句：OWL 阵营并非写不了别名——W3C 的 SKOS 标准里就有「替代标签」（altLabel），只是繁琐得多；而蚂蚁集团的知识引擎 KAG 走了第三条路——自研带推理的 SPG 建模语言，不碰 OWL 也照样推理。可见「好写」和「能推理」并非天生互斥，只是工程上很难兼得。没有对错，只有场景合不合适。

### 谁来填这些行？——ABox 的两种生产方式

TBox 几百行，写一次用很久，人写没问题。那 ABox 的数据行呢？「张三任职于腾讯」这种事实，总得有人写进去吧？——有两条路，对应两个时代：

| | 老路：人工录入 | 新路：程序抽取 |
| --- | --- | --- |
| 怎么干 | 领域专家读完文档，用编辑器逐条敲三元组 | LLM 读文档，自动吐出三元组，程序写入图数据库 |
| 成本 | 恐怖：十万字文档人工抽取要数周 | 一张 API 账单，几秒到几分钟 |
| 可靠性 | 准，但人会累、会漏 | 会归错类、漏抽、重复，需要校对和重试 |
| 人的角色 | 录入员 | 审核员：写好 TBox，抽查机器人填得对不对 |

所以「ABox 通常不手写」的意思就是生产方式的更替：**数据行还是那些数据行，只是从「人一行行录入」换成了「流水线自动生成」。**Jonex 的 Stage 4 就是这条流水线：LLM 拿着 TBox 的类型清单对文本做归类、消歧、补属性，产出本体数据写进 Neo4j，抽错了还有对账重试（最多 3 次）。

顺带解开一个大疑问：**知识图谱是 1998 年就有的老概念，为什么最近两年才在工业界起飞？**因为 LLM 把「抽取」这一步的成本砍掉了一两个数量级——原来雇不起的录入员，现在是一张 API 账单。

### 这两个 Box 的数据分别存在哪？

向量有向量数据库，图谱有图数据库——那 TBox 和 ABox 还要再配数据库吗？**不用：TBox 通常就是一个文件，ABox 就存在图数据库里。**它俩不需要新家。

| | TBox（规则） | ABox（事实） |
| --- | --- | --- |
| 装什么 | 类型、属性、关系定义 | 实体实例 + 关系事实 |
| 数据量 | 极小：几十到几百行 | 随文档量持续增长 |
| 存在哪 | **一个文件**（YAML 或 OWL），跟代码一起进版本管理 | **图数据库**（如 Neo4j），程序抽取后写入 |
| Jonex 对应物 | default.yaml 配置文件 | Neo4j 里的实体节点和关系 |

所以一套知识引擎里数得着的存储就三种：**文件**装 TBox、**向量库**装「块 + 坐标」、**图数据库**装「实体 + 关系」——其中按 TBox 的规矩登记进图数据库的那部分，就是 ABox。没有第四种「本体数据库」等着你。

两个补充：① Jonex 的 Neo4j 里其实住着**两种图**——LightRAG 自动抽的「野生图」（不守规矩，见关系就抽）和按 TBox 登记的 ABox（守规矩的强类型实体），两套并存、各查各的。② 学院派那边确实有把两半一起装进数据库的完全体方案：专门的**三元组库**（triple store，如 GraphDB、Jena Fuseki），TBox 和 ABox 一起存、用 SPARQL 查询（语义网世界的 SQL）——OWL 用得认真的机构走的是这条路。

### 进阶视野：当本体不止是「手册」——Palantir 的操作层革命

前面我们把本体讲成「编目规则手册」。现在看产业界最激进的玩法：把本体做成**直接驱动业务的操作系统**。

小结里那句话在学术界有正式出处：「概念化的明确规范说明」（Gruber, 1993），Studer 等（1998）又补上「形式化、共享」两个限定——本节的 TBox/ABox，就是这句话的工程化拆解。

再来看一个扎心的行业现状：企业花大钱建数据湖、买 BI 看板，但数据只是「**给人看的快照**」——看板说该补货了，员工看一眼屏幕，转身去订单系统里**手工录入**。分析和执行两张皮，中间靠人肉搬运，AI 建得再好也落不了地。

```html
<div class="figure">
<svg width="100%" viewBox="0 0 820 320" xmlns="http://www.w3.org/2000/svg" font-family="PingFang SC, Microsoft YaHei, sans-serif">
  <defs>
    <marker id="ar6" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="#5C564C"/></marker>
    <marker id="ar6r" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="#B4441C"/></marker>
    <marker id="ar6g" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="#3D5A45"/></marker>
  </defs>
  <!-- 左：传统模式 -->
  <rect x="20" y="26" width="380" height="258" rx="10" fill="#FBF0EE" stroke="#B4441C" stroke-width="1.5"/>
  <text x="210" y="54" text-anchor="middle" font-size="14.5" font-weight="700" fill="#B4441C">传统模式：数据只给人看</text>
  <g font-size="12.5" font-weight="600">
    <rect x="45" y="76" width="115" height="42" rx="8" fill="#fff" stroke="#5C564C" stroke-width="1.4"/><text x="102" y="102" text-anchor="middle">数据源</text>
    <rect x="45" y="172" width="115" height="48" rx="8" fill="#fff" stroke="#5C564C" stroke-width="1.4"/><text x="102" y="193" text-anchor="middle">数据湖 / BI</text><text x="102" y="211" text-anchor="middle" font-size="10.5" fill="#8B857A" font-weight="400">给人看的看板</text>
    <rect x="250" y="76" width="115" height="42" rx="8" fill="#fff" stroke="#5C564C" stroke-width="1.4"/><text x="307" y="102" text-anchor="middle">员工</text>
    <rect x="250" y="172" width="115" height="48" rx="8" fill="#fff" stroke="#5C564C" stroke-width="1.4"/><text x="307" y="193" text-anchor="middle">业务系统</text><text x="307" y="211" text-anchor="middle" font-size="10.5" fill="#8B857A" font-weight="400">ERP / 订单 / CRM</text>
  </g>
  <line x1="102" y1="118" x2="102" y2="170" stroke="#5C564C" stroke-width="1.8" marker-end="url(#ar6)"/>
  <text x="118" y="148" font-size="11" fill="#8B857A">每夜抽取</text>
  <line x1="160" y1="188" x2="248" y2="104" stroke="#5C564C" stroke-width="1.8" marker-end="url(#ar6)"/>
  <text x="204" y="140" font-size="11" fill="#8B857A">人看屏幕</text>
  <line x1="307" y1="118" x2="307" y2="170" stroke="#B4441C" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#ar6r)"/>
  <text x="307" y="146" text-anchor="middle" font-size="11" fill="#B4441C">人肉录入 ✗</text>
  <text x="210" y="268" text-anchor="middle" font-size="12.5" fill="#B4441C" font-weight="600">分析与执行两张皮，中间靠人肉搬运</text>
  <!-- 右：本体操作层 -->
  <rect x="420" y="26" width="380" height="258" rx="10" fill="#F2F5F1" stroke="#3D5A45" stroke-width="1.8"/>
  <text x="610" y="54" text-anchor="middle" font-size="14.5" font-weight="700" fill="#3D5A45">本体操作层：数据直接驱动业务</text>
  <g font-size="12.5" font-weight="600">
    <rect x="448" y="76" width="150" height="50" rx="8" fill="#F7F3E8" stroke="#B98A2F" stroke-width="1.8"/><text x="523" y="97" text-anchor="middle" fill="#B98A2F">本体</text><text x="523" y="115" text-anchor="middle" font-size="10.5" fill="#8B857A" font-weight="400">名词 + 动词</text>
    <rect x="652" y="76" width="120" height="50" rx="8" fill="#fff" stroke="#5C564C" stroke-width="1.4"/><text x="712" y="97" text-anchor="middle">数据源</text><text x="712" y="115" text-anchor="middle" font-size="10.5" fill="#8B857A" font-weight="400">ERP·CRM·传感器</text>
    <rect x="650" y="176" width="122" height="48" rx="8" fill="#fff" stroke="#5C564C" stroke-width="1.4"/><text x="711" y="197" text-anchor="middle">AI / 应用</text><text x="711" y="215" text-anchor="middle" font-size="10.5" fill="#8B857A" font-weight="400">读结构化数据</text>
    <rect x="445" y="176" width="120" height="48" rx="8" fill="#fff" stroke="#5C564C" stroke-width="1.4"/><text x="505" y="197" text-anchor="middle">人审核</text><text x="505" y="215" text-anchor="middle" font-size="10.5" fill="#8B857A" font-weight="400">批准 / 驳回</text>
  </g>
  <line x1="652" y1="101" x2="600" y2="101" stroke="#5C564C" stroke-width="1.8" marker-end="url(#ar6)"/>
  <text x="626" y="92" text-anchor="middle" font-size="11" fill="#8B857A">索引</text>
  <path d="M 560 126 Q 630 150 690 174" fill="none" stroke="#5C564C" stroke-width="1.8" marker-end="url(#ar6)"/>
  <text x="636" y="158" font-size="11" fill="#8B857A">提供数据+权限</text>
  <line x1="650" y1="200" x2="567" y2="200" stroke="#5C564C" stroke-width="1.8" marker-end="url(#ar6)"/>
  <text x="608" y="192" text-anchor="middle" font-size="11" fill="#8B857A">动作提案</text>
  <line x1="505" y1="176" x2="505" y2="130" stroke="#3D5A45" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#ar6g)"/>
  <text x="493" y="158" text-anchor="end" font-size="11" fill="#3D5A45">审核通过 · 写回</text>
  <text x="610" y="268" text-anchor="middle" font-size="12.5" fill="#3D5A45" font-weight="600">AI 只能在定义好的「动词」内提案，闭环写回本体</text>
</svg>
<div class="figcap">图 35｜传统两张皮与本体操作层（附录A）</div>
</div>
```

Palantir（千亿美金市值的数据公司，CIA 起家）的答案，就是把本体升级成「**操作层（Operational Layer）**」：不只描述世界，还能**改**世界。秘诀是把企业建模成「名词 + 动词」：

| 两类元素 | 装什么 | 对应你已学过的 |
| --- | --- | --- |
| **名词**（语义层） | 对象类型、属性、关系 | 就是本节的 TBox / ABox |
| **动词**（动作层） | 下单、审批、改状态……带副作用的业务操作 | 传统写在各应用代码里；Palantir 把它请进本体 |

关键在动词那半边：「下单、审批、改状态」这类动作传统上散落在各种应用代码里，和数据模型两张皮；把它们显式定义进本体之后，AI 和应用就能**在围栏内直接执行业务**，结果写回本体，形成闭环。空客把 A350 的约 500 万个零件、供应商、进度全部本体化，交付周期缩短约三分之一（数字来自 Palantir 官方案例页，听个量级就好）；日本 SOMPO 用它做保险反欺诈，八千多人日常在用。

这个思路还顺手治了第 03 节留下的病根——**幻觉**。LLM 不再直接碰原始数据，而是面对本体里定义好的名词与动词：它只能在「已定义的动作」范围内**提案**，由人审核后才真正执行。语义的墙，把幻觉关在了门外。这比 RAG 的「带引用回答」又往前走了一步：不止说得对，还能**做得对**。

:::提示
**两条彩蛋：**① 连「改本体」这件事本身都有治理流程——变更要走「分支 → 提案 → 评审 → 合并」，相当于给数据建模引入了程序员的 Pull Request；Jonex 配套建模小工具 Nexonto 里的「工作副本 + 修订冲突检测」，正是这套思想的开源平民版。② Jonex 的 GitHub 话题里挂着 "fde"（Forward Deployed Engineer，Palantir 著名的前置部署工程师模式）——明摆着的致敬。开源世界正在把这套打法平民化。
:::

### 本节小结：所以，本体到底是什么？

**本体是一份明确写下来的领域概念规范——规定这个领域里有哪些概念、每个概念有什么属性、概念之间允许什么关系。**学术界的说法「概念化的明确规范说明」（Gruber, 1993），说的就是这句白话。

结构上由两半组成：**TBox（规则）**——一个小文件，几十到几百行；**ABox（事实）**——按规则登记进图数据库的实体和关系。就像工作簿的结构层和数据层。

它解决三件事：**对齐**（「企业」「公司」「机构」归成一类）、**把关**（不合规的数据进不了库）、**推理**（OWL 派还能从已有事实推出新事实）。

最后一个最容易混的边界：**本体是规范，知识图谱是数据。**TBox 是编目手册，图谱是按手册登记出来、挂满卡片的那面墙——手册不是墙，但没有手册，墙上的卡片会越挂越乱。

离开本体论之前，把四个词最后对齐一次。用厨房类比说：知识库是整座厨房，本体是这家厨房的《菜品标准手册》——手册不是厨房里的又一台电器，它是厨房运转所依据的规范。

| 词 | 一句话 | 在档案馆里 | 在 Jonex 里 |
| --- | --- | --- | --- |
| 知识库 | 装知识的整套系统 | 整座档案馆 | 整个平台（21 个容器） |
| 向量检索 | 按「意思近」找的一种找法 | 老师傅的语感 | Milvus + Embedding |
| 知识图谱 | 实体 + 关系织成的数据网 | 关系网墙 | Neo4j 里的图数据 |
| 本体 | 管图谱数据怎么登记的规则 | 编目规则手册 | default.yaml（TBox）+ 按它登记的 ABox |

三条关系串起全部：**① 包含**——知识库是整套系统，向量库和图数据库（图谱住在里面）都是它的零件，不是兄弟；**② 管辖**——本体只管图谱那一路，ABox 按它的规矩登记、违规进不了库，而向量那路凭语感、完全不归它管（所以 Milvus 里没有「守不守规矩」一说）；**③ 转化**——图谱里守规矩的部分就是本体落地后的 ABox，不守的是野生图。一句话终极版：**知识库是整座档案馆，向量检索和图谱是两种找法，本体是馆里的立法者——它不管你用什么找法，只规定登记进图谱的数据必须长什么样。**（把这四个词画进同一张图的全景图，就在第 07 节。）

## 07｜全景图：四个概念如何拼成一个系统

现在把前面几节拼起来。下面这张图，就是几乎所有知识引擎（包括 Jonex）的骨架。

```html
<div class="figure">
<svg width="100%" viewBox="0 0 860 560" xmlns="http://www.w3.org/2000/svg" font-family="PingFang SC, Microsoft YaHei, sans-serif">
  <defs><marker id="ar5" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="#5C564C"/></marker></defs>
  <!-- 本体 顶部 -->
  <rect x="280" y="14" width="300" height="64" rx="10" fill="#F7F3E8" stroke="#B98A2F" stroke-width="2"/>
  <text x="430" y="40" text-anchor="middle" font-size="15.5" font-weight="700" fill="#B98A2F">本体（规则手册 / TBox）</text>
  <text x="430" y="62" text-anchor="middle" font-size="12" fill="#8B857A">定义：有哪些概念、允许什么关系</text>
  <!-- 原始资料 -->
  <rect x="30" y="130" width="180" height="96" rx="10" fill="#EFEAE0" stroke="#22201C" stroke-width="1.6"/>
  <text x="120" y="158" text-anchor="middle" font-size="14.5" font-weight="700">原始资料</text>
  <text x="120" y="182" text-anchor="middle" font-size="12" fill="#5C564C">PDF · Word · 网页</text>
  <text x="120" y="203" text-anchor="middle" font-size="12" fill="#5C564C">音频 · 视频</text>
  <!-- 解析 -->
  <rect x="250" y="130" width="150" height="96" rx="10" fill="#EFEAE0" stroke="#22201C" stroke-width="1.6"/>
  <text x="325" y="158" text-anchor="middle" font-size="14.5" font-weight="700">① 解析</text>
  <text x="325" y="182" text-anchor="middle" font-size="12" fill="#5C564C">文档版式识别</text>
  <text x="325" y="203" text-anchor="middle" font-size="12" fill="#5C564C">语音转文字</text>
  <!-- 向量库 -->
  <rect x="460" y="108" width="180" height="110" rx="10" fill="#FBF6F1" stroke="#C24A20" stroke-width="2"/>
  <text x="550" y="134" text-anchor="middle" font-size="14.5" font-weight="700" fill="#C24A20">② 向量库</text>
  <text x="550" y="158" text-anchor="middle" font-size="12" fill="#5C564C">每段文字 → 一串数字</text>
  <text x="550" y="179" text-anchor="middle" font-size="12" fill="#5C564C">按「意思近」组织</text>
  <text x="550" y="202" text-anchor="middle" font-size="11.5" fill="#C24A20">（老师傅的语感卡）</text>
  <!-- 图谱 -->
  <rect x="670" y="108" width="160" height="110" rx="10" fill="#F2F5F1" stroke="#3D5A45" stroke-width="2"/>
  <text x="750" y="134" text-anchor="middle" font-size="14.5" font-weight="700" fill="#3D5A45">③ 知识图谱</text>
  <text x="750" y="158" text-anchor="middle" font-size="12" fill="#5C564C">抽出实体和关系</text>
  <text x="750" y="179" text-anchor="middle" font-size="12" fill="#5C564C">按「逻辑」组织</text>
  <text x="750" y="202" text-anchor="middle" font-size="11.5" fill="#3D5A45">（关系网墙 / ABox）</text>
  <!-- 本体箭头到图谱 -->
  <path d="M 560 78 Q 750 82 752 106" fill="none" stroke="#B98A2F" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#ar5)"/>
  <text x="668" y="74" font-size="12" fill="#B98A2F">按手册约束抽取</text>
  <!-- 流程箭头 -->
  <line x1="210" y1="178" x2="248" y2="178" stroke="#5C564C" stroke-width="2" marker-end="url(#ar5)"/>
  <path d="M 400 158 Q 435 148 458 148" fill="none" stroke="#5C564C" stroke-width="2" marker-end="url(#ar5)"/>
  <path d="M 400 208 Q 530 250 668 216" fill="none" stroke="#5C564C" stroke-width="2" marker-end="url(#ar5)"/>
  <text x="515" y="252" font-size="12" fill="#8B857A">抽事实</text>
  <!-- 知识库大框 -->
  <rect x="240" y="92" width="600" height="140" rx="14" fill="none" stroke="#22201C" stroke-width="1.2" stroke-dasharray="3 5"/>
  <text x="835" y="252" font-size="12" fill="#8B857A" text-anchor="end">└ 这三样合起来 = 知识库</text>
  <!-- 问答区 -->
  <rect x="80" y="330" width="180" height="70" rx="10" fill="#EFEAE0" stroke="#22201C" stroke-width="1.6"/>
  <text x="170" y="358" text-anchor="middle" font-size="14" font-weight="700">用户提问</text>
  <text x="170" y="382" text-anchor="middle" font-size="12" fill="#5C564C">「李四同事公司总部在哪？」</text>
  <!-- 检索 -->
  <rect x="330" y="322" width="170" height="86" rx="10" fill="#fff" stroke="#22201C" stroke-width="2"/>
  <text x="415" y="348" text-anchor="middle" font-size="14" font-weight="700">④ 检索（RAG 前半）</text>
  <text x="415" y="371" text-anchor="middle" font-size="12" fill="#C24A20">向量路：找意思近的</text>
  <text x="415" y="391" text-anchor="middle" font-size="12" fill="#3D5A45">图谱路：走关系推理</text>
  <!-- LLM -->
  <rect x="570" y="322" width="170" height="86" rx="10" fill="#22201C"/>
  <text x="655" y="348" text-anchor="middle" font-size="14" font-weight="700" fill="#F4EFE6">⑤ LLM 撰稿</text>
  <text x="655" y="371" text-anchor="middle" font-size="12" fill="#B8B0A0">问题 + 两路资料</text>
  <text x="655" y="391" text-anchor="middle" font-size="12" fill="#B8B0A0">只准照资料答</text>
  <!-- 答案 -->
  <rect x="330" y="470" width="410" height="70" rx="10" fill="#F2F5F1" stroke="#3D5A45" stroke-width="2"/>
  <text x="535" y="498" text-anchor="middle" font-size="14" font-weight="700" fill="#3D5A45">⑥ 答案 + 出处 +（可选）推理路径</text>
  <text x="535" y="522" text-anchor="middle" font-size="12" fill="#5C564C">「深圳。依据：李四→腾讯→总部位于→深圳」</text>
  <!-- 问答箭头 -->
  <line x1="260" y1="365" x2="328" y2="365" stroke="#5C564C" stroke-width="2" marker-end="url(#ar5)"/>
  <line x1="500" y1="365" x2="568" y2="365" stroke="#5C564C" stroke-width="2" marker-end="url(#ar5)"/>
  <path d="M 655 408 Q 655 450 600 470" fill="none" stroke="#5C564C" stroke-width="2" marker-end="url(#ar5)"/>
  <!-- 库到检索 -->
  <path d="M 550 218 Q 470 280 428 320" fill="none" stroke="#C24A20" stroke-width="2" marker-end="url(#ar5)"/>
  <path d="M 750 218 Q 660 285 480 320" fill="none" stroke="#3D5A45" stroke-width="2" marker-end="url(#ar5)"/>
  <text x="645" y="302" font-size="12" fill="#3D5A45">图谱一路 ↓</text>
  <text x="496" y="296" font-size="12" fill="#C24A20">向量一路 ↓</text>
</svg>
<div class="figcap">图 36｜知识引擎全景：四个概念拼成一个系统（附录A）</div>
</div>
```

看着复杂，其实每一段你都已经认识了：**本体**是顶上的规则手册；**知识库**是上半部从解析到索引的整套仓库设施；**向量库和知识图谱**是两种并排的索引；**RAG** 是下半部的取用流程；LLM 只是最后负责组织语言的那位「撰稿人」。

## 08｜实战对号：这些概念在 Jonex 里的位置

拿一个真实开源项目 Jonex 检验一下理解——每个概念都能在它身上找到对应零件。

| 概念 | Jonex 里的对应物 | 用的现成组件 |
| --- | --- | --- |
| 知识库 | 整个平台（21 个容器的系统） | 容器化部署（Docker）+ PostgreSQL + MinIO |
| 多模态解析 | 入库流水线 Stage 1–2 | MinerU（文档）、Whisper（音频；视频可切云端转写） |
| 向量索引 | Stage 3：切块 + Embedding | LightRAG（开源检索引擎）+ Milvus |
| 知识图谱 | Stage 3–4：图谱抽取 + 本体 ABox | LightRAG 图谱 + Neo4j |
| 本体（TBox） | 按领域选用的 YAML 配置（default.yaml 等） | 自研（轻量方案） |
| 本体（ABox） | Stage 4 抽出的实体关系，写入 Neo4j | 自研抽取流程 + Neo4j |
| RAG | 检索服务 + 引用溯源 | LightRAG 混合检索 |
| LLM | 外接模型（平台本身不含） | 任何 OpenAI 兼容 API |

:::提示
**看懂了这张表，你就看懂了任何一个知识引擎。**下次遇到新项目（RAGFlow、KAG、Dify……），先找它的「解析 → 索引 → 检索 → 生成」四段各用什么实现，五分钟就能摸清骨架。顺带一提：这座档案馆最终要变成 Agent 随手可调的服务——Jonex 自带一个 MCP 服务器容器（MCP：让 AI 助手以标准方式调用外部工具的协议），还有个配套的轻量本体建模小工具 Nexonto；那是另一篇的故事。
:::

## 09｜收尾心法：三问定位法＋延伸阅读

以后再遇到号称「本体驱动」「知识引擎」的项目，问三个问题就能给它验明正身。

**第一问：TBox 用什么写？**

YAML/JSON（务实派，十分钟上手，无推理）、OWL/RDF（学院派，支持继承和逻辑推理），还是自研 schema 加内置推理（第三条路）。Jonex 是第一条；KAG 走第三条（自研 SPG，自带推理）；TrustGraph 支持导入标准 OWL。

**第二问：ABox 存在哪、怎么进来？**

存 Neo4j 这类图数据库，还是和文档混在一起？事实靠 LLM 自动抽取，还是人工录入？抽取错了有没有重试和校正机制？

**第三问：有没有推理引擎？**

能不能从已有事实**推出**新事实（爸爸的爸爸=爷爷）？没有的话，「本体驱动」多半只是「用 schema 约束了一下抽取」——像 Jonex。

### 毕业自测

**合上本篇，你能答出这五题吗？**① RAG 治 LLM 的哪两个毛病？② 向量检索与图谱检索各擅长什么、各怕什么？③ TBox 和 ABox，谁是表结构、谁是数据行？④ 为什么换 Embedding 模型必须重建索引？⑤ 用「三问定位法」给 Jonex 验一次正身。

### 延伸阅读

| 想深入… | 去看 | 为什么 |
| --- | --- | --- |
| 本体工程理论 | **OpenSPG / KAG**（蚂蚁集团） | 有完整的 SPG 建模理论和中文文档 |
| 标准本体语言 | W3C 的 **OWL / RDF / SHACL** 规范 | 语义网标准家族：OWL 写本体、RDF 定数据格式、SHACL 做校验 |
| 检索原理 | **LightRAG**（港大）、微软 **GraphRAG** | 图谱增强检索（GraphRAG）的两个标杆实现 |
| 产品化样本 | **Jonex**（本篇主角之一） | 看本体如何被「工程化落地」成产品 |
| 产业实践 | **Palantir** Foundry 的本体与 AIP | 「本体即操作层」的最激进实践；AIP 是其 AI 平台（空客、SOMPO 案例） |

最后回到那张档案馆的图。知识在变、工具在变、模型在变，但四个角色的分工一直没变：**有人建仓库，有人定规则，有人织关系网，有人跑腿取料。**你现在认得它们了。

本篇原为独立成篇的《一篇搞懂：RAG · 知识库 · 知识图谱 · 本体论》（知识工程图解），收入本书时按附录体例改排，文字与图示保留原貌。
