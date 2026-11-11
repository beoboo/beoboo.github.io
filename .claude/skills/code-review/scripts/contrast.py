#!/usr/bin/env python3
"""WCAG contrast of the colour pairs the page actually puts together, in
both themes, computed from the tokens in style.css (stdlib only).

    python3 -I contrast.py <repo>/style.css

The (first) theme is the first `:root` block; a dark variant, if any, is the
`:root` inside `@media (prefers-color-scheme: dark)`. Pairs are foreground on
background, with the AA threshold each needs: 4.5 for text, 3 for large
text and for non-text UI (borders, focus rings, icons).
"""
import re
import sys

# (foreground, background, where the page uses it, threshold)
PAIRS = [
    ("--text", "--bg", "body text", 4.5),
    ("--text", "--surface", "text on cards", 4.5),
    ("--text-muted", "--bg", "muted text on the page", 4.5),
    ("--text-muted", "--surface", "muted text on cards", 4.5),
    ("--text-muted", "--surface-2", "tags; muted text in the tinted section", 4.5),
    ("--accent", "--bg", "links, eyebrows, section numbers", 4.5),
    ("--accent", "--surface", "card category labels, 'View on GitHub'", 4.5),
    ("--accent", "--surface-2", "repo names in the tinted section", 4.5),
    ("--accent-contrast", "--accent", "primary button label", 4.5),
    ("--accent-contrast", "--accent-hover", "primary button label, hovered", 4.5),
    ("--accent-hover", "--accent-soft", "strong skill pills", 4.5),
    ("--accent", "--accent-soft", "patent icon", 3.0),
    ("--blue", "--bg", "section numbers, eyebrow, employers", 4.5),
    ("--blue", "--surface", "card labels, repo names, skill groups", 4.5),
    ("--blue", "--surface-2", "labels in the tinted section", 4.5),
    ("--blue", "--blue-soft", "core-skill pills", 4.5),
    ("--blue", "--bg", "focus ring", 3.0),
    ("--line", "--bg", "card and divider borders (decorative)", 1.0),
]
FIXED = []


def lum(hexcol):
    h = hexcol.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    def ch(v):
        v = int(v, 16) / 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(h[i:i + 2]) for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def tokens(block):
    return dict(re.findall(r"(--[\w-]+)\s*:\s*(#[0-9a-fA-F]{3,6})\b", block))


def main():
    css = re.sub(r"/\*.*?\*/", "", open(sys.argv[1]).read(), flags=re.S)
    light = tokens(re.search(r":root\s*{(.*?)}", css, re.S).group(1))
    dark_m = re.search(r"prefers-color-scheme:\s*dark\)\s*{\s*:root\s*{(.*?)}", css, re.S)
    themes = {"theme": light}
    if dark_m:   # a second, dark theme under prefers-color-scheme
        themes = {"light": light, "dark": {**light, **tokens(dark_m.group(1))}}
    for name, t in themes.items():
        print(f"[{name}]")
        if not t:
            print("  no dark theme found")
            continue
        for fg, bg, where, need in PAIRS:
            if fg in t and bg in t:
                r = ratio(t[fg], t[bg])
                verdict = "ok" if r >= need else f"FAILS {need}:1"
                print(f"  {r:5.2f}:1  {verdict:<11} {fg} {t[fg]} on {bg} {t[bg]} — {where}")
    print("[fixed colours]")
    for fg, bg, where, need in FIXED:
        r = ratio(fg, bg)
        print(f"  {r:5.2f}:1  {'ok' if r >= need else f'FAILS {need}:1':<11} {fg} on {bg} — {where}")


if __name__ == "__main__":
    main()
