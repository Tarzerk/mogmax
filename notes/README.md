# MOGMAX — Story Notes

*Design & writing notes for **MOGMAX**, a comedy "looksmaxxing/mogging" parody visual novel (Ren'Py). This folder is the story side of the project; the game itself lives in `../game/`.*

## Start here
1. **`STORY_BIBLE.md`** — read this first. The durable design doc: premise, characters, the theme spine, the Eugene mog/lift mechanic + ending matrix, the *Bully* lens, the transitions/pacing rule, the ending map, a **chapter status table** (what's built vs. drafted), and a polish backlog.
2. **`CH4-5_DRAFT.md`** — the pre-production script for chapters that aren't built yet (prose + sample dialogue).

## The two-file convention (split by lifecycle)
- **`STORY_BIBLE.md`** = the *why*. Intent, structure, rationale. Rarely deleted.
- **`CH4-5_DRAFT.md`** = a *disposable* draft. When a chapter ships into `.rpy`, cut its section from here and flip its row in the bible's status table to ✅.

## The one rule that prevents drift
- The **game code** (`../game/*.rpy`) is the source of truth for what the game *does*.
- These **notes** are the source of truth for what it *should* do and *why*.
- **Don't keep a second copy of shipped dialogue in the notes.** Once a line is in `.rpy`, that's its home. The draft is the only place dialogue lives in prose — and only until that chapter is built.

## Project layout (quick reference)
- `../game/chapter1.rpy … chapter3.rpy` — the built chapters (the current source of truth for Ch1–3).
- `../game/script.rpy` — shared characters, transforms, game state.
- `notes/` — you are here (story bible + drafts).

## Viewing
`glow -p STORY_BIBLE.md` — files are written unwrapped so glow renders them cleanly (no stray `**` artifacts).
