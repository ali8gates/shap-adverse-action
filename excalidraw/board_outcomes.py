"""Board 3: how we validated it, and what it changed.

Validation flow at the top (shadow scoring through second-line review),
then where the code lives and what the March 31 validation slice showed.
"""

from build_boards import (
    ORANGE, RED, BLUE, GREEN, YELLOW, WHITE, VIOLET, MUTED,
    arrow_svg, render, rough_rect_svg, text_svg,
    excal_rect, excal_text, excal_arrow, write_scene,
)

WIDTH, HEIGHT = 1240, 780


def box_block(x, y, w, h, lines, fill, first_size=14, rest_size=12, width_chars=None):
    wc = width_chars or max(16, int(w / 6.6))
    out = rough_rect_svg(x, y, w, h, fill)
    cursor = y + 22
    for i, line in enumerate(lines):
        size = first_size if i == 0 else rest_size
        weight = "bold" if i == 0 else "normal"
        color = "#1e1e1e" if i == 0 else MUTED
        out += text_svg(x + 12, cursor, line, size=size, weight=weight, color=color, width_chars=wc)
        cursor += (17 if i == 0 else 15)
    return out


def build_outcomes_board():
    body = ""

    flow_y = 96
    box_w, box_h = 195, 96
    steps = [
        (["Shadow scoring", "on live traffic"], BLUE, 40),
        (["Backfill on", "historical cohorts"], BLUE, 255),
        (["Compare features,", "scores, AA reasons"], YELLOW, 470),
        (["Second-line Model Risk", "and Compliance review"], ORANGE, 685),
        (["Turn on for", "real customers"], GREEN, 900),
    ]
    for lines, color, x in steps:
        body += box_block(x, flow_y, box_w, box_h, lines, color, width_chars=24)

    for i in range(len(steps) - 1):
        x1 = steps[i][2] + box_w
        x2 = steps[i + 1][2]
        y = flow_y + box_h / 2
        body += arrow_svg(x1 + 4, y, x2 - 4, y)

    body += text_svg(40, flow_y - 20, "How we validated it before anything shipped", size=15.5, weight="bold", width_chars=70)

    section_y = 250
    body += text_svg(40, section_y, "Where the code lives", size=15.5, weight="bold")
    code_items = [
        "direction.py, signed per-record SHAP direction",
        "reason_selection.py, top 4 positive-only reasons",
        "data_contracts.py, CRA lookback and segment checks",
        "templates.py, reason code to text, quality gate",
        "pipeline.py, ties scoring through to the letter",
        "backfill.py, live vs backfill match reporting",
        "tests/, 26 passing tests across every module",
    ]
    dx, dy, dw, dh, gap = 40, section_y + 22, 560, 44, 9
    for i, item in enumerate(code_items):
        yy = dy + i * (dh + gap)
        body += box_block(dx, yy, dw, dh, [item], WHITE, first_size=13, width_chars=68)

    out_x = 660
    body += text_svg(out_x, section_y, "March 31 validation slice", size=15.5, weight="bold")
    outcomes = [
        ("100% match", "Feature values, model scores, and AA reasons, live vs backfill", GREEN),
        ("Zero training-serving skew", "on the validated cohort", GREEN),
        ("4 reasons rendered, every time", "multi-reason letters no longer drop to just one code", VIOLET),
        ("From soft declines to real ones", "risk-based pricing and denials we can stand behind", WHITE),
    ]
    ow, oh, ogap = 540, 62, 10
    for i, (big, small, color) in enumerate(outcomes):
        yy = dy + i * (oh + ogap)
        body += box_block(out_x, yy, ow, oh, [big, small], color, width_chars=58)

    render("board-3-validation-and-outcomes", WIDTH, HEIGHT, body, title="How we validated it, and what it changed")

    # ---- excalidraw scene ----
    elements = []
    for lines, color, xx in steps:
        elements.append(excal_rect(xx, flow_y, box_w, box_h, bg=color))
        elements.append(excal_text(xx + 10, flow_y + 10, "\n".join(lines), font_size=12.5, width=box_w - 20, height=box_h - 20))
    for i in range(len(steps) - 1):
        x1 = steps[i][2] + box_w
        x2 = steps[i + 1][2]
        y = flow_y + box_h / 2
        elements.append(excal_arrow(x1 + 4, y, x2 - 4, y))

    elements.append(excal_text(40, section_y - 14, "Where the code lives", font_size=16, width=400))
    for i, item in enumerate(code_items):
        yy = dy + i * (dh + gap)
        elements.append(excal_rect(dx, yy, dw, dh, bg=WHITE))
        elements.append(excal_text(dx + 10, yy + 10, item, font_size=12, width=dw - 20, height=dh - 18))

    elements.append(excal_text(out_x, section_y - 14, "March 31 validation slice", font_size=16, width=400))
    for i, (big, small, color) in enumerate(outcomes):
        yy = dy + i * (oh + ogap)
        elements.append(excal_rect(out_x, yy, ow, oh, bg=color))
        elements.append(excal_text(out_x + 10, yy + 8, f"{big}\n{small}", font_size=12, width=ow - 20, height=oh - 12))

    write_scene("board-3-validation-and-outcomes", elements)


if __name__ == "__main__":
    build_outcomes_board()
