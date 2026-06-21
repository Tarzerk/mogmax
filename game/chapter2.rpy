# MOGMAX — Chapter 2: Brainmaxxing
# Characters (c, h, p, b, narrator) are defined in script.rpy

default brain_score = 0
default chapter2_attempt = 1
default final_score = 0
default ch2_studied = set()
default ch2_clav_quip = ""

# Quiz timer state — total 105s to answer all 10 questions, buzzer at <=10s
default quiz_start_time = 0.0
default quiz_duration = 105.0
default buzzer_played = False

image bg library = bg_image("images/bg_library.jpg")
image bg classroom = bg_image("images/bg_classroom.jpg")
image bg classroom_silent = bg_image("images/bg_classroom_silent.jpg")
image bg bedroom_dawn = bg_image("images/bg_bedroom_dawn.jpg")
image bg city_view = bg_image("images/bg_city_view.jpg")
image bg shattered_mirror = bg_image("images/bg_shattered_mirror.jpg")
image bg hope = bg_image("images/bg_hope.jpg")
image bg god_rays = bg_image("images/bg_god_rays.jpg")
image bg flashback = "#0a0a0a"
image bg hallway = bg_image("images/bg_hallway.jpg")


# Bullying images for the mirror-scene flashback.
# Falls back to solid black if the file isn't present, so the scene
# never crashes while assets are being added.
init python:
    def bully_bg(num):
        path = "images/bg_bully_{}.jpg".format(num)
        if renpy.loader.loadable(path):
            return bg_image(path)
        return Solid("#0a0a0a")

image bg bully1 = bully_bg(1)
image bg bully2 = bully_bg(2)
image bg bully3 = bully_bg(3)


# ─── Fail-state screen (Quit to main / Restart chapter) ──────
screen fail_screen():
    modal True
    add Solid("#000000")

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 22

        text "CHAPTER 2 — FAILED":
            size 70
            color "#ff4444"
            xalign 0.5

        text "Score: [final_score] / 100":
            size 34
            color "#cccccc"
            xalign 0.5

        null height 50

        textbutton "RESTART CHAPTER":
            action Return("restart")
            xalign 0.5
            text_size 36
            text_color "#88ff88"
            text_hover_color "#ffffff"
            text_idle_color "#88ff88"

        textbutton "QUIT TO MAIN MENU":
            action Return("quit")
            xalign 0.5
            text_size 36
            text_color "#ff8888"
            text_hover_color "#ffffff"
            text_idle_color "#ff8888"


init python:
    import time as _qtime

    def _wait_until_music_pos(target_seconds, channel="music", max_wait=90.0):
        """Block until the given music channel's playback position reaches
        target_seconds (or max_wait elapses, as a safety net)."""
        deadline = _qtime.time() + max_wait
        while _qtime.time() < deadline:
            pos = renpy.music.get_pos(channel=channel) or 0
            if pos >= target_seconds:
                return
            renpy.pause(0.25, hard=True)

    def _quiz_tick():
        """Fired ~4x/sec by the quiz_question screen. Plays the buzzer
        SFX once when ≤10s remain, and force-ends the quiz at ≤0s."""
        remaining = store.quiz_duration - (_qtime.time() - store.quiz_start_time)
        if not store.buzzer_played and remaining <= 10:
            renpy.play("audio/quiz_buzzer.mp3", channel="sound")
            store.buzzer_played = True
        if remaining <= 0:
            renpy.end_interaction("timeout")


init python:
    # Ten vocab words for the Brainmaxxing quiz — a mix of easier SAT, mid SAT,
    # and a couple of hard SAT/GRE holdouts so the list isn't uniformly brutal.
    # Each entry: correct def + two plausible wrongs + one brainrot joke option +
    # a Clav-voiced mogging-themed example sentence.
    VOCAB = [
        # Easier SAT
        {"word": "gregarious", "correct": "sociable, fond of company",
         "wrong_a": "scholarly, fond of books", "wrong_b": "easily irritated",
         "joke": "rizz-coded",
         "example": "Brayden is {b}gregarious{/b}. He has friends. You have... aspirations. — Clav"},

        {"word": "tenacious", "correct": "persistent, holding firmly",
         "wrong_a": "loud and aggressive", "wrong_b": "having teeth",
         "joke": "L-resistant",
         "example": "Your mewing routine is {b}tenacious{/b}. Your jaw, however, remains stubbornly average. — Clav"},

        {"word": "candor", "correct": "honest, frank expression",
         "wrong_a": "a kind of sweet pastry", "wrong_b": "fear of enclosed spaces",
         "joke": "no-cap energy",
         "example": "I appreciate your {b}candor{/b} when you admit you are chopped. It saves us both time. — Clav"},

        {"word": "jovial", "correct": "cheerful and good-humored",
         "wrong_a": "youthful and inexperienced", "wrong_b": "related to jewelry",
         "joke": "drip-coded",
         "example": "Mr. Harker is not {b}jovial{/b}. Do not attempt to make him laugh. You will lose. — Clav"},

        # Mid SAT
        {"word": "obsequious", "correct": "excessively eager to please",
         "wrong_a": "loud and easily provoked", "wrong_b": "elderly or aged",
         "joke": "skibidi-adjacent",
         "example": "The waiter was so {b}obsequious{/b} to Brayden that he comped his croissant. You paid full price. — Clav"},

        {"word": "ephemeral", "correct": "lasting only briefly",
         "wrong_a": "eternal and unchanging", "wrong_b": "made of metal",
         "joke": "fanum-tax energy",
         "example": "Your high school aura is {b}ephemeral{/b}. Use it now. Or do not. It is already fading. — Clav"},

        {"word": "supercilious", "correct": "arrogantly superior",
         "wrong_a": "extremely silly", "wrong_b": "ceiling-related",
         "joke": "Chad behavior",
         "example": "Brayden's {b}supercilious{/b} smirk has been studied by anthropologists. Do not try to mirror it. — Clav"},

        {"word": "mellifluous", "correct": "sweet and smooth-sounding",
         "wrong_a": "yellow in color", "wrong_b": "sticky to the touch",
         "joke": "bussin frfr",
         "example": "His voice was {b}mellifluous{/b}. Yours sounds like a printer with a paper jam. — Clav"},

        # Hard SAT / GRE (kept for flavor)
        {"word": "magnanimous", "correct": "generous, especially in victory",
         "wrong_a": "physically large", "wrong_b": "secretly cruel",
         "joke": "sigma-coded",
         "example": "I will not destroy you today. Consider it {b}magnanimous{/b}. Take notes. — Clav"},

        {"word": "pulchritudinous", "correct": "physically beautiful",
         "wrong_a": "extremely angry", "wrong_b": "containing pulp",
         "joke": "gyatt",
         "example": "Brayden's maxilla growth was so {b}pulchritudinous{/b} the yearbook added a new category. — Clav"},
    ]

    # Clav cut-in quips. One is picked at random when the study screen opens
    # and shown as a subtitle under the header — keeps Clav's voice present
    # in the flashcard phase even though the dialogue loop is gone.
    CLAV_STUDY_QUIPS = [
        "Don't cheat with the back of the notebook.",
        "I can see you stalling.",
        "Flip them all. I'll know if you skipped one.",
        "Stop staring at the joke options. There's a reason they're called that.",
        "Pulchritudinous is on the test. Memorize it.",
        "You have ninety minutes. You've used eight.",
        "If you can't read it, sound it out. Then weep.",
        "Read every example. Yes, every one. I wrote them.",
        "You blinked. I noticed.",
    ]


# ═════════════════════════════════════════════════════════════
# SCENE 1 — CLAV'S BOOTCAMP (LIBRARY)
# Attempt 1: full bootcamp.
# Attempt 2+: shortened (skip per-word teach loop).
# ═════════════════════════════════════════════════════════════

label chapter2_start:
    $ brain_score = 0
    # Title card on black for legibility, then fade into the library.
    scene bg black with fade
    pause 0.4
    show text "{size=54}Chapter 2 — Brainmaxxing{/size}" at truecenter with dissolve
    pause 2.0
    hide text with dissolve

    scene bg library with fade
    # Quiet library ambience runs through the bootcamp + flashcard study.
    play music "audio/library_ambient.mp3" fadein 2.0 volume persistent.vol_bed

    if chapter2_attempt == 1:
        narrator "After school. The library is empty except for the back booth."
        show clav thinking at clav_body
        narrator "Clav is already there, reading. He doesn't look up when you sit down."
    else:
        narrator "Back to the booth. Clav is already there. He doesn't look up."
        show clav stern at clav_body
        narrator "He slides the notebook across the table without a word."
        c "From the top."

    pause 0.5

    if chapter2_attempt == 1:
        show clav stern at clav_body
        c "Sit."
        p "Hey. So I —"
        c "Sit."
        p "...sitting."
        narrator "A stopwatch hits the table. Face up. He clicks it."
        c "Ninety minutes. Ten words."
        c "You will know every one of them or we sit here until you do."
        c "Sit up."
        show clav thinking at clav_body
        c "Tomorrow morning. Harker. Snap vocab quiz."
        c "Sixty or higher and the room finally looks at you."
        show clav smirk at clav_body
        c "Less than that and you are a ghost again."
        show clav stern at clav_body
        c "Notebook's in front of you. Get to work."
    else:
        show clav stern at clav_body
        c "Same ten. Lock in."

    # Reset flashcard state and pick a fresh Clav quip for this attempt.
    # Player flips cards at their own pace and clicks TAKE THE QUIZ to advance.
    $ ch2_studied = set()
    $ ch2_clav_quip = renpy.random.choice(CLAV_STUDY_QUIPS)
    call screen study_flashcards
    jump study_done


label study_done:
    pause 0.5
    show clav smirk at clav_body
    c "Enough."
    narrator "Clav clicks the stopwatch a final time and stands."
    c "Sleep. Don't cope-scroll tonight."
    show clav stern at clav_body
    c "If I see you on TikTok after midnight I am not coming to the library tomorrow."
    show clav stern at clav_body
    c "We're done here for now. Don't make that mean nothing."
    hide clav
    narrator "He leaves. You sit alone in the booth with The List."
    pause 1.0
    scene bg black with fade
    pause 0.6
    show text "THE NEXT MORNING" at truecenter with dissolve
    pause 1.8
    hide text with dissolve
    jump class_quiz


# ═════════════════════════════════════════════════════════════
# SCENE 2 — THE QUIZ (CLASSROOM)
# Joke option appears on only 3 of 7 questions (randomized per attempt).
# Score is hidden until reveal.
# ═════════════════════════════════════════════════════════════

label class_quiz:
    scene bg classroom with fade
    play music "audio/quiz_tension.mp3" fadeout 1.5 fadein 1.5 volume persistent.vol_music
    narrator "Mr. Harker's first-period English."
    show harker pointing at harker_body
    h "Notebooks closed. Pop quiz."
    narrator "The popular kids groan. Brayden slumps theatrically in the back row."
    narrator "You sit up straight."
    show harker stopwatch at harker_body
    h "[povname]. We will start with you."

    $ brain_score = 0
    $ shuffled_vocab = list(VOCAB)
    $ renpy.random.shuffle(shuffled_vocab)

    # Pick 4 of the 10 question indices to receive the brainrot joke option.
    # The other 6 get a plausible wrong distractor pulled from another word.
    $ joke_question_indices = set(renpy.random.sample(range(len(shuffled_vocab)), 4))

    # Start the 105-second countdown (matches the length of quiz_tension.mp3).
    $ quiz_start_time = _qtime.time()
    $ buzzer_played = False

    $ quiz_idx = 0

label quiz_loop:
    if quiz_idx >= len(shuffled_vocab):
        jump quiz_finished

    $ q = shuffled_vocab[quiz_idx]
    $ q_word = q["word"]
    $ q_num = quiz_idx + 1

    python:
        if quiz_idx in joke_question_indices:
            # Joke-option question
            choices_list = [
                (q["correct"], "correct"),
                (q["wrong_a"], "wrong"),
                (q["wrong_b"], "wrong"),
                (q["joke"], "joke"),
            ]
        else:
            # Four plausible options — third wrong pulled from another word
            other_words = [v for v in VOCAB if v["word"] != q["word"]]
            other = renpy.random.choice(other_words)
            extra_wrong = renpy.random.choice([other["wrong_a"], other["wrong_b"]])
            choices_list = [
                (q["correct"], "correct"),
                (q["wrong_a"], "wrong"),
                (q["wrong_b"], "wrong"),
                (extra_wrong, "wrong"),
            ]
        renpy.random.shuffle(choices_list)

    $ result = renpy.call_screen("quiz_question", q_num=q_num, total=len(shuffled_vocab), word=q_word, options=choices_list)

    # Time's up — bail straight to the score reveal regardless of progress.
    if result == "timeout":
        jump quiz_timeout

    if result == "correct":
        $ brain_score += 1
        # Silence is the tell.
    elif result == "joke":
        narrator "{i}Brayden laughs out loud. Mr. Harker does not.{/i}"
    else:
        narrator "{i}Brayden coughs into his hand. Mr. Harker's pen does not move.{/i}"

    $ quiz_idx += 1
    jump quiz_loop


# Force-end path when the timer runs out — current correct count is final.
label quiz_timeout:
    stop music fadeout 1.0
    pause 0.4
    narrator "{i}Time is up. Pencils down.{/i}"
    pause 1.0
    $ final_score = int((brain_score / float(len(VOCAB))) * 100)
    narrator "Mr. Harker walks to his desk and totals what you managed to finish."
    pause 0.8
    narrator "He looks up."
    pause 0.4
    show harker tired at harker_body
    h "[povname]."
    if final_score >= 60:
        pause 0.7
        narrator "He pauses."
        pause 0.4
        narrator "Longer than he needs to."
        pause 0.6
        show harker glasses at harker_body
        h "Your score is {b}[final_score]{/b}."
        pause 1.4
        jump pass_class_scene
    else:
        show harker facepalm at harker_body
        h "Your score is {b}[final_score]{/b}."
        pause 1.2
        jump fail_class_scene


label quiz_finished:
    $ final_score = int((brain_score / float(len(VOCAB))) * 100)
    pause 0.6
    show harker pointing at harker_body
    h "Pencils down."
    stop music fadeout 2.0
    pause 0.4
    narrator "Mr. Harker walks to his desk and totals your sheet."
    pause 0.8
    narrator "He looks up."
    pause 0.4
    show harker tired at harker_body
    h "[povname]."

    # Pass-only pause beat — let the mog land.
    if final_score >= 60:
        pause 0.7
        narrator "He pauses."
        pause 0.4
        narrator "Longer than he needs to."
        pause 0.6
        show harker glasses at harker_body
        h "Your score is {b}[final_score]{/b}."
        pause 1.4
        jump pass_class_scene
    else:
        show harker facepalm at harker_body
        h "Your score is {b}[final_score]{/b}."
        pause 1.2
        jump fail_class_scene


# ═════════════════════════════════════════════════════════════
# SCENE 3A — PASS (≥60)
# ═════════════════════════════════════════════════════════════

label pass_class_scene:
    # Silent scene (sfx only) — clear any inherited track so a jump/skip into
    # it doesn't bleed a previous scene's music. (No-op in normal play.)
    stop music fadeout 0.5
    scene bg classroom_silent with fade
    show harker glasses at harker_body
    narrator "Mr. Harker slowly removes his glasses."
    narrator "He looks at your sheet. Then at you."
    h "...Well. You finally passed."
    hide harker
    pause 0.6
    play sound "audio/bell_school.mp3" volume persistent.vol_sfx
    narrator "The bell rings."
    narrator "As you gather your books, every head in the room turns."
    narrator "{i}No one speaks.{/i}"
    narrator "Eyebrows raise."
    show brayden neutral at clav_body
    narrator "In the back row, Brayden stops chewing. He stares at your score on Mr. Harker's sheet. He doesn't say anything."
    narrator "{i}That's new.{/i}"
    hide brayden
    $ brayden_threatened = True
    pause 0.5
    p "(...did I just mog the class?)"
    pause 1.4

    # ── THE MOG MOMENT ──
    # Timed to mogging_sfx.mp3 — the hit lands at 5.75s into the file.
    # Note: each `with dissolve` adds ~0.5s of wait that pauses don't count,
    # so the YOU and JUST dissolves shave 1.0s of total time. Pauses are
    # tuned with that overhead in mind.
    scene bg black
    play sound "audio/mogging_sfx.mp3" volume persistent.vol_sfx
    pause 1.0
    show text "{size=110}{color=#88ff88}{b}YOU{/b}{/color}" at truecenter with dissolve
    pause 1.5
    hide text
    show text "{size=110}{color=#88ff88}{b}JUST{/b}{/color}" at truecenter with dissolve
    pause 2.25
    hide text
    show text "{size=130}{color=#88ff88}{b}BRAINMOGGED{/b}{/color}" at truecenter with vpunch
    pause 3.2
    hide text with dissolve
    pause 0.5

    # ── STAT REVEAL ── RPG-style level-up after the mog lands.
    show text "{size=44}{color=#88ff88}{b}INTELLIGENCE  ++{/b}{/color}" at Transform(xalign=0.5, ypos=0.38, yanchor=0.0) with dissolve
    pause 0.75
    show text "{size=44}{color=#88ff88}{b}INTELLIGENCE  ++\nCOMMUNICATION  ++{/b}{/color}" at Transform(xalign=0.5, ypos=0.38, yanchor=0.0) with dissolve
    pause 0.75
    show text "{size=44}{color=#88ff88}{b}INTELLIGENCE  ++\nCOMMUNICATION  ++\nCONFIDENCE  ++{/b}{/color}" at Transform(xalign=0.5, ypos=0.38, yanchor=0.0) with dissolve
    pause 2.2
    hide text with dissolve
    pause 0.6

    # Clav is waiting in the hallway. He doesn't say well done.
    scene bg hallway with fade
    show clav smirk at clav_body
    c "One quiz."
    show clav stern at clav_body
    c "Don't confuse a step for the summit."
    hide clav with dissolve
    pause 0.8

    scene bg black with fade
    show text "THE NEXT MORNING" at truecenter with dissolve
    # Start the mirror theme quietly here, under the title card — it swells to
    # full once the bedroom appears (in mirror_scene). <from 42> + noloop match
    # the scene's own playback so there's no restart on the handoff.
    play music "<from 42>audio/mirror_scene.mp3" noloop fadein 2.5 volume 0.2
    pause 2.0
    hide text with dissolve
    jump mirror_scene


# ═════════════════════════════════════════════════════════════
# SCENE 4 — MIRROR & CITY (RESOLUTION)
# ═════════════════════════════════════════════════════════════

# ─── Cinematic helpers for the mirror monologue ──────────────
# Slow "Ken Burns" drifts so every background is alive (never dead-static),
# plus a letterbox (top/bottom black bars) to flag the cutscene.
transform kb_zoom:
    subpixel True
    zoom 1.05
    linear 32.0 zoom 1.18

transform kb_pan_right:
    subpixel True
    zoom 1.14 xoffset -45
    linear 32.0 xoffset 45

transform kb_pan_left:
    subpixel True
    zoom 1.14 xoffset 45
    linear 32.0 xoffset -45

transform letterbar_top:
    yalign 0.0
    yoffset -90
    ease 0.7 yoffset 0

transform letterbar_bottom:
    yalign 1.0
    yoffset 90
    ease 0.7 yoffset 0

screen letterbox():
    zorder 80
    add Solid("#000000", xysize=(config.screen_width, 90)) at letterbar_top
    add Solid("#000000", xysize=(config.screen_width, 90)) at letterbar_bottom


label mirror_scene:
    # Cinematic: letterbox bars in + a slow Ken Burns drift on every background.
    # Text appears crisp (no fade); the images carry the motion.
    show screen letterbox
    show bg bedroom_dawn at kb_zoom with fade
    # The mirror theme is already playing quietly from the NEXT MORNING card;
    # swell it to full now that the bedroom is on screen. If the scene is
    # entered directly (e.g. a dev jump), start the track here instead so it
    # isn't silent. (All _wait_until_music_pos values are absolute seconds into
    # mirror_scene.mp3; <from 42> skipped the slow intro, drop @1:13, peak @~1:35.)
    if "mirror_scene.mp3" in (renpy.music.get_playing(channel="music") or ""):
        # Pre-rolled from the NEXT MORNING card — swell it to full.
        $ renpy.music.set_volume(persistent.vol_music, delay=2.0, channel="music")
    else:
        # Entered directly, or a stale track is still playing — replace it.
        play music "<from 42>audio/mirror_scene.mp3" noloop fadein 1.0 volume persistent.vol_music

    # One dim overlay over the whole sequence so captions read cleanly.
    show expression Solid("#000000aa") as dim_overlay

    # ══ SAD (~0:44–1:03) — the honest inventory. Full lines, no fade on text. ══
    $ _wait_until_music_pos(44.0)
    show expression Text("I'm nothing special.", size=46, color="#dcdcdc", italic=True, xmaximum=1150, text_align=0.5) as nartext at Transform(xalign=0.5, yalign=0.80)

    $ _wait_until_music_pos(48.0)
    show expression Text("Average face. Average build. Average everything.", size=42, color="#dcdcdc", italic=True, xmaximum=1150, text_align=0.5) as nartext at Transform(xalign=0.5, yalign=0.80)

    $ _wait_until_music_pos(52.0)
    show expression Text("As a kid, I was sure I'd grow into someone.", size=42, color="#dcdcdc", italic=True, xmaximum=1150, text_align=0.5) as nartext at Transform(xalign=0.5, yalign=0.80)

    $ _wait_until_music_pos(56.0)
    show expression Text("Middle school. Freshman year. Still sure.", size=42, color="#dcdcdc", italic=True, xmaximum=1150, text_align=0.5) as nartext at Transform(xalign=0.5, yalign=0.80)

    $ _wait_until_music_pos(60.0)
    show expression Text("...Some nights, I'm still sure.", size=42, color="#dcdcdc", italic=True, xmaximum=1150, text_align=0.5) as nartext at Transform(xalign=0.5, yalign=0.80)

    $ _wait_until_music_pos(63.0)
    show expression Text("And there's no room I walk into where I'm the best at anything.", size=40, color="#dcdcdc", italic=True, xmaximum=1150, text_align=0.5) as nartext at Transform(xalign=0.5, yalign=0.80)

    # ══ Flashbacks (~1:07–1:12) — the images speak; just the quotes. ══
    $ _wait_until_music_pos(66.0)
    hide nartext
    show bg bully1 at kb_pan_left with Dissolve(0.3)
    show expression Text("\"Move, NPC.\"\n{size=26}— eighth grade{/size}", size=46, color="#e8e8e8", text_align=0.5, xmaximum=1150) as fbtext at Transform(xalign=0.5, yalign=0.82)

    $ _wait_until_music_pos(68.0)
    show bg bully2 at kb_pan_right with Dissolve(0.3)
    show expression Text("\"Look at this LTN.\"\n{size=26}— ninth grade{/size}", size=44, color="#e8e8e8", text_align=0.5, xmaximum=1150) as fbtext at Transform(xalign=0.5, yalign=0.82)

    $ _wait_until_music_pos(70.0)
    show bg bully3 at kb_zoom with Dissolve(0.3)
    show expression Text("\"Chopped.\"\n{size=26}— tenth grade{/size}", size=52, color="#ffffff", text_align=0.5, xmaximum=1150) as fbtext at Transform(xalign=0.5, yalign=0.82)

    # ══ DROP @1:13 — the verdict shatters (hard cut, on the beat). ══
    $ _wait_until_music_pos(73.0)
    hide fbtext
    show bg shattered_mirror at kb_zoom
    $ _wait_until_music_pos(73.6)
    show expression Text("So. Average me.", size=48, color="#ffffff", italic=True, xmaximum=1150, text_align=0.5) as nartext at Transform(xalign=0.5, yalign=0.80)

    $ _wait_until_music_pos(77.0)
    show expression Text("You got time to be looking down?", size=46, color="#ffffff", italic=True, xmaximum=1150, text_align=0.5) as nartext at Transform(xalign=0.5, yalign=0.80)

    # ══ The lift — turn to hope (1:13–1:35) ══
    $ _wait_until_music_pos(81.0)
    hide nartext
    show bg hope at kb_pan_right with Dissolve(0.6)
    show expression Text("I can change.", size=56, color="#ffffff", bold=True, xmaximum=1150, text_align=0.5) as chadcard at Transform(xalign=0.5, yalign=0.80)

    $ _wait_until_music_pos(85.0)
    show expression Text("I'm done being someone the room forgets.", size=52, color="#ffffff", bold=True, xmaximum=1150, text_align=0.5) as chadcard at Transform(xalign=0.5, yalign=0.80)

    $ _wait_until_music_pos(89.0)
    show expression Text("I'll do it until I can.", size=56, color="#ffffff", bold=True, xmaximum=1150, text_align=0.5) as chadcard at Transform(xalign=0.5, yalign=0.80)

    $ _wait_until_music_pos(92.0)
    show expression Text("No more looking down.", size=56, color="#ffffff", bold=True, xmaximum=1150, text_align=0.5) as chadcard at Transform(xalign=0.5, yalign=0.80)

    # ══ PEAK — heaven shows and the line fades out, a beat of heaven-only, then
    # the real drop @~1:35. ("I will mog the world" fires +1.7s to hit the beat;
    # a blank, text-free moment in between is intentional.) ══
    $ _wait_until_music_pos(95.0)
    show bg god_rays at kb_zoom with Dissolve(0.8)
    hide chadcard with dissolve

    $ _wait_until_music_pos(96.7)
    show expression Text("I will mog the world.", size=96, color="#88ff88", bold=True) as chadcard at truecenter with Dissolve(0.4)

    $ _wait_until_music_pos(101.0)
    hide chadcard
    hide dim_overlay
    hide screen letterbox

    scene bg black with fade
    pause 0.6

    # Stacked end card — small caps "END OF CHAPTER 2" above, big green
    # "BRAINMAXXED" below. Same family as the BRAINMOGGED reveal card.
    show expression Text("END OF CHAPTER 2", size=42, color="#aaaaaa", bold=True) as endline_top at Transform(xalign=0.5, yalign=0.38) with dissolve
    pause 0.5
    show expression Text("BRAINMAXXED", size=130, color="#88ff88", bold=True) as endline_bot at Transform(xalign=0.5, yalign=0.52) with dissolve
    pause 3.0
    hide endline_top with dissolve
    hide endline_bot with dissolve
    pause 0.4

    $ persistent.chapter2_complete = True

    # ══ Credits roll over the song's "tears" tail (1:35–end). roll_credits is
    # callable and returns here; the song keeps playing under it. After the
    # player dismisses the credits, offer a save point, then into Chapter 3
    # (whose own `stop music` clears the track on entry). ══
    $ credits_from_chapter = 2
    call roll_credits

    call chapter_break("Chapter 2 complete")
    jump chapter3_start


# ═════════════════════════════════════════════════════════════
# SCENE 3B — FAIL (<60)
# ═════════════════════════════════════════════════════════════

label fail_class_scene:
    stop music fadeout 0.5  # silent scene — clear inherited music (audio-hardening)
    scene bg classroom with fade
    show harker tired at harker_body
    narrator "Mr. Harker doesn't snap at you."
    narrator "He just looks at the paper."
    narrator "He sighs through his nose."
    show harker glasses at harker_body
    narrator "Takes off his glasses."
    narrator "Pinches the bridge of his nose."
    narrator "He says nothing."
    narrator "Somehow that's worse than yelling."
    hide harker
    pause 1.0
    show brayden smirk at clav_body
    b "Bro. You really thought \"skibidi\" was a definition? That's negative aura, dawg."
    hide brayden
    narrator "The class loses it. Phones come out. Someone is filming."
    pause 0.8
    narrator "Nobody around you laughs either. They just look away."
    narrator "{i}Pity is louder than mockery.{/i}"
    pause 1.0
    scene bg hallway with fade
    narrator "You gather your books. The hallway feels longer than usual."
    p "(Invisible.)"
    p "(Still invisible.)"
    p "(Worse than invisible — now they know I tried.)"
    pause 1.0

    python:
        clav_texts = [
            "sighhh you are such a normie....",
            "yawn. booth. don't be late.",
            "i thought you were different. clearly not. library.",
            "mid effort. mid result. we go again.",
            "embarrassing. for me. booth in ten.",
            "this is the part where you cope. i'll wait.",
            "truly the most normie thing i've ever seen. library. now.",
        ]
        clav_msg = clav_texts[(chapter2_attempt - 1) % len(clav_texts)]

    narrator "Your phone buzzes."
    show clav facepalm at clav_body
    narrator "{color=#9aa8ff}CLAV 🥶{/color}"
    narrator "{i}\"[clav_msg]\"{/i}"
    hide clav
    pause 1.5

    # Fail screen — player chooses to restart or quit to main menu
    call screen fail_screen
    $ fail_choice = _return

    if fail_choice == "restart":
        $ chapter2_attempt += 1
        scene bg black with fade
        pause 0.4
        jump chapter2_start
    else:
        return
