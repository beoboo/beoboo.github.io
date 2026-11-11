#!/usr/bin/env python3
"""Static scan of the CV site for the review lenses (stdlib only).

    python3 -I scan.py <repo> [page]          page defaults to index.html

Prints candidates, not findings, in sections the briefs refer to:
  [html]   tag balance, duplicate ids, anchors without a target, links that
           open a new tab without rel, images without alt, inline styles
  [dead]   CSS classes nothing in the HTML uses; HTML classes no CSS styles;
           custom properties defined and never used, or used and never defined
  [dup]    declaration blocks the stylesheet holds twice; inline SVG markup
           the page repeats
  [css]    breakpoints, !important, raw colours outside the picture rules,
           id selectors, deep selectors
  [seo]    title, description, canonical, social tags, JSON-LD, headings,
           lang, robots.txt / sitemap.xml / 404.html, icons
  [sizes]  every tracked file, in bytes
"""
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "source", "track", "wbr"}
# SVG children are often self-closed (<path/>); html.parser reports those as
# startendtag, so only unclosed non-void HTML elements are counted below.
PICTURE_SELECTORS = (".thumb-", ".project-badge", ".code-art", ".sketch-art")


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.problems = [], []
        self.ids, self.classes = Counter(), Counter()
        self.links, self.imgs, self.inline_styles = [], [], []
        self.headings, self.meta, self.links_rel = [], [], []
        self.title, self._in_title, self._in_heading = "", False, None
        self.jsonld, self._in_jsonld, self._buf = [], False, []
        self.svgs, self._svg_depth, self._svg_buf = [], 0, []
        self.lang = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        line = self.getpos()[0]
        if tag == "html":
            self.lang = a.get("lang")
        if self._svg_depth:
            self._svg_depth += 1
            self._svg_buf.append(f"<{tag} {sorted(attrs)}>")
        elif tag == "svg":
            self._svg_depth, self._svg_buf = 1, [f"<svg {sorted(attrs)}>"]
            self._svg_line = line
        if tag not in VOID and not self._svg_depth:
            self.stack.append((tag, line))
        if "id" in a:
            self.ids[a["id"]] += 1
        for c in (a.get("class") or "").split():
            self.classes[c] += 1
        if a.get("style"):
            self.inline_styles.append((line, tag, a["style"]))
        if tag == "a":
            self.links.append((line, a))
        if tag == "img":
            self.imgs.append((line, a))
        if tag == "meta":
            self.meta.append(a)
        if tag == "link":
            self.links_rel.append(a)
        if tag == "title":
            self._in_title = True
        if re.fullmatch(r"h[1-6]", tag):
            self._in_heading = [tag, line, ""]
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in_jsonld, self._buf = True, []

    def handle_startendtag(self, tag, attrs):
        if self._svg_depth:
            self._svg_buf.append(f"<{tag} {sorted(attrs)}/>")
        else:
            self.handle_starttag(tag, attrs)
            if tag not in VOID and self.stack and self.stack[-1][0] == tag:
                self.stack.pop()

    def handle_endtag(self, tag):
        line = self.getpos()[0]
        if self._svg_depth:
            self._svg_buf.append(f"</{tag}>")
            self._svg_depth -= 1
            if self._svg_depth == 0:
                self.svgs.append((self._svg_line, "".join(self._svg_buf)))
            return
        if tag == "title":
            self._in_title = False
        if self._in_heading and tag == self._in_heading[0]:
            self.headings.append((self._in_heading[0], self._in_heading[1],
                                  " ".join(self._in_heading[2].split())))
            self._in_heading = None
        if tag == "script" and self._in_jsonld:
            self.jsonld.append("".join(self._buf))
            self._in_jsonld = False
        if tag in VOID:
            return
        if not self.stack:
            self.problems.append(f"line {line}: </{tag}> with nothing open")
            return
        if self.stack[-1][0] == tag:
            self.stack.pop()
            return
        open_tags = [t for t, _ in self.stack]
        if tag in open_tags:
            while self.stack and self.stack[-1][0] != tag:
                t, l = self.stack.pop()
                self.problems.append(f"line {l}: <{t}> not closed before </{tag}> at line {line}")
            self.stack.pop()
        else:
            self.problems.append(f"line {line}: stray </{tag}>")

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_heading:
            self._in_heading[2] += data
        if self._in_jsonld:
            self._buf.append(data)


def css_rules(css):
    """(selector, body, line) for every rule, flattening @media blocks."""
    css_nc = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), css, flags=re.S)
    rules, i, depth, start, media = [], 0, 0, 0, []
    sel_start = 0
    while i < len(css_nc):
        ch = css_nc[i]
        if ch == "{":
            head = css_nc[sel_start:i].strip()
            if head.startswith("@"):
                media.append(head)
                sel_start = i + 1
            else:
                start = i + 1
                close = css_nc.index("}", i)
                line = css_nc.count("\n", 0, sel_start) + 1
                rules.append((" ".join(head.split()), css_nc[start:close].strip(), line, " ".join(media)))
                i = close
                sel_start = i + 1
        elif ch == "}":
            if media:
                media.pop()
            sel_start = i + 1
        i += 1
    return rules, css_nc


def main():
    repo = Path(sys.argv[1])
    page_name = sys.argv[2] if len(sys.argv) > 2 else "index.html"
    html = (repo / page_name).read_text()
    css = (repo / "style.css").read_text()
    p = Page()
    p.feed(html)

    print("[html]")
    for prob in p.problems:
        print("  tag:", prob)
    for t, l in p.stack:
        print(f"  tag: line {l}: <{t}> never closed")
    for i, n in p.ids.items():
        if n > 1:
            print(f"  duplicate id: #{i} x{n}")
    for line, a in p.links:
        href = a.get("href", "")
        if href.startswith("#") and len(href) > 1 and href[1:] not in p.ids:
            print(f"  anchor without target: line {line} href={href}")
        if a.get("target") == "_blank" and "noopener" not in (a.get("rel") or ""):
            print(f"  new tab without rel=noopener: line {line} {href}")
        if not href:
            print(f"  <a> without href: line {line}")
    for line, a in p.imgs:
        if "alt" not in a:
            print(f"  img without alt: line {line} {a.get('src')}")
    for line, tag, style in p.inline_styles:
        print(f"  inline style: line {line} <{tag}> {style}")

    rules, css_nc = css_rules(css)
    css_classes = set(re.findall(r"\.(-?[_a-zA-Z][\w-]*)", " ".join(r[0] for r in rules)))
    html_classes = set(p.classes)
    print("\n[dead]")
    for c in sorted(css_classes - html_classes):
        print(f"  CSS class no element uses: .{c}")
    for c in sorted(html_classes - css_classes):
        print(f"  HTML class no CSS rule styles: .{c} (x{p.classes[c]})")
    defined = set(re.findall(r"(--[\w-]+)\s*:", css_nc))
    used = set(re.findall(r"var\((--[\w-]+)", css_nc + html))
    for v in sorted(defined - used):
        print(f"  custom property defined, never used: {v}")
    for v in sorted(used - defined - {"--lang"}):
        print(f"  custom property used, never defined: {v}")

    print("\n[dup]")
    bodies = defaultdict(list)
    for sel, body, line, media in rules:
        decls = tuple(sorted(d.strip() for d in body.split(";") if d.strip()))
        if len(decls) >= 3:
            bodies[decls].append(f"{sel} (line {line}{', ' + media if media else ''})")
    for decls, where in bodies.items():
        if len(where) > 1:
            print(f"  same {len(decls)} declarations in: " + " | ".join(where))
    svg_count = Counter(s for _, s in p.svgs)
    first_line = {}
    for line, s in p.svgs:
        first_line.setdefault(s, line)
    for s, n in svg_count.most_common():
        if n > 1:
            print(f"  inline SVG repeated x{n}, first at line {first_line[s]} ({len(s)} chars each)")

    print("\n[css]")
    bps = Counter(re.findall(r"@media[^{]*?\((?:min|max)-width:\s*([\d.]+(?:px|rem|em))", css_nc))
    print("  breakpoints: " + ", ".join(f"{b} x{n}" for b, n in sorted(bps.items(), key=lambda x: float(re.sub('[a-z]', '', x[0])))))
    for sel, body, line, media in rules:
        if "!important" in body:
            print(f"  !important: line {line} {sel[:60]} {('in ' + media) if media else ''}")
        if re.search(r"(^|[\s,>+~])#[\w-]", sel):
            print(f"  id selector: line {line} {sel[:60]}")
        if len(re.findall(r"[.#\w\]:)]\s+[.#\w\[:]", sel)) >= 3:
            print(f"  deep selector: line {line} {sel[:60]}")
        if not sel.startswith(":root") and not any(s in sel for s in PICTURE_SELECTORS):
            for colour in re.findall(r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)", body):
                print(f"  raw colour outside the picture rules: line {line} {sel[:50]} {colour}")

    print("\n[seo]")
    t = " ".join(p.title.split())
    print(f"  title ({len(t)} chars): {t}")
    meta = {(m.get('name') or m.get('property')): m.get('content') for m in p.meta if m.get('name') or m.get('property')}
    d = meta.get("description") or ""
    print(f"  description ({len(d)} chars): {d[:80]}{'…' if len(d) > 80 else ''}")
    for key in ("robots", "og:type", "og:url", "og:title", "og:description", "og:image",
                "og:image:alt", "og:locale", "og:site_name", "twitter:card", "twitter:image"):
        print(f"  {key}: {meta.get(key, '— missing')}")
    rels = defaultdict(list)
    for l in p.links_rel:
        rels[l.get("rel")].append(l.get("href", "")[:60])
    for r in ("canonical", "icon", "apple-touch-icon", "manifest", "preload", "alternate"):
        print(f"  link rel={r}: {rels.get(r, '— missing')}")
    print(f"  html lang: {p.lang}")
    for block in p.jsonld:
        try:
            data = json.loads(block)
            print(f"  JSON-LD ok: @type={data.get('@type')} keys={sorted(data)}")
        except json.JSONDecodeError as e:
            print(f"  JSON-LD does not parse: {e}")
    h1s = [h for h in p.headings if h[0] == "h1"]
    print(f"  h1 count: {len(h1s)}")
    prev = 0
    for tag, line, text in p.headings:
        lvl = int(tag[1])
        flag = "  <- skips a level" if lvl > prev + 1 else ""
        print(f"  {'  ' * (lvl - 1)}{tag} line {line}: {text[:70]}{flag}")
        prev = lvl
    for f in ("robots.txt", "sitemap.xml", "404.html", ".nojekyll", "CNAME"):
        print(f"  {f}: {'present' if (repo / f).exists() else 'absent'}")

    print("\n[sizes]")
    files = subprocess.run(["git", "-C", str(repo), "ls-files"], capture_output=True, text=True).stdout.split()
    files += subprocess.run(["git", "-C", str(repo), "ls-files", "--others", "--exclude-standard"],
                            capture_output=True, text=True).stdout.split()
    for f in sorted(set(files)):
        fp = repo / f
        if fp.is_file() and not f.startswith(".claude/"):
            print(f"  {fp.stat().st_size:>8}  {f}")


if __name__ == "__main__":
    main()
