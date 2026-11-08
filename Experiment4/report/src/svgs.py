# -*- coding: utf-8 -*-
"""SVG + table generators for the lab report (all circuit/timing data computed, not typed)."""
import itertools

NAVY = "#16305c"; BLUE = "#2b5aa6"; ORANGE = "#c2410c"; TEAL = "#0f766e"; VIOLET = "#7c3aed"; ROSE = "#be123c"
GRID = "#c9d3e6"

DEFS = ('<defs><marker id="ar%s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker></defs>')


def svg(w, h, body, uid="a"):
    return (f'<svg class="dg" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img">'
            + DEFS % (uid, NAVY) + body + '</svg>')


def txt(x, y, s, cls="sv", anchor="middle", extra=""):
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}" {extra}>{s}</text>'


def box(x, y, w, h, fill="#eef3fb", stroke=NAVY, r=8, sw=1.6):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def line(pts, uid="a", arrow=False, color=NAVY, sw=1.6, dash=""):
    p = " ".join(f"{x},{y}" for x, y in pts)
    m = f' marker-end="url(#ar{uid})"' if arrow else ""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="{sw}"{m}{d}/>'


def dot(x, y):
    return f'<circle cx="{x}" cy="{y}" r="3" fill="{NAVY}"/>'


# ---------------------------------------------------------------- block diagram
def block_diagram():
    b = ""
    # left column
    b += box(10, 20, 130, 66) + txt(75, 46, "ورودی‌های موازی", "svp") + txt(75, 66, "A  B  C  D", "sv en")
    b += box(10, 112, 130, 66) + txt(75, 138, "ورودی سریال", "svp") + txt(75, 158, "SE  /  SL", "sv en")
    b += box(10, 204, 130, 66) + txt(75, 230, "کلیدهای کنترل", "svp") + txt(75, 250, "PE  /  DIR", "sv en")
    # mux
    b += box(200, 20, 150, 250, fill="#fff4e0", stroke=ORANGE)
    b += txt(275, 46, "انتخابگر ۲ به ۱ (×۴)", "svp") + txt(275, 64, "AND-OR  یا  74157", "sv en")
    for i in range(4):
        b += box(222, 84 + i * 44, 106, 32, fill="#ffffff", stroke=ORANGE, r=6, sw=1.2)
        b += txt(275, 105 + i * 44, f"MUX {'ABCD'[i]}", "sv en")
    # FF
    b += box(410, 20, 150, 250, fill="#e6f3ef", stroke=TEAL)
    b += txt(485, 46, "چهار فلیپ‌فلاپ D", "svp") + txt(485, 64, "7474 × 2", "sv en")
    for i in range(4):
        b += box(432, 84 + i * 44, 106, 32, fill="#ffffff", stroke=TEAL, r=6, sw=1.2)
        b += txt(485, 105 + i * 44, f"D-FF  Q{'ABCD'[i]}", "sv en")
    # right
    b += box(620, 20, 130, 86, fill="#eef3fb") + txt(685, 50, "نمایشگر خروجی", "svp") + txt(685, 70, "LED / Logic Analyser", "sv en small")
    b += box(620, 134, 130, 86, fill="#eef3fb") + txt(685, 164, "رمزگشا / آشکارساز", "svp") + txt(685, 184, "Johnson · Detector", "sv en small")
    # clock
    b += box(410, 300, 150, 52, fill="#f3ecfd", stroke=VIOLET) + txt(485, 322, "مولد کلاک", "svp") + txt(485, 340, "555 / DCLOCK", "sv en small")
    # arrows
    b += line([(140, 53), (200, 53)], arrow=True) + line([(140, 145), (200, 145)], arrow=True) + line([(140, 237), (200, 237)], arrow=True)
    b += line([(350, 145), (410, 145)], arrow=True)
    b += line([(560, 53), (620, 53)], arrow=True) + line([(560, 177), (620, 177)], arrow=True)
    b += line([(485, 300), (485, 270)], arrow=True, color=VIOLET)
    b += txt(485, 292, "CLK", "sv en small", extra='fill="%s"' % VIOLET)
    # feedback
    b += line([(560, 250), (590, 250), (590, 285), (275, 285), (275, 270)], arrow=True, color=TEAL, dash="5 4")
    b += txt(430, 380, "مسیر بازخورد: Q طبقه‌ی قبل  ←  ورودی طبقه‌ی بعد  (و Q̅D ← SE در شمارنده‌ی جانسون)", "sv small", extra=f'fill="{TEAL}"')
    return svg(770, 395, b, "b1")


# ---------------------------------------------------------------- one-stage gate level
def and_gate(x, y, w=34, h=50):
    return f'<path d="M{x},{y} H{x+w*0.5} A{h/2},{h/2} 0 0 1 {x+w*0.5},{y+h} H{x} Z" fill="#fff" stroke="{NAVY}" stroke-width="1.6"/>'


def or_gate(x, y, w=44, h=50):
    return (f'<path d="M{x},{y} Q{x+w*0.45},{y} {x+w},{y+h/2} Q{x+w*0.45},{y+h} {x},{y+h} '
            f'Q{x+w*0.25},{y+h/2} {x},{y} Z" fill="#fff" stroke="{NAVY}" stroke-width="1.6"/>')


def stage_diagram():
    b = ""
    b += txt(10, 48, "In<tspan baseline-shift=\"sub\" font-size=\"9\">i</tspan>", "sv en", "start")
    b += txt(10, 104, "PE", "sv en", "start")
    b += txt(10, 166, "Q<tspan baseline-shift=\"sub\" font-size=\"9\">i-1</tspan>", "sv en", "start")
    # AND1
    b += and_gate(160, 30)
    b += line([(46, 44), (160, 44)]) + line([(46, 104), (80, 104), (80, 68), (160, 68)])
    # AND2
    b += and_gate(160, 150)
    b += line([(46, 162), (160, 162)])
    b += dot(80, 104) + line([(80, 104), (80, 188), (112, 188)])
    # NOT gate
    b += f'<path d="M112,176 L112,200 L134,188 Z" fill="#fff" stroke="{NAVY}" stroke-width="1.6"/><circle cx="138" cy="188" r="4" fill="#fff" stroke="{NAVY}" stroke-width="1.6"/>'
    b += line([(142, 188), (160, 188)])
    b += txt(150, 215, "PE̅", "sv en small")
    # OR
    b += or_gate(262, 94)
    b += line([(194+0, 55), (232, 55), (232, 105), (266, 105)]) + line([(194, 175), (232, 175), (232, 133), (266, 133)])
    b += line([(306, 119), (360, 119)])
    # DFF
    b += box(360, 80, 86, 100, fill="#e6f3ef", stroke=TEAL, r=4)
    b += txt(375, 124, "D", "sv en", "middle") + txt(403, 108, "D-FF", "sv en small") + txt(432, 124, "Q", "sv en")
    b += f'<path d="M360,158 L372,166 L360,174" fill="none" stroke="{TEAL}" stroke-width="1.6"/>'
    b += line([(300, 166), (360, 166)], color=VIOLET) + txt(290, 170, "CLK", "sv en small", "end", extra=f'fill="{VIOLET}"')
    b += line([(446, 119), (500, 119)], arrow=True, uid="s1") + txt(506, 123, "Q<tspan baseline-shift=\"sub\" font-size=\"9\">i</tspan>", "sv en", "start")
    b += txt(215, 18, "D<tspan baseline-shift=\"sub\" font-size=\"9\">i</tspan> = PE·In<tspan baseline-shift=\"sub\" font-size=\"9\">i</tspan> + PE̅·Q<tspan baseline-shift=\"sub\" font-size=\"9\">i-1</tspan>", "sv en", extra=f'fill="{ORANGE}"')
    return svg(540, 232, b, "s1")


# ---------------------------------------------------------------- Johnson ring
def johnson_diagram():
    b = ""
    names = "ABCD"
    for i in range(4):
        x = 90 + i * 150
        b += box(x, 56, 90, 78, fill="#e6f3ef", stroke=TEAL, r=5)
        b += txt(x + 18, 100, "D", "sv en") + txt(x + 45, 78, "D-FF", "sv en small") + txt(x + 72, 100, "Q", "sv en")
        b += f'<path d="M{x},116 L{x+11},124 L{x},132" fill="none" stroke="{TEAL}" stroke-width="1.6"/>'
        b += txt(x + 45, 150, f"Q{names[i]}", "sv en", extra=f'fill="{BLUE}"')
        if i < 3:
            b += line([(x + 90, 96), (x + 150, 96)], arrow=True, uid="j1")
        b += line([(x - 30, 124), (x, 124)], color=VIOLET) if False else ""
    # clock bus
    b += line([(60, 24), (620, 24)], color=VIOLET) + txt(40, 28, "CLK", "sv en small", "end", extra=f'fill="{VIOLET}"')
    for i in range(4):
        x = 90 + i * 150
        b += line([(x - 14, 24), (x - 14, 124), (x, 124)], color=VIOLET) + dot(x - 14, 24)
    # feedback from last Q' (bubble at output)
    b += line([(630 + 0, 96), (668, 96)], arrow=True, uid="j1") + txt(672, 100, "QD", "sv en small", "start")
    b += line([(618, 96), (618, 178), (24, 178), (24, 96), (90, 96)], arrow=True, color=ORANGE, uid="j1")
    b += f'<circle cx="618" cy="96" r="0"/>'
    b += txt(320, 198, "Q̅D  ←  SE   (اتصال خروجی وارون طبقه‌ی آخر به ورودی سریال)", "sv small", extra=f'fill="{ORANGE}"')
    b += txt(42, 90, "SE", "sv en small", "end")
    return svg(700, 210, b, "j1")


# ---------------------------------------------------------------- DIP pinouts
def dip(x0, title, left, right, color=NAVY):
    h = 7 * 30 + 24
    b = f'<rect x="{x0+60}" y="20" width="110" height="{h}" rx="6" fill="#f4f7fc" stroke="{color}" stroke-width="1.8"/>'
    b += f'<path d="M{x0+95},20 a20,20 0 0 0 40,0" fill="#fff" stroke="{color}" stroke-width="1.6"/>'
    b += txt(x0 + 115, 20 + h / 2 + 4, title, "svp en", extra='font-size="15"')
    for i, name in enumerate(left):
        y = 46 + i * 30
        b += f'<line x1="{x0+44}" y1="{y}" x2="{x0+60}" y2="{y}" stroke="{color}" stroke-width="2"/>'
        b += txt(x0 + 71, y + 4, str(i + 1), "sv en small", "start", extra='fill="#555"')
        b += txt(x0 + 40, y + 4, name, "sv en small", "end")
    for i, name in enumerate(right):
        y = 46 + i * 30
        b += f'<line x1="{x0+170}" y1="{y}" x2="{x0+186}" y2="{y}" stroke="{color}" stroke-width="2"/>'
        b += txt(x0 + 159, y + 4, str(14 - i), "sv en small", "end", extra='fill="#555"')
        b += txt(x0 + 190, y + 4, name, "sv en small", "start")
    return b


def pinouts():
    l95 = ["SER IN", "A", "B", "C", "D", "MODE", "GND"]
    r95 = ["VCC", "QA", "QB", "QC", "QD", "CLK1 (R)", "CLK2 (L)"]
    l74 = ["1CLR̅", "1D", "1CLK", "1PRE̅", "1Q", "1Q̅", "GND"]
    r74 = ["VCC", "2CLR̅", "2D", "2CLK", "2PRE̅", "2Q", "2Q̅"]
    b = dip(0, "7495", l95, r95, BLUE) + dip(390, "7474", l74, r74, TEAL)
    return svg(780, 260, b, "p1")


# ---------------------------------------------------------------- detector block
def detector_diagram():
    b = ""
    b += txt(25, 74, "X", "svp en", "middle") + line([(40, 70), (80, 70)], arrow=True, uid="d1")
    names = "ABCD"
    for i in range(4):
        x = 80 + i * 110
        b += box(x, 36, 80, 68, fill="#e6f3ef", stroke=TEAL, r=6)
        b += txt(x + 40, 66, "D-FF", "sv en small") + txt(x + 40, 88, f"Q{names[i]}", "sv en", extra=f'fill="{BLUE}"')
        if i < 3:
            b += line([(x + 80, 70), (x + 110, 70)], arrow=True, uid="d1")
    b += txt(260, 20, "ثبات ۴ بیتی (پنجره‌ی لغزنده)", "svp small")
    # taps down
    for i, tgt in zip(range(4), (0, 0, 1, 1)):
        x = 120 + i * 110
        b += line([(x, 104), (x, 150 if tgt == 0 else 150)])
    b += box(100, 150, 150, 46, fill="#fff4e0", stroke=ORANGE) + txt(175, 178, "XOR : QA ⊕ QB", "sv en")
    b += box(320, 150, 150, 46, fill="#fff4e0", stroke=ORANGE) + txt(395, 178, "XNOR : QC ⊙ QD", "sv en")
    b += line([(120, 150), (120, 140)]) if False else ""
    b += line([(175, 196), (175, 240), (300, 240)], arrow=True, uid="d1") + line([(395, 196), (395, 240), (360, 240)], arrow=True, uid="d1")
    b += box(300, 218, 60, 44, fill="#fdeaea", stroke=ROSE) + txt(330, 245, "AND", "sv en")
    b += line([(360, 240), (360, 240)])
    b += line([(300, 240), (300, 240)])
    b += line([(330, 262), (330, 292)], arrow=True, uid="d1") + txt(330, 310, "Z", "svp en") + txt(400, 250, "Z = (QA ⊕ QB)·(QC ⊙ QD)", "sv en small", "start", extra=f'fill="{ROSE}"')
    # tap labels
    return svg(560, 322, b, "d1")


# ---------------------------------------------------------------- timing waves
def wave(rows, n_edges, title="", uw=40, label_w=64, hi=None, highlight=None):
    """rows: list of (name, values, start_time, colour, kind) ; values hold 1 unit each.
    clock: kind 'clk'. time unit = 1 clock period. edge k at t=k."""
    rh = 36
    H = 24 + len(rows) * rh + 14
    W = label_w + int((n_edges + 1.3) * uw) + 10
    x0 = label_w
    b = ""
    # grid + edge numbers
    for k in range(0, n_edges + 1):
        x = x0 + k * uw
        b += f'<line x1="{x}" y1="22" x2="{x}" y2="{H-10}" stroke="{GRID}" stroke-width="1" stroke-dasharray="3 3"/>'
        b += txt(x, 14, str(k), "sv en tiny", extra='fill="#777"')
    for r, (name, vals, st, col, kind) in enumerate(rows):
        y_top = 28 + r * rh
        yh, yl = y_top + 4, y_top + rh - 10
        b += txt(label_w - 10, (yh + yl) / 2 + 4, name, "sv en small", "end", extra=f'fill="{col}"')
        if kind == "clk":
            pts = []
            for k in range(0, n_edges + 1):
                xs = x0 + k * uw
                pts += [(xs, yl), (xs, yh), (xs + uw / 2, yh), (xs + uw / 2, yl)]
            pts.append((x0 + (n_edges + 1) * uw, yl))
            pts = pts[1:]
            b += line(pts, color=col, sw=1.8)
            continue
        pts = []
        prev = None
        for i, v in enumerate(vals):
            xs = x0 + (st + i) * uw
            xe = xs + uw
            y = yh if v else yl
            if prev is None:
                pts.append((xs, y))
            elif prev != v:
                pts.append((xs, yh if prev else yl)); pts.append((xs, y))
            if highlight and name == highlight and v:
                b += f'<rect x="{xs}" y="{yh}" width="{uw}" height="{yl-yh}" fill="{col}" opacity="0.18"/>'
            pts.append((xe, y))
            prev = v
        b += line(pts, color=col, sw=2)
    return svg(W, H, b, "w")


def step_r(s, se): return (se, s[0], s[1], s[2])
def step_l(s, sl): return (s[1], s[2], s[3], sl)
def st(s): return "".join(map(str, s))


def wave_right():
    s = (1, 0, 1, 0); hist = [s]
    for _ in range(5):
        s = step_r(s, 0); hist.append(s)
    rows = [("CLK", None, 0, NAVY, "clk"), ("SE", [0] * 6, 0, GRID if False else "#777", "d")]
    for i, nm in enumerate(["QA", "QB", "QC", "QD"]):
        rows.append((nm, [h[i] for h in hist], 0, [BLUE, ORANGE, TEAL, VIOLET][i], "d"))
    return wave(rows, 5, uw=52)


def johnson_states():
    s = (0, 0, 0, 0); out = []
    for _ in range(17):
        out.append(s); s = step_r(s, 1 - s[3])
    return out


def wave_johnson():
    h = johnson_states()
    rows = [("CLK", None, 0, NAVY, "clk")]
    for i, nm in enumerate(["QA", "QB", "QC", "QD"]):
        rows.append((nm, [x[i] for x in h], 0, [BLUE, ORANGE, TEAL, VIOLET][i], "d"))
    return wave(rows, 16, uw=34)


STREAM = [int(c) for c in "1101110001011101"]
WINDOW = {"1011", "0111", "0100", "1000"}


def detector_trace():
    s = (0, 0, 0, 0); rows = [(0, None, st(s), 0)]
    for k, x in enumerate(STREAM, 1):
        s = step_r(s, x)
        rows.append((k, x, st(s), int(st(s) in WINDOW)))
    return rows


def wave_detector():
    tr = detector_trace()
    rows = [("CLK", None, 0, NAVY, "clk"),
            ("X", STREAM, 0.5, "#555", "d")]
    for i, nm in enumerate(["QA", "QB", "QC", "QD"]):
        rows.append((nm, [int(r[2][i]) for r in tr], 0, [BLUE, ORANGE, TEAL, VIOLET][i], "d"))
    rows.append(("Z", [r[3] for r in tr], 0, ROSE, "d"))
    return wave(rows, 16, uw=34, highlight="Z")


# ---------------------------------------------------------------- tables
def bits(s):
    return f'<span class="bin">{s}</span>'


def table(head, rows, cls="", widths=None):
    h = "".join(f"<th>{c}</th>" for c in head)
    r = ""
    for row in rows:
        r += "<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>"
    return f'<table class="data {cls}"><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table>'


def tbl_shift_right():
    s = (1, 0, 1, 0); rows = [["۰", "—", bits("0"), bits(st(s))]]
    for k in range(1, 5):
        s = step_r(s, 0); rows.append([str(k), "↓", bits("0"), bits(st(s))])
    t1 = table(["شماره‌ی کلاک", "لبه", "SE", "QA QB QC QD"], rows, "c")
    s = (0, 0, 0, 0); rows = [["۰", "—", "—", bits(st(s))]]
    for k, x in enumerate([1, 1, 0, 1], 1):
        s = step_r(s, x); rows.append([str(k), "↑", bits(str(x)), bits(st(s))])
    t2 = table(["شماره‌ی کلاک", "لبه", "SE", "QA QB QC QD"], rows, "c")
    return t1, t2


def tbl_johnson():
    h = johnson_states()[:9]
    dec = ["Q̅A·Q̅D", "QA·Q̅B", "QB·Q̅C", "QC·Q̅D", "QA·QD", "Q̅A·QB", "Q̅B·QC", "Q̅C·QD"]
    rows = []
    for k in range(8):
        s = h[k]
        rows.append([f"S{k}", bits(st(s)), bits(str(1 - s[3])), f'<span class="en">{dec[k]}</span>', bits(st(h[k + 1]))])
    return table(["حالت", "QA QB QC QD", "SE = Q̅D", "عبارت رمزگشایی", "حالت بعد"], rows, "c")


def tbl_invalid():
    s = (1, 0, 1, 0); rows = []
    for k in range(8):
        n = step_r(s, 1 - s[3]); rows.append([f"U{k}", bits(st(s)), bits(st(n))]); s = n
    return table(["حالت", "QA QB QC QD", "حالت بعد"], rows, "c")


def tbl_bidir():
    s = (0, 1, 1, 0); rows = [["۰", "—", "—", "—", bits(st(s))]]
    k = 0
    for _ in range(3):
        s = step_r(s, 1); k += 1; rows.append([str(k), bits("1"), bits("1"), "—", bits(st(s))])
    for _ in range(3):
        s = step_l(s, 0); k += 1; rows.append([str(k), bits("0"), "—", bits("0"), bits(st(s))])
    return table(["کلاک", "DIR", "SE", "SL", "QA QB QC QD"], rows, "c")


def tbl_7495():
    rows = [["بارگذاری", bits("1"), bits("1010"), "CP2 ↓", "—", bits("1010")]]
    s = (1, 0, 1, 0)
    for x in (1, 0, 0):
        s = step_r(s, x); rows.append(["شیفت راست", bits("0"), "—", "CP1 ↓", bits(str(x)), bits(st(s))])
    return table(["عملیات", "MODE", "A B C D", "کلاک", "SER", "QA QB QC QD"], rows, "c")


def tbl_detector():
    tr = detector_trace(); rows = []
    for k, x, s, z in tr[1:]:
        arr = s[::-1]
        cls = ' class="hit"' if z else ""
        warm = "" if k >= 4 else '<span class="mut">ناقص</span>'
        rows.append(f"<tr{cls}><td>{k}</td><td>{bits(str(x))}</td><td>{bits(s)}</td><td>{bits(arr)}</td><td>{bits(str(z))}</td><td>{warm}</td></tr>")
    head = "".join(f"<th>{c}</th>" for c in ["کلاک", "X", "QA QB QC QD", "۴ بیت آخر به ترتیب ورود", "Z", "توضیح"])
    return f'<table class="data c"><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table>'


def tbl_detector_map():
    seqs = ["1101", "1110", "0010", "0001"]
    rows = [[bits(q), bits(q[::-1]), bits(str(int(q[::-1], 2)))] for q in seqs]
    return table(["دنباله (ترتیب ورود)", "محتوای ثبات QA QB QC QD", "مینترم"], rows, "c")


ALL = dict(
    SVG_BLOCK=block_diagram, SVG_STAGE=stage_diagram, SVG_JOHNSON=johnson_diagram, SVG_PINOUT=pinouts,
    SVG_DETECTOR=detector_diagram, SVG_W_RIGHT=wave_right, SVG_W_JOHNSON=wave_johnson, SVG_W_DETECTOR=wave_detector,
    TBL_JOHNSON=tbl_johnson, TBL_INVALID=tbl_invalid, TBL_BIDIR=tbl_bidir, TBL_7495=tbl_7495,
    TBL_DETECTOR=tbl_detector, TBL_DETMAP=tbl_detector_map,
)
