# ----------------------------------------------------------------- social cards: one number per generated page (GEO strategy 6.3)
# A 1200 x 630 PNG per model, grid, glossary, compare and answer page, drawn from the same values as the page, in the
# design of assets/social-card.png (dark paper, the mark, Archivo for the figure, IBM Plex Mono for the labels).
# Pillow is a build dependency for the cards only: without it the build keeps the PNGs already on disk and says so.
FONTS = HERE / "fonts"
CARDS_REL = "assets/cards"
CARD_W, CARD_H = 1200, 630
CARD_BG, CARD_INK, CARD_INK2, CARD_MUTED, CARD_MINT, CARD_RULE = "#0E1411", "#E7EEE9", "#C9D2CD", "#8E9A93", "#5FCF97", "#1F6B47"
outputs_bin: dict[str, bytes] = {}
try:
    from PIL import Image as _PILImage, ImageDraw as _PILDraw, ImageFont as _PILFont
    CARDS_OK = all((FONTS / f).exists() for f in ("Archivo[wdth,wght].ttf", "IBMPlexMono-Regular.ttf", "IBMPlexMono-Medium.ttf"))
except ImportError:   # pragma: no cover
    CARDS_OK = False
_font_cache: dict[tuple, object] = {}


def _font(kind: str, size: int):
    key = (kind, size)
    if key not in _font_cache:
        if kind in ("bold", "medium"):
            f = _PILFont.truetype(str(FONTS / "Archivo[wdth,wght].ttf"), size)
            f.set_variation_by_axes([700 if kind == "bold" else 500, 100])   # axes: weight, width
        else:
            f = _PILFont.truetype(str(FONTS / ("IBMPlexMono-Medium.ttf" if kind == "mono-medium" else "IBMPlexMono-Regular.ttf")), size)
        _font_cache[key] = f
    return _font_cache[key]


def _wrap(draw, text: str, font, max_w: int, max_lines: int) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while draw.textlength(last + "...", font=font) > max_w and " " in last:
            last = last.rsplit(" ", 1)[0]
        lines[-1] = last.rstrip(",;:.") + "..."
    return lines


def card_png(eyebrow: str, value: str, unit: str, label: str, footer: str) -> bytes:
    im = _PILImage.new("RGB", (CARD_W, CARD_H), CARD_BG)
    d = _PILDraw.Draw(im)
    # the mark (assets/logo: a 64-unit grid), small, top left, with the wordmark beside it
    s, ox, oy = 1.5, 96, 64
    d.rectangle([ox + 22 * s, oy + 18 * s, ox + 42 * s, oy + 46 * s], fill=CARD_MINT)
    pts = [(ox + 4 * s, oy + 46 * s), (ox + 22 * s, oy + 46 * s), (ox + 22 * s, oy + 18 * s), (ox + 42 * s, oy + 18 * s), (ox + 42 * s, oy + 46 * s), (ox + 60 * s, oy + 46 * s)]
    d.line(pts, fill=CARD_INK, width=int(4 * s), joint="curve")
    for (x, y) in (pts[0], pts[-1]):
        d.ellipse([x - 2 * s, y - 2 * s, x + 2 * s, y + 2 * s], fill=CARD_INK)
    wm = _font("bold", 40)
    d.text((ox + 64 * s + 22, oy + 46 * s - 40), "Lead", font=wm, fill=CARD_INK)
    d.text((ox + 64 * s + 22 + d.textlength("Lead ", font=wm), oy + 46 * s - 40), "Green", font=wm, fill=CARD_MINT)
    # eyebrow
    eb = _font("mono-medium", 24)
    d.text((96, 186), eyebrow.upper(), font=eb, fill=CARD_MINT)
    # the number and its unit, sized to fit beside each other
    size = 190
    while size > 90:
        vf = _font("bold", size)
        uf = _font("mono", max(26, size // 5))
        if d.textlength(value, font=vf) + 24 + d.textlength(unit, font=uf) <= CARD_W - 192:
            break
        size -= 10
    vb = vf.getbbox(value)
    base_y = 236 + (190 - size) // 2
    d.text((96 - vb[0], base_y), value, font=vf, fill=CARD_INK)
    d.text((96 + d.textlength(value, font=vf) + 24, base_y + (vb[3] - vb[1]) * 0.55), unit, font=uf, fill=CARD_MUTED)
    # the label, up to two lines
    lf = _font("medium", 38)
    y = base_y + (vb[3] - vb[1]) + 56
    for line in _wrap(d, label, lf, CARD_W - 192, 2):
        d.text((96, y), line, font=lf, fill=CARD_INK2)
        y += 48
    # footer and rule
    ff = _font("mono", 22)
    d.text((96, 556), footer, font=ff, fill=CARD_MUTED)
    d.rectangle([96, 598, CARD_W - 96, 600], fill=CARD_RULE)
    im = im.quantize(colors=128, method=_PILImage.Quantize.MEDIANCUT, dither=_PILImage.Dither.NONE)
    buf = io.BytesIO()
    im.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def card_for(path: str, card: dict) -> tuple[str, str]:
    """Render (or keep) the card for a page path like 'models/qwen-3-32b/' and return (og:image URL, alt text)."""
    name = slug(path.strip("/")) or "home"
    rel = f"{CARDS_REL}/{name}.png"
    footer = f"leadgreen.ai/{path} · release {DATA_VERSION} · a Katonic project"
    alt = f"{card['value']} {card['unit']}: {card['label']}".strip()
    if CARDS_OK:
        outputs_bin[rel] = card_png(card["eyebrow"], card["value"], card["unit"], card["label"], footer)
    elif not (ROOT / rel).exists():
        return f"{SITE}/assets/social-card.png", "Lead Green: the energy behind the token"
    return f"{SITE}/{rel}", alt

