"""Board 1: the problem, as it existed before this fix.

The old posture, where the SHAP math broke, where the data broke, and
where the pipeline broke, laid out as four columns under one flow.
"""

from build_boards import (
    ORANGE, RED, BLUE, GREEN, YELLOW, WHITE, VIOLET, MUTED, STROKE,
    arrow_svg, render, rough_rect_svg, text_svg,
    excal_rect, excal_text, excal_arrow, write_scene,
)

WIDTH, HEIGHT = 1400, 940


def box_block(x, y, w, h, lines, fill, first_size=13.5, rest_size=11.5, width_chars=None):
    wc = width_chars or max(14, int(w / 6.4))
    out = rough_rect_svg(x, y, w, h, fill)
    cursor = y + 22
    for i, line in enumerate(lines):
        size = first_size if i == 0 else rest_size
        weight = "bold" if i == 0 else "normal"
        color = "#1e1e1e" if i == 0 else MUTED
        out += text_svg(x + 10, cursor, line, size=size, weight=weight, color=color, width_chars=wc)
        cursor += (17 if i == 0 else 14)
    return out


def build_problem_board():
    body = ""

    flow_y = 96
    box_w, box_h = 200, 92
    steps = [
        (["Plaid + CRA feeds", "land in the data lake"], BLUE, 40),
        (["Features built into", "risk model tables"], BLUE, 260),
        (["Model scores the", "application"], BLUE, 480),
        (["SHAP direction from", "batch mean, not per record"], RED, 700),
        (["Top 4 reasons picked", "by absolute magnitude"], RED, 920),
        (["Customer gets a", "soft $20 line instead"], ORANGE, 1140),
    ]
    for lines, color, x in steps:
        body += box_block(x, flow_y, box_w, box_h, lines, color, width_chars=25)

    for i in range(len(steps) - 1):
        x1 = steps[i][2] + box_w
        x2 = steps[i + 1][2]
        y = flow_y + box_h / 2
        body += arrow_svg(x1 + 4, y, x2 - 4, y)

    section_y = 236
    col_w, col_h, gap, item_gap = 320, 66, 24, 12
    cols_x = [40, 384, 728, 1072]

    body += text_svg(cols_x[0], section_y, "The old posture", size=15, weight="bold")
    posture = [
        "Couldn't defend a real decline, so we gave a small line instead",
        "That muted our ability to cut the risk tail",
        "We kept absorbing losses on customers we already knew were bad risk",
    ]
    for i, item in enumerate(posture):
        yy = section_y + 22 + i * (col_h + item_gap)
        body += box_block(cols_x[0], yy, col_w, col_h, [item], WHITE, width_chars=40)

    body += text_svg(cols_x[1], section_y, "Where the SHAP math broke", size=15, weight="bold")
    shap_bugs = [
        "Direction came from batch mean SHAP, not the individual record",
        "Top 4 reasons ranked by absolute magnitude, not by risk direction",
        "A large risk-reducing feature could show up as a reason for decline",
    ]
    for i, item in enumerate(shap_bugs):
        yy = section_y + 22 + i * (col_h + item_gap)
        body += box_block(cols_x[1], yy, col_w, col_h, [item], RED, width_chars=40)

    body += text_svg(cols_x[2], section_y, "Where the data broke", size=15, weight="bold")
    data_bugs = [
        "CRA and non-CRA feeds categorize the same transaction differently",
        "125 day and 180 day lookback windows used inconsistently",
        "CRA baseline and cash flow segments not always both present",
    ]
    for i, item in enumerate(data_bugs):
        yy = section_y + 22 + i * (col_h + item_gap)
        body += box_block(cols_x[2], yy, col_w, col_h, [item], YELLOW, width_chars=40)

    body += text_svg(cols_x[3], section_y, "Where the pipeline broke", size=15, weight="bold")
    pipeline_bugs = [
        "Reason codes with no mapped template text produced blank emails",
        "Multi-reason cases sometimes rendered only the first code",
        "Fully null feature sets fell through without a defined path",
    ]
    for i, item in enumerate(pipeline_bugs):
        yy = section_y + 22 + i * (col_h + item_gap)
        body += box_block(cols_x[3], yy, col_w, col_h, [item], VIOLET, width_chars=40)

    render("board-1-the-problem", WIDTH, HEIGHT, body, title="Adverse action at Varo, before this fix")

    # ---- excalidraw scene ----
    elements = []
    for lines, color, xx in steps:
        elements.append(excal_rect(xx, flow_y, box_w, box_h, bg=color))
        elements.append(excal_text(xx + 8, flow_y + 8, "\n".join(lines), font_size=12, width=box_w - 16, height=box_h - 16))
    for i in range(len(steps) - 1):
        x1 = steps[i][2] + box_w
        x2 = steps[i + 1][2]
        y = flow_y + box_h / 2
        elements.append(excal_arrow(x1 + 4, y, x2 - 4, y))

    columns = [
        ("The old posture", posture, WHITE),
        ("Where the SHAP math broke", shap_bugs, RED),
        ("Where the data broke", data_bugs, YELLOW),
        ("Where the pipeline broke", pipeline_bugs, VIOLET),
    ]
    for (title, items, color), cx in zip(columns, cols_x):
        elements.append(excal_text(cx, section_y - 14, title, font_size=15, width=col_w))
        for i, item in enumerate(items):
            yy = section_y + 22 + i * (col_h + item_gap)
            elements.append(excal_rect(cx, yy, col_w, col_h, bg=color))
            elements.append(excal_text(cx + 8, yy + 8, item, font_size=11, width=col_w - 16, height=col_h - 16))

    write_scene("board-1-the-problem", elements)


if __name__ == "__main__":
    build_problem_board()
