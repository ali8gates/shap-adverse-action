"""Builds the three whiteboards for this repo.

For each board this produces two files:
  - a real .excalidraw scene file, openable and editable in Excalidraw
  - a PNG preview of that scene, for display on GitHub

Random jitter uses a fixed seed so the hand-drawn wobble is reproducible.

Style note: this uses a plain white canvas, a light square dot grid, and
Excalidraw's own default palette for fills. Text uses a plain sans-serif
(Excalidraw's "Normal" font option) rather than a hand-lettered font, so
this board reads differently from the dot-paper board used elsewhere in
my other repos.
"""

import json
import random
import time
import uuid

BG = "#ffffff"
GRID = "#eceef1"
STROKE = "#1e1e1e"
TEXT_COLOR = "#1e1e1e"
MUTED = "#6b7280"

RED = "#ffc9c9"
GREEN = "#b2f2bb"
BLUE = "#a5d8ff"
YELLOW = "#ffec99"
VIOLET = "#eebefa"
ORANGE = "#ffd8a8"
WHITE = "#ffffff"

FONT = "Lato, 'DejaVu Sans', sans-serif"

random.seed(11)


def esc(text: str) -> str:
    return text.replace("&", "and").replace("<", "").replace(">", "")


def wobble_rect_path(x: float, y: float, w: float, h: float, jitter: float = 2.2) -> str:
    """A rounded rectangle path with a hand-drawn double-stroke feel, built
    from two slightly offset passes over the same corner points."""

    def pts():
        r = min(18, w / 4, h / 4)
        corners = [
            (x + r, y),
            (x + w - r, y),
            (x + w, y + r),
            (x + w, y + h - r),
            (x + w - r, y + h),
            (x + r, y + h),
            (x, y + h - r),
            (x, y + r),
        ]
        return [(px + random.uniform(-jitter, jitter), py + random.uniform(-jitter, jitter)) for px, py in corners]

    def path_from(points):
        d = f"M {points[0][0]:.1f} {points[0][1]:.1f} "
        for px, py in points[1:]:
            d += f"L {px:.1f} {py:.1f} "
        d += "Z"
        return d

    p1 = path_from(pts())
    p2 = path_from(pts())
    return p1, p2


def rough_rect_svg(x, y, w, h, fill, stroke=STROKE, sw=1.6) -> str:
    p1, p2 = wobble_rect_path(x, y, w, h)
    out = f'<path d="{p1}" fill="{fill}" stroke="none" opacity="0.9"/>\n'
    out += f'<path d="{p1}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>\n'
    out += f'<path d="{p2}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" opacity="0.55"/>\n'
    return out


def rough_line_svg(x1, y1, x2, y2, stroke=STROKE, sw=1.8, jitter=1.6) -> str:
    mx, my = (x1 + x2) / 2 + random.uniform(-jitter, jitter), (y1 + y2) / 2 + random.uniform(-jitter, jitter)
    return f'<path d="M {x1:.1f} {y1:.1f} Q {mx:.1f} {my:.1f} {x2:.1f} {y2:.1f}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"/>\n'


def arrow_svg(x1, y1, x2, y2, stroke=STROKE, sw=1.8, label: str | None = None) -> str:
    import math

    out = rough_line_svg(x1, y1, x2, y2, stroke=stroke, sw=sw)
    ang = math.atan2(y2 - y1, x2 - x1)
    for sign in (1, -1):
        a = ang + math.pi + sign * 0.42
        ex = x2 + 11 * math.cos(a)
        ey = y2 + 11 * math.sin(a)
        out += (
            f'<path d="M {x2:.1f} {y2:.1f} L {ex:.1f} {ey:.1f}" fill="none" '
            f'stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"/>\n'
        )
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - 8
        out += text_svg(mx, my, label, size=13, anchor="middle", color=MUTED, italic=True)
    return out


def wrap(text: str, width_chars: int) -> list[str]:
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if len(trial) > width_chars and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def text_svg(x, y, text, size=14, weight="normal", anchor="start", color=TEXT_COLOR, width_chars=40, italic=False, line_height=1.35) -> str:
    lines = wrap(text, width_chars)
    out = ""
    style = "italic" if italic else "normal"
    for i, line in enumerate(lines):
        out += (
            f'<text x="{x:.1f}" y="{y + i * size * line_height:.1f}" font-family="{FONT}" '
            f'font-size="{size}" font-weight="{weight}" font-style="{style}" fill="{color}" '
            f'text-anchor="{anchor}">{esc(line)}</text>\n'
        )
    return out


def sticky(x, y, w, h, title, body, fill, title_size=15, body_size=12.5, width_chars=None) -> str:
    out = rough_rect_svg(x, y, w, h, fill)
    wc = width_chars or max(18, int(w / 7.2))
    out += text_svg(x + 12, y + 24, title, size=title_size, weight="bold", width_chars=wc)
    out += text_svg(x + 12, y + 44, body, size=body_size, color=MUTED, width_chars=wc)
    return out


def grid_svg(width, height, step=20) -> str:
    out = f'<rect x="0" y="0" width="{width}" height="{height}" fill="{BG}"/>\n'
    dots = []
    for gx in range(0, width, step):
        for gy in range(0, height, step):
            dots.append(f'<circle cx="{gx}" cy="{gy}" r="1" fill="{GRID}"/>')
    out += "".join(dots) + "\n"
    return out


def frame(width, height, body_svg, title=None) -> str:
    header = ""
    if title:
        header = text_svg(28, 34, title, size=20, weight="bold", width_chars=90)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">\n{grid_svg(width, height)}{header}{body_svg}</svg>'
    )


def render(name: str, width: int, height: int, body_svg: str, title: str | None = None) -> None:
    svg = frame(width, height, body_svg, title=title)
    svg_path = f"/home/user/workspace/shap-aa/repo/excalidraw/{name}.svg"
    png_path = f"/home/user/workspace/shap-aa/repo/excalidraw/{name}.png"
    with open(svg_path, "w") as f:
        f.write(svg)
    import cairosvg

    cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=width * 2, output_height=height * 2)
    print(f"rendered {png_path}")


# ---------------------------------------------------------------------------
# .excalidraw scene builder (real, importable JSON)
# ---------------------------------------------------------------------------

def _seed():
    return random.randint(1, 2_000_000_000)


def excal_rect(x, y, w, h, bg=WHITE, stroke=STROKE, fill_style="hachure", roughness=1) -> dict:
    return {
        "id": str(uuid.uuid4()),
        "type": "rectangle",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0,
        "strokeColor": stroke,
        "backgroundColor": bg,
        "fillStyle": fill_style,
        "strokeWidth": 1,
        "strokeStyle": "solid",
        "roughness": roughness,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": {"type": 3},
        "seed": _seed(),
        "version": 1,
        "versionNonce": _seed(),
        "isDeleted": False,
        "boundElements": [],
        "updated": int(time.time() * 1000),
        "link": None,
        "locked": False,
    }


def excal_text(x, y, text, font_size=16, color=TEXT_COLOR, width=200, height=25, container_id=None) -> dict:
    return {
        "id": str(uuid.uuid4()),
        "type": "text",
        "x": x, "y": y, "width": width, "height": height,
        "angle": 0,
        "strokeColor": color,
        "backgroundColor": "transparent",
        "fillStyle": "hachure",
        "strokeWidth": 1,
        "strokeStyle": "solid",
        "roughness": 1,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": None,
        "seed": _seed(),
        "version": 1,
        "versionNonce": _seed(),
        "isDeleted": False,
        "boundElements": [],
        "updated": int(time.time() * 1000),
        "link": None,
        "locked": False,
        "text": text,
        "fontSize": font_size,
        "fontFamily": 2,
        "textAlign": "left",
        "verticalAlign": "top",
        "containerId": container_id,
        "originalText": text,
        "lineHeight": 1.25,
        "baseline": font_size,
    }


def excal_arrow(x1, y1, x2, y2, stroke=STROKE) -> dict:
    x, y = x1, y1
    w, h = x2 - x1, y2 - y1
    return {
        "id": str(uuid.uuid4()),
        "type": "arrow",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0,
        "strokeColor": stroke,
        "backgroundColor": "transparent",
        "fillStyle": "hachure",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 1,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": {"type": 2},
        "seed": _seed(),
        "version": 1,
        "versionNonce": _seed(),
        "isDeleted": False,
        "boundElements": [],
        "updated": int(time.time() * 1000),
        "link": None,
        "locked": False,
        "points": [[0, 0], [w, h]],
        "lastCommittedPoint": None,
        "startBinding": None,
        "endBinding": None,
        "startArrowhead": None,
        "endArrowhead": "triangle",
    }


def make_scene(elements: list[dict]) -> dict:
    return {
        "type": "excalidraw",
        "version": 2,
        "source": "https://github.com/ali8gates/shap-adverse-action",
        "elements": elements,
        "appState": {
            "gridSize": 20,
            "viewBackgroundColor": "#ffffff",
        },
        "files": {},
    }


def write_scene(name: str, elements: list[dict]) -> None:
    scene = make_scene(elements)
    path = f"/home/user/workspace/shap-aa/repo/excalidraw/{name}.excalidraw"
    with open(path, "w") as f:
        json.dump(scene, f, indent=2)
    print(f"wrote {path}")


def box_with_label(elements, x, y, w, h, title, body, bg):
    r = excal_rect(x, y, w, h, bg=bg)
    elements.append(r)
    elements.append(excal_text(x + 10, y + 10, title, font_size=16, width=w - 20, height=22))
    elements.append(excal_text(x + 10, y + 34, body, font_size=13, color="#495057", width=w - 20, height=h - 40))


if __name__ == "__main__":
    from board_problem import build_problem_board
    from board_fix import build_fix_board
    from board_outcomes import build_outcomes_board

    build_problem_board()
    build_fix_board()
    build_outcomes_board()
