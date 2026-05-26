# MOGMAX — Background Asset Reference

Replace any image listed below by dropping a file with the **exact filename** into [game/images/](game/images/). Ren'Py picks it up automatically on next launch — no code changes required.

---

## Format spec

- **File format**: JPG preferred (smaller filesize, no transparency needed). PNG OK if you have it.
- **Resolution**: **1920×1080** preferred. **1280×720** minimum.
- **Aspect ratio**: **16:9** (the game runs at 1280×720 virtual; Ren'Py scales to fit).
- **Color space**: sRGB.
- **Naming**: lowercase, underscores, no spaces — must match the filenames in the table below exactly.

---

## Backgrounds in the game right now

All currently point at placeholder JPGs lifted from Ren'Py's `the_question` sample project. Replace each with your own to fully theme the game.

| Scene name in script | Current placeholder | What it should look like | Used in |
|---|---|---|---|
| `bg cafeteria` | `bg_lecturehall.jpg` | School cafeteria — tables, fluorescent lights, popular kids visible in background, generally lonely / institutional vibe | Ch1 — opening scene |
| `bg cafeteria_clav` | `bg_lecturehall.jpg` | Same cafeteria but tighter / darker / more focused — the moment Clav sits down. Could be the same image or a darkened variant | Ch1 — Clav's intro |
| `bg library` | `bg_uni.jpg` | School library, back-booth area. Shelves of books, dim lighting, single lamp on a study table. Slightly oppressive | Ch2 — bootcamp / flashcard study |
| `bg classroom` | `bg_lecturehall.jpg` | Standard high-school classroom. Desks in rows, blackboard at front, Mr. Harker's domain | Ch2 — quiz intro + fail scene |
| `bg classroom_silent` | `bg_lecturehall.jpg` | Same classroom but more dramatic — empty/quiet feel, slightly dimmer or with a softer light. The moment after the player mogs the class | Ch2 — pass scene |
| `bg bedroom_dawn` | `bg_meadow.jpg` | Protagonist's bedroom at dawn. Blinds half-open, morning light, a mirror visible on the wall. Personal / quiet | Ch2 — mirror scene |
| `bg city_view` | `bg_uni.jpg` | Looking out a window over a city skyline. Cold, indifferent, urban. Slight haze, sun coming up | Ch2 — resolution moment |
| `bg flashback` | (solid `#0a0a0a`) | Stylized memory cuts — best left abstract / near-black. Don't replace unless you want a specific flashback look | Ch2 — bully memories |
| `bg hallway` | `bg_uni.jpg` | Empty school hallway after the bell. Lockers on both sides, fluorescent lights, longer-than-it-needs-to-be perspective | Ch2 — fail-walk scene |

---

## How to replace

1. Save your replacement image as `game/images/bg_lecturehall.jpg` (or whichever filename from the table).
2. To use a different filename, edit `image bg X = "images/your_file.jpg"` in either:
   - `game/script.rpy` (cafeteria, cafeteria_clav)
   - `game/chapter2.rpy` (library, classroom, classroom_silent, bedroom_dawn, city_view, flashback, hallway)
3. Relaunch the game — Ren'Py recompiles on startup.

---

## Quick checklist for a full art pass

If you want to commission/generate art and replace everything, you need **8 unique backgrounds**:

1. ☐ Cafeteria (wide shot, lonely table)
2. ☐ Cafeteria — Clav focus (tighter / dimmer variant of #1)
3. ☐ Library (back-booth study area)
4. ☐ Classroom (Mr. Harker's room — neutral)
5. ☐ Classroom — silent / dramatic (variant of #4)
6. ☐ Bedroom at dawn (with mirror)
7. ☐ City view from window
8. ☐ School hallway (lockers)

Optional 9th: stylized flashback layer (or keep solid black).

---

## Other image assets in the project

These come from the Ren'Py template and aren't backgrounds, but they exist if you want to know:

- `game/gui/main_menu.png` — main menu background (currently a stock dark plate)
- `game/gui/game_menu.png` — in-game pause-menu background
- `game/gui/button/*.png` — button textures
- `game/gui/frame.png` — text-box frame
- `game/gui/namebox.png` — speaker-name plate

To re-theme the menu screens too, replace those — same drop-in pattern.
