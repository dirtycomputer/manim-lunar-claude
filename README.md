# 中国命理学 · Manim 讲解视频

用 [Manim Community](https://www.manim.community/) 制作的中文科普动画，
配音由 [manim-voiceover](https://voiceover.manim.community/) + gTTS 生成。

成片时长约 4 分钟，1920×1080 / 30fps，含中文旁白音轨。

## 内容结构

| 章节 | 主题 | 动画 |
| --- | --- | --- |
| 片头 | 中国命理学总览 | 标题、印章 |
| 一 | 阴阳 | 太极图绘制与旋转、对立统一举例 |
| 二 | 五行 | 五行环，相生（顺时针弧线箭头）、相克（五角星连线） |
| 三 | 天干地支 | 十天干 / 十二地支按五行着色，六十甲子 |
| 四 | 十二生肖 | 地支—生肖对应环 |
| 五 | 四柱八字 | 年月日时四柱，八字与五行分布 |
| 结语 | 理性看待 | 说明八字并无科学依据 |

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

# 成片（1080p30）
manim -r 1920,1080 --fps 30 chinese_numerology.py ChineseNumerology
```

输出位于 `media/videos/chinese_numerology/1080p30/ChineseNumerology.mp4`，
同时会生成字幕文件 `ChineseNumerology.srt`。

gTTS 需要联网合成语音；首次渲染后音频会缓存在 `media/voiceovers/`，
之后重复渲染不再请求网络。

## 说明

视频中的命理内容按传统说法介绍，仅作文化科普；结语中已明确指出八字并无科学依据。
