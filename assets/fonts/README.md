# Self-hosted fonts

This folder holds local copies of the three web fonts used by the Lead Green site, and the stylesheet that loads them. Serving the fonts from the site itself means pages make no requests to Google Fonts or any other third party, so the site's "no tracking" statement stays true.

To use them, link fonts.css from the page head in place of the Google Fonts stylesheet and its preconnect links. The urls inside fonts.css are relative, so it works from any page as long as the font files stay next to it.

## Families and weights

| Family | Used for | Weights | Files |
|---|---|---|---|
| Archivo | headings and large figures | 500, 700 | one variable font file per subset serves both weights |
| Public Sans | body text | 400, 600 | one variable font file per subset serves both weights |
| IBM Plex Mono | labels, numbers and code | 400, 500 | one static file per weight and subset |

Every face is the normal (upright) style. The font-family names are exactly Google's ("Archivo", "Public Sans", "IBM Plex Mono"), so the site stylesheet needs no change.

## Subsets kept

Only the latin and latin-ext subsets are kept. Together they cover English and the accented Latin letters used across Europe. Google also serves vietnamese, cyrillic and cyrillic-ext subsets for some of these families; those were not downloaded. Each rule in fonts.css keeps Google's unicode-range, so a browser only fetches the latin-ext file when a page uses a character from that range.

## Files and sources

| File | Bytes | Source |
|---|---|---|
| fonts.css | 5546 | written from the Google Fonts stylesheet below, with local urls |
| archivo-500-700-latin-ext.woff2 | 32608 | https://fonts.gstatic.com/s/archivo/v25/k3kPo8UDI-1M0wlSV9XAw6lQkqWY8Q82sLyTOxK-vA.woff2 |
| archivo-500-700-latin.woff2 | 34928 | https://fonts.gstatic.com/s/archivo/v25/k3kPo8UDI-1M0wlSV9XAw6lQkqWY8Q82sLydOxI.woff2 |
| ibm-plex-mono-400-latin-ext.woff2 | 13348 | https://fonts.gstatic.com/s/ibmplexmono/v20/-F63fjptAgt5VM-kVkqdyU8n1iEq129k.woff2 |
| ibm-plex-mono-400-latin.woff2 | 14708 | https://fonts.gstatic.com/s/ibmplexmono/v20/-F63fjptAgt5VM-kVkqdyU8n1i8q1w.woff2 |
| ibm-plex-mono-500-latin-ext.woff2 | 13432 | https://fonts.gstatic.com/s/ibmplexmono/v20/-F6qfjptAgt5VM-kVkqdyU8n3twJwl5FgtIU.woff2 |
| ibm-plex-mono-500-latin.woff2 | 14888 | https://fonts.gstatic.com/s/ibmplexmono/v20/-F6qfjptAgt5VM-kVkqdyU8n3twJwlBFgg.woff2 |
| public-sans-400-600-latin-ext.woff2 | 18472 | https://fonts.gstatic.com/s/publicsans/v21/ijwRs572Xtc6ZYQws9YVwnNIfJ7Cww.woff2 |
| public-sans-400-600-latin.woff2 | 26832 | https://fonts.gstatic.com/s/publicsans/v21/ijwRs572Xtc6ZYQws9YVwnNGfJ4.woff2 |
| OFL-Archivo.txt | 4388 | https://raw.githubusercontent.com/google/fonts/main/ofl/archivo/OFL.txt |
| OFL-PublicSans.txt | 4390 | https://raw.githubusercontent.com/google/fonts/main/ofl/publicsans/OFL.txt |
| OFL-IBMPlexMono.txt | 4456 | https://raw.githubusercontent.com/google/fonts/main/ofl/ibmplexmono/OFL.txt |

The @font-face rules come from this Google Fonts stylesheet, fetched with a desktop Chrome user agent so that it lists woff2 files:

https://fonts.googleapis.com/css2?family=Archivo:wght@500;700&family=Public+Sans:wght@400;600&family=IBM+Plex+Mono:wght@400;500&display=swap

Font versions, from the file paths on fonts.gstatic.com: Archivo v25, Public Sans v21, IBM Plex Mono v20.

Retrieved on 2026-09-27 (UTC).

## Licence

All three families are licensed under the SIL Open Font License, Version 1.1, which allows the fonts to be bundled and redistributed with a website. The licence text and copyright notice for each family sit alongside the fonts:

- OFL-Archivo.txt for Archivo (Copyright 2020 The Archivo Project Authors)
- OFL-PublicSans.txt for Public Sans (Copyright 2015 The Public Sans Project Authors)
- OFL-IBMPlexMono.txt for IBM Plex Mono (Copyright 2017 IBM Corp.)

The woff2 files are exactly as Google Fonts serves them. Nothing in them was changed.

## Updating

Fetch the stylesheet url above with a current desktop Chrome user agent, keep the latin and latin-ext blocks, download their woff2 files, then update fonts.css and this file. When Google releases a new version of a font, its file urls change too.
