# Stitch — Design System

Stitch is a tailoring shop order ledger: customers, cloth stock, garments, orders, and
due dates. The auth pages (`login.html`, `registration.html`) already established a real
visual identity — a tailor's measuring tape rendered as a dark editorial panel next to a
warm paper-like form. Every other page (home, gender picker, add order, garment picker,
all orders, all customers) currently falls back to raw Bootstrap 4 defaults and needs to
be brought into this same identity. This document is the single source of truth for
extending that identity consistently.

**Do not invent a new visual direction.** The job here is extension, not a redesign.

---

## 1. Concept

The tailor's tape measure is the signature motif: a vertical rule with tick marks and
numbers, already used on the auth screen. Carry it through as a structural device —
not just decoration — anywhere it can legitimately encode something real: order
sequence numbers, days-remaining countdowns, measurement fields, table row markers.

The overall feel: a small, well-run tailoring shop's paper ledger, digitized. Warm,
precise, unfussy. Not a generic SaaS admin dashboard.

---

## 2. Color palette

| Token | Hex | Use |
|---|---|---|
| `--ink` | `#1a1a2e` | Primary text, dark panels, nav/footer background |
| `--paper` | `#FAF7F2` | Light panel background, page background |
| `--paper-alt` | `#f8f9fa` | Secondary surface (currently `body` background in `style.css`) |
| `--accent` | `#534AB7` | Primary actions, links, focus states |
| `--accent-hover` | `#3C3489` | Hover state for accent |
| `--rule` | `#d8d4c8` | Input underlines, hairline dividers on paper surfaces |
| `--muted` | `#76746e` | Secondary/help text on paper surfaces |
| `--muted-dark` | `#9a98ab` | Secondary text on dark surfaces |
| `--tape-line` | `#43405a` / `#6f6c89` | Tape rail / tick marks on dark surfaces |
| `--error` | `#A32D2D` | Error text, invalid field borders |
| `--error-bg` | `#FCEBEB` | Error banner background |
| `--error-border` | `#F09595` | Error banner border |
| `--urgent` | `#B5651D` (proposed) | Status = Urgent badge |
| `--success` | `#2E7D32` (proposed) | Status = Delivered/Complated badge |

Do not introduce new accent hues. If a status color is needed beyond what's listed
(Confirmed, Processing, Urgent, Complated, Delivered, Cenceled), derive it as a tint of
`--ink` or `--muted` rather than adding a new saturated color to the palette.

---

## 3. Typography

| Role | Family | Notes |
|---|---|---|
| Display / headings | `Fraunces` (already loaded via Google Fonts, opsz axis 9..144) | Used at weight 400–500 only. This carries the "ledger" personality — don't use it for body copy or UI chrome. |
| Body / UI | System stack: `'Segoe UI', system-ui, -apple-system, sans-serif` | Everything else: labels, buttons, table cells, nav. |
| Numeric / data / measurements | `JetBrains Mono` (already loaded) | Use for anything that reads as a measurement, count, or precise figure: order IDs, day counters, tape numbers, phone numbers in tables. This is what makes numbers feel "measured" rather than incidental. |

Type scale (already established in `style.css`, keep consistent):
- h1: 2rem / 700
- h2: 1.5rem / 600
- h3: 1.25rem / 600
- h4: 1rem / 600
- body: 16px / 1.6 line-height
- auth-heading (Fraunces): 1.65rem / 500 — use this scale for page titles too, not h1 Segoe UI, to keep the editorial voice on every page, not just auth.

---

## 4. Layout & structure

- Sticky dark nav (`#1a1a2e`), already built in `base.html` — keep as-is.
- Content max-width: 1100px, centered (`.container`, `main` already do this) — reuse, don't redeclare.
- Cards/panels on paper background (`#FAF7F2` or `#f8f9fa`) with generous padding (2–3rem), soft shadow, no hard borders — matching `.auth-screen`'s `border-radius: 14px` and `box-shadow: 0 30px 80px -20px rgba(0,0,0,0.45)` treatment, scaled down for inline page content (a card doesn't need a shadow that heavy; use something like `0 8px 24px -8px rgba(0,0,0,0.12)` for in-page cards, reserving the dramatic shadow for full-screen moments like auth).
- Forms: underline-style inputs (no boxes), per `.auth-field input` — apply this to every form in the app (add order, garment picker, gender picker) instead of Bootstrap's default boxed `<select>`/`<input>`, for consistency.
- Tables (All Orders, All Customers): strip Bootstrap's default look. Use hairline row dividers (`--rule`), Fraunces for nothing here (tables stay in body/mono type), JetBrains Mono for numeric columns (Days, phone, due date), and status as a small pill/badge rather than plain text.
- Buttons: one primary style (accent fill, per `.auth-submit`), one secondary/ghost style (outline or text-only, `--ink` or `--muted`), one destructive style (`--error`). Retire ad hoc Bootstrap `.btn-dark`, `.btn-danger`, etc. in favor of these three.

---

## 5. The tape-measure motif — where else it can go

Already used: vertical tape on the auth dark panel.

Extend to (only where it means something, not as decoration):
- **Garment picker / order builder**: a horizontal or vertical tape showing progress through the multi-step session flow (gender → garment → measurements → confirm), with ticks marking each step — this is a real sequence, so numbering is justified here.
- **All Orders table**: the `Days` / `Due` column can borrow the tape's tick-mark typography (JetBrains Mono, small caps label) to reinforce "this is a measured countdown," especially once the urgency auto-update (Urgent status at ≤2 days) ships — a tape running low visually reinforces urgency better than a plain number.
- **Order detail page**: measurements (chest, waist, length, etc., in `Cloth`/`Order` models) are the most literal use of a tape — render actual measurement fields against a ruled/ticked background.

Do not add the tape motif to pages where it doesn't correspond to something real (e.g. the customer list, login confirmation states) — per the design principle, structural devices must encode true information, not decorate.

---

## 6. Tech stack (current, as found in the repo)

- **Backend**: Django 5.2.15, apps: `AuthApp`, `Order`, `Cloth`, `Bill`
- **Templates**: Django Template Language, `base.html` (main app) + `auth_base.html` (auth screens) as the two layout roots
- **CSS**: plain CSS in `static/css/style.css` (global) and `static/css/auth.css` (auth-specific) — no preprocessor, no Tailwind/build step
- **JS**: jQuery 3.6 (loaded in `base.html`) + vanilla `<script>` blocks per template (e.g. delete-modal wiring in `allOrders.html`/`allCustomer.html`)
- **UI framework**: Bootstrap 4 (via CDN) — currently used inconsistently (raw `.btn-dark`, `.table-hover`, modal component) and is the main source of the "generic" look; the design direction above intentionally moves away from Bootstrap's visual defaults while keeping its modal/JS behavior where already wired up (delete confirmation modals) to avoid a rewrite of working interaction logic.
- **Fonts**: Google Fonts — Fraunces (variable, opsz 9..144, weights 400/500), JetBrains Mono (400/500) — already linked in `auth_base.html`; needs to be added to `base.html` too so non-auth pages can use them.
- **Icons**: Font Awesome 4.7 (CDN, already in `base.html`)

No component library, no CSS framework rewrite is in scope — this is about disciplined use of existing plain CSS, extended consistently, not a stack change.

---

## 7. Pages needing this treatment (in priority order)

1. `templates/home.html` — currently empty; needs to become the dashboard/landing view
2. `Order/templates/Order/allOrders.html` — main table view, Bootstrap defaults
3. `AuthApp/templates/AuthApp/allCustomer.html` — same table pattern, same fix
4. `Order/templates/Order/gender.html` — bare two-button form, no styling at all
5. `Order/templates/Order/addOrder.html` — bare form, no styling, doesn't even extend `base.html` currently
6. `Order/templates/Order/garment_picker.html` — bare form + garment list, extends `base.html` but unstyled

Already on-brand and should be used as the reference: `login.html`, `registration.html`, `auth_base.html`, `auth.css`.

---

## 8. What "done" looks like for each page

- Uses `--ink` / `--paper` / `--accent` tokens above, no ad hoc colors
- Headings in Fraunces, body/UI in the system sans stack, numeric data in JetBrains Mono
- Forms use underline-style fields, not Bootstrap boxed inputs
- Buttons reduced to the three defined styles (primary/secondary/destructive)
- No unstyled Bootstrap defaults left showing (`.table`, `.btn-dark`, etc. either restyled or removed)
- Responsive down to mobile (auth screen's `@media (max-width: 760px)` pattern is the reference for how to collapse a two-panel/table layout)
- Visible keyboard focus retained on all interactive elements
- Any addition of the tape motif is justified by real sequence/measurement content, not decoration

---

Fill in `[PAGE NAME]` / `[template path]` per the priority list in §7 and run it once
per page rather than all six at once — this keeps each diff reviewable and prevents
drift from the documented system.
