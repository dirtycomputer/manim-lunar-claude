"""中国命理学：古籍与名词 —— 使用 Manim + manim-voiceover 制作。

渲染：
    manim -r 1920,1080 --fps 30 numerology_classics.py NumerologyClassics
"""

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

from numerology_common import (
    CN, CN_BOLD, INK, PAPER, SEAL, GOLD,
    WUXING, ZHI_WUXING, DIZHI,
    cn, section_title,
)

# ---------------------------------------------------------------- 图形工具


def yao(is_yang, w=1.05, sw=8, color=PAPER):
    """一爻：阳爻为实线，阴爻为断线。"""
    if is_yang:
        return Line(LEFT * w / 2, RIGHT * w / 2, stroke_width=sw, color=color)
    gap = w * 0.26
    return VGroup(
        Line(LEFT * w / 2, LEFT * gap / 2, stroke_width=sw, color=color),
        Line(RIGHT * gap / 2, RIGHT * w / 2, stroke_width=sw, color=color),
    )


def gua(bits, w=1.05, sw=8, buff=0.15, color=PAPER):
    """由若干爻叠成的卦；bits 自下而上，True 为阳。"""
    return VGroup(*[yao(b, w, sw, color) for b in reversed(bits)]).arrange(DOWN, buff=buff)


def book_card(title, meta, width=3.1, height=1.25, accent=GOLD):
    """一张古籍卡片。"""
    box = RoundedRectangle(width=width, height=height, corner_radius=0.1,
                           color=accent, stroke_width=2)
    box.set_stroke(accent, 2, opacity=0.65).set_fill(accent, 0.05)
    t = cn(f"《{title}》", size=27, color=PAPER)
    m = cn(meta, size=19, color=accent)
    text = VGroup(t, m).arrange(DOWN, buff=0.16).move_to(box)
    return VGroup(box, text)


# 八卦：自下而上的爻，配自然象
BAGUA = [
    ("乾", (1, 1, 1), "天"), ("兑", (1, 1, 0), "泽"),
    ("离", (1, 0, 1), "火"), ("震", (1, 0, 0), "雷"),
    ("巽", (0, 1, 1), "风"), ("坎", (0, 1, 0), "水"),
    ("艮", (0, 0, 1), "山"), ("坤", (0, 0, 0), "地"),
]


class NumerologyClassics(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="zh-CN", tld="com"))

        self.scene_intro()
        self.scene_yijing()
        self.scene_lineage_early()
        self.scene_lineage_late()
        self.scene_shishen()
        self.scene_yongshen()
        self.scene_dayun()
        self.scene_dizhi_relations()
        self.scene_shensha()
        self.scene_outro()

    # ------------------------------------------------------------ 工具

    def hold(self, tracker):
        rest = tracker.get_remaining_duration()
        if rest > 0:
            self.wait(rest)

    def clear_all(self, run_time=0.8):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=run_time)

    # ------------------------------------------------------------ 片头

    def scene_intro(self):
        title = cn("命理古籍与名词", size=80, color=PAPER, font=CN_BOLD, weight=BOLD)
        subtitle = cn("典籍源流 · 术语释义", size=34, color=GOLD)
        subtitle.next_to(title, DOWN, buff=0.55)
        rule_top = Line(LEFT * 3.6, RIGHT * 3.6, color=GOLD, stroke_width=2)
        rule_top.next_to(title, UP, buff=0.55).set_opacity(0.7)
        rule_bot = rule_top.copy().next_to(subtitle, DOWN, buff=0.5)

        with self.voiceover(
            text="上一集，我们讲了命理学的基本框架。这一集，来看看它的典籍源流，"
                 "以及那些常被提起、却未必说得清的术语。"
        ) as t:
            self.play(Write(title), run_time=2.2)
            self.play(Create(rule_top), Create(rule_bot),
                      FadeIn(subtitle, shift=UP * 0.3), run_time=1.6)
            self.hold(t)

        self.clear_all()

    # ------------------------------------------------------------ 易经

    def scene_yijing(self):
        head = section_title("一、源头：《易经》")

        yang = VGroup(yao(True), cn("阳爻", size=24, color=GOLD)).arrange(DOWN, buff=0.22)
        yin = VGroup(yao(False), cn("阴爻", size=24, color="#7FA8D9")).arrange(DOWN, buff=0.22)
        yaos = VGroup(yang, yin).arrange(RIGHT, buff=1.5).shift(UP * 0.7)

        with self.voiceover(
            text="一切命理典籍的源头，是《易经》。"
                 "它以阴爻和阳爻为最小的单位，一实一断，对应阴阳两种状态。"
        ) as t:
            self.play(FadeIn(head, shift=DOWN * 0.2), run_time=0.9)
            self.play(FadeIn(yang, shift=UP * 0.2), run_time=1.0)
            self.play(FadeIn(yin, shift=UP * 0.2), run_time=1.0)
            self.hold(t)

        # 三爻成卦 —— 八卦
        cards = VGroup()
        for name, bits, xiang in BAGUA:
            g = gua(bits, w=1.0, sw=9, buff=0.18)
            lbl = cn(f"{name} · {xiang}", size=23, color=GOLD)
            cards.add(VGroup(g, lbl).arrange(DOWN, buff=0.22))
        cards.arrange(RIGHT, buff=0.55).shift(DOWN * 0.5)

        with self.voiceover(
            text="三爻相叠，便构成八卦：乾为天，兑为泽，离为火，震为雷，"
                 "巽为风，坎为水，艮为山，坤为地。"
        ) as t:
            self.play(FadeOut(yaos), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.25) for c in cards],
                                  lag_ratio=0.28), run_time=4.4)
            self.hold(t)

        formula = cn("八卦相重  →  八 × 八 = 六十四卦", size=36, color=GOLD)
        formula.shift(DOWN * 2.55)
        note = cn("本为占筮之书，后世奉为群经之首", size=28, color=PAPER)
        note.shift(DOWN * 3.3)

        with self.voiceover(
            text="八卦两两相重，就得到六十四卦。《易经》本是一部占筮之书，"
                 "后来被奉为群经之首，也为后世的术数，提供了最基本的符号语言。"
        ) as t:
            self.play(cards.animate.scale(0.9).shift(UP * 0.4), run_time=0.9)
            self.play(Write(formula), run_time=1.8)
            self.play(FadeIn(note, shift=UP * 0.2), run_time=1.2)
            self.hold(t)

        self.clear_all()

    # ------------------------------------------------------------ 典籍：唐宋

    def scene_lineage_early(self):
        head = section_title("二、典籍源流（上）")

        axis = Arrow(LEFT * 6.2, RIGHT * 6.2, color=GOLD, stroke_width=3,
                     max_tip_length_to_length_ratio=0.03).shift(DOWN * 0.2)
        axis.set_opacity(0.75)

        marks = VGroup()
        for x, era in [(-4.6, "先秦"), (-0.6, "唐"), (3.4, "宋")]:
            tick = Line(UP * 0.16, DOWN * 0.16, color=GOLD, stroke_width=3)
            tick.move_to(axis.get_center() + RIGHT * x)
            lbl = cn(era, size=26, color=GOLD).next_to(tick, DOWN, buff=0.22)
            marks.add(VGroup(tick, lbl))

        with self.voiceover(text="命理学的成型，经历了漫长的演变。") as t:
            self.play(FadeIn(head, shift=DOWN * 0.2), run_time=0.8)
            self.play(GrowArrow(axis), run_time=1.2)
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.3), run_time=1.2)
            self.hold(t)

        c1 = book_card("易经", "先秦 · 群经之首").move_to(axis.get_center() + RIGHT * -4.6 + UP * 1.5)
        c2 = book_card("李虚中命书", "唐 · 李虚中注").move_to(axis.get_center() + RIGHT * -0.6 + UP * 1.5)
        c3 = book_card("渊海子平", "南宋 · 徐升 编").move_to(axis.get_center() + RIGHT * 3.4 + UP * 1.5)

        note2 = cn("年、月、日  三柱论命", size=25, color=PAPER)
        note2.move_to(axis.get_center() + RIGHT * -0.6 + DOWN * 1.3)
        note3 = cn("改以日干为主，四柱定型", size=25, color=PAPER)
        note3.move_to(axis.get_center() + RIGHT * 3.4 + DOWN * 2.2)

        with self.voiceover(
            text="唐代的李虚中，以年、月、日三柱推命，被视为子平术的先声。"
        ) as t:
            self.play(FadeIn(c1, shift=DOWN * 0.25), run_time=0.9)
            self.play(FadeIn(c2, shift=DOWN * 0.25), run_time=0.9)
            self.play(FadeIn(note2, shift=UP * 0.2), run_time=0.9)
            self.hold(t)

        with self.voiceover(
            text="到了宋代，徐子平改以日干为核心，四柱八字的格局就此确立。"
                 "后人编成《渊海子平》，是现存最早的系统性子平专著。"
        ) as t:
            self.play(FadeIn(c3, shift=DOWN * 0.25), run_time=0.9)
            self.play(FadeIn(note3, shift=UP * 0.2), run_time=0.9)
            self.play(Indicate(c3, color=GOLD, scale_factor=1.08), run_time=1.2)
            self.hold(t)

        self.clear_all()

    # ------------------------------------------------------------ 典籍：明清

    def scene_lineage_late(self):
        head = section_title("二、典籍源流（下）")

        books = [
            ("三命通会", "明 · 万民英", GOLD),
            ("神峰通考", "明 · 张楠", GOLD),
            ("子平真诠", "清 · 沈孝瞻 · 论格局", PAPER),
            ("滴天髓阐微", "清 · 任铁樵 增注 · 论中和", PAPER),
            ("穷通宝鉴", "原名《栏江网》· 论调候", PAPER),
            ("紫微斗数全书", "旧题陈抟传 · 星曜命盘", "#7FA8D9"),
        ]
        cards = VGroup(*[book_card(t, m, width=3.9, height=1.35, accent=a)
                         for t, m, a in books])
        cards.arrange_in_grid(rows=2, cols=3, buff=(0.5, 0.75)).shift(DOWN * 0.35)

        with self.voiceover(
            text="明代万民英编纂《三命通会》，汇集历代命理学说，后被收入《四库全书》；"
                 "同时期还有张楠的《神峰通考》。"
        ) as t:
            self.play(FadeIn(head, shift=DOWN * 0.2), run_time=0.8)
            self.play(FadeIn(cards[0], shift=UP * 0.3), run_time=1.1)
            self.play(FadeIn(cards[1], shift=UP * 0.3), run_time=1.1)
            self.hold(t)

        with self.voiceover(
            text="清代出现了两部影响深远的著作：沈孝瞻的《子平真诠》，专讲格局；"
                 "任铁樵增注的《滴天髓阐微》，则重气势与中和。"
                 "另有《穷通宝鉴》，原名《栏江网》，专论调候取用。"
        ) as t:
            for c in cards[2:5]:
                self.play(FadeIn(c, shift=UP * 0.3), run_time=1.0)
            self.hold(t)

        with self.voiceover(
            text="此外还有一条并行的路径：《紫微斗数全书》，旧题陈抟所传，"
                 "以星曜排布命盘，与八字并称。"
        ) as t:
            self.play(FadeIn(cards[5], shift=UP * 0.3), run_time=1.1)
            self.play(Indicate(cards[5], color="#7FA8D9", scale_factor=1.06), run_time=1.2)
            self.hold(t)

        self.clear_all()

    # ------------------------------------------------------------ 日主与十神

    def scene_shishen(self):
        head = section_title("三、日主与十神")

        hub = Circle(radius=0.52, color=GOLD, stroke_width=4).set_fill(GOLD, 0.12)
        hub_t = cn("日主", size=30, color=GOLD, font=CN_BOLD, weight=BOLD).move_to(hub)
        hub_g = VGroup(hub, hub_t).move_to(UP * 2.55)
        hub_note = cn("日柱天干 —— 代表命主本人", size=25, color=PAPER)
        hub_note.next_to(hub_g, RIGHT, buff=0.7)

        with self.voiceover(
            text="读古籍，先要过术语这一关。第一个关键词是日主，也叫日元，"
                 "指四柱中日柱的天干，代表命主本人。其余七个字，都是相对日主来看的。"
        ) as t:
            self.play(FadeIn(head, shift=DOWN * 0.2), run_time=0.8)
            self.play(GrowFromCenter(hub_g), run_time=1.1)
            self.play(FadeIn(hub_note, shift=LEFT * 0.3), run_time=1.1)
            self.hold(t)

        rows_data = [
            ("生我者", "印", "正印　偏印", WUXING["水"]),
            ("我生者", "食伤", "食神　伤官", WUXING["木"]),
            ("我克者", "财", "正财　偏财", WUXING["土"]),
            ("克我者", "官杀", "正官　七杀", WUXING["火"]),
            ("同我者", "比劫", "比肩　劫财", WUXING["金"]),
        ]
        ys = [1.45, 0.68, -0.09, -0.86, -1.63]
        rows = VGroup()
        for (rel, cat, pair, col), y in zip(rows_data, ys):
            a = cn(rel, size=27, color=PAPER).move_to([-4.6, y, 0])
            arr = Arrow(LEFT * 0.3, RIGHT * 0.3, color=col, stroke_width=3,
                        max_tip_length_to_length_ratio=0.35).move_to([-3.1, y, 0])
            b = cn(cat, size=30, color=col, font=CN_BOLD, weight=BOLD).move_to([-2.0, y, 0])
            c = cn(pair, size=28, color=col).move_to([1.2, y, 0])
            rows.add(VGroup(a, arr, b, c))

        with self.voiceover(
            text="以日主为中心，按五行的生克关系，就得到五类：生我者为印，我生者为食伤，"
                 "我克者为财，克我者为官杀，与我同类者为比劫。"
        ) as t:
            for r in rows:
                self.play(FadeIn(r, shift=RIGHT * 0.3), run_time=0.78)
            self.hold(t)

        rule = VGroup(
            cn("再分阴阳：阴阳相同者 —— 偏印 · 食神 · 偏财 · 七杀 · 比肩", size=25, color=GOLD),
            cn("阴阳相异者 —— 正印 · 伤官 · 正财 · 正官 · 劫财", size=25, color=GOLD),
        ).arrange(DOWN, buff=0.24).shift(DOWN * 2.75)

        with self.voiceover(
            text="每一类再按阴阳区分：阴阳相同的一个，与阴阳相异的一个。"
                 "五类各分为二，合起来正好十个，这就是十神。"
        ) as t:
            self.play(FadeIn(rule[0], shift=UP * 0.2), run_time=1.1)
            self.play(FadeIn(rule[1], shift=UP * 0.2), run_time=1.1)
            self.play(LaggedStart(*[Indicate(r[3], scale_factor=1.12) for r in rows],
                                  lag_ratio=0.25), run_time=2.4)
            self.hold(t)

        self.clear_all()

    # ------------------------------------------------------------ 旺衰与用神

    def scene_yongshen(self):
        head = section_title("四、旺衰与用神")

        bar = Line(LEFT * 4.6, RIGHT * 4.6, color=PAPER, stroke_width=4).shift(UP * 0.35)
        bar.set_opacity(0.5)
        left_l = cn("身弱", size=30, color=WUXING["水"]).next_to(bar.get_left(), DOWN, buff=0.35)
        mid_l = cn("中和", size=32, color=GOLD).next_to(bar.get_center(), DOWN, buff=0.35)
        right_l = cn("身强", size=30, color=WUXING["火"]).next_to(bar.get_right(), DOWN, buff=0.35)
        mid_tick = Line(UP * 0.22, DOWN * 0.22, color=GOLD, stroke_width=3).move_to(bar.get_center())

        pointer = Triangle(color=SEAL, fill_opacity=1).scale(0.19).rotate(PI)
        pointer.next_to(bar.get_center() + RIGHT * 3.1, UP, buff=0.08)

        with self.voiceover(
            text="有了十神，接下来要判断日主的旺衰，也就是身强还是身弱。"
        ) as t:
            self.play(FadeIn(head, shift=DOWN * 0.2), run_time=0.8)
            self.play(Create(bar), FadeIn(mid_tick), run_time=1.0)
            self.play(FadeIn(left_l), FadeIn(mid_l), FadeIn(right_l), run_time=0.9)
            self.play(FadeIn(pointer, shift=DOWN * 0.3), run_time=0.8)
            self.hold(t)

        with self.voiceover(
            text="命局讲求中和。太旺，就需要克制与宣泄；太弱，就需要生助与扶持。"
        ) as t:
            self.play(pointer.animate.shift(LEFT * 6.2), run_time=1.6)
            self.play(pointer.animate.shift(RIGHT * 3.1), run_time=1.6)
            self.play(Flash(mid_tick, color=GOLD, line_length=0.25), run_time=1.0)
            self.hold(t)

        good = VGroup(
            cn("用神", size=38, color=WUXING["木"], font=CN_BOLD, weight=BOLD),
            cn("使命局趋于平衡的五行", size=25, color=PAPER),
        ).arrange(DOWN, buff=0.2)
        bad = VGroup(
            cn("忌神", size=38, color=SEAL, font=CN_BOLD, weight=BOLD),
            cn("加剧失衡的五行", size=25, color=PAPER),
        ).arrange(DOWN, buff=0.2)
        pair = VGroup(good, bad).arrange(RIGHT, buff=2.6).shift(DOWN * 1.75)

        cite = cn("《滴天髓》论中和　·　《穷通宝鉴》论调候", size=27, color=GOLD)
        cite.shift(DOWN * 3.15)

        with self.voiceover(
            text="那个能让命局趋于平衡的五行，称为用神；反之，加剧失衡的，称为忌神。"
        ) as t:
            self.play(FadeIn(good, shift=UP * 0.25), run_time=1.1)
            self.play(FadeIn(bad, shift=UP * 0.25), run_time=1.1)
            self.hold(t)

        with self.voiceover(
            text="《滴天髓》所说的中和之道，《穷通宝鉴》所讲的调候取用，"
                 "都是围绕着这一点展开的。"
        ) as t:
            self.play(Write(cite), run_time=2.0)
            self.hold(t)

        self.clear_all()

    # ------------------------------------------------------------ 大运与流年

    def scene_dayun(self):
        head = section_title("五、大运与流年")

        with self.voiceover(
            text="八字是静态的，人生却是流动的。"
        ) as t:
            self.play(FadeIn(head, shift=DOWN * 0.2), run_time=0.8)
            self.hold(t)

        gz = ["丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申"]
        blocks = VGroup()
        for i, g in enumerate(gz):
            box = Rectangle(width=2.05, height=1.15, color=GOLD, stroke_width=2)
            box.set_stroke(GOLD, 2, opacity=0.6).set_fill(GOLD, 0.05)
            txt = cn(g, size=32, color=PAPER).move_to(box)
            age = cn(f"{i * 10 + 3}–{i * 10 + 12} 岁", size=19, color=GOLD)
            age.next_to(box, UP, buff=0.16)
            blocks.add(VGroup(box, txt, age))
        blocks.arrange(RIGHT, buff=0.16).shift(UP * 0.75)

        dy_lbl = cn("大运 · 每十年一步", size=27, color=GOLD)
        dy_lbl.next_to(blocks, UP, buff=0.62)

        with self.voiceover(
            text="从月柱推出的大运，每十年一步，标记着人生的阶段。"
        ) as t:
            self.play(FadeIn(dy_lbl), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.25) for b in blocks],
                                  lag_ratio=0.3), run_time=3.0)
            self.hold(t)

        ticks = VGroup()
        for i in range(60):
            x = blocks.get_left()[0] + 0.02 + i * (blocks.width - 0.04) / 59
            ticks.add(Line(UP * 0.13, DOWN * 0.13, color=WUXING["水"], stroke_width=2)
                      .move_to([x, -0.65, 0]))
        ly_lbl = cn("流年 · 每一年的干支", size=27, color=WUXING["水"])
        ly_lbl.next_to(ticks, DOWN, buff=0.35)

        with self.voiceover(
            text="而每一年的干支，则称为流年。"
        ) as t:
            self.play(LaggedStart(*[FadeIn(k) for k in ticks], lag_ratio=0.03), run_time=2.0)
            self.play(FadeIn(ly_lbl), run_time=0.8)
            self.hold(t)

        concl = cn("原局八字  ＋  大运  ＋  流年  →  看生克变化", size=32, color=GOLD)
        concl.shift(DOWN * 2.75)

        with self.voiceover(
            text="命理师所谓的看运，就是把大运和流年的干支，与原局的八字放在一起，"
                 "观察其中生克关系的变化。"
        ) as t:
            self.play(Write(concl), run_time=2.2)
            self.hold(t)

        self.clear_all()

    # ------------------------------------------------------------ 刑冲合害

    def scene_dizhi_relations(self):
        head = section_title("六、刑冲合害")

        R = 2.35
        center = DOWN * 0.15
        ring = Circle(radius=R, color=GOLD, stroke_width=2).move_to(center)
        ring.set_stroke(GOLD, 2, opacity=0.4).set_fill(opacity=0)

        pos = []
        nodes = VGroup()
        for i, z in enumerate(DIZHI):
            ang = PI / 2 - i * TAU / 12
            p = center + R * np.array([np.cos(ang), np.sin(ang), 0])
            pos.append(p)
            nodes.add(cn(z, size=32, color=WUXING[ZHI_WUXING[z]],
                         font=CN_BOLD, weight=BOLD).move_to(p))

        with self.voiceover(
            text="地支之间，还有一套特殊的关系，古籍里合称刑冲合害。"
        ) as t:
            self.play(FadeIn(head, shift=DOWN * 0.2), run_time=0.8)
            self.play(Create(ring), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(n, scale=0.7) for n in nodes],
                                  lag_ratio=0.12), run_time=2.0)
            self.hold(t)

        chong = VGroup(*[
            Line(pos[i], pos[i + 6], color=SEAL, stroke_width=2.5, stroke_opacity=0.85)
            .set_length(Line(pos[i], pos[i + 6]).get_length() - 0.9)
            for i in range(6)
        ])
        chong_lbl = cn("六冲 —— 圆环上正对的两支：子午 · 丑未 · 寅申 · 卯酉 · 辰戌 · 巳亥",
                       size=26, color=SEAL).to_edge(DOWN, buff=0.5)

        with self.voiceover(
            text="相冲，是圆环上正对的两支：子午相冲，丑未相冲，寅申相冲，"
                 "卯酉相冲，辰戌相冲，巳亥相冲，一共六组。"
        ) as t:
            self.play(FadeIn(chong_lbl), run_time=0.7)
            for c in chong:
                self.play(Create(c), run_time=0.52)
            self.hold(t)

        self.play(FadeOut(chong), FadeOut(chong_lbl), run_time=0.7)

        sanhe = [((8, 0, 4), "水"), ((2, 6, 10), "火"), ((11, 3, 7), "木"), ((5, 9, 1), "金")]
        tris = VGroup(*[
            Polygon(pos[a], pos[b], pos[c], color=WUXING[e],
                    stroke_width=3, stroke_opacity=0.9, fill_opacity=0)
            for (a, b, c), e in sanhe
        ])
        he_lbl = VGroup(
            cn("三合 —— 相隔四位的三支结成一局", size=26, color=GOLD),
            cn("申子辰合水　寅午戌合火　亥卯未合木　巳酉丑合金", size=25, color=PAPER),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.4)

        with self.voiceover(
            text="三合，是相隔四位的三支结成一局：申子辰合水，寅午戌合火，"
                 "亥卯未合木，巳酉丑合金。此外还有六合、相刑与相害。"
        ) as t:
            self.play(FadeIn(he_lbl), run_time=0.8)
            for tri in tris:
                self.play(Create(tri), run_time=0.75)
            self.hold(t)

        self.clear_all()

    # ------------------------------------------------------------ 神煞

    def scene_shensha(self):
        head = section_title("七、神煞")

        data = [
            ("天乙贵人", "逢凶化吉的助力", GOLD),
            ("桃　　花", "人缘与情感", "#D96BA0"),
            ("驿　　马", "奔波与迁移", WUXING["水"]),
            ("华　　盖", "孤高、艺术与宗教", "#9B8CD9"),
        ]
        cards = VGroup()
        for name, desc, col in data:
            box = RoundedRectangle(width=3.15, height=1.9, corner_radius=0.12,
                                   color=col, stroke_width=2)
            box.set_stroke(col, 2, opacity=0.65).set_fill(col, 0.06)
            n = cn(name, size=31, color=col, font=CN_BOLD, weight=BOLD)
            d = cn(desc, size=21, color=PAPER)
            cards.add(VGroup(box, VGroup(n, d).arrange(DOWN, buff=0.24).move_to(box)))
        cards.arrange(RIGHT, buff=0.42).shift(UP * 0.35)

        with self.voiceover(
            text="最后是神煞。它们是依照特定规则查出的符号，"
                 "例如天乙贵人、桃花、驿马、华盖。"
        ) as t:
            self.play(FadeIn(head, shift=DOWN * 0.2), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.3) for c in cards],
                                  lag_ratio=0.35), run_time=3.2)
            self.hold(t)

        note = VGroup(
            cn("唐宋古法中占比很重", size=29, color=PAPER),
            cn("明清以后逐渐让位于五行生克，成为参考", size=29, color=GOLD),
        ).arrange(DOWN, buff=0.32).shift(DOWN * 2.15)

        with self.voiceover(
            text="神煞在唐宋古法中占比很重，明清以后，逐渐让位于五行生克，成为一种参考。"
        ) as t:
            self.play(FadeIn(note[0], shift=UP * 0.2), run_time=1.1)
            self.play(FadeIn(note[1], shift=UP * 0.2), run_time=1.1)
            self.hold(t)

        self.clear_all()

    # ------------------------------------------------------------ 结语

    def scene_outro(self):
        head = section_title("结语")

        lines = VGroup(
            cn("这些名词，构成了阅读命理古籍的基本词汇", size=34, color=PAPER),
            cn("但它们描述的是一套自洽的符号系统", size=34, color=GOLD),
            cn("而不是经过验证的科学结论", size=34, color=SEAL),
        ).arrange(DOWN, buff=0.55).shift(UP * 0.2)

        with self.voiceover(
            text="这些名词，构成了阅读命理古籍的基本词汇。但需要提醒的是，"
                 "它们描述的是一套自洽的符号系统，而不是经过验证的科学结论。"
        ) as t:
            self.play(FadeIn(head, shift=DOWN * 0.2), run_time=0.8)
            self.play(FadeIn(lines[0], shift=UP * 0.2), run_time=1.3)
            self.play(FadeIn(lines[1], shift=UP * 0.2), run_time=1.3)
            self.play(FadeIn(lines[2], shift=UP * 0.2), run_time=1.3)
            self.hold(t)

        final = cn("当作文化史来读", size=70, color=GOLD, font=CN_BOLD, weight=BOLD)
        sub = cn("或许比当作命运的答案，更有意思", size=30, color=PAPER)
        sub.next_to(final, DOWN, buff=0.5)

        with self.voiceover(
            text="把它当作文化史来读，或许比当作命运的答案，更有意思。"
        ) as t:
            self.play(FadeOut(lines), FadeOut(head), run_time=0.8)
            self.play(Write(final), run_time=2.0)
            self.play(FadeIn(sub, shift=UP * 0.2), run_time=1.2)
            self.hold(t)

        self.wait(1.2)
