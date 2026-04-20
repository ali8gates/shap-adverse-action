"""Board 2: the corrected design.

The same four columns as the problem board, but showing what changed in
each one, under a flow that ends at a letter instead of a mean $20 line.
"""

from build_boards import (
    RED, BLUE, GREEN, YELLOW, WHITE, VIOLET, MUTED, STROKE,
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


def build_fix_board():
    body = ""

    flow_y = 96
    box_w, box_h = 200, 92
    steps = [
        (["Signed SHAP value", "per customer, per feature"], BLUE, 40),
        (["Top 4 positive SHAP", "values only"], GREEN, 260),
        (["Mapped to an approved", "reason code"], GREEN, 480),
        (["Quality gate checks", "every code has text"], GREEN, 700),
        (["Data contract checks", "run before scoring"], GREEN, 920),
        (["Full 4-reason letter", "goes to the customer"], BLUE, 1140),
    ]
    for lines, color, x in steps:
        body += box_block(x, flow_y, box_w, box_h, lines, color, width_chars=25)

    for i in range(len(steps) - 1):
        x1 = steps[i][2] + box_w
        x2 = steps[i + 1][2]
        y = flow_y + box_h / 2
        body += arrow_svg(x1 + 4, y, x2 - 4, y)

    section_y = 236
    col_w, col_h, item_gap = 320, 66, 12
    cols_x = [40, 384, 728, 1072]

    body += text_svg(cols_x[0], section_y, "Direction, fixed", size=15, weight="bold")
    direction_fix = [
        "Direction comes from this record's own signed SHAP value",
        "Never averaged across a batch or a feature's dataset-wide mean",
        "Matches how a customer or a regulator actually reads a reason",
    ]
    for i, item in enumerate(direction_fix):
        yy = section_y + 22 + i * (col_h + item_gap)
        body += box_block(cols_x[0], yy, col_w, col_h, [item], WHITE, width_chars=40)

    body += text_svg(cols_x[1], section_y, "Selection, fixed", size=15, weight="bold")
    selection_fix = [
        "Ranked by SHAP value, not by absolute magnitude",
        "Only risk-increasing SHAP values become a customer-facing reason",
        "Risk-reducing values stay in the logs and model monitoring only",
    ]
    for i, item in enumerate(selection_fix):
        yy = section_y + 22 + i * (col_h + item_gap)
        body += box_block(cols_x[1], yy, col_w, col_h, [item], GREEN, width_chars=40)

    body += text_svg(cols_x[2], section_y, "Data contracts, hardened", size=15, weight="bold")
    data_fix = [
        "CRA and non-CRA lookback windows normalized to one standard",
        "Both CRA baseline and cash flow segments required together",
        "Checks run before scoring, so a bad feed never reaches a decision",
    ]
    for i, item in enumerate(data_fix):
        yy = section_y + 22 + i * (col_h + item_gap)
        body += box_block(cols_x[2], yy, col_w, col_h, [item], YELLOW, width_chars=40)

    body += text_svg(cols_x[3], section_y, "Pipeline, hardened", size=15, weight="bold")
    pipeline_fix = [
        "Every reason code audited against its template text, no gaps",
        "Rendering loops the full reason list, never just the first code",
        "Fully null feature sets get an explicit insufficient-information path",
    ]
    for i, item in enumerate(pipeline_fix):
        yy = section_y + 22 + i * (col_h + item_gap)
        body += box_block(cols_x[3], yy, col_w, col_h, [item], VIOLET, width_chars=40)

    render("board-2-the-fix", WIDTH, HEIGHT, body, title="SHAP driven adverse action, the corrected design")

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
        ("Direction, fixed", direction_fix, WHITE),
        ("Selection, fixed", selection_fix, GREEN),
        ("Data contracts, hardened", data_fix, YELLOW),
        ("Pipeline, hardened", pipeline_fix, VIOLET),
    ]
    for (title, items, color), cx in zip(columns, cols_x):
        elements.append(excal_text(cx, section_y - 14, title, font_size=15, width=col_w))
        for i, item in enumerate(items):
            yy = section_y + 22 + i * (col_h + item_gap)
            elements.append(excal_rect(cx, yy, col_w, col_h, bg=color))
            elements.append(excal_text(cx + 8, yy + 8, item, font_size=11, width=col_w - 16, height=col_h - 16))

    write_scene("board-2-the-fix", elements)


if __name__ == "__main__":
    build_fix_board()
