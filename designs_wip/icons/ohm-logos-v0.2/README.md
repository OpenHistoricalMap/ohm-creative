# ohm-logos-v0.2

OpenHistoricalMap logo concept set, version 0.2.

14 candidate concepts. Numbering preserves history: there is no #12 (an earlier
concept was retired during exploration).

## Changes from v0.1

- **#3 Pyramid + tower**: pyramid scaled to 90% with left edge fixed at x=14;
  tower body shifted right by 15% of its width (3.6 units in 100-unit canvas).
- All other concepts unchanged from v0.1.

## Files

- `00-grid.svg` — overview grid showing all 14 concepts at 128×128
- `01` through `15` — individual concept SVGs (skipping `12`)
- `variations/` — exploration artifacts that are NOT part of the canonical set

## Concepts

| #  | Name                       | Notes                                                                |
|----|----------------------------|----------------------------------------------------------------------|
| 01 | Hourglass globe            | Teal hourglass + amber bulbs                                         |
| 02 | Hourglass + water/land     | Indigo hourglass + nested water/land bulbs                           |
| 03 | Pyramid + tower            | Forest pyramid (90%) + ochre tower (shifted right)                   |
| 04 | Sundial                    | Burgundy half-disc + cream gnomon                                    |
| 05 | Folded map                 | Slate map silhouette + slate-ochre time arrow                        |
| 06 | Simplification             | Olive map + parchment circle (magnifying glass) + dark teal H        |
| 07 | Negative space             | Dark teal map silhouette with parchment circle + teal H              |
| 08 | Map + hourglass cutout     | Dark teal map silhouette with hourglass-shaped cutout                |
| 09 | Map + sundial cutout       | Dark teal map silhouette with half-disc cutout + gray gnomon overlay |
| 10 | OHM concept                | Three-silhouette overlap: green map, blue circle, orange hourglass   |
| 11 | OHM with border            | OHM concept with parchment hourglass outline                         |
| 13 | Square monster             | 90-degree winding line, 9 filled rectangles, parchment background    |
| 14 | Curved monster             | Single stroked path, smooth corners, parchment background            |
| 15 | Curved monster + water     | Curved monster overlay on parchment-and-water split background       |

## Design tokens

- OHM green: `#6b9938` / curved monster green: `#6b9940`
- OHM blue: `#4f7aaa`
- OHM orange: `#e07a00`
- Parchment: `#f4ead5` / curved monster parchment: `#f3ead5`
- Dark teal: `#1a4a52`
- Olive: `#7a9a44`
- Sundial gnomon gray: `#c8d0d0`
- Water blue: `#aac2e5`

## Source-of-truth notes

- All concepts use a 100×100 viewBox unless noted (concept 5 is `-15 0 130 100`,
  concepts 10–11 are `0 0 200 200`, concepts 14–15 are `0 0 80 80`).
- Concepts 14 and 15 are copies of authoritative files exported from
  Adobe Illustrator.
- Other concepts are programmatically generated.
