# Formats

Three shapes: what a reviewer returns, the report a review writes, and the
ledger the skill reads at the start and writes at the end.

## 1. A finding, as a reviewer returns it

One block per finding, nothing outside the blocks. `Priority` and `Effort`
are the reviewer's suggestion; the merge step decides.

```
### <A|B|C|D|E|F|G|H>-<n>: <one line, the problem not the fix>
- Where: style.css:640-668 (or index.html:449, or "375-dark-04.png")
- Rule: <rule, success criterion or house convention by name>
- Priority: P2
- Effort: S
- What: <two to four lines: what the code does and why that breaks the rule>
- Change: <the concrete proposal — which rule to merge into which, which
  element to use instead, the exact tag to add>
- Evidence:
  ```css
  <the lines, at most eight>
  ```
```

## 2. The report — `docs/reviews/<date>-since-<base>.md`

```markdown
# Site review — <date>, since <base>

Range: <base>..<HEAD sha or "working tree">, <N> files, +<a> −<b> lines.
Commits: <one line per subject>
Inputs: screens <taken | not taken: why>; scan <N candidates>; contrast <N pairs, N failing>; links <N checked, N not 200>; sources <N repos, app page, CV>.
Kept: A 3/4 · B 2/3 · C 4/4 · D 1/2 · E 5/6 · F 2/2 · G 6/6 · H 3/5 — findings that survived the merge and the check, of those returned.

| ID | P | Lens | Effort | Where | Finding | Decision |
|----|---|------|--------|-------|---------|----------|
| CR-001 | P1 | G | S | index.html:15 | ... | fix now |

## Findings

### CR-001 · P1 · SEO · S — <one line>
**Where** index.html:15-20
**Rule** <name>
**What** ...
**Change** ...
```html
<evidence>
```
**Decision** fix now / later / won't fix — <the user's reason, when given>

## Still open from earlier reviews
| ID | P | Where | Finding | Since |

## Not raised
<one line each for a reviewer finding dropped in the merge: house rule,
out of range, not confirmed in the code, or refuted by the verifier with
its reason — so the next review can see what was already looked at>
```

The Decision column and lines are filled in after the interview. The
report is public (Pages serves it): no private details from the CV.

## 3. The ledger — `docs/reviews/LEDGER.md`

```markdown
# Review ledger

The memory of `/code-review`: read before every review, written after.
IDs are `CR-nnn`, unique across all reviews. A house rule is a finding the
user rejected together with the reason, and it is why the same finding is
not raised twice.

## House rules
| Since | Rule | Reason | Origin |
|-------|------|--------|--------|

## Open
| ID | P | Lens | Where | Finding | Since |
|----|---|------|-------|---------|-------|

## Done
| ID | P | Lens | Where | Finding | Fixed |
|----|---|------|-------|---------|-------|

## Reviews
| Date | Range | Report | Findings | Fix now | Later | Won't fix | Kept |
|------|-------|--------|----------|---------|-------|-----------|------|
```

The Kept cell repeats the report's Kept line (`A 3/4 · B 2/3 …`); the
next review reads it to tell a lens that drifted.

A house rule is written as the exclusion a reviewer can apply, in the
user's words where they gave them: "The 2000s roles stay in full — the
user wants the whole career visible, not a summary." The Origin column is
the CR ID it came from, so the report holds the full story.
