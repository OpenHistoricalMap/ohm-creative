"""
Checks designs_wip/icons/ for SVG files not yet in DESCRIPTIONS.md.
For each missing file, calls Claude to read the SVG and generate a
display name and one-sentence description, then appends the entry.
"""

import re
import sys
from pathlib import Path

import anthropic

ICONS_DIR = Path("designs_wip/icons")
DESCRIPTIONS_FILE = ICONS_DIR / "DESCRIPTIONS.md"
SKIP = {"00-grid.svg"}


def parse_descriptions(text: str) -> set[str]:
    """Return the set of filenames that already have an entry."""
    found = set()
    for section in re.split(r"\n## ", text):
        first_line = section.strip().split("\n")[0].strip()
        if first_line.endswith(".svg"):
            found.add(first_line)
    return found


def filename_stem(filename: str) -> str:
    """'08-map-hourglass-cutout.svg' -> 'map hourglass cutout'"""
    base = filename.removesuffix(".svg")
    m = re.match(r"^\d+[^a-zA-Z]*(.*)", base)
    return (m.group(1) if m else base).replace("-", " ").replace("_", " ")


def generate_entry(filename: str, svg_content: str) -> dict:
    client = anthropic.Anthropic()
    stem = filename_stem(filename)

    prompt = f"""This SVG is a logo concept for OpenHistoricalMap (OHM), \
an open-source historical mapping project. The filename hint is "{stem}".

SVG content:
{svg_content}

Provide a display name and a one-sentence visual description for use in a \
design-review gallery. Be specific about shapes and colors you can read from \
the SVG. Keep the description under 25 words.

Reply in exactly this format (no extra text):
name: <2-4 word title-case name>
description: <one sentence>"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=128,
        messages=[{"role": "user", "content": prompt}],
    )

    text = message.content[0].text
    name_m = re.search(r"^name:\s*(.+)$", text, re.MULTILINE)
    desc_m = re.search(r"^description:\s*(.+)$", text, re.MULTILINE)

    return {
        "name": name_m.group(1).strip() if name_m else stem.title(),
        "description": desc_m.group(1).strip() if desc_m else "",
    }


def main() -> int:
    existing_text = DESCRIPTIONS_FILE.read_text() if DESCRIPTIONS_FILE.exists() else ""
    already_described = parse_descriptions(existing_text)

    svgs = sorted(f for f in ICONS_DIR.glob("*.svg") if f.name not in SKIP)
    missing = [f for f in svgs if f.name not in already_described]

    if not missing:
        print("All SVGs already have descriptions — nothing to do.")
        return 0

    print(f"{len(missing)} SVG(s) need descriptions: {[f.name for f in missing]}")

    new_blocks = []
    for svg_path in missing:
        print(f"  Generating entry for {svg_path.name}…", flush=True)
        entry = generate_entry(svg_path.name, svg_path.read_text())
        print(f"    name: {entry['name']}")
        print(f"    description: {entry['description']}")
        new_blocks.append(
            f"\n## {svg_path.name}\n"
            f"name: {entry['name']}\n"
            f"description: {entry['description']}\n"
        )

    with DESCRIPTIONS_FILE.open("a") as f:
        f.write("\n" + "".join(new_blocks))

    print(f"\nAppended {len(new_blocks)} entry/entries to {DESCRIPTIONS_FILE}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
