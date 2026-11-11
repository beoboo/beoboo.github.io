---
name: code-review
description: Review the CV site (index.html, style.css, docs/) through eight lenses — structure and semantics, CSS quality, consistency (the house components and tokens), rendering (what a visitor sees at each width and in print, read from screenshots), content (every claim against the CV and the repos it cites), accessibility (WCAG 2.2 AA, with measured contrast), SEO and delivery (search, social previews, structured data, GitHub Pages) and dead code and duplication (read from a scan) — refute every P0 and P1 before it is raised, rate each finding P0–P3, remember it in docs/reviews/, and settle the findings with the user one at a time. Use when asked to /code-review, "review the site", "review what changed since the last deploy", "is the site SEO compliant", or "what should be cleaned up before I push". Adapted from the Music Practice Tracker's /code-review. It replaces the bundled /code-review by name; that one stays reachable as /review.
argument-hint: "[all | base commit | from..to] [theme]"
---

# Review the site since what is live

Eight reviewers look at the same changes from eight angles, the findings are
merged, checked (every P0 and P1 by a second agent whose job is to refute
it), rated and written down, and then the user decides each one in turn.
The review is for four things the user wants of the site: it tells the
truth about the user, it reads well for every visitor on every device, it is
found and previewed properly by search engines and social networks, and
its code stays small and consistent enough to keep editing by hand. The
ledger in `docs/reviews/` is there so nothing is raised twice: a finding
the user rejected becomes a house rule the next review respects, and one
the user deferred is a reminder, not a fresh discovery.

Nothing in `index.html`, `style.css` or the site's other files changes
until the interview is over and the user has given the go (§6).

The repository is public and GitHub Pages serves all of it from the root
of https://beoboo.github.io/, `docs/reviews/` included. Reports and the
ledger quote code, never the private details the CV PDF holds (home
address, phone, date of birth).

## 1. Scope

The site deploys on every push to `main`, so "what has not shipped" is
`origin/main` to the working tree — committed and uncommitted alike.

```bash
git fetch -q origin                                  # read-only; refreshes origin/main
git diff --stat origin/main                          # committed + uncommitted
git ls-files --others --exclude-standard             # untracked files
git log --oneline origin/main..HEAD
```

An argument overrides the base: a commit (`65b93ed`) or a range
(`65b93ed..HEAD`). Then diff exactly that.

`all` is the baseline: every file of the site as it stands (`git ls-files
| grep -v '^.claude/' | xargs wc -c`). There is no diff; the reviewers get
the file list with sizes and read everything. The report is
`<date>-baseline.md`. **With no ledger yet, the first review is `all`.**

A theme after the range (`all the projects section`, `seo`) narrows every
brief to that area, and the visual findings become drafts (§5).

If nothing in the range touches the site (only `.claude/` or
`docs/reviews/`), tell the user in one line and offer `all` instead of
running eight reviewers on nothing.

Say in a line what is being reviewed: the range (or "the whole site"), the
number of files and the size of the diff. Then gather the measured inputs
and load the memory.

### Measured inputs

Five lenses read measurements, not only code. Gather them before briefing,
into the scratchpad. The scripts are in this skill's `scripts/`; run the
Python ones with `python3 -I`. A measurement that cannot be taken is said
so, to the lens and in the report's header, and the review goes on without
it.

```bash
S=<scratchpad>/review; K=.claude/skills/code-review/scripts
bash $K/screens.sh . $S/screens          # D, F, C: slices at 320/375/768/1440; print.pdf
python3 -I $K/scan.py . > $S/scan.txt    # H, A, C, G: dead, dup, css, html and seo sections
python3 -I $K/contrast.py style.css > $S/contrast.txt   # F
bash $K/links.sh . > $S/links.txt        # D, G: every link followed; the live site's robots, sitemap, 404
CV_PDF=<path> bash $K/sources.sh . $S/sources   # E: linked READMEs, the practice app's page, the CV
```

**Screens** are what a visitor sees; a lens that judges layout reads the
slices it needs (`screens.txt` lists them) before the CSS. **The scan**
lists candidates, not findings. **Links** follows every link: LinkedIn
answers bots with 999, which is its bot wall, not a broken link. **Sources**
are the ground truth for the content lens. The CV PDF is not in the repo
(it carried private details and was removed on purpose): ask the user for
the current one and pass its path as `CV_PDF`.

## 2. Memory

`docs/reviews/LEDGER.md` is the skill's memory, in the format of
[references/formats.md](references/formats.md). Read four sections before
briefing anyone (with no ledger, create it from the template at the end):

- **House rules** — findings the user rejected, with why. They go to the
  reviewers verbatim as exclusions, and a merged finding that matches one is
  dropped, not re-argued.
- **Open** — accepted but not done. Not re-reviewed; listed at the end of
  the report under "Still open" and asked about once at the end of the
  interview (§5).
- **Done** — the next ID is one past the highest ID anywhere in the ledger.
- **Reviews** — the Kept column of the last row says how many of each
  lens's findings survived the check. A lens that lost more than a third
  of its findings last time is told so in its brief, with one of the
  findings that was not in the code, so it reads more carefully.

## 3. Eight reviewers, in parallel

Launch eight `general-purpose` agents in one message and wait for all
eight. Each gets the brief for its lens from
[references/lenses.md](references/lenses.md), pasted in full, plus:

- the range and the changed-file list from §1, and the theme if there is one;
- the house rules, verbatim;
- the finding format from [references/formats.md](references/formats.md);
- the standing instructions below;
- its measured inputs from §1, by path — the screens to D, F and C, the
  scan to H, A, C and G, the contrast table to F, the links to D and G,
  the sources to E — or the line saying why there is none;
- for B, [references/web-rules.md](references/web-rules.md) pasted below
  the brief.

The standing instructions, for every reviewer:

> Read-only: do not edit or format any file of the site; write only to
> the scratchpad. Read the whole file around every hunk, not just the hunk;
> a rule is only duplicated or a component only bypassed in the context of
> what surrounds it. For anything you call a violation, quote the lines
> with their line numbers. For anything you call a duplicate, name the
> existing thing with its location. For anything you call a rendering
> problem, name the screenshot slice that shows it. Report only what is in
> the range (a pre-existing problem that the range made worse counts; one
> it merely sits next to does not) — in an `all` run, everything is. Every
> P0 and P1 you raise goes to a second agent whose job is to refute it, so
> give it the width, theme, input or state that makes the problem happen.
> Return every P0 and P1 you can support, and at most five findings below
> that: the ones that cost most to leave alone. That is a bar, not a quota
> — a clean site gets a short list, and an empty list is a fine answer.
> Stay inside your lens; each brief ends with what to leave to the others.
> End with one line on what you did not get to. Return the findings in the
> given format and nothing else.

The lenses are narrow on purpose, so the same problem seen from two sides
arrives twice and is merged in §4 rather than argued eight times.

## 4. Merge, check, rate

1. **Merge.** Same location, same problem from two lenses → one finding
   carrying both lenses. Keep the better proposal.
2. **Drop** anything a house rule covers, and anything outside the range.
3. **Check** every finding against the code before it reaches the user: open
   the location, confirm the lines say what the reviewer says; for a
   rendering finding, open the slice. Reviewers are thorough but they
   drift; a finding you could not confirm is deleted, not hedged. For a
   "use X" finding, open X and confirm it actually fits; for an "unused"
   one, grep the name yourself. Count, per lens, how many findings came
   back and how many survived the merge and the check (a merged pair
   survives for both lenses): the report's Kept line and the ledger's
   Kept column.
4. **Refute** every finding that would be a P0 or a P1 after the check. One
   `general-purpose` agent per finding, all in one message, each with the
   finding in full and this brief:

   > Your job is to break this finding. Read the code it names and
   > everything that styles or links to it; render it if it is visual
   > (`.claude/skills/code-review/scripts/screens.sh`, into the scratchpad);
   > read-only for the site. Either produce the concrete state — the
   > width, the theme, the visitor, the search result, the source line —
   > that makes the claimed problem happen, quoting each line, or say what
   > stops it. Answer with one of: `CONFIRMED` and the trace; `REFUTED`
   > and the line that stops it; `UNDECIDED` and what you could not settle.

   Refuted → deleted, listed under "Not raised" with the verifier's reason.
   Undecided → kept at its priority, and its question says it is
   unverified. Confirmed → the trace is the scene the question opens with
   (§5). A finding no verifier could confirm is never a P0.
5. **Rate**, on what it costs to leave it alone:
   - **P0** — wrong now: a claim about the user that is false or a contact
     link that does not reach the user; private data on the page; the page
     broken or unreadable at a common width or in one theme; the site not
     deploying or not indexable at all. Fix before the next push.
   - **P1** — a real defect: something rendered wrong for some visitors, a
     WCAG 2.2 AA failure, a claim no source backs, a search or social
     preview that comes out wrong, or a structural problem that every edit
     makes more expensive (a second copy of a component, a token bypassed
     across the stylesheet). Fix in this round.
   - **P2** — a clear violation with a clear refactor, worth doing the next
     time someone opens the file. Most CSS-quality and dead-code findings
     live here.
   - **P3** — taste: a word, a small tidy-up, a nicer shape. Batch or skip.
6. **Estimate** the effort of the proposal: S (minutes, one place), M (an
   hour, several places, screens to recheck), L (a plan of its own).
7. **Number** them `CR-nnn`, continuing the ledger, ordered by priority then
   by file.

A proposal is concrete or it is not a finding: "move the six repeated
arrow SVGs into one `<symbol id="i-arrow">` and `<use>` it", not "consider
reducing duplication". The user decides from the proposal, so it has to
be decidable.

## 5. Report, then interview

Write the report to `docs/reviews/<yyyy-mm-dd>-since-<base>.md` (or
`-<from>-to-<to>.md` for a range, `-baseline.md` for `all`) in the format from
[references/formats.md](references/formats.md). When the Claude Docs
connector is available, publish the findings as a doc as well — a summary,
one section per priority, each finding with its recommendation and the
reason — and give the link before the first question; the user reads it
while answering. In the reply, give the counts per priority and the
summary table, nothing more.

Then take the findings **one at a time** with AskUserQuestion, P0 first,
never a closing list. The header carries the ID and the place in the round
("CR-012 · 3/14"), the text "(3 of 14)", counting every question the round
will ask, a finding split into several questions included; when an answer
opens a follow-up, the total grows and says so.

**The question is about three short sentences**: what goes wrong for the
visitor, what changes, and the recommendation with its reason.

- **What goes wrong** is one plain scene with a real visitor in it — a
  recruiter skimming on a phone, an engineer opening the projects, someone
  sharing the link on LinkedIn, a screen-reader user, Google — not the
  selectors and properties that cause it: "shared on LinkedIn, the link
  shows no picture, just a grey box". No numbers unless the number is the
  point.
- **What changes** is one plain line of what is different afterwards
  ("the link preview shows your name and title on a card"). A change no
  visitor can see opens with "Code only." and says "nothing changes on
  screen", because the user decides code and visible changes differently.
- **The recommendation** comes first among the options, marked
  "(Recommended)", with its reason in a few words: "Fix now: recruiters
  share links like this", "Later: do it with CR-004, which reshapes the
  same section".
- **Leave out** file names, selectors (unless the finding is about a name),
  effort letters and verifier caveats. The report holds them, and "Show
  me" is there for them.

The options:

- **Fix now** — for P0, P1 defects, anything at S, and code-only tidies at
  M unless they are risky: the user takes those.
- **Later** — goes to the ledger's Open section. For L refactors and risky
  M ones that are not defects, and for content or design decisions the
  user should weigh — say that it is one.
- **Won't fix** — becomes a house rule. Recommend it when the finding is
  right by the book and wrong for this site, and say why. When the user
  picks it, follow with one short question for the reason: "Disagree with
  the rule here", "It's deliberate", "Not worth it on a one-page site", or
  their own words. The reason is what makes the rule usable next time.
- **Show me** — quote the code and the proposed change in full (and the
  slice, for a visual one), then ask again.

A finding about the content itself — a claim, a description, a word about
the user — is always asked, never assumed: the user is the source.

**A themed review** draws its visual findings: each one is a
today-beside-proposed pair of screenshots (the proposal rendered from a
copy of the page in the scratchpad with `screens.sh`), looked at before
asking, and its question names the pair.

Three escape hatches, each one question: when more than ten P2s remain,
ask whether to go through them one by one, only where the user might
disagree with the recommendation (content, Later recommendations and
visible changes), or take the recommendations as they stand; when more
than five P3s remain, the same for them; and when the ledger had open
items, finish with "N earlier findings are still open — go through them
now, or leave them?".

## 6. Ask for the go, then act

The interview only collects answers; nothing is changed while it runs.
When the last answer is in, **sort the Fix now findings in the order you
prefer to fix them** — P0 and P1 defects first, then what other fixes
build on, then the rest — and **ask for the go in one short question**:
how many will be fixed, the Later and Won't fix findings in a line each,
and anything a decision made inconsistent (a Won't fix whose fix another
Fix now needs). Group fixes yourself where they touch the same area, but
do not lay out the groups: sort them by your preference and ask for the go.

Look at `git status` first: another session may be editing the tree at the
same time. Findings in files it has changed are left to it unless the user
says otherwise, and the go question says which. Stage by path — for a file
both sessions touched, a blob built from HEAD plus this review's hunks —
never with a bare `git add -A`.

Only after the go:

- **Fix now**, in your order. Open every message with the finding it is
  about, **[Fix 3/12 · CR-008]**, and end every update — a finding started,
  a check run, a commit, a "still working" note — with how many are done
  and how many are left, naming what is left ("3 of 12 done; 9 left: CR-009
  to CR-017"). The user should never have to ask. Keep each fix to its
  finding; no drive-by cleanups (they are the next review's findings).
- **Check the fixes** the way the review measured them: `scan.py` again,
  `contrast.py` if a colour moved, `screens.sh` and a look at the slices
  for anything visual, at 320 and 375 px as well as desktop, `links.sh` if a link
  or a served file changed. Say what you looked at.
- **Ledger.** Fixed → Done with today's date; Later → Open; Won't fix →
  House rules with the reason; and a row for this review in Reviews, with
  the Kept counts. Fill in the report's Decision column.
- **CLAUDE.md mirrors the house rules**, so ordinary sessions edit the site
  the house way instead of having it caught at review. Regenerate the
  section headed `## House rules (from /code-review)` from the ledger's
  table — one line per rule with its reason, nothing else in that section
  — and leave the rest of the file alone (create the file if it is missing).
- **One commit per fix**, so any fix can be reverted alone — or one commit
  for a few fixes that touch the same area and are done together. The
  report, the ledger and CLAUDE.md go in a last commit of their own. Use
  conventional subjects: `fix:` for what a visitor would notice, written as
  what they notice; `refactor:`, `style:`, `seo:`-type changes as `feat:` or
  `fix:` by whether they add or repair; `docs:` for the review files. Each
  body names its CR IDs with their one line. With no fixes, the report and
  ledger still go in, as `docs: site review since <base>`. One git step per
  Bash call, the Co-Authored-By trailer at the end, straight on `main`, with
  the repo's own identity (`git config user.email` is beoboo's noreply
  address — check before the first commit). **No push**: pushing `main`
  redeploys https://beoboo.github.io/, so it waits until the user asks.

Close with the counts (fixed / later / won't fix), the commits, and that
the live site changes only when `main` is pushed.
