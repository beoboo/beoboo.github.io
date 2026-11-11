# The eight lenses

Each section is one reviewer's brief. Paste it whole into that reviewer's
prompt, after the range, the file list and the house rules. The briefs name
the house way as it stood when they were written — classes and tokens
move, so a reviewer checks with grep before asserting "everything else
does X".

The site's shape, for all eight: one page, `index.html` — the sticky
header and nav, the hero (name, title, contact buttons, the GitHub-avatar
portrait), then numbered sections `01 About`, `02 Experience`, `03 Skills`,
`04 Projects` (Software cards, "Also on GitHub" list, "Beyond code"
cards) and `05 Education & Patent`, then the footer. One stylesheet,
`style.css`, in numbered parts (1 design tokens … 11 footer & print), one
dark theme for everyone (navy; orange `--accent` for action, `--blue` for
structure, `--gradient` for highlights), no JavaScript beyond a JSON-LD
block. At the root, beside the page: `404.html`, `robots.txt`,
`sitemap.xml`, the favicons and `assets/og-card.jpg` (with its SVG
source). `docs/reviews/` holds this skill's reports; there is no CV PDF on
purpose (it carried private details). `.nojekyll` makes GitHub Pages serve
the files as they are, from the root of https://beoboo.github.io/. No
build step, no framework, no external code except the Google Fonts
stylesheet and the GitHub avatar.

---

## Lens A — Structure and semantics

You review the HTML as a document: whether its elements say what the
content is, and whether its outline holds up.

- **The outline.** One `h1`; `h2` per numbered section, `h3` below, no
  level skipped; a heading that is not a heading (a styled label as `h3`,
  a group title that labels nothing) or a label that is a heading in
  disguise. The scan's `[seo]` section prints the outline.
- **Elements for what they are.** Landmarks (`header`, `nav`, `main`,
  `footer`, `section` with `aria-labelledby`), lists for lists, `article`
  for a self-contained card, `time` with a machine-readable `datetime`, a
  `dl` for terms and values, `a` for navigation and `button` for actions,
  `aside` for what is tangential. A `div` or `span` doing an element's job.
- **Validity.** Unclosed or misnested elements, duplicate ids, an anchor
  pointing at no id, attributes on the wrong element, an `aria-*` that
  contradicts the element or repeats what it already says. The scan's
  `[html]` section lists the mechanical ones; read the rest.
- **The head.** Charset first, viewport, `lang`, title, description,
  `color-scheme`, the order resources load in. (What search and social
  networks read from it is G's.)
- **Links.** `target="_blank"` with `rel="noopener noreferrer"`, link text
  that says where it goes, the same destination linked two ways, a link
  whose whole card is the target (the stretched-link pattern) and what
  else inside the card becomes unreachable.
- **Content in markup.** Text that belongs in CSS (`::after` content
  carrying meaning, decorative characters in text), presentation in
  markup (inline `style`, `<br>` for spacing), comments that have gone
  stale.

Ignore: CSS (B, C), what renders at which width (D), whether a claim is
true (E), accessibility beyond structure — contrast, focus, motion (F),
search metadata (G), and unused or repeated markup (H).

---

## Lens B — CSS quality

You review `style.css` (and any `style` attribute) against
`web-rules.md`, pasted below the brief: the rules for a hand-written,
framework-free stylesheet. The rules file says what the guides say; this
brief says how to read them on this site, and where the two differ, the
brief wins.

- **Tokens are the single source of truth.** Colours, fonts, radii,
  shadows and the easing live in `:root` and the dark `:root`; a value
  repeated as a literal where a token exists, or a literal repeated three
  or more times that should be one, is the finding — name the token.
  Picture rules (`.thumb-*`, `.code-art`, `.project-badge` and the inline
  SVG illustrations) draw fixed-colour images the same in both themes;
  their hex values are the picture, not a bypassed token.
- **Specificity stays flat.** Class selectors, at most one descendant
  step, no ids, `!important` only in the reduced-motion and print blocks.
  A selector that only wins by being longer, or a rule that undoes another.
- **Mobile-first and few breakpoints.** `min-width` queries building up
  from the phone layout; the scan's `[css]` section lists the breakpoints
  in use. A breakpoint that exists for one rule where a neighbouring one
  would do, or a `max-width` query patching a mobile-first rule, is a
  finding; fluid `clamp()` and `auto-fill` grids are the house way of
  needing fewer.
- **One responsibility per rule.** A component's look in its own rules,
  layout of children by the parent (`gap`, grid), state as `is-*`,
  variants as `--modifier`. A rule mixing two components; margin on a
  component that only one parent needs.
- **Magic numbers.** A value that only works because of another value
  elsewhere (the timeline's `--line-x` is the house way: the derivation is
  in a comment); an unexplained offset, an `rem` next to `px` for the same
  kind of measure.
- **Comments say why.** Section headers and the why behind a trick stay;
  a comment restating the declaration, or one that no longer matches it,
  goes.

Ignore: whether the page uses the house components and tokens the same way
everywhere (C), what renders wrong (D), contrast and motion (F),
performance (G), and selectors nothing uses or blocks held twice (H).

---

## Lens C — Consistency

You review whether the page does things the way the rest of it does, and
whether something new rebuilt what the page already has. For every new
element, class, colour or pattern in the range, ask "what does the page
already have for this?" and search `index.html` and `style.css` before
answering. A finding here names the existing thing — "builds its own
label; `.project-cat` is the one every card uses" — or it is not a
finding.

The house way (check with grep before asserting):

- **Sections**: `section.section` with `aria-labelledby`, inside it
  `.container.section-grid` with a `header.section-head` (a
  `.section-index` number and an `h2`) and a `.section-body`; the
  projects section is the one that uses `.section-head--split` above
  full-width grids, and `.section--tinted`.
- **Lists of dated things**: `ol.timeline` > `li.timeline-item` (with
  `is-current` for the present role) > `.timeline-content` holding
  `h3.timeline-role` with the employer inside it as `span.timeline-org`
  (`Company · City, Country`), then `p.timeline-date` with `time`
  elements (read after the heading, shown in the left column),
  `.timeline-desc`, `ul.timeline-points`.
  Dates are years, `2017 – 2022`, en dash with spaces, "Present".
- **Tags**: `.pills` (with `.pill--strong`, plus a visually hidden "(core
  skill)", for the strongest) for skills;
  `ul.tags` for project and education tags. Never a third chip style.
- **Cards**: `article.project-card` (`is-link` when it links somewhere)
  > `.project-thumb.thumb-<kind>` with a `.project-badge` icon, then
  `.project-body` with `.project-cat` (`Kind · Language`),
  `h4.project-title` (the stretched link, named by `aria-labelledby` from
  the title and the `.project-more` call to action), `.project-desc`,
  `ul.tags` (no tag repeating the label's language), `.project-more`.
  Smaller links go in `.repo-list`.
- **Icons**: inline Lucide-style SVG, `class="icon"`, `viewBox="0 0 24
  24"`, stroke from CSS, `aria-hidden="true"` when decorative; an icon
  used more than once is a `<symbol>` in the `.sprite` sheet at the top
  of `<body>`, drawn with `<use>`.
- **Lists**: every `list-style: none` list carries `role="list"`.
- **Buttons and links**: `.btn.btn-primary` / `.btn-ghost`; external links
  `target="_blank" rel="noopener noreferrer"` with a visually hidden
  "(opens in a new tab)".
- **Colours and type**: tokens only outside the picture rules — orange
  for links, buttons and calls to action, blue for labels, employers, core
  skills and the focus ring; the small uppercase labels share one grouped
  rule in part 2; the serif
  (`--font-serif`) for `h1`, `h2` and card titles, the sans for everything
  else, `--font-mono` for code and repo names; uppercase tracked labels
  (`.eyebrow`, `.section-index`, `.project-cat`, `.callout-label`, group
  titles) at `.75rem`–`.8125rem`, weight 600, `.12em` tracking.
- **Words**: British spelling (behaviour, colour, practise as the verb),
  "·" as the separator in labels, "–" in ranges, first person in the
  about text and project descriptions.

Read the screens the brief carries for what grep cannot see: two things
meant to match that do not (a card taller than its row, labels at
different sizes, spacing that differs between sections).

Ignore: the quality of a rule in itself (B), a rendering defect (D),
whether a word is true (E), and code that is copied rather than a second
way of doing it (H).

---

## Lens D — Rendering

You review what a visitor sees. The screens the brief carries are the
page at 320 and 375 px (phones), 768 px (a tablet) and 1440 px (a
desktop), sliced top to bottom, and `print.pdf`. Open them before
the CSS; then read the CSS to explain what you saw and to find what the
slices do not show (320 px, 1024 px, a long word, a missing font).

- **Layout.** Horizontal scroll or clipped text at any width; elements
  overlapping (a badge over text, the sticky header over an anchor
  target); a grid leaving an orphan or a ragged row; content squeezed
  between breakpoints (check the widths either side of each breakpoint
  in the scan's `[css]` list by reading the rules).
- **The theme.** One dark theme: a hard-coded light colour on a token
  background, a shadow lost on navy, an illustration that glows; contrast
  is F's, correctness is yours.
- **The nav.** Every item reachable at 320 px, the sticky header's height
  matched by `scroll-padding-top`, an anchor landing under the header.
- **Print.** `print.pdf`: what is hidden, what breaks across pages, links
  printed, colours gone.
- **Fallbacks.** Without the web fonts (the system stack takes over: does
  anything overflow?), without `color-mix` or `backdrop-filter`, with
  reduced motion.
- **Links and files.** The links list: anything not 200 (other than
  LinkedIn's 999), a missing local file, the CV download.

For each defect, say at which width and theme it shows and which slice
shows it; a suspicion you could not see or derive is not a finding.

Ignore: style of the CSS (B), consistency (C), whether the text is right
(E), contrast and screen readers (F), and search metadata (G).

---

## Lens E — Content and the reader

You review what the page says about the user and how a reader takes it
in. The ground truth is the sources the brief carries: the CV PDF the user
supplies outside the repo (read it whole; with none, say so and treat the
last report as the record of what was confirmed), the README and metadata of every repository the
page links to, and the Music Practice Tracker's live landing page. The
user's own words in an earlier review's house rules count as a source.

Two passes: the facts, then the reader.

**The facts — every claim to its source.** Walk the page top to bottom:
the title and summary, every fact in About, every role (title, company,
place, dates, each bullet), every skill, every project description and
tag, education, the patent, the footer. For each, name the line of the
source that backs it. A claim with no source, a claim that says more
than its source (a number, a superlative, a result), a date or title that
differs from the CV, a project description that no longer matches its
README, or a link whose destination is not what the text says, is a
finding that quotes both. Something in the CV that matters and the page
leaves out is a finding too, P2 unless it is the user's best evidence.

**Privacy.** The page never shows the home address, phone number or date
of birth, and links no document that does (the user removed the CV PDF
for that reason).

**The reader.** Three readers, thirty seconds each:

- **A recruiter on a phone**: within the first screen, who, what role,
  how senior, where, how to reach them? Is the strongest evidence (current
  role, years, CTO roles, the patent, the emulator) where they will see it?
- **An engineer checking the work**: do the projects say what is
  technically interesting and link to code they can read? Is "ongoing"
  honest?
- **A hiring manager reading it through**: is the experience section the
  right length — do the 2000s roles earn their space? Does the voice stay
  one voice (first person, plain claims, no filler)?

**Words.** Spelling and grammar; British spelling throughout (the house
way); names of things as their owners write them (WebAssembly, GitLab,
RustNES, egui); the same thing called the same everywhere; nothing a
recruiter would read as a typo or an exaggeration.

For each finding, say what the reader concludes: "a recruiter reading
'2010' alone thinks it was a gap year; the CV says March to October".

Priority for this lens: P0 a claim that is false or private data on the
page; P1 a claim no source backs, or the first screen failing the
recruiter; P2 an omission or a reader's stumble; P3 wording.

Ignore: markup (A), CSS (B, C), rendering (D), accessibility (F), and the
words search engines read in the head (G) — but the visible title and
summary are yours.

---

## Lens F — Accessibility

You review the page against WCAG 2.2 AA, as a keyboard user, a
screen-reader user, a low-vision user and someone who turned off motion.
The brief carries the contrast table (`contrast.txt`, the token pairs the
page uses) and the screens; read the table first, then check
the pairs it does not cover by reading where colours meet in the CSS.

- **Perceivable.** Contrast below 4.5:1 for text or 3:1 for large text,
  icons, borders that carry meaning and the focus ring; text in images;
  information by colour alone; gradient text over the glows.
- **Operable.** Every link and control reachable by keyboard in reading
  order, the focus always visible (and not hidden under the sticky
  header), the skip link working, target size at least 24×24 CSS px for
  the nav and tags that are links, nothing that moves without
  `prefers-reduced-motion` stopping it, no hover-only content.
- **Understandable.** `lang` on the page and on any passage in another
  language; link text that makes sense out of context ("View on GitHub"
  inside a card whose name is the link); abbreviations a screen reader
  will mangle.
- **Robust.** What the accessibility tree says: decorative SVG hidden,
  meaningful SVG named, `aria-label` matching the visible text (WCAG
  2.5.3), `aria-labelledby` pointing at real ids, landmarks and headings
  that let someone jump to "Experience", lists announced as lists, the
  stretched card link and what a screen reader reads for the whole card.

For each finding, name the success criterion and the user who hits it:
"a screen-reader user tabbing to a card hears 'link, RustNES' and nothing
of what it is (2.4.4)".

Ignore: heading structure as structure (A), CSS quality (B), visual
defects that are not barriers (D), and wording (E).

---

## Lens G — SEO and delivery

You review how the site is found, previewed and served: by Google and
Bing, by LinkedIn, Slack, WhatsApp and X when someone shares the link,
and by GitHub Pages. The brief carries the scan's `[seo]` section (the
head as a crawler reads it, the heading outline, which crawl files exist),
the `[sizes]` section, and the links list with the live site's responses.

- **Search basics.** A unique `title` of 50–60 characters that leads with
  the name and the role; a meta description of 140–160 characters that a
  person would click; a canonical URL that is the one Pages serves (with
  the trailing slash); `lang`; one `h1`; no `noindex` by accident; text
  content (not images) carrying the keywords a recruiter searches —
  name, role, location, core technologies.
- **Social previews.** Open Graph (`og:title`, `og:description`,
  `og:url`, `og:type`, `og:image` at 1200×630 with `og:image:alt`,
  `og:site_name`, `og:locale`) and `twitter:card` (`summary_large_image`).
  Without `og:image` every share is a grey box: say so plainly. The image
  must be a real file at an absolute URL, under ~1 MB.
- **Structured data.** The JSON-LD `Person`: valid JSON, the properties
  Google reads (`name`, `url`, `jobTitle`, `image`, `sameAs`,
  `worksFor`, `alumniOf`, `address`, `knowsAbout`), values that match the
  visible page, nothing on it the page does not say.
- **Crawl files.** `robots.txt` (allowing the site, naming the sitemap,
  and keeping crawlers out of `docs/reviews/` and `.claude/`, which Pages
  also serves), `sitemap.xml` (the page, with a current `lastmod`), a
  `404.html` that leads back home (Pages serves it for every missing
  path).
- **Icons and app metadata.** The SVG favicon plus a PNG
  `apple-touch-icon` (180×180) and a 32×32 PNG fallback for crawlers and
  Safari; `theme-color`.
- **Performance as ranking.** What delays the first paint: the Google
  Fonts stylesheet (preconnect is there; `display=swap`; how many
  families and weights), render-blocking CSS, page and PDF weight from
  `[sizes]`, anything that shifts the layout as it loads (fonts swapping,
  images without dimensions).
- **Pages specifics.** `.nojekyll`, the PDF's crawlable link and file
  name, the live headers (cache, content type), whether every file Pages
  serves is meant to be public.

For each finding, say what the searcher or sharer sees: "the link pasted
into LinkedIn shows the title and a blank grey image".

Priority for this lens: P0 the site not indexable or the canonical
pointing elsewhere; P1 a missing social image, a missing or wrong
description, structured data that is invalid or contradicts the page, no
robots/sitemap/404; P2 icons, performance, polish; P3 taste.

Ignore: heading structure for its own sake (A), visible wording (E), and
accessibility (F).

---

## Lens H — Dead code and duplication

You review what the site carries without using, and what it holds twice.
Start from the scan the brief carries: CSS classes no element uses, HTML
classes no rule styles, custom properties defined and never used (or used
and never defined), declaration blocks the stylesheet holds twice, and
inline SVG the page repeats. They are candidates, not findings — a class
can be a hook a sibling rule needs, two blocks can look alike for good
reason — so open each one you raise and grep its name yourself. In a
ranged run, take the candidates in the changed lines; then read the diff
for what the scan cannot see.

Dead:

- **Nothing uses it.** A rule whose selector matches nothing on the page;
  a custom property nothing reads; a media query whose rules are all
  overridden; a file nothing links (an image, a PDF, a stylesheet).
- **Never reached.** A rule for a state the markup never has, a
  breakpoint whose rules equal the ones below it, a fallback declaration
  every supported browser overrides (say which browsers you assumed).
- **Left behind.** Commented-out markup or CSS; a comment naming a class,
  section or file that no longer exists; a placeholder comment for work
  that is done.

Twice:

- **Copies.** The same declarations in two rules (name both and the one
  selector list they become); the same SVG drawn several times (an icon
  set as `<symbol>`s and `<use>` is the usual fold); two components that
  differ only in a value (one becomes a modifier).
- **Markup.** A block of HTML repeated with small changes where a shared
  class would make the differences explicit.

For each finding, say what removing or folding it changes: "nothing on
screen; 2 kB less HTML and one place to change the arrow". Deleting dead
code is P2; a copy whose two halves already disagree is a defect and P1.

Ignore: whether the CSS is well shaped (B), a second way of doing
something the page already does (C), and markup semantics (A).
