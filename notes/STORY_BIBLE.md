# MOGMAX — Story Bible

*The durable design doc — the "why" behind the game. For what the game literally does, read `game/*.rpy`. For chapters that aren't built yet, see `CH4-5_DRAFT.md`. (See `README.md` for how these notes are organized.)*

## Chapter status
| Chapter | Status | Lives in |
|---|---|---|
| Ch1 — Chopped | ✅ in code | `game/chapter1.rpy` |
| Ch2 — Brainmaxxing | ✅ in code | `game/chapter2.rpy` |
| Ch3 — The Mogbender | ✅ in code · *Eugene redesign pending* | `game/chapter3.rpy` |
| Ch4 — Auramaxxing | 📝 draft | `CH4-5_DRAFT.md` |
| Ch5 — The Final Boss | 📝 draft | `CH4-5_DRAFT.md` |

---

## Premise
You play a bullied, nameless high schooler at the very bottom of the social food chain — an **LTN ("Low Tier Normie")**: invisible, forgettable, zero aura. The game is the deadpan-comedic story of climbing out of that hole through "mogging" (self-improvement taken to absurd, conspiratorial extremes) — and what it costs you along the way.

## The story so far (Ch1–2)
**Ch1 — Chopped.** Alone in the cafeteria with a week-old wet sandwich, you're humiliated by **Brayden**, the apex popular kid. **Clav** — sharp, calm, surgical — sits down uninvited, says he's been watching you, and slides two pills across the table: **red** (become a Chad → you're in, training starts; canonical path) or **blue** (remain an LTN → cold bad ending: a "case file" prints stamped CLOSED, and the **Gigachad** at a city-window desk mutters *"How shameful."*).

**Ch2 — Brainmaxxing.** Clav drills you through a timed library vocab bootcamp, then **Mr. Harker** springs a timed pop quiz. **Pass (≥60):** the class goes silent, even Brayden rattled — a "YOU JUST BRAINMOGGED" reveal, a mirror flashback to years of bullying, and a resolve ("I will mog the world") → BRAINMAXXED, into Ch3. **Fail (<60):** the class mocks/films you, Clav texts his disappointment, restart or quit.

**Arc:** invisible LTN → chooses self-improvement → proves himself mentally (Brain). The recurring mystery is the **Gigachad** — the unreachable "ceiling."

---

## The spine (what's working — protect it)
- **Choices are deliberately fake until the finale.** Ch1 sandwich, Ch1 pills, Ch4 silent-nod finisher, Ch5 the first choice that truly matters. The game trains you to distrust choices, then hands you a real one.
- **"What actually mogs what" keeps escalating:** Brain → Frame → Aura → (Friendship / Utility). The two endings are the two final answers.
- **The Casio watch = the thesis.** Utility mogs aura. The bad ending isn't a punishment, it's the argument: you became all aura, no substance.
- **Eugene is the moral ledger** (see Core mechanic).

## Characters
- **You / the LTN** — the bottom of the hierarchy, climbing. The new "Jimmy" (see Lens).
- **Clav** — mentor who turns villain in Ch4. The former low-status kid who already conquered the hierarchy and got consumed by it; can't stand being surpassed. = *Jimmy-who-became-Gary.*
- **Brayden** — the apex jock; the *false* antagonist, beaten for good in Ch4's Mog-Off.
- **Eugene** — invisible unpaid intern; who *you* used to be. The game's moral ledger.
- **The Gigachad** — the unreachable ceiling; the mystery Clav "got close" to.
- **The Casio judge** — utility incarnate; out-mogs maxed aura without looking up (Ending A).

---

## Core mechanic — the Eugene choice ("mog him or lift him")
**The problem with the old Ch3 version:** the Eugene choice was *be nice* vs. *be cold*. Kindness was free; cruelty was cartoonish. Nothing at stake — yet it's the one choice meant to carry the whole good ending.

**The fix:** Eugene is who *you* were in Ch1 — invisible, unpaid, the wet-sandwich LTN. By Ch3 you've trained Brain/Frame/Aura, so for the first time you can **mog a real person**, unforced. The choice becomes: *now that you have the power, what do you point it at?* It's a dry-run for the Ch5 finale (mog Clav vs. lift the cafeteria). Same power, two directions. The passive "walk past" option is removed on purpose — you can't be neutral about power once you have it.

> ⚠ **Critical:** *mog* must be genuinely **tempting** (the rush of finally being on top, Clav's approval, "for once someone's below me"). If it reads as an obvious evil button, it's just the old nice/cold problem again.

### The payoff — Eugene colors ALL four endings (2×2)
*(Ch3 choice × Ch5 choice. Don't gate Eugene to just the good ending — make the Ch3 choice felt no matter what.)*

| | **Refuse Clav (good)** | **Mog Clav (Dark Chad)** |
|---|---|---|
| **Lifted Eugene** | ① Full good ending | ④ Tragic bad ending |
| **Mogged Eugene** | ② Lonelier good ending | ③ Inevitable bad ending |

- **① Lifted → Refuse:** crowd skeptical until Eugene steps forward *first* — "He saw me when nobody else would." His vouch lands because he's the lowest-status person there. Crowd swings.
- **② Mogged → Refuse:** same noble choice, but Eugene won't vouch (arms crossed). You win *alone*, the hard way. *Tone: earned solitude, not the game scolding you.* Small ambiguous nod on the way out.
- **③ Mogged → Mog:** Eugene was the first domino. Courtroom collapse flashes back to the closet — *re-show it literally, replay his line.* The arrest is just the bill.
- **④ Lifted → Mog:** you proved you could be better. Catch Eugene's disappointed face as you fall — one silent beat, no lecture. The wound is that you knew the other road.

Put the best lines in the **mismatch cells (② and ④)** — ① and ③ are the "expected" paths.

---

## Lens — *Bully* (Canis Canem Edit)
The arc rhymes with Bully, with one twist: **Clav ≈ Jimmy-who-became-Gary.** He already ran the climb and conquered the hierarchy, then got consumed by it. **Brayden = a clique-leader boss** you beat on the way up. **Clav = the Gary turn** — rather than fight head-on, he manipulates the school against you (rumor campaign), then becomes the true final boss. **You = the new Jimmy.** Ending B = Jimmy's real resolution (didn't want to rule by fear, wanted to belong). Ending A = you *become* Clav; the cycle repeats.

*Tentative:* one planted line in Ch5 making the mirror text — e.g. Clav: *"I ate that sandwich too."* (Still deciding: planted line vs. subtext.)

## Transitions & pacing (game-wide)
**Default:** a 2–4 line establishing beat before any new location — *when, where, how you got here, headspace.* Template: ① time/place stamp → ② one sensory anchor (sound/light) → ③ motion or arrival → ④ optional internal line. Then get out of the way — over-padding kills pacing too.

**Hard cut only when disorientation IS the point** (surprise, betrayal, shock) — signal with a jarring SFX or smash-to-black.
- *Keep hard (earned):* Ch3 honk-honk abduction; Ch4-end betrayal cut-to-black.
- *Needs a bridge (currently cold):* Ch1→Ch2 library (plant the appointment at the end of Ch1, establish on arrival); chapter intros that jump from title card straight into a room.

## Ending map
- **A — The Dark Chad (bad):** out-mog Clav with toxicity → drunk on aura, arrested for refusing to break a mewing streak → courtroom → the **Casio judge** out-mogs you with pure utility, never looking up → stats shatter, 30 days community service. *Utility mogs aura; you became Clav.*
- **B — The True Gigachad (good):** refuse to mog → "Power of Friendship" beam, sincerely *see* the whole cafeteria → Eugene gate (per matrix) → Clav evaporates (vampire-at-dawn) → MOGKAGE earned the right way → steps scene → *"It was never about becoming a Chad. It was about the friends you mogged along the way."*

---

## Polish backlog (already-built chapters + open threads)
- **Ch3 Eugene redesign (mog/lift)** — drafted, *not yet in code.* Full scene + matrix above; Ren'Py draft retired (rewrite from this when implementing). Needs `default mogged_eugene = False`.
- **Ch1–3 LTN monologue punch-ups** — lean on the parenthetical internal voice (the Ch2 fail "(Invisible.)(Still invisible.)..." is the sharpest device in the game). A handful of 1-line inserts; no story change.
- **Ch1→Ch2 library transition** — plant Clav's appointment at the end of Ch1, establish on arrival in Ch2.
- **Ch3 "moggers" walk-and-talk** — Clav's speech over gold-lit silhouette displays into the training wing (relocates the cut Ch2 "people who mog without trying" beat). Drafted in `CH4-5_DRAFT.md`.
- **Open threads:** make "mog" tempting (not an evil button); lock the Clav mirror line; confirm MOGKAGE placement (currently held to Ending B); give Ending B the Casio courtroom's specificity; confirm Eugene is planted clearly in Ch4 + Ch5 Act 1.
