"""中国命理学系列视频的共用样式与工具。"""

from manim import *

# ---------------------------------------------------------------- 字体与配色

CN = "Noto Serif CJK SC"          # 正文中文字体
CN_BOLD = "Noto Sans CJK SC"      # 标题中文字体

INK = "#0B0E14"                   # 背景（墨色）
PAPER = "#EDE4D3"                 # 前景（宣纸色）
SEAL = "#C0392B"                  # 印章红
GOLD = "#D4AF37"

config.background_color = INK

# 五行配色
WUXING = {
    "木": "#4CAF50",
    "火": "#E5533D",
    "土": "#C89B4A",
    "金": "#D9D4C5",
    "水": "#4A90D9",
}

# 天干 / 地支 的五行归属
GAN_WUXING = {
    "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
    "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水",
}
ZHI_WUXING = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土", "巳": "火",
    "午": "火", "未": "土", "申": "金", "酉": "金", "戌": "土", "亥": "水",
}

TIANGAN = list("甲乙丙丁戊己庚辛壬癸")
DIZHI = list("子丑寅卯辰巳午未申酉戌亥")
SHENGXIAO = list("鼠牛虎兔龙蛇马羊猴鸡狗猪")


def cn(text, size=36, color=PAPER, font=CN, weight=NORMAL):
    """快捷创建中文 Text。"""
    return Text(text, font=font, font_size=size, color=color, weight=weight)


def section_title(text):
    """章节标题（带下划线）。"""
    t = cn(text, size=44, color=GOLD, font=CN_BOLD, weight=BOLD).to_edge(UP, buff=0.5)
    line = Line(LEFT, RIGHT, color=GOLD, stroke_width=2).set_width(t.width + 0.8)
    line.next_to(t, DOWN, buff=0.18).set_opacity(0.6)
    return VGroup(t, line)
