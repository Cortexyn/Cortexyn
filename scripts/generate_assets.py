#!/usr/bin/env python3
"""Generate the static, GitHub-safe SVG modules used by the profile README."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "profile.json"
ASSET_DIR = ROOT / "assets"

TEAL = "#1be0d0"
ORANGE = "#ff9b42"
INK = "#041416"
PANEL = "#082326"
TEXT = "#d9f5f2"
MUTED = "#83aaa8"


def escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def shell(width: int, height: int, title: str, description: str, body: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">{escape(title)}</title>
  <desc id="desc">{escape(description)}</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{INK}"/><stop offset="1" stop-color="#0b2023"/></linearGradient>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{TEAL}"/><stop offset=".72" stop-color="{TEAL}" stop-opacity=".35"/><stop offset="1" stop-color="{ORANGE}"/></linearGradient>
    <pattern id="grid" width="18" height="18" patternUnits="userSpaceOnUse"><path d="M18 0H0V18" fill="none" stroke="#a3fffa" stroke-opacity=".025"/></pattern>
  </defs>
  <style>
    .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace; }}
    .title {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace; font-weight:700; fill:{TEXT}; }}
    .muted {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace; fill:{MUTED}; }}
  </style>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="14" fill="url(#bg)" stroke="url(#edge)" stroke-width="2"/>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="14" fill="url(#grid)"/>
{body}
</svg>
'''


def focus_svg(item: dict[str, object]) -> str:
    title = escape(item["title"])
    code = escape(item["code"])
    lines = [escape(line) for line in item["lines"]]
    body = f'''  <path d="M18 48H202" stroke="{TEAL}" stroke-opacity=".25"/>
  <circle cx="26" cy="26" r="10" fill="none" stroke="{ORANGE}"/>
  <path d="M21 26h10M26 21v10" stroke="{ORANGE}" stroke-width="1.5"/>
  <text x="196" y="31" text-anchor="end" class="mono" fill="{TEAL}" font-size="11">NODE {code}</text>
  <text x="18" y="75" class="title" font-size="17">{title}</text>
  <g class="muted" font-size="13">
    <text x="18" y="103">{lines[0]}</text>
    <text x="18" y="124">{lines[1]}</text>
    <text x="18" y="145">{lines[2]}</text>
  </g>
  <circle cx="198" cy="143" r="3" fill="{TEAL}"/>
  <path d="M180 143h11" stroke="{TEAL}" stroke-opacity=".5"/>'''
    return shell(220, 164, str(item["title"]), ", ".join(item["lines"]), body)


def project_svg(item: dict[str, object]) -> str:
    accent = TEAL if item.get("accent") == "teal" else ORANGE
    tags = list(item["tags"])
    x = 24
    tag_markup: list[str] = []
    for tag in tags:
        width = 18 + len(str(tag)) * 8
        tag_markup.append(
            f'<rect x="{x}" y="132" width="{width}" height="24" rx="6" fill="#0b2c2f" stroke="{accent}" stroke-opacity=".55"/>'
            f'<text x="{x + width / 2:.1f}" y="148" text-anchor="middle" class="mono" fill="{TEXT}" font-size="11">{escape(tag)}</text>'
        )
        x += width + 10
    body = f'''  <path d="M0 48H580" stroke="{accent}" stroke-opacity=".23"/>
  <rect x="22" y="19" width="9" height="9" rx="2" fill="{accent}"/>
  <text x="43" y="30" class="mono" fill="{accent}" font-size="12" letter-spacing="1">{escape(item['kind'])}</text>
  <text x="556" y="30" text-anchor="end" class="mono" fill="{MUTED}" font-size="11">OPEN NODE ↗</text>
  <text x="24" y="78" class="title" font-size="23">{escape(item['title'])}</text>
  <text x="24" y="102" class="muted" font-size="14">{escape(item['description'])}</text>
  <text x="24" y="121" class="muted" font-size="12" fill-opacity=".78">{escape(item['detail'])}</text>
  {''.join(tag_markup)}
  <path d="M486 143h47l11-11" fill="none" stroke="{accent}" stroke-opacity=".5"/>
  <circle cx="548" cy="128" r="4" fill="none" stroke="{accent}"/>'''
    description = f"{item['title']}: {item['description']}. {item['detail']}"
    return shell(580, 176, str(item["title"]), description, body)


def stack_svg(items: list[str]) -> str:
    positions = [(38, 70), (250, 70), (490, 70), (705, 70), (865, 70), (38, 135), (245, 135), (402, 135), (555, 135), (890, 135)]
    widths = [190, 218, 193, 138, 174, 185, 135, 132, 313, 155]
    cards: list[str] = []
    if not (len(items) == len(positions) == len(widths)):
        raise ValueError("The stack layout must define exactly ten items")
    for index, (label, (x, y), width) in enumerate(zip(items, positions, widths)):
        color = TEAL if index % 3 else ORANGE
        cards.append(
            f'<rect x="{x}" y="{y}" width="{width}" height="42" rx="9" fill="#0a292c" stroke="{color}" stroke-opacity=".62"/>'
            f'<circle cx="{x + 20}" cy="{y + 21}" r="5" fill="{color}"/>'
            f'<text x="{x + 35}" y="{y + 27}" class="title" font-size="14">{escape(label)}</text>'
        )
    body = f'''  <text x="38" y="38" class="mono" fill="{TEAL}" font-size="13" letter-spacing="1.4">SYSTEM MATRIX // PUBLIC BUILD LOG</text>
  <text x="1162" y="38" text-anchor="end" class="mono" fill="{MUTED}" font-size="12">10 ACTIVE SIGNALS</text>
  {''.join(cards)}
  <path d="M38 205H400l24-17h338l24 17h376" fill="none" stroke="{ORANGE}" stroke-opacity=".42"/>
  <circle cx="424" cy="188" r="4" fill="{TEAL}"/><circle cx="786" cy="205" r="4" fill="{ORANGE}"/>'''
    return shell(1200, 230, "Cortexyn technology matrix", ", ".join(items), body)


def beyond_svg(items: list[dict[str, object]]) -> str:
    cards: list[str] = []
    for index, item in enumerate(items):
        x = 38 + index * 384
        accent = TEAL if index != 1 else ORANGE
        lines = item["lines"]
        cards.append(f'''<g transform="translate({x} 62)">
    <rect width="356" height="135" rx="12" fill="{PANEL}" stroke="{accent}" stroke-opacity=".55"/>
    <text x="20" y="31" class="mono" fill="{accent}" font-size="11" letter-spacing="1.3">{escape(item['code'])} // 0{index + 1}</text>
    <text x="20" y="63" class="title" font-size="19">{escape(item['title'])}</text>
    <text x="20" y="92" class="muted" font-size="13">{escape(lines[0])}</text>
    <text x="20" y="112" class="muted" font-size="13">{escape(lines[1])}</text>
    <circle cx="329" cy="25" r="4" fill="{accent}"/>
  </g>''')
    body = f'''  <text x="38" y="36" class="mono" fill="{ORANGE}" font-size="13" letter-spacing="1.4">OFF-DUTY SIGNALS // HUMAN LAYER</text>
  {''.join(cards)}'''
    description = "; ".join(f"{item['title']}: {' '.join(item['lines'])}" for item in items)
    return shell(1200, 225, "Beyond the code", description, body)


def generated_assets(data: dict[str, object]) -> dict[Path, str]:
    assets: dict[Path, str] = {}
    for item in data["focus"]:
        assets[ASSET_DIR / f"focus-{item['slug']}.svg"] = focus_svg(item)
    for item in data["projects"]:
        assets[ASSET_DIR / f"project-{item['slug']}.svg"] = project_svg(item)
    assets[ASSET_DIR / "tech-stack.svg"] = stack_svg(data["stack"])
    assets[ASSET_DIR / "beyond-code.svg"] = beyond_svg(data["beyond"])
    return assets


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated assets are not current")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    assets = generated_assets(data)
    stale: list[Path] = []
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    for path, content in assets.items():
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            stale.append(path)
            if not args.check:
                path.write_text(content, encoding="utf-8")
    if args.check and stale:
        names = ", ".join(str(path.relative_to(ROOT)) for path in stale)
        raise SystemExit(f"Generated assets are stale: {names}")
    verb = "Verified" if args.check else "Generated"
    print(f"{verb} {len(assets)} static SVG assets from {DATA_PATH.name}.")


if __name__ == "__main__":
    main()
