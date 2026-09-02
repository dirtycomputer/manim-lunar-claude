"""中国命理学讲解视频 —— 使用 Manim + manim-voiceover 制作。

渲染：
    manim -qh chinese_numerology.py ChineseNumerology
"""

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

from numerology_common import (
    CN, CN_BOLD, INK, PAPER, SEAL, GOLD,
    WUXING, GAN_WUXING, ZHI_WUXING,
    TIANGAN, DIZHI, SHENGXIAO,
    cn, section_title,
)


def taiji(radius=1.7):
    """构造一个太极图。"""
    r = radius
    yang = Sector(radius=r, angle=PI, start_angle=-PI / 2)      # 右半 —— 阳（白）
    yang.set_fill(PAPER, 1).set_stroke(width=0)
    yin = Sector(radius=r, angle=PI, start_angle=PI / 2)        # 左半 —— 阴（黑）
    yin.set_fill("#15181F", 1).set_stroke(width=0)

    top = Circle(radius=r / 2).move_to(UP * r / 2)
    top.set_fill("#15181F", 1).set_stroke(width=0)
    bottom = Circle(radius=r / 2).move_to(DOWN * r / 2)
    bottom.set_fill(PAPER, 1).set_stroke(width=0)

    dot_top = Circle(radius=r / 8).move_to(UP * r / 2).set_fill(PAPER, 1).set_stroke(width=0)
    dot_bottom = Circle(radius=r / 8).move_to(DOWN * r / 2).set_fill("#15181F", 1).set_stroke(width=0)

    rim = Circle(radius=r, color=GOLD, stroke_width=3)
    return VGroup(yang, yin, top, bottom, dot_top, dot_bottom, rim)


def wuxing_node(name, radius=0.46):
    """五行节点：带色环的圆 + 文字。"""
    c = WUXING[name]
    circ = Circle(radius=radius, color=c, stroke_width=4).set_fill(c, 0.16)
    label = cn(name, size=34, color=c, font=CN_BOLD, weight=BOLD).move_to(circ)
    return VGroup(circ, label)


class ChineseNumerology(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="zh-CN", tld="com"))

        self.scene_intro()
        self.scene_yinyang()
        self.scene_wuxing()
        self.scene_ganzhi()
        self.scene_shengxiao()
        self.scene_bazi()
        self.scene_outro()

    # ------------------------------------------------------------ 工具

    def hold(self, tracker):
        """配音尚未结束时留白等待。"""
        rest = tracker.get_remaining_duration()
        if rest > 0:
            self.wait(rest)

    def clear_all(self, run_time=0.8):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=run_time)

    # ------------------------------------------------------------ 片头

    def scene_intro(self):
        title = cn("中国命理学", size=88, color=PAPER, font=CN_BOLD, weight=BOLD)
        subtitle = cn("阴阳 · 五行 · 干支 · 八字", size=34, color=GOLD)
        subtitle.next_to(title, DOWN, buff=0.55)

        rule_top = Line(LEFT * 3.2, RIGHT * 3.2, color=GOLD, stroke_width=2)
        rule_top.next_to(title, UP, buff=0.55).set_opacity(0.7)
        rule_bot = rule_top.copy().next_to(subtitle, DOWN, buff=0.5)

        seal = Square(side_length=0.9, color=SEAL, stroke_width=4).set_fill(SEAL, 0.9)
        seal_txt = cn("命", size=40, color=PAPER, font=CN_BOLD, weight=BOLD).move_to(seal)
        seal_grp = VGroup(seal, seal_txt).to_corner(DR, buff=0.9)

        with self.voiceover(
            text="中国命理学，是中国传统文化中，用来推演人生规律的一套符号系统。"
                 "它以阴阳五行为根基，用天干地支记录时间，再由此推断一个人的性格与运势走向。"
        ) as t:
            self.play(Write(title), run_time=2.2)
            self.play(
                Create(rule_top), Create(rule_bot),
                FadeIn(subtitle, shift=UP * 0.3),
                run_time=1.6,
            )
            self.play(FadeIn(seal_grp, scale=0.7), run_time=1.0)
            self.hold(t)

        self.clear_all()

    # ------------------------------------------------------------ 阴阳

    def scene_yinyang(self):
        head = section_title("一、阴阳")
        tj = taiji().shift(DOWN * 0.4)

        with self.voiceover(text="一切的起点，是阴阳。") as t:
            self.play(FadeIn(head, shift=DOWN * 0.2), run_time=1.0)
            self.play(GrowFromCenter(tj), run_time=1.6)
            self.hold(t)

        pairs = VGroup(
            cn("白昼  —  黑夜", size=30),
            cn("炎热  —  寒冷", size=30),
            cn("运动  —  静止", size=30),
        ).arrange(DOWN, buff=0.42).to_edge(RIGHT, buff=1.0).shift(DOWN * 0.3)

        with self.voiceover(
            text="古人观察到，世间万物都存在着相互对立、又彼此依存的两面："
                 "白天与黑夜，炎热与寒冷，运动与静止。"
        ) as t:
            self.play(tj.animate.shift(LEFT * 3.0).scale(0.92), run_time=1.2)
            for p in pairs:
                self.play(FadeIn(p, shift=LEFT * 0.4), run_time=0.7)
            self.hold(t)

        lab_yang = cn("阳", size=32, color=GOLD).next_to(tj, UP, buff=0.25).shift(RIGHT * 0.8)
        lab_yin = cn("阴", size=32, color="#7FA8D9").next_to(tj, DOWN, buff=0.25).shift(LEFT * 0.8)
        note = cn("阳中有阴，阴中有阳", size=32, color=GOLD)
        note.next_to(pairs, DOWN, buff=0.7)

        with self.voiceover(
            text="阳中有阴，阴中有阳。二者此消彼长，永不静止。这就是太极图所描绘的世界观。"
        ) as t:
            self.play(FadeIn(lab_yang), FadeIn(lab_yin), run_time=0.8)
            self.play(Write(note), run_time=1.2)
            self.play(Rotate(tj, angle=TAU, about_point=tj.get_center()), run_time=4.0, rate_func=linear)
            self.hold(t)

        self.clear_all()

    # ------------------------------------------------------------ 五行

    def scene_wuxing(self):
        head = section_title("二、五行")

        names = ["木", "火", "土", "金", "水"]
        R = 2.1
        center = DOWN * 0.15
        pts = [center + R * np.array([np.cos(PI / 2 - i * TAU / 5),
                                      np.sin(PI / 2 - i * TAU / 5), 0]) for i in range(5)]
        nodes = VGroup(*[wuxing_node(n).move_to(p) for n, p in zip(names, pts)])

        with self.voiceover(
            text="在阴阳之下，古人进一步把万物归纳为五种基本属性，称为五行："
                 "木、火、土、金、水。"
        ) as t:
            self.play(FadeIn(head, shift=DOWN * 0.2), run_time=0.9)
            for n in nodes:
                self.play(GrowFromCenter(n), run_time=0.55)
            self.hold(t)

        # 相生：沿圆周顺时针
        sheng_arrows = VGroup()
        for i in range(5):
            a = nodes[i][0].get_center()
            b = nodes[(i + 1) % 5][0].get_center()
            d = normalize(b - a)
            arr = CurvedArrow(
                a + d * 0.55, b - d * 0.55,
                angle=-TAU / 10, color=WUXING[names[i]],
                stroke_width=4, tip_length=0.22,
            )
            sheng_arrows.add(arr)

        sheng_lbl = cn("相生：木生火 → 火生土 → 土生金 → 金生水 → 水生木", size=28, color=PAPER)
        sheng_lbl.to_edge(DOWN, buff=0.45)

        with self.voiceover(
            text="五行之间首先是相生：木生火，火生土，土生金，金生水，水又生木。循环往复，生生不息。"
        ) as t:
            self.play(FadeIn(sheng_lbl), run_time=0.7)
            for arr in sheng_arrows:
                self.play(Create(arr), run_time=0.62)
            self.play(Indicate(sheng_lbl, color=GOLD, scale_factor=1.06), run_time=1.0)
            self.hold(t)

        # 相克：五角星连线
        self.play(FadeOut(sheng_arrows), FadeOut(sheng_lbl), run_time=0.7)
        ke_pairs = [(0, 2), (1, 3), (2, 4), (3, 0), (4, 1)]
        ke_arrows = VGroup()
        for i, j in ke_pairs:
            arr = Arrow(
                nodes[i][0].get_center(), nodes[j][0].get_center(),
                buff=0.5, color=SEAL, stroke_width=3.5,
                max_tip_length_to_length_ratio=0.08,
            )
            ke_arrows.add(arr)

        ke_lbl = cn("相克：木克土  土克水  水克火  火克金  金克木", size=28, color=SEAL)
        ke_lbl.to_edge(DOWN, buff=0.45)
        balance = cn("相生使万物生长，相克使系统平衡", size=30, color=GOLD)
        balance.next_to(ke_lbl, UP, buff=0.28)

        with self.voiceover(
            text="同时还有相克：木克土，土克水，水克火，火克金，金克木。"
                 "相生使万物生长，相克使系统保持平衡。"
        ) as t:
            self.play(FadeIn(ke_lbl), run_time=0.6)
            for arr in ke_arrows:
                self.play(Create(arr), run_time=0.5)
            self.play(FadeIn(balance, shift=UP * 0.2), run_time=1.0)
            self.hold(t)

        self.clear_all()

    # ------------------------------------------------------------ 天干地支

    def scene_ganzhi(self):
        head = section_title("三、天干地支")

        gan_lbl = cn("十天干", size=30, color=GOLD)
        gan = VGroup(*[
            cn(g, size=40, color=WUXING[GAN_WUXING[g]], font=CN_BOLD, weight=BOLD)
            for g in TIANGAN
        ]).arrange(RIGHT, buff=0.52)
        gan_row = VGroup(gan_lbl, gan).arrange(RIGHT, buff=0.7).shift(UP * 1.1)

        zhi_lbl = cn("十二地支", size=30, color=GOLD)
        zhi = VGroup(*[
            cn(z, size=40, color=WUXING[ZHI_WUXING[z]], font=CN_BOLD, weight=BOLD)
            for z in DIZHI
        ]).arrange(RIGHT, buff=0.42)
        zhi_row = VGroup(zhi_lbl, zhi).arrange(RIGHT, buff=0.7).shift(DOWN * 0.45)
        VGroup(gan_row, zhi_row).move_to(UP * 0.55).scale(0.95)

        with self.voiceover(
            text="有了五行，还需要一套记录时间的坐标，这就是天干地支。"
        ) as t:
            self.play(FadeIn(head, shift=DOWN * 0.2), run_time=0.9)
            self.hold(t)

        with self.voiceover(
            text="十天干：甲、乙、丙、丁、戊、己、庚、辛、壬、癸。每两个天干对应一种五行。"
        ) as t:
            self.play(FadeIn(gan_lbl), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(g, shift=DOWN * 0.25) for g in gan], lag_ratio=0.22), run_time=3.0)
            self.hold(t)

        with self.voiceover(
            text="十二地支：子、丑、寅、卯、辰、巳、午、未、申、酉、戌、亥。"
        ) as t:
            self.play(FadeIn(zhi_lbl), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(z, shift=DOWN * 0.25) for z in zhi], lag_ratio=0.2), run_time=3.2)
            self.hold(t)

        # 干支相配 → 六十甲子
        combo = VGroup(*[
            cn(TIANGAN[i % 10] + DIZHI[i % 12], size=32, color=PAPER)
            for i in range(6)
        ]).arrange(RIGHT, buff=0.55).shift(DOWN * 2.0 + LEFT * 0.55)
        dots = cn("……", size=32, color=PAPER).next_to(combo, RIGHT, buff=0.4)
        cycle = cn("六十甲子  ——  六十年一轮回", size=34, color=GOLD)
        cycle.shift(DOWN * 3.0)

        with self.voiceover(
            text="天干与地支依次相配，阳干配阳支，阴干配阴支，共可组成六十种搭配，"
                 "称为六十甲子。六十年，正好是一个完整的轮回。"
        ) as t:
            self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in combo], lag_ratio=0.3), run_time=2.4)
            self.play(FadeIn(dots), run_time=0.5)
            self.play(Write(cycle), run_time=1.6)
            self.hold(t)

        self.clear_all()

    # ------------------------------------------------------------ 十二生肖

    def scene_shengxiao(self):
        head = section_title("四、十二生肖")

        R = 2.3
        center = UP * 0.05
        ring = Circle(radius=R, color=GOLD, stroke_width=2).move_to(center)
        ring.set_stroke(GOLD, 2, opacity=0.45).set_fill(opacity=0)

        items = VGroup()
        for i, (z, s) in enumerate(zip(DIZHI, SHENGXIAO)):
            ang = PI / 2 - i * TAU / 12
            pos = center + R * np.array([np.cos(ang), np.sin(ang), 0])
            zt = cn(z, size=30, color=WUXING[ZHI_WUXING[z]], font=CN_BOLD, weight=BOLD)
            st = cn(s, size=24, color=PAPER)
            grp = VGroup(zt, st).arrange(DOWN, buff=0.08).move_to(pos)
            items.add(grp)

        with self.voiceover(
            text="十二地支，又各自对应着一种生肖："
                 "鼠、牛、虎、兔、龙、蛇、马、羊、猴、鸡、狗、猪。"
        ) as t:
            self.play(FadeIn(head, shift=DOWN * 0.2), run_time=0.8)
            self.play(Create(ring), run_time=1.2)
            self.play(LaggedStart(*[FadeIn(g, scale=0.6) for g in items], lag_ratio=0.25), run_time=4.2)
            self.hold(t)

        note = VGroup(
            cn("出生那年的地支", size=28, color=GOLD),
            cn("就是你的属相", size=28, color=GOLD),
        ).arrange(DOWN, buff=0.18).move_to(center)
        with self.voiceover(text="你所熟悉的属相，正是来源于出生那一年的地支。") as t:
            self.play(Write(note), run_time=1.8)
            self.play(Indicate(items[2], color=GOLD, scale_factor=1.35), run_time=1.2)
            self.hold(t)

        self.clear_all()

    # ------------------------------------------------------------ 四柱八字

    def scene_bazi(self):
        head = section_title("五、四柱八字")

        pillars = [("年柱", "甲", "子"), ("月柱", "丙", "寅"),
                   ("日柱", "戊", "辰"), ("时柱", "庚", "申")]

        cols = VGroup()
        for name, g, z in pillars:
            title = cn(name, size=28, color=GOLD)
            box = RoundedRectangle(width=1.9, height=2.5, corner_radius=0.12,
                                   color=GOLD, stroke_width=2)
            box.set_stroke(GOLD, 2, opacity=0.55).set_fill(GOLD, 0.045)
            gt = cn(g, size=58, color=WUXING[GAN_WUXING[g]], font=CN_BOLD, weight=BOLD)
            zt = cn(z, size=58, color=WUXING[ZHI_WUXING[z]], font=CN_BOLD, weight=BOLD)
            chars = VGroup(gt, zt).arrange(DOWN, buff=0.42).move_to(box)
            col = VGroup(title, VGroup(box, chars)).arrange(DOWN, buff=0.28)
            cols.add(col)
        cols.arrange(RIGHT, buff=0.55).shift(DOWN * 0.35)

        with self.voiceover(text="命理学中最常见的方法，是四柱八字。") as t:
            self.play(FadeIn(head, shift=DOWN * 0.2), run_time=0.9)
            self.hold(t)

        with self.voiceover(
            text="把一个人出生的年、月、日、时，各用一组干支来表示，就得到四根柱子，称为四柱。"
                 "四柱一共八个字，所以又叫八字。"
        ) as t:
            for c in cols:
                self.play(FadeIn(c, shift=UP * 0.3), run_time=0.85)
            self.hold(t)

        brace = Brace(cols, DOWN, color=GOLD)
        brace_txt = cn("八个字 —— 八字", size=32, color=GOLD).next_to(brace, DOWN, buff=0.2)

        with self.voiceover(
            text="例如某人生于甲子年、丙寅月、戊辰日、庚申时。"
        ) as t:
            self.play(GrowFromCenter(brace), FadeIn(brace_txt), run_time=1.2)
            self.hold(t)

        with self.voiceover(
            text="命理师会分析这八个字当中，五行的强弱与生克关系，"
                 "据此描述一个人的性格倾向与人生格局。"
        ) as t:
            tally = VGroup(*[
                cn(f"{k} {v}", size=27, color=WUXING[k])
                for k, v in [("木", 2), ("火", 1), ("土", 2), ("金", 2), ("水", 1)]
            ]).arrange(RIGHT, buff=0.55)
            tally_lbl = cn("五行分布", size=27, color=PAPER)
            tally_row = VGroup(tally_lbl, tally).arrange(RIGHT, buff=0.5)
            tally_row.next_to(brace_txt, DOWN, buff=0.3)

            self.play(FadeOut(brace), FadeOut(brace_txt), run_time=0.5)
            tally_row.next_to(cols, DOWN, buff=0.45)
            self.play(FadeIn(tally_row, shift=UP * 0.2), run_time=1.2)
            self.play(LaggedStart(*[Indicate(x, scale_factor=1.2) for x in tally], lag_ratio=0.3), run_time=2.2)
            self.hold(t)

        self.clear_all()

    # ------------------------------------------------------------ 结语

    def scene_outro(self):
        head = section_title("结语")

        l1 = cn("八字并没有科学依据", size=38, color=SEAL)
        l2 = cn("它是古人理解世界的一套模型", size=34, color=PAPER)
        l3 = cn("万物相互关联，动态平衡", size=34, color=GOLD)
        lines = VGroup(l1, l2, l3).arrange(DOWN, buff=0.55).shift(UP * 0.2)

        with self.voiceover(
            text="需要说明的是，八字并没有科学依据。它更像是古人用来理解世界的一套模型，"
                 "反映的是中国传统的哲学思维——万物相互关联，动态平衡。"
        ) as t:
            self.play(FadeIn(head, shift=DOWN * 0.2), run_time=0.8)
            self.play(Write(l1), run_time=1.6)
            self.play(FadeIn(l2, shift=UP * 0.2), run_time=1.2)
            self.play(FadeIn(l3, shift=UP * 0.2), run_time=1.2)
            self.hold(t)

        final = cn("命由己造", size=76, color=GOLD, font=CN_BOLD, weight=BOLD)
        sub = cn("了解传统，是了解文化的一扇窗", size=30, color=PAPER)
        sub.next_to(final, DOWN, buff=0.5)

        with self.voiceover(
            text="了解它，是了解中国文化的一扇窗口。至于人生，终究还是掌握在自己手中。"
        ) as t:
            self.play(FadeOut(lines), FadeOut(head), run_time=0.8)
            self.play(Write(final), run_time=2.0)
            self.play(FadeIn(sub, shift=UP * 0.2), run_time=1.2)
            self.hold(t)

        self.wait(1.2)
