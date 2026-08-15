# Plainsight Visual & Brand Guidelines

> **Internal reference only**: not published in the playbook.
> **Source of truth:** the [Plainsight Brand Kit](https://github.com/PlainsightPro/brand-kit). This document mirrors it for search. When they disagree, the brand kit wins. For automated output, agents must read `assets/templates/brand.json` from the brand kit whole and place the asset files directly.

---

## The Golden Rule for Agents

If you produce any Plainsight-branded output (slides, proposals, posts, diagrams, web pages): fetch the brand kit repo (`PlainsightPro/brand-kit`), read `assets/templates/brand.json` in full, and place the logo and triangle **asset files** from `assets/`. Never redraw the triangle or logo from a description. Redrawn triangles are the number one source of off-brand output (filled or sharp-cornered triangles). The Plainsight triangle is always a **wireframe outline with rounded corners, never a solid filled shape**.

---

## Color Scheme

| Role | Hex | Usage |
|---|---|---|
| **Blue** | `#000075` | Primary brand color, headings, dark backgrounds |
| **Orange** | `#d5693a` | Accent only: links, highlights, CTAs, bullets. Never a full-section or full-slide background |
| **Orange (triangle asset only)** | `#BD5428` | Appears only inside `triangle-orange.svg`. Not a UI color |
| **Cream** | `#fcf8f3` | Default page and slide background |
| **White** | `#ffffff` | Cards and content containers |
| **Mist** | `#f6f6fa` | Light background variant |
| **Muted cream** | `#F3ECE4` | Alternating section backgrounds (web) |
| **Dark text** | `#1a1a3e` | Body text on light backgrounds |
| **Muted blue** | `#8888bb` | Secondary metadata, labels, counters |
| **Light navy** | `#b0b0d0` | Subtitle text on dark backgrounds |
| **Light gray** | `#e8e8e8` | Subtle card borders |

Rules: blue and cream alternate as backgrounds, white is for cards, orange is always an accent and never a background. Text on blue is white or light navy; text on cream is blue or dark text. All pairings meet WCAG AA.

### Medallion / Semantic Layer Colors (Mermaid diagrams)

| Layer | Fill | Stroke | Text |
|---|---|---|---|
| **Bronze** (Landing / Staging) | `#CD7F32` | `#8B4513` | Light (`#FFFFFF`) |
| **Silver** (ADS / Intermediate) | `#C0C0C0` | `#808080` | Dark (`#111827`) |
| **Gold** (Business products: dims/facts/OBT/feature store) | `#FFD700` | `#DAA520` | Dark (`#111827`) |

Use dashed strokes (`stroke-dasharray: 5 5`) for optional components. These fills apply to medallion diagram boxes only, never to the Plainsight triangle, which is always a wireframe outline and never filled.

---

## Typography

| Element | Font | Notes |
|---|---|---|
| Headings | **Titillium Web**, bold, uppercase for section headings | Fallback: Segoe UI, Arial |
| Body | **Epilogue** | Fallback: Segoe UI, Arial |

Maximum 2 font weights per slide or section. No italics in carousels or slides. Short blocks: 1-2 sentences per paragraph on slides.

---

## Triangle Decoration System

The Plainsight triangle is the signature brand mark used as corner decoration on slides, website sections, and marketing materials. It is a **wireframe outline triangle with rounded corners. It is never rendered as a solid filled triangle.** Always place the canonical asset files from the brand kit; never redraw the shape.

### Assets

Canonical files in the brand kit under `assets/graphics/`:

| File | Outline color | Native size | Use on |
|---|---|---|---|
| `triangle-blue.svg` (+ `.png`) | Blue `#000075` | 313 × 358 px | Light / cream backgrounds |
| `triangle-orange.svg` (+ `.png`) | Orange `#BD5428` | 313 × 358 px | Blue backgrounds, hero accents |
| `triangle-white.svg` (+ `.png`) | White | 313 × 358 px | Blue or dark backgrounds |

Note for implementers: inside the SVG files the wireframe outline is painted via a `fill` attribute on the traced path. That is an SVG implementation detail. The triangle as seen on the canvas is a wireframe outline, never a solid filled shape.

### Color Pairing Rule

Pick the triangle color that **contrasts** with the background:

| Background | Triangle to use |
|---|---|
| Light / cream (`#fcf8f3`) | Blue (`triangle-blue.svg`) |
| Blue (`#000075`) | Orange (`triangle-orange.svg`) or White |
| Dark / black | White (`triangle-white.svg`) or Orange |

Only these three triangle colors exist. The triangle is always the wireframe outline asset, never a filled shape and never recolored.

### Rendering Parameters (LinkedIn slides, 1080 × 1350)

- **Scale:** 1.1× native → **344 × 394 px** per triangle
- **Pairs:** triangles appear in asymmetric pairs, two same-sized wireframe triangles offset from each other
- **Offset within a pair:** 90 px horizontal, 60 px vertical
- **Visibility:** 60% of each triangle visible; 40% bleeds off the canvas edge
- Always place the asset files (`triangle-blue.svg` etc.); never redraw or fill the triangle

### Top-Right Pair Positioning

Two equally-sized wireframe triangles (asset files, never redrawn, never filled), asymmetrically nested for an overlapping outline effect:

```
Back triangle:
  x = WIDTH − tri_w + 30
  y = HEIGHT − 0.4 × tri_h

Front triangle:
  shifted left 90 px and down 60 px from the back triangle
```

The back triangle sits closer to the corner (more hidden); the front triangle is more visible, creating depth. Used in LinkedIn Template A (together with the bottom-left pair).

### Bottom-Left Pair Positioning

Creates a "mountain silhouette" effect with the right triangle sitting higher. Same rule as everywhere: wireframe outline asset files, never filled.

```
Left triangle (lower):
  x = −30
  y = −0.4 × tri_h − 60

Right triangle (higher):
  x = −30 + 120
  y = −0.4 × tri_h
```

Used in both LinkedIn templates (Template B uses only this pair).

### Placement by Medium

| Context | Where | Color | Notes |
|---|---|---|---|
| LinkedIn Template A | Top-right + bottom-left pairs | Blue | Geometry above |
| LinkedIn Template B | Bottom-left pair only | Blue | Cleaner top area |
| Website cream sections | Top-right corner | Blue at 10-15% opacity | |
| Website navy sections | Top-right + bottom-left | White at 5-10% opacity | CTA/footer only |
| Website hero | Top-right, one triangle max | Orange or blue | |
| Presentations | Corner decoration | Match background | Subtle, never obscure content |

### Hard Rules

1. Never fill the triangle with a solid color; it is a wireframe outline with rounded corners.
2. Never redraw or approximate the triangle; place the asset files.
3. Only three triangle colors exist: blue, orange, white.
4. One motif per piece: triangles or rocket, not both.
5. No triangle larger than one third of the page; they are accents, not heroes.
6. Decorative only: never obscure text or interactive content (`pointer-events: none`, `aria-hidden="true"`).

---

## Logo

Canonical files in the brand kit under `assets/logos/`: `plainsight-logo-blue.svg` for light backgrounds, `plainsight-logo-white.svg` for blue or dark backgrounds. Always place the asset files; never redraw or restyle the logo.

| Medium | Placement |
|---|---|
| LinkedIn visuals | Bottom-right, 150 px wide, 36 px from bottom edge, blue version |
| Website | Header 160 × 28 px; blue on light, white on navy footer |
| Presentations | Title and closing slides only, bottom-right, matched to background |
| MkDocs site header | Height `1.6rem` |

---

## Website Header Adaptation (MkDocs docs site)

For the MkDocs site header (blue `#000075` background): orange wireframe triangle pair (asset files, never filled), scaled to `0.22` of native (≈ 69 × 79 px), offsets scaled proportionally (~20 px horizontal, ~13 px vertical), back triangle ~41% hidden off the right and top edges, rendered via CSS `::after` on `.md-header`, hidden on mobile (`max-width: 76.25em`).

---

## Dark Mode Overrides (docs site)

| Element | Color |
|---|---|
| Nav section headers | `#8888cc` |
| Primary | Same as light (`#000075`) |
| Accent | Same as light (`#d5693a`) |
