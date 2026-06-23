# MOGMAX — Chapter 3: The Mogbender
# Characters (c, b, p, eu, sol, cap, stranger, narrator), the placeholder
# helpers (sprite_or_placeholder, bg_or_placeholder, play_sfx,
# play_music_safe) and the brayden/gigachad/eugene image defs all live in
# script.rpy.
#
# NOTE: the five training-montage minigames are STUBS. Each is a title card
# + a narrator beat that auto-advances. Mechanics are TBD and specified
# separately — only the minigame interior is blank; the surrounding beats
# are final.

# ─── Chapter backgrounds (placeholder-guarded) ───────────────
image bg ch3_bedroom    = bg_or_placeholder("images/backgrounds/bg_ch3_bedroom.jpg", "bedroom (alarm)")
image bg ch3_road       = bg_or_placeholder("images/backgrounds/bg_ch3_road.jpg", "desert road")
image bg ch3_gate       = bg_or_placeholder("images/backgrounds/bg_ch3_gate.jpg", "restricted gate")
image bg ch3_sign       = bg_or_placeholder("images/backgrounds/bg_ch3_sign.jpg", "area 51 warning sign")
image bg ch3_corridor   = bg_or_placeholder("images/backgrounds/bg_ch3_corridor.jpg", "base corridor")
image bg ch3_vault      = bg_or_placeholder("images/backgrounds/bg_ch3_vault.jpg", "vault door")
image bg ch3_lab        = bg_or_placeholder("images/backgrounds/bg_ch3_lab.jpg", "research lab")
image bg ch3_whiteboard = bg_or_placeholder("images/backgrounds/bg_ch3_whiteboard.jpg", "whiteboards")
image bg ch3_filewall   = bg_or_placeholder("images/backgrounds/bg_ch3_filewall.jpg", "gigachad file wall")
image bg ch3_gym        = bg_or_placeholder("images/backgrounds/bg_ch3_gym.jpg", "training gym")
image bg ch3_janitor    = bg_or_placeholder("images/backgrounds/bg_ch3_janitor.jpg", "janitor closet")
image bg scan_granted   = "#0a2a0a"


# ═════════════════════════════════════════════════════════════
# CHAPTER 3 — THE MOGBENDER
# ═════════════════════════════════════════════════════════════

label chapter3_start:
    # Fade out whatever was carried in from Chapter 2 (the gigachad/mirror
    # theme). Ch3's own beds load via play_music_safe, so without this the
    # Ch2 theme would bleed straight through the opening.
    stop music fadeout 2.0
    scene bg black with fade
    pause 0.4
    show text "{size=54}Chapter 3 — The Mogbender{/size}" at truecenter with dissolve
    pause 2.0
    hide text with dissolve

    # ── SCENE 1 — THE PICKUP ──
    scene bg ch3_bedroom with fade
    # Bright stock bedroom -> tint dark for the pre-dawn feel (same trick as
    # the desert night return).
    show expression Solid("#0a1430cc") as night_tint
    narrator "Black. Dead asleep. The kind of sleep that doesn't ask questions."
    pause 0.4
    play sound "audio/honk.mp3" volume persistent.vol_sfx
    narrator "{b}HONK HONK.{/b}"
    narrator "A car horn blares outside your window. You jolt awake."
    show clav stern at clav_body
    c "Get up. We're leaving."
    p "...where exactly?"
    c "I said let's go."
    hide clav
    narrator "No further explanation. The car is already running."
    pause 0.6

    # ── SCENE 2 — THE ROAD ──
    scene bg ch3_road with fade
    play music "audio/desert_ambient.mp3" fadein 1.5 volume persistent.vol_bed
    narrator "Timelapse. Desert highway. Hours pass."
    call screen ch3_travel_bar
    p "Clav I literally have school tomorrow —"
    show clav stern at clav_body
    c "Shut it."
    p "Are we almost —"
    c "Shut it."
    hide clav
    narrator "More road. A tumbleweed. A gas station that sells only protein shakes."
    pause 0.5

    # ── SCENE 3 — THE SIGN ──
    scene bg ch3_sign with fade
    narrator "The car stops. The camera pans to a sign staked in the dirt."
    narrator "{b}⚠ RESTRICTED AREA — USE OF DEADLY FORCE AUTHORIZED ⚠{/b}"
    p "I think we should not be going here."
    narrator "Clav smirks. Says nothing."
    scene bg ch3_gate with fade
    narrator "The car rolls up to the gate. A chain-link fence. A STOP sign. Two soldiers."
    sol "Turn around. Now."
    p "Clav. We CANNOT be here."
    narrator "A shadow falls over the soldiers. A Captain steps forward."
    cap "OPEN IT UP."
    sol "...Yes sir."
    narrator "The gate grinds open."
    pause 0.5


# ── SCENE 4 — INSIDE THE BASE ──
label ch3_base:
    scene bg ch3_corridor with fade
    # Crossfade the desert ambient into the sci-fi base bed for the
    # infiltration + reveal (Scenes 4-6). Hot master, so ducked hard to bed
    # level; the montage track crossfades it back out in Scene 7.
    play music "audio/base_ambient.mp3" fadeout 2.0 fadein 2.0 volume persistent.vol_bed
    narrator "Layer after layer of security. Retinal scans. Badge checks. Armed guards."
    narrator "And yet — nobody stops you. Nobody even looks twice."
    narrator "It's like you were expected."
    p "I can't believe I'm actually here."
    p "...Are aliens real?"
    show clav smirk at clav_body
    c "You have a lot to learn, normie."
    hide clav
    scene bg ch3_vault with fade
    narrator "You reach a massive vault door. Clav steps forward. A scanner activates. Blue light sweeps slowly across his jaw."
    play sound "audio/scan.mp3" volume (persistent.vol_sfx * 0.85)
    pause 0.6
    scene bg scan_granted with dissolve
    show text "{size=44}{color=#88ff88}🔵 JAWLINE SCAN CONFIRMED{/color}" at truecenter with dissolve
    pause 1.4
    hide text
    show text "{size=70}{color=#88ff88}{b}ACCESS GRANTED{/b}{/color}" at truecenter with dissolve
    pause 1.4
    hide text
    show text "{size=46}{color=#88ff88}👁  WELCOME TO GIGAMAXING{/color}" at truecenter with dissolve
    pause 1.8
    hide text with dissolve

    # ── SCENE 5 — THE REVEAL ──
    scene bg ch3_lab with fade
    show clav thinking at clav_body
    c "Most people think Area 51 is about aliens. Advanced weapons. Classified tech."
    c "That's exactly what we want them to think."
    c "The real research has been going on for 60 years."
    p "...What research?"
    c "Frame. Brain. Aura. The US government cracked gigamaxxing before the internet even existed."
    hide clav
    scene bg ch3_whiteboard with fade
    narrator "The room opens up. Whiteboards covered in mewing diagrams. Posture charts. Vocabulary trees. A framed photo of a jaw — classified EYES ONLY."
    show clav stern at clav_body
    c "[povname]. With great power comes great responsibility."
    c "Trust the process."
    hide clav
    pause 0.6

    # ── SCENE 6 — THE GIGACHAD FILE ──
    scene bg ch3_filewall with fade
    narrator "On the wall: a long row of classified personnel files. Faces redacted."
    show gigachad wall at clav_body with dissolve
    narrator "One is different — no redaction. Just a silhouette so perfectly proportioned it hurts to look at."
    narrator "{b}⬛ LEVEL: GIGACHAD — CLEARANCE BEYOND THIS FACILITY{/b}"
    p "Who is that?"
    hide gigachad with dissolve
    show clav stern at clav_body
    c "Not a who. A limit."
    c "That's the ceiling. Top of the scale."
    c "Nobody reaches it. Some people get close."
    c "I got close."
    hide clav
    narrator "He doesn't elaborate. He walks away."
    narrator "You stare at the file a moment longer. Somewhere in the back of your head — a desk. A city window. A report being set down."
    narrator "You don't know why the silhouette feels familiar."
    pause 0.8


# ── SCENE 7 — THE TRAINING MONTAGE (5 minigame STUBS) ──
label ch3_training:
    scene bg ch3_gym with fade
    show gigachad wall at clav_body
    play music "audio/training_montage.mp3" fadeout 1.5 fadein 1.0 volume persistent.vol_music
    narrator "Clav leads you into the training wing. Different people run each station. None of them introduce themselves. They don't need to."
    narrator "In the back, barely visible — a massive figure leaning against the wall. Just existing."
    pause 0.5

    # MINIGAME STUB 1 — PUSHUP PROTOCOL  (TODO: implement minigame screen)
    show text "{size=54}PUSHUP PROTOCOL{/size}" at truecenter with dissolve
    pause 1.6
    hide text with dissolve
    narrator "Spam to the burn. A posture alarm fires mid-rep. The guy with the clipboard writes something down. Stone-faced."

    # MINIGAME STUB 2 — HEEL INSERTION  (TODO: implement minigame screen)
    show text "{size=54}HEEL INSERTION{/size}" at truecenter with dissolve
    pause 1.6
    hide text with dissolve
    narrator "One clean press. No crease. Two inches taller, and the world looks slightly more winnable."

    # MINIGAME STUB 3 — MEWING GEOMETRY  (TODO: implement minigame screen)
    show text "{size=54}MEWING GEOMETRY{/size}" at truecenter with dissolve
    pause 1.6
    hide text with dissolve
    narrator "Tongue to the correct palate position. Eight seconds. No second chances."

    # MINIGAME STUB 4 — SIGMA VOCAB DRILL  (TODO: implement minigame screen)
    show text "{size=54}SIGMA VOCAB DRILL{/size}" at truecenter with dissolve
    pause 1.6
    hide text with dissolve
    narrator "Rapid-fire definitions. It gets faster every round. Pulchritudinous. Again."

    # MINIGAME STUB 5 — CASIO CALIBRATION  (TODO: implement minigame screen)
    show text "{size=54}CASIO CALIBRATION{/size}" at truecenter with dissolve
    pause 1.6
    hide text with dissolve
    narrator "Type any equation on the tiny rubber buttons. The watch only ever returns one result: {color=#88ff88}AURA: RISING.{/color}"

    pause 0.4
    show clav smirk at clav_body
    c "Adequate."
    hide clav
    # The figure that was leaning on the wall shifts once, then leaves.
    show gigachad wall at clav_body with hpunch
    pause 0.6
    hide gigachad with dissolve
    narrator "By the side door, the figure that was leaning on the wall is gone. He was never introduced. He will not be explained."
    stop music fadeout 1.5
    pause 0.6


# ── SCENE 8 — EUGENE (MEANINGFUL CHOICE) ──
label ch3_eugene:
    stop music fadeout 0.5  # silent scene — clear inherited music (audio-hardening)
    scene bg ch3_janitor with fade
    narrator "A mop squeaks across the floor in the corner. You turn."
    show eugene neutral at clav_body
    p "...Eugene?"
    eu "Oh. Hey."
    p "What are you doing here?"
    eu "Internship. They said it was unpaid but the wi-fi is really fast."
    narrator "He keeps mopping. Like this is completely normal."
    menu:
        "Eugene mops, completely unbothered."
        "That's actually kind of based.":
            $ helped_eugene = True
            narrator "Eugene stops mopping. Looks at you properly for the first time."
            eu "...Thanks. Most of the ones who come through here don't even see me."
            narrator "He gives a small nod. Something shifts between you."
        "Walk past him without a word.":
            $ helped_eugene = False
            narrator "He goes back to mopping. The mop squeaks."
    hide eugene with dissolve
    pause 0.6


# ── SCENE 9 — THE RETURN ──
label ch3_return:
    # Reuse the daytime desert road, tinted dark-navy for night (same road =
    # continuity, and guaranteed people-free). The night_tint clears on the
    # scene change to black at the end.
    scene bg ch3_road with fade
    show expression Solid("#0a1430cc") as night_tint
    play music "audio/desert_ambient.mp3" fadein 1.0 volume persistent.vol_bed
    narrator "Exterior. Night. Back in the car. Desert highway reversed."
    p "So what was the point of all that?"
    show clav stern at clav_body
    c "You needed to see that this is real."
    c "The grind isn't some internet thing. It's classified. It's ancient. It matters."
    p "...We're gonna be in so much trouble for missing school."
    c "You're different now. Act like it."
    hide clav
    narrator "Silence. Desert. Stars."
    pause 0.6
    play sound "audio/text_buzz.mp3" volume persistent.vol_sfx
    narrator "Your phone buzzes."
    narrator "{color=#7ab8ff}BRAYDEN{/color}"
    narrator "{i}\"yo heard you been acting different lately\"{/i}"
    pause 0.5
    narrator "{i}\"don't get any ideas lol\"{/i}"
    pause 0.6
    narrator "{i}He can sense it. The hierarchy is shifting.{/i}"
    pause 1.0

    stop music fadeout 2.0
    scene bg black with fade
    pause 0.4

    # Stacked end card — same family as the Chapter 2 BRAINMAXXED card.
    show expression Text("END OF CHAPTER 3", size=42, color="#aaaaaa", bold=True) as endline_top at Transform(xalign=0.5, yalign=0.38) with dissolve
    pause 0.5
    show expression Text("THE MOGBENDER", size=120, color="#88ff88", bold=True) as endline_bot at Transform(xalign=0.5, yalign=0.52) with dissolve
    pause 2.8
    hide endline_top with dissolve
    hide endline_bot with dissolve
    pause 0.4

    $ persistent.chapter3_complete = True
    $ credits_from_chapter = 3
    jump roll_credits
