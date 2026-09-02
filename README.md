# 中国命理学 · Manim 讲解视频

用 [Manim Community](https://www.manim.community/) 制作的中文科普动画系列，
配音由 [manim-voiceover](https://voiceover.manim.community/) + gTTS 生成。
输出 1920×1080 / 30fps，含中文旁白音轨与 `.srt` 字幕。

## 两集内容

### 第一集：`chinese_numerology.py` → `ChineseNumerology`（约 4 分 07 秒）

基本框架。

| 章节 | 主题 | 动画 |
| --- | --- | --- |
| 片头 | 中国命理学总览 | 标题、印章 |
| 一 | 阴阳 | 太极图绘制与旋转、对立统一举例 |
| 二 | 五行 | 五行环，相生（顺时针弧线箭头）、相克（五角星连线） |
| 三 | 天干地支 | 十天干 / 十二地支按五行着色，六十甲子 |
| 四 | 十二生肖 | 地支—生肖对应环 |
| 五 | 四柱八字 | 年月日时四柱，八字与五行分布 |
| 结语 | 理性看待 | 说明八字并无科学依据 |

### 第二集：`numerology_classics.py` → `NumerologyClassics`（约 6 分）

典籍源流与术语。

| 章节 | 主题 | 动画 |
| --- | --- | --- |
| 片头 | 命理古籍与名词 | 标题 |
| 一 | 源头《易经》 | 阴阳爻 → 八卦（线条绘制）→ 六十四卦 |
| 二上 | 典籍源流（先秦—唐—宋） | 时间轴 + 古籍卡片，三柱到四柱的演变 |
| 二下 | 典籍源流（明—清） | 六部要籍卡片阵列 |
| 三 | 日主与十神 | 以日主为中心的五类生克关系表 + 阴阳分野 |
| 四 | 旺衰与用神 | 身弱—中和—身强刻度尺，用神 / 忌神 |
| 五 | 大运与流年 | 十年一步的大运区块 + 流年刻度 |
| 六 | 刑冲合害 | 地支环上的六冲直径与三合三角 |
| 七 | 神煞 | 天乙贵人、桃花、驿马、华盖 |
| 结语 | 理性看待 | 强调是符号系统而非科学结论 |

涉及的古籍：《易经》《李虚中命书》《渊海子平》《三命通会》《神峰通考》
《子平真诠》《滴天髓阐微》《穷通宝鉴》《紫微斗数全书》。

## 文件结构

- `numerology_common.py` —— 两集共用的字体、配色、五行/干支常量与文字工具
- `chinese_numerology.py` —— 第一集场景
- `numerology_classics.py` —— 第二集场景

## 环境准备

系统依赖（Debian / Ubuntu）：

```bash
sudo apt-get install -y ffmpeg sox libcairo2-dev libpango1.0-dev pkg-config fonts-noto-cjk
```

Python 依赖：

```bash
python3 -m venv venv && . venv/bin/activate
pip install -r requirements.txt
```

字体使用 `Noto Serif CJK SC` 与 `Noto Sans CJK SC`，由 `fonts-noto-cjk` 提供。

## 渲染

```bash
# 快速预览（480p15）
manim -ql chinese_numerology.py ChineseNumerology
manim -ql numerology_classics.py NumerologyClassics

# 成片（1080p30）
manim -r 1920,1080 --fps 30 chinese_numerology.py ChineseNumerology
manim -r 1920,1080 --fps 30 numerology_classics.py NumerologyClassics
```

输出位于 `media/videos/<脚本名>/1080p30/`，同时生成同名 `.srt` 字幕。

gTTS 需要联网合成语音；首次渲染后音频会缓存在 `media/voiceovers/`，
之后重复渲染不再请求网络。

## 说明

视频中的命理内容按传统说法与文献记载介绍，仅作文化科普；
两集结语都已明确指出八字并无科学依据。
部分古籍的作者归属（如《滴天髓》托名刘基、《紫微斗数全书》旧题陈抟传）
按传统说法标注为「旧题」「传」，并非确证。
