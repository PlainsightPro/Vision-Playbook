# Plainsight Visual & Brand Guidelines

> **Internal reference only** — not published in the playbook.
> This document captures the visual system used across Plainsight slides, website, and branded materials.

---

## Color Scheme

| Role | Hex | Usage |
|---|---|---|
| **Dark Blue** | `#000075` | Primary brand color, headers, nav sections, backgrounds |
| **Orange** | `#D5693A` | Accent color, links, highlights, CTAs |
| **Orange (SVG variant)** | `#BD5428` | Used in the `driehoek oranje.svg` brand asset |
| **Cream** | `#FCF8F3` | Default page background |
| **Light cream** | `#FDFAF7` | Light background variant |
| **Light blue** | `#1a1a9a` | Primary light variant |
| **Dark blue (dark)** | `#00005a` | Primary dark variant |

### Medallion / Semantic Layer Colors (Mermaid diagrams)

| Layer | Fill | Stroke | Text |
|---|---|---|---|
| **Bronze** (Landing / Staging) | `#CD7F32` | `#8B4513` | Light (`#FFFFFF`) |
| **Silver** (ADS / Intermediate) | `#C0C0C0` | `#808080` | Dark (`#111827`) |
| **Gold** (Business products: dims/facts/OBT/feature store) | `#FFD700` | `#DAA520` | Dark (`#111827`) |

Use dashed strokes (`stroke-dasharray: 5 5`) for optional components.

---

## Triangle Decoration System

The Plainsight triangle is the signature brand mark used as corner decoration on slides, website headers, and marketing materials.

### Assets

| File | Color | Native Size | Fill |
|---|---|---|---|
| `driehoek blauw.svg` | Dark blue | 313 × 358 px | `#000075` |
| `driehoek oranje.svg` | Orange | 313 × 358 px | `#BD5428` |
| `driehoek wit.svg` | White | 313 × 358 px | White |

### Color Pairing Rule

Pick the triangle color that **contrasts** with the background:

| Background | Triangle pair to use |
|---|---|
| Light / cream (`#FCF8F3`) | Blue (`driehoek blauw.svg`) |
| Dark blue (`#000075`) | Orange (`driehoek oranje.svg`) |
| Dark / black | White (`driehoek wit.svg`) or Orange |

### Rendering Parameters

- **Scale:** 1.1× native → **344 × 394 px** per triangle
- **Gap between overlapping pair:** 90 px horizontal, 60 px vertical
- **Visibility:** 60% of each triangle is visible; 40% is hidden off the canvas edge

### Top-Right Pair Positioning

Two equally-sized triangles, asymmetrically nested to create an overlapping outline effect.

```
Back triangle:
  x = WIDTH − tri_w + 30
  y = HEIGHT − 0.4 × tri_h

Front triangle:
  shifted left 90 px and down 60 px from the back triangle
```

The back triangle sits closer to the corner edge (more hidden). The front triangle is more visible, creating depth.

```
    ╭──────────────────────────────╮
    │                     ╱╲  ←back│  (40% hidden beyond edge)
    │                   ╱╱  ╲╲    │
    │                 ╱╱      ╲╲  │
    │               ╱╱    ╱╲   ╲╲ │
    │             ╱╱    ╱    ╲  ╲╲│
    │           ╱╱    ╱        ╲  │
    │         ╱╱    ╱  ←front   ╲ │
    │        ╱────╱──────────────╲│
    │                              │
    ╰──────────────────────────────╯
```

### Bottom-Left Pair Positioning

Creates a "mountain silhouette" effect with the right triangle sitting higher.

```
Left triangle (lower):
  x = −30
  y = −0.4 × tri_h − 60

Right triangle (higher):
  x = −30 + 120
  y = −0.4 × tri_h
```

```
    ╭──────────────────────────────╮
    │                              │
    │  ╱╲                          │
    │╱    ╲   ╱╲  ←right (higher)  │
    │       ╲╱    ╲                │
    │╱╲      ╲      ╲             │
    │  ←left  ╲──────╲────────────│
    │(lower)                       │
    ╰──────────────────────────────╯
```

### Website Header Adaptation

For the MkDocs site header (dark blue `#000075` background):

- Uses **orange** triangles (`#D5693A` accent)
- Proportionally scaled down to fit header height (~60px)
- Scale factor: `0.22` of native (triangle ≈ 69 × 79 px)
- Gap proportionally scaled: ~20 px H, ~13 px V
- Back triangle at ~41% hidden off right and top edges
- Front triangle more visible, shifted left and down
- Rendered via CSS `::after` pseudo-element on `.md-header`
- Hidden on mobile (`max-width: 76.25em`)
- Asset: `docs/assets/triangles-header.svg`

---

## Typography

| Element | Weight | Size |
|---|---|---|
| Page title (`h1`) | 700 (bold) | 2.2em |
| Nav section headers | 700 (bold) | — |

---

## Logo

- Header logo height: `1.6rem`
- Asset: `docs/assets/logo.svg`
- Subheader link style: orange text (`#D5693A`), `0.65rem` font size

---

## Dark Mode Overrides

| Element | Color |
|---|---|
| Nav section headers | `#8888cc` |
| Primary | Same as light (`#000075`) |
| Accent | Same as light (`#D5693A`) |
