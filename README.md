# MOGMAX

*A satirical visual novel about the looksmaxxing epidemic of 2026.*

> **Based on a true story.**

Built in [Ren'Py](https://www.renpy.org/) 8.5. Two chapters, ~15–20 minutes to play through, branching ending, soundtracked and shaderless. Made by **Tarzerk** & **Cebolla**.

---

## What is this

You're a low-tier normie at a high school. A guy named **Clav** sits down across from you at lunch, calls you out, and offers a choice between two pills.

- **Red pill** → Chapter 2: a brutal vocab quiz, a public mog, and a sunrise resolution.
- **Blue pill** → roll credits. Stay the way you are.

Chapter 2 is a bootcamp + flashcard study + timed vocab quiz where your score determines whether you mog the whole class or get filmed eating it. Music-synced cinematics, custom UI screens, on-the-beat reveals.

---

## Playing it

There are two ways in: download a prebuilt copy (easiest, no Ren'Py install) or run from source. Prebuilt copies are produced by the GitHub Actions pipeline.

### Get a build

**Easiest (no GitHub account needed)** — grab a tagged release from the [**Releases page**](https://github.com/Tarzerk/mogmax/releases). Pick the latest version, then download the file matching your platform:

| Platform | Asset |
|---|---|
| Windows | `MOGMAX-<version>-pc.zip` |
| macOS | `MOGMAX-<version>-mac.dmg` (or `MOGMAX-<version>-mac.zip` as fallback) |
| iOS / Android | `MOGMAX-<version>-pc.zip` (yes — same file as Windows; see below) |

Release downloads are public — anyone with the link can grab them, no sign-in required. This is the right link to send to friends.

**Latest dev build (requires GitHub login)** — every push to a `v*` tag, plus any manual run, produces fresh builds attached to the [Actions run page](https://github.com/Tarzerk/mogmax/actions/workflows/build.yml). Click into a run → scroll to **Artifacts** → download:

| Platform | Artifact |
|---|---|
| Windows | `MOGMAX-windows-and-pocket` |
| macOS | `MOGMAX-mac-dmg` (or `MOGMAX-mac-zip` as fallback) |
| iOS / Android | `MOGMAX-windows-and-pocket` |

GitHub gives you each artifact as a `.zip` wrapper. Unzip it first, then follow the platform steps below.

### Windows

1. Unzip `MOGMAX-windows-and-pocket.zip`.
2. Inside the inner `MOGMAX-<version>-pc/` folder, double-click **`MOGMAX.exe`**.

That's it — no install step. To uninstall, just delete the folder.

> First-launch SmartScreen warning is normal (the .exe isn't code-signed). Click **More info → Run anyway**.

### macOS

1. Double-click `MOGMAX-mac-dmg.zip` to unzip it, then double-click `MOGMAX-<version>-mac.dmg` to mount.
2. Drag **`MOGMAX.app`** into your `Applications` folder.
3. **First launch only:** right-click `MOGMAX.app` → **Open** → confirm. (Plain double-click will be blocked by Gatekeeper because the app isn't notarized.)

If Gatekeeper still refuses, run this once in Terminal:

```bash
xattr -dr com.apple.quarantine /Applications/MOGMAX.app
```

### iOS / iPadOS / Android (via Ren'Py Pocket)

[Ren'Py Pocket](https://renpyandroid.com/) is a mobile app that runs Ren'Py games from a zip. The same `MOGMAX-windows-and-pocket.zip` works as the mobile package — it contains the `game/` and `renpy/` folders Pocket expects.

1. Install **Ren'Py Pocket** ([iOS App Store](https://apps.apple.com/us/app/renpy-pocket/id6748696950) / Android equivalent).
2. Download `MOGMAX-windows-and-pocket.zip` from the Actions tab onto your phone, *or* keep it on your computer and use Pocket's **Wi-Fi Transfer**:
   - In Pocket, tap **Wi-Fi Transfer** to start a local server.
   - Open the address it shows in your computer's browser.
   - Drag the zip into the browser page — it uploads and installs.
3. Tap **MOGMAX** in Pocket's library to launch.

> If iOS rejects the import, unzip in the Files app, long-press the folder, **Compress**, then import that new zip. (iOS occasionally chokes on zips produced on other OSes.)

### Run from source (developers)

Requires the [Ren'Py SDK 8.5+](https://www.renpy.org/latest.html).

1. Clone this repo.
2. Open the Ren'Py launcher.
3. Preferences → set **Projects Directory** to the folder *containing* your clone.
4. Back at the main launcher, **MOGMAX** appears in the project list — click **Launch Project**.

Or, from the command line:

```bash
"path/to/renpy-sdk/renpy.exe" "path/to/mogmax"
```

### Dev shortcuts

While running in dev mode (default for unbuilt projects):

- **Shift + D** — opens a dev "skip to scene" menu (Ch1 / Ch2 / quiz / pass / mirror / credits). Saves you replaying the quiz on every iteration.
- **Shift + O** — opens the Ren'Py console for arbitrary `jump <label>` commands.
- **Ctrl** — hold to fast-skip dialogue.

---

## Project layout

```
mogmax/
├── README.md             ← you are here
├── BACKGROUNDS.md        ← spec for swapping background art
├── SCRIPT.md             ← human-readable transcript of all dialogue
├── .gitignore
└── game/
    ├── script.rpy        ← Chapter 1 (cafeteria, pill choice, both endings)
    ├── chapter2.rpy      ← Chapter 2 (bootcamp, quiz, mirror finale)
    ├── screens.rpy       ← all custom UI (main menu, choice, study cards,
    │                       quiz, fail screen, chapter select, dev skip menu)
    ├── credits.rpy       ← end credits roll
    ├── options.rpy       ← project config
    ├── gui.rpy           ← GUI constants (from the_question template)
    ├── bee_movie.txt     ← bonus credits filler
    ├── audio/            ← 12 mp3 files (see below)
    ├── images/           ← 10 jpg backgrounds (see BACKGROUNDS.md)
    └── gui/              ← UI textures from Ren'Py template
```

### Audio (`game/audio/`)

| File | Used for |
|---|---|
| `main_menu_theme.mp3` | main menu loop, carries into Ch1 intro |
| `cafeteria_ambient.mp3` | Ch1 cafeteria background loop |
| `tray_slam.mp3` | one-shot — Clav's tray slams on the table (Ch1) |
| `pill_pickup.mp3` | one-shot — pill choice menu appears |
| `swallow_sfx.mp3` | one-shot — fires when you pick a pill |
| `library_ambient.mp3` | Ch2 bootcamp + flashcards background loop |
| `quiz_tension.mp3` | Ch2 quiz background loop |
| `quiz_buzzer.mp3` | one-shot — 10 seconds remaining on quiz timer |
| `bell_school.mp3` | one-shot — bell rings on Ch2 pass |
| `mogging_sfx.mp3` | one-shot — BRAINMOGGED reveal hit (5.75s mark) |
| `mirror_theme.mp3` | mirror scene background (sad piano) |
| `gigachad_theme.mp3` | skyline finale + chad-ending credits |

### Backgrounds (`game/images/`)

10 jpgs, all 16:9. See [BACKGROUNDS.md](BACKGROUNDS.md) for the per-scene mapping and recommended replacement specs.

---

## Notable design choices

- **Custom flashcard study screen** — Ch2's vocab "study session" is a 5×2 grid of cards you flip individually, not a 49-click dialogue slog.
- **Pinned-question quiz screen** — the word you're being tested on stays visible on top of the answer buttons. No more "wait, what was the question?"
- **Timed quiz** — 105 seconds total (matches the music track). Buzzer at 10s remaining, auto-submit at 0.
- **Music-synced cinematics** — the skyline finale auto-times text reveals to specific positions in the gigachad theme so the drop lands on "I will mog the world." regardless of clicking speed.
- **Bullying flashback** — Ch2 mirror scene flashes three real-photo bg's mid-monologue.
- **Persistent progress** — chapter select unlocks chapters as you complete them. Saved across sessions.
- **Bee Movie credits** — the full 1,363-line Bee Movie script scrolls past after the cast. Skippable, but it's there.

---

## Credits

- **Development & writing**: Tarzerk & Cebolla
- **Engine**: [Ren'Py](https://www.renpy.org/) by Tom "PyTom" Rothamel
- **GUI scaffolding**: adapted from the `the_question` sample project bundled with the Ren'Py SDK
- **Bonus credits filler**: *the Bee Movie* (Dreamworks, 2007)

---

## License

All original code and writing in this project is © 2026 Tarzerk & Cebolla. The bundled Bee Movie script is included under fair-use parody / homage and is © Dreamworks. Ren'Py and `the_question` template assets are under their original licenses (MIT-equivalent for Ren'Py; freely distributable for the template).
