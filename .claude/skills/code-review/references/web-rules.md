# The rules the CSS-quality lens applies

The rules for a hand-written, framework-free stylesheet and the markup it
styles, as the guides put them; how to read them on this site is Lens B's
brief, which wins where the two differ. Refer to a rule by its name in a
finding. This list was written from memory of the guides and has not been
checked against their text; if a finding needs a guide's wording, open
the guide first.

## CSS Guidelines — Harry Roberts

- **Single source of truth.** Every design value is defined once (a
  custom property) and referenced everywhere else.
- **Specificity is a cost.** Keep it low and flat: classes, not ids or
  element chains; never win a conflict by adding a selector.
- **Selector intent.** A selector says what it styles (`.project-title`),
  not where it happens to sit (`.project-card div h3`).
- **Separate structure from skin.** Layout of children belongs to the
  parent; a component does not position itself for one particular parent.
- **No undoing.** A rule that resets what an earlier rule set is a sign the
  earlier rule did too much.
- **Comment the why.** Section titles and the reason behind a non-obvious
  value; never what the declaration already says.
- **`!important` is proactive only** — in utilities that must always win
  (print, reduced motion), never to fix a specificity fight.

## Naming (BEM-like, as this site uses it)

- A component is a prefix: `.project-card`, `.project-thumb`,
  `.project-body`, `.project-title`.
- A variant is a modifier: `.section--tinted`, `.code-art--plain`.
- A state is `is-*`: `.is-current`, `.is-link`.
- One word per concept: the same thing has the same name in every
  component (`-cat` for the small label above a title, `-desc` for the
  body text).

## Clean Code, read for CSS — Robert C. Martin

- **One responsibility per rule**: a rule styles one component or one
  state of it.
- **Small**: a rule long enough to need sub-headings is two components.
- **Names reveal intent**; a comment explaining a class name is a name
  that failed.
- **No duplication**: the same declarations in two rules are one rule with
  two selectors, or one class.

## Responsive and intrinsic design — Every Layout, Ethan Marcotte

- **Mobile-first**: base rules are the narrow layout; `min-width` queries
  add.
- **Fewer breakpoints**: let content decide; fluid type and spacing with
  `clamp()`, grids with `auto-fill`/`minmax()`, wrapping flex rows.
- **Relative units** for type and spacing (`rem`), `px` for hairlines and
  fixed artwork.
- **No fixed heights** on anything holding text.

## Platform rules

- **Respect preferences**: `prefers-color-scheme`, `prefers-reduced-motion`,
  `color-scheme` declared.
- **Progressive enhancement**: a declaration newer browsers need has a
  fallback before it where older ones would break (`background` before
  `color-mix`).
- **No inline styles** except a custom property passed to a component
  (`style="--lang:#dea584"`).
