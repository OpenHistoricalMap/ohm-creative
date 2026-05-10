"""
Keeps designs_wip/icons/DESCRIPTIONS.md in sync with the SVGs in that folder:

- For each SVG present but missing from DESCRIPTIONS.md, calls Claude to read
  the SVG and generate a display name + one-sentence description, then appends
  the entry.
- For each DESCRIPTIONS.md entry whose SVG no longer exists, removes the entry.

Preserves the file header (everything before the first `## ` section) and the
relative order of all entries that remain valid.
"""

import re
import sys
from pathlib import Path

import anthropic

ICONS_DIR = Path("designs_wip/icons")
DESCRIPTIONS_FILE = ICONS_DIR / "DESCRIPTIONS.md"
SKIP = {"00-grid.svg"}
# Skip Claude call for SVGs larger than this — they blow past the model's
# input-token limit. Falls back to a filename-derived stub entry instead.
MAX_SVG_BYTES = 80_000


def is_favico(filename: str) -> bool:
    return filename.endswith("-favico.svg")


def parse_descriptions(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Split the file into (header, [(filename, raw_block), ...]) preserving order.

    Header is everything before the first `## ` line. Each entry's raw_block is
    the full text of that section, starting with the `## filename.svg` line.
    """
    parts = re.split(r"(?=^## )", text, flags=re.MULTILINE)
    header = ""
    entries: list[tuple[str, str]] = []
    for part in parts:
        if part.startswith("## "):
            first_line = part.split("\n", 1)[0]
            filename = first_line[3:].strip()
            if filename.endswith(".svg"):
                entries.append((filename, part.rstrip()))
        else:
            header = part
    return header, entries


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
    header, entries = parse_descriptions(existing_text)

    current_svgs = {
        f.name for f in ICONS_DIR.glob("*.svg")
        if f.name not in SKIP and not is_favico(f.name)
    }
    existing_names = {filename for filename, _ in entries}

    # Drop stale entries (SVG no longer in the folder)
    stale = existing_names - current_svgs
    if stale:
        for s in sorted(stale):
            print(f"  Dropping stale entry: {s}")
        entries = [(f, b) for f, b in entries if f not in stale]

    # Generate entries for missing SVGs
    missing = sorted(current_svgs - existing_names)
    added = 0
    for filename in missing:
        svg_path = ICONS_DIR / filename
        size = svg_path.stat().st_size

        if size > MAX_SVG_BYTES:
            print(
                f"  ⚠  {filename} is {size:,} bytes — too large for Claude. "
                f"Using filename-based stub."
            )
            entry = {
                "name": filename_stem(filename).title(),
                "description": (
                    "Auto-description skipped (SVG exceeds size limit). "
                    "Please edit this entry manually."
                ),
            }
        else:
            print(f"  Generating entry for {filename}…", flush=True)
            try:
                entry = generate_entry(filename, svg_path.read_text())
            except Exception as e:
                print(f"  ⚠  Claude call failed for {filename}: {e}. Using stub.")
                entry = {
                    "name": filename_stem(filename).title(),
                    "description": (
                        "Auto-description failed. Please edit this entry manually."
                    ),
                }

        print(f"    name: {entry['name']}")
        print(f"    description: {entry['description']}")
        block = (
            f"## {filename}\n"
            f"name: {entry['name']}\n"
            f"description: {entry['description']}"
        )
        entries.append((filename, block))
        added += 1

    if not stale and not missing:
        print("DESCRIPTIONS.md is in sync — nothing to do.")
        return 0

    new_text = header.rstrip() + "\n\n" + "\n\n".join(b for _, b in entries) + "\n"
    DESCRIPTIONS_FILE.write_text(new_text)

    print(f"\nDESCRIPTIONS.md updated: +{added} added, -{len(stale)} dropped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
