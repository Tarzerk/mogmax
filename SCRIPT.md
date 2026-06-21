# MOGMAX — Full Script

*A satirical visual novel about the Mogging Epidemic of 2026.*
*Developed by Tarzerk & Cebolla.*

---

## Main Menu

The game opens to a custom MOGMAX main menu:

- **NEW GAME** — Start fresh from Chapter 1.
- **CONTINUE** — Resume from the most recent save *(only shown if a save exists)*.
- **CHAPTER SELECT** — Jump to a previously-completed chapter *(only shown after completing Chapter 1; warns before overwriting current progress)*.
- **SETTINGS** — Ren'Py preferences (text speed, volume, etc.).
- **QUIT**

### Chapter Unlock Rules
- **Chapter 1** — Always unlocked.
- **Chapter 2** — Unlocks after completing Chapter 1 (either pill ending counts).
- *(Future Chapter 3 — Will unlock after completing Chapter 2.)*

---

# Chapter 1 — Chopped

### Opening

*Black screen.*
**Title card:** `MOGMAX`
**Subtitle:** `Chapter 1 — Chopped`

**Text input prompt:** *What's your name?*
*(Player types a name → stored as `[name]`. Blank input defaults to "You".)*

---

### Scene — The Cafeteria

*Background: cafeteria.*

> **NARRATOR:** *Your name is [name]. At least, that's what it says on the detention slip sitting on Mr. Harker's desk — again.*
>
> **NARRATOR:** *It's a Tuesday. Or maybe Wednesday.*
>
> **NARRATOR:** *Honestly, you stopped keeping track somewhere around the third time you failed PE.*
>
> **NARRATOR:** *You're sitting in the back of the cafeteria, alone, picking at a wet sandwich you found in your own backpack from last week.*
>
> **NARRATOR:** *The expiration date is not something you want to think about.*
>
> **NARRATOR:** *Across the room, the popular kids are laughing.*
>
> **NARRATOR:** *You don't know what the joke is. You never do.*
>
> **NARRATOR:** *But somehow, you're pretty sure it's you.*
>
> **NARRATOR:** *A tray slams on the table across from you.*
>
> **NARRATOR:** *You flinch hard enough to knock your juice box onto the floor.*

*Camera shifts. Clav has sat down.*

> **CLAV:** Relax.
>
> **NARRATOR:** *The voice is calm. Too calm. You look up.*
>
> **NARRATOR:** *A guy sits across from you like he owns the cafeteria.*
>
> **NARRATOR:** *Sharp eyes, clean fit, the kind of posture that makes you suddenly aware of how bad yours is.*
>
> **NARRATOR:** *He looks at you the way a surgeon looks at a problem — like he already knows the solution.*
>
> **CLAV:** You're [name], right?
>
> **NARRATOR:** *Not a question, really.*
>
> **[name]:** ...Yeah?
>
> **CLAV:** I'm Clav.
>
> **NARRATOR:** *He leans forward.*
>
> **CLAV:** And I've been watching you for a while.
>
> **[name]:** That's... kind of creepy.
>
> **NARRATOR:** *He smirks.*
>
> **CLAV:** Maybe. But here's the thing, [name] — I think you're wasting your life.
>
> **NARRATOR:** *He pulls out two pills. One red, one blue.*
>
> **NARRATOR:** *Slides them across the table.*
>
> **CLAV:** So I'm giving you a choice.

---

### The Pill Choice

> **Choice:** *Two pills sit on the table. Clav watches, arms crossed.*
>
> - **The blue pill.** → LTN Ending *(unlabeled — player picks blind)*
> - **The red pill.** → Chad Ending → Chapter 2 *(unlabeled — player picks blind)*

---

### LTN Ending (Blue Pill)

> **NARRATOR:** *You reach for the blue pill.*
>
> **NARRATOR:** *You swallow it before you can think about it.*
>
> **CLAV:** ...blue.
>
> **CLAV:** Of course.
>
> **CLAV:** You picked the LTN pill. The Low Tier Normie pill.
>
> **CLAV:** In case you were wondering.
>
> **CLAV:** You just signed up to spend the rest of your life eating wet sandwiches in the back of the cafeteria.
>
> **CLAV:** That's fine. Someone has to.
>
> **NARRATOR:** *Clav sighs, stands up, and walks away without another word.*
>
> **NARRATOR:** *The cafeteria carries on around you.*
>
> **NARRATOR:** *Nothing changes.*

→ **Roll credits.** Chapter 1 marked complete.

---

### Chad Ending (Red Pill)

> **NARRATOR:** *You reach out and take the red pill.*
>
> **NARRATOR:** *Clav nods slowly, like he already knew.*
>
> **CLAV:** Good.
>
> **CLAV:** The work starts now.

*Black screen → title card: `— Chapter 2 —` → transition to Chapter 2.*
Chapter 1 marked complete. Chapter 2 unlocked in Chapter Select.

---

# Chapter 2 — Brainmaxxing

### Title Card

`CHAPTER 2 — ATTEMPT [n]` *(n = 1 on first try, increments on each fail-restart)*

---

### Scene 1 — Clav's Bootcamp (Library)

*Background: library, dim. Stopwatch on the table.*

**First attempt:**

> **NARRATOR:** *After school. The library is empty except for the back booth.*
>
> **NARRATOR:** *Clav is already there, reading. He doesn't look up when you sit down.*
>
> **CLAV:** Sit.
>
> **[name]:** Hey. So I —
>
> **CLAV:** Sit.
>
> **[name]:** ...sitting.
>
> **NARRATOR:** *A stopwatch hits the table. Face up. He clicks it.*
>
> **CLAV:** Ninety minutes. Seven words.
>
> **CLAV:** You will know every one of them or we sit here until you do.
>
> **CLAV:** Sit up.
>
> **CLAV:** Tomorrow morning. Harker. Snap vocab quiz.
>
> **CLAV:** Sixty or higher and the room finally looks at you.
>
> **CLAV:** Less than that and you are a ghost again.
>
> **CLAV:** Repeat the words after me.

**Subsequent attempts** (after a fail):

> **NARRATOR:** *Back to the booth. Clav is already there. He doesn't look up.*
>
> **NARRATOR:** *He slides the notebook across the table without a word.*
>
> **CLAV:** From the top.
>
> **CLAV:** Same seven. Try not to embarrass us both this time.

---

### The Drill (for each of the 7 words)

> **CLAV:** Word.
>
> **CLAV:** [word].
>
> **[name]:** [word].
>
> **CLAV:** Means: [definition].
>
> **[name]:** [definition].
>
> **CLAV:** Example.
>
> **NARRATOR:** *[example sentence]*

**After the 4th word — mid-session drill break:**

> **CLAV:** Stop. Drill.
>
> **NARRATOR:** *Clav rattles off the last four definitions in random order. You bark each matching word back.*
>
> **NARRATOR:** *You miss two. He says "again." You get them. He moves on.*

---

### The 7 Vocab Words

| # | Word | Definition | Example |
|---|------|------------|---------|
| 1 | **obsequious** | excessively eager to please | *The waiter was so obsequious to Brayden that he comped his croissant. You paid full price.* |
| 2 | **sycophant** | a flatterer who serves the powerful | *You laughed at every joke the gigachad made. You were a sycophant. Now you are a man.* |
| 3 | **magnanimous** | generous, especially in victory | *I will not destroy you today. Consider it magnanimous. Take notes.* |
| 4 | **pulchritudinous** | physically beautiful | *Brayden's maxilla growth was so pulchritudinous the yearbook added a new category.* |
| 5 | **mellifluous** | sweet and smooth-sounding | *His voice was mellifluous. Yours sounds like a printer with a paper jam.* |
| 6 | **pusillanimous** | cowardly, lacking courage | *Do not be pusillanimous. Eat the pill. Take the L. Move.* |
| 7 | **supercilious** | arrogantly superior | *Brayden's supercilious smirk has been studied by anthropologists.* |

---

### End of Study Session

> **CLAV:** Enough.
>
> **NARRATOR:** *Clav clicks the stopwatch a final time and stands.*
>
> **CLAV:** Sleep. Don't cope-scroll tonight.
>
> **CLAV:** If I see you on TikTok after midnight I am not coming to the library tomorrow.
>
> **NARRATOR:** *He leaves. You sit alone in the booth with The List.*

**Title card:** `THE NEXT MORNING`

---

### Scene 2 — The Quiz (Classroom)

*Background: classroom.*

> **NARRATOR:** *Mr. Harker's first-period English.*
>
> **MR. HARKER:** Notebooks closed. Pop quiz.
>
> **NARRATOR:** *The popular kids groan. Brayden slumps theatrically in the back row.*
>
> **NARRATOR:** *You sit up straight.*
>
> **MR. HARKER:** [name]. We will start with you.

**The quiz — for each of 7 questions:**

> **MR. HARKER:** Question [n] of 7. Define: **[word]**.

Player picks from 4 shuffled options:
- The correct definition
- Two plausible wrong definitions
- One absurd joke option (e.g., *"skibidi-adjacent"*, *"gyatt"*, *"bussin frfr"*) — never correct

**Per-question feedback (the score itself is hidden):**
- **Correct** → silence. No narrator line. (The lack of reaction IS the tell.)
- **Wrong** → *Brayden coughs into his hand. Mr. Harker's pen does not move.*
- **Joke option** → *Brayden laughs out loud. Mr. Harker does not.*

---

### Score Reveal

After all 7 questions:

> **MR. HARKER:** Pencils down.
>
> **NARRATOR:** *Mr. Harker walks to his desk and totals your sheet.*
>
> **NARRATOR:** *He looks up.*
>
> **MR. HARKER:** [name]. Your score is **[percentage]**.

**Threshold: 60.** → 5/7 correct = 71% **PASS** | 4/7 correct = 57% **FAIL**.

---

### Scene 3A — PASS (≥60)

> **NARRATOR:** *Mr. Harker slowly removes his glasses.*
>
> **NARRATOR:** *He stares.*
>
> **MR. HARKER:** ...See me after class.
>
> **NARRATOR:** *Not in trouble. Impressed.*
>
> **NARRATOR:** *The bell rings.*
>
> **NARRATOR:** *As you gather your books, every head in the room turns.*
>
> **NARRATOR:** *No one speaks.*
>
> **NARRATOR:** *Eyebrows raise.*
>
> **NARRATOR:** *Maddie catches your eye. Her gaze lingers half a second too long before she looks away.*
>
> **NARRATOR:** *In the back row, Brayden stops chewing his gum.*
>
> **[name]:** (...did I just mog the class?)

**Title card:** `THE NEXT MORNING`

---

### Scene 4 — Mirror Monologue (Resolution)

*A timed, music-driven cutscene — no clicks. Letterbox bars + a slow Ken Burns drift on every background; captions are subtitles (bottom) except the final line. Scored by `mirror_scene.mp3` from 0:42, which pre-rolls quietly under the "THE NEXT MORNING" card and swells in. Beats are synced to the song: sad inventory → flashbacks → shatter on the 1:13 drop → the lift → peak at ~1:35.*

*Background: bedroom mirror, dawn.* Internal monologue (Tanaka-inspired):

> *I'm nothing special. Average face. Average build. Average everything.*
>
> *As a kid, I was sure I'd grow into someone. Middle school. Freshman year. Still sure. ...Some nights, I'm still sure.*
>
> *And there's no room I walk into where I'm the best at anything.*

*Flashback quote cards (rapid, the low point):*

> "Move, NPC." — eighth grade
>
> "Look at this LTN." — ninth grade
>
> "Chopped." — tenth grade

*The drop (1:13): the mirror **shatters** — hard cut to broken glass.*

> *So. Average me. You got time to be looking down?*

*Turn to hope (god-rays):*

> **[name]:** I can change.
>
> **[name]:** I'm done being someone the room forgets.
>
> **[name]:** I'll do it until I can.
>
> **[name]:** No more looking down.

*Heaven (god rays) holds a beat with no text, then the peak at ~1:35, center screen:*

> **[name]:** I will mog the world.

**End card:** `END OF CHAPTER 2 — BRAINMAXXED`

→ Credits roll over the song's tail, then straight into Chapter 3.

---

### Scene 3B — FAIL (<60)

*Background: classroom.*

> **NARRATOR:** *Mr. Harker doesn't snap at you.*
>
> **NARRATOR:** *He just looks at the paper.*
>
> **NARRATOR:** *He sighs through his nose.*
>
> **NARRATOR:** *Takes off his glasses.*
>
> **NARRATOR:** *Pinches the bridge of his nose.*
>
> **NARRATOR:** *He says nothing.*
>
> **NARRATOR:** *Somehow that's worse than yelling.*
>
> **BRAYDEN:** Bro.
>
> **BRAYDEN:** You really thought "skibidi" was a definition?
>
> **BRAYDEN:** That's negative aura, dawg.
>
> **NARRATOR:** *The class loses it. Phones come out. Someone is filming.*
>
> **NARRATOR:** *From two rows over, casual, like it doesn't matter:*
>
> **NARRATOR:** *"Same [name] as ninth grade. Crazy how some people just don't grow."*
>
> **NARRATOR:** *Maddie doesn't laugh.*
>
> **NARRATOR:** *She doesn't mock.*
>
> **NARRATOR:** *She looks at her desk. And doesn't look up.*
>
> **NARRATOR:** *Pity is louder than mockery.*

*Hallway.*

> **NARRATOR:** *You gather your books. The hallway feels longer than usual.*
>
> **[name]:** (Invisible.)
>
> **[name]:** (Still invisible.)
>
> **[name]:** (Worse than invisible — now they know I tried.)
>
> **NARRATOR:** *Your phone buzzes.*
>
> **NARRATOR:** **CLAV 🥶**
>
> **NARRATOR:** *"[rotating message]"*

**Clav's texts rotate by attempt number** (1 → 7, then loops):

1. *sighhh you are such a normie....*
2. *yawn. booth. don't be late.*
3. *i thought you were different. clearly not. library.*
4. *mid effort. mid result. we go again.*
5. *embarrassing. for me. booth in ten.*
6. *this is the part where you cope. i'll wait.*
7. *truly the most normie thing i've ever seen. library. now.*

---

### Fail Screen

A modal overlay:

```
CHAPTER 2 — FAILED
Score: [score] / 100
Attempt [n]

[ RESTART CHAPTER ]
[ QUIT TO MAIN MENU ]
```

- **RESTART CHAPTER** → `chapter2_attempt += 1` → back to Scene 1 (Clav's Bootcamp) with vocab order shuffled.
- **QUIT TO MAIN MENU** → returns to main menu.

---

# Credits

*Auto-scrolling credits roll (~240 seconds, click to skip).*

```
                  MOGMAX

         Chapter 1 — Chopped
       Chapter 2 — Brainmaxxing


              Developed by

                 Tarzerk
                    &
                 Cebolla


           — bonus material —
      the Bee Movie (Dreamworks, 2007)

         [full 1,363-line Bee Movie script]


         Thank you for playing.

              Stay sigma.
```

→ Returns to main menu.
