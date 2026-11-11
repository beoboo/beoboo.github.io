# Review ledger

The memory of `/code-review`: read before every review, written after.
IDs are `CR-nnn`, unique across all reviews. A house rule is a finding the
user rejected together with the reason, and it is why the same finding is
not raised twice.

## House rules
| Since | Rule | Reason | Origin |
|-------|------|--------|--------|
| 2026-11-11 | Overlapping roles in Experience stay unexplained (Di-SiDE alongside Moneyfarm, Demetra alongside Abbeynet): do not raise year overlaps or ask how they worked. | Not worth explaining: overlaps are normal in a career like this, and the page doesn't need to justify them. | CR-023 |

## Open
| ID | P | Lens | Where | Finding | Since |
|----|---|------|-------|---------|-------|
| CR-001 | P1 | E·F·G | git history | Follow-up: purge the removed CV PDF from history at the next push (rewrite and force-push `main`, with its own confirmation) — the user chose to purge it | 2026-11-11 |
| CR-040 | P3 | G | index.html:56-58 | Self-host the two Google Fonts woff2 files (and preload the serif) to drop a font origin from first paint; the avatar part is done | 2026-11-11 |

## Done
| ID | P | Lens | Where | Finding | Fixed |
|----|---|------|-------|---------|-------|
| CR-001 | P1 | E·F·G | index.html, docs/ | The CV download published private details (removed, PDF deleted) | 2026-11-11 |
| CR-002 | P1 | D·F | style.css | Nav clipped below 352 px; focus rings clipped | 2026-11-11 |
| CR-003 | P1 | F | style.css | Nav contrast under the translucent header | 2026-11-11 |
| CR-004 | P1 | E | index.html | munote overstated as behaviour-first | 2026-11-11 |
| CR-005 | P1 | E | index.html | envoy-oidc-filter described as an OIDC filter (dropped) | 2026-11-11 |
| CR-006 | P1 | E | index.html | Woodwork placeholder description (card removed) | 2026-11-11 |
| CR-007 | P1 | G | index.html, assets/ | No social image or card type | 2026-11-11 |
| CR-008 | P1 | G | robots.txt, sitemap.xml | No robots.txt or sitemap | 2026-11-11 |
| CR-009 | P1 | G | 404.html | No custom 404 | 2026-11-11 |
| CR-010 | P2 | A·C | index.html | Education in no date order | 2026-11-11 |
| CR-011 | P2 | A | index.html | Group and card titles at one heading level | 2026-11-11 |
| CR-012 | P2 | A | index.html, style.css | Experience headings named only the role | 2026-11-11 |
| CR-013 | P2 | A | index.html | Patent as an aside | 2026-11-11 |
| CR-014 | P2 | B·C·H | style.css | Label style written out eight times | 2026-11-11 |
| CR-015 | P2 | B | style.css | a:hover outranked link components | 2026-11-11 |
| CR-016 | P2 | B | style.css | One-off breakpoints for two grids | 2026-11-11 |
| CR-017 | P2 | B·H | style.css | Declarations restating or undoing the base | 2026-11-11 |
| CR-018 | P2 | B | style.css | Variants via :not() and longer selectors | 2026-11-11 |
| CR-019 | P2 | D | style.css, index.html | Light illustrations glowed in dark mode | 2026-11-11 |
| CR-020 | P2 | D | style.css | Sideways scroll below 307 px | 2026-11-11 |
| CR-021 | P2 | D | style.css | Print showed no project URLs | 2026-11-11 |
| CR-022 | P2 | E | index.html | First screen hid the current employer | 2026-11-11 |
| CR-023 | P2 | E | index.html | PRG Travel's year-only date (overlaps: house rule) | 2026-11-11 |
| CR-024 | P2 | E | index.html | Four project lines said more than their repos | 2026-11-11 |
| CR-025 | P2 | E | index.html | Patent had no office, year or link | 2026-11-11 |
| CR-026 | P2 | F | index.html | Card calls to action hidden from assistive tech | 2026-11-11 |
| CR-027 | P2 | F | style.css | Footer link indistinguishable from text | 2026-11-11 |
| CR-028 | P2 | F | index.html | Safari dropped list semantics | 2026-11-11 |
| CR-029 | P2 | F | index.html, style.css | Core skills told apart by colour only | 2026-11-11 |
| CR-030 | P2 | G | index.html | Meta description too long, repeated the title | 2026-11-11 |
| CR-031 | P2 | G | index.html | JSON-LD Person thin | 2026-11-11 |
| CR-032 | P2 | G | index.html, icons | Favicon only a data: URI | 2026-11-11 |
| CR-033 | P2 | H | style.css | Half of the code/terminal rule never applied | 2026-11-11 |
| CR-034 | P3 | A | index.html | "Learning by building" link named its destination wrongly | 2026-11-11 |
| CR-035 | P3 | C | index.html | Card labels in different patterns | 2026-11-11 |
| CR-036 | P3 | C | index.html | Descriptions switched voice | 2026-11-11 |
| CR-037 | P3 | C | index.html | Employer lines off pattern | 2026-11-11 |
| CR-038 | P3 | D | style.css | Orphaned third card on tablets (settled by CR-006) | 2026-11-11 |
| CR-039 | P3 | D | style.css | Two-column layout split too early at 900 px | 2026-11-11 |
| CR-040 | P3 | G | index.html | Avatar preconnect and size (fonts: Open) | 2026-11-11 |
| CR-041 | P3 | H | style.css | Card edge repeated in three rules | 2026-11-11 |
| CR-042 | P3 | H | index.html | Arrow icon drawn six times | 2026-11-11 |

## Reviews
| Date | Range | Report | Findings | Fix now | Later | Won't fix | Kept |
|------|-------|--------|----------|---------|-------|-----------|------|
| 2026-11-11 | all (65b93ed) | [2026-11-11-baseline.md](2026-11-11-baseline.md) | 42 | 41 (+ CR-038 settled by CR-006) | 1 (CR-040's fonts) | 1 (CR-023's overlaps) | A 5/5 · B 5/5 · C 5/5 · D 6/6 · E 9/10 · F 7/7 · G 8/8 · H 5/5 |
