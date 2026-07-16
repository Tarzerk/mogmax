# MOGMAX — Chapter 3: The Mogbender
# Characters (c, b, p, eu, sol, cap, stranger, narrator), the placeholder
# helpers (sprite_or_placeholder, bg_or_placeholder, play_sfx,
# play_music_safe) and the brayden/gigachad/eugene image defs all live in
# script.rpy.
#
# NOTE: Mewing Geometry is playable. The other training stations are still
# represented by a short montage placeholder until their mechanics are built.

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
    show expression Text("CHAPTER 3 — THE MOGBENDER", style="story_card_text", size=46) as text at truecenter with dissolve
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
    narrator "At first there are streetlights. Then fewer streetlights. Then the road becomes one long dark line under the headlights."
    show clav stern at clav_body

    menu:
        "Clav drives like this is normal."
        "Ask where you're going.":
            p "Where are we going?"
            c "West."
            p "That is not an answer."
            c "It's a direction."
        "Ask if this is legal.":
            p "Is this legal?"
            c "Most important things aren't."
            p "That made me feel worse."
            c "Good. You're listening."
        "Sit in silence like a man.":
            narrator "You sit in silence like a man."
            pause 0.4
            p "...Are we there yet?"
            c "No."

    hide clav
    narrator "Ten minutes becomes forty. Houses turn into gas stations. Gas stations turn into nothing."
    show clav stern at clav_body
    p "Clav, I literally have school tomorrow."
    c "You had school yesterday. Look what it did for you."
    p "Honestly... valid."
    hide clav
    pause 0.5
    call screen ch3_travel_bar

    # ── SCENE 3 — THE SIGN ──
    scene bg ch3_sign with fade
    play music "audio/base_ambient.mp3" fadeout 1.5 fadein 1.5 volume persistent.vol_bed
    narrator "The car stops. The camera pans to a sign staked in the dirt."
    narrator "{b}⚠ RESTRICTED AREA — USE OF DEADLY FORCE AUTHORIZED ⚠{/b}"
    p "I think we should not be going here."
    narrator "Clav smirks. Says nothing."
    scene bg ch3_gate with fade
    narrator "The car rolls up to the gate. A chain-link fence. A STOP sign. Two soldiers."
    show soldier at soldier_left with dissolve
    sol "Turn around. Now."
    p "Clav. We CANNOT be here."
    narrator "A shadow falls over the soldiers. A Captain steps forward."
    show captain at captain_enter
    cap "OPEN IT UP."
    sol "...Yes sir."
    hide captain with dissolve
    hide soldier with dissolve
    narrator "The gate grinds open."
    pause 0.5


# ── SCENE 4 — INSIDE THE BASE ──
label ch3_base:
    scene bg ch3_corridor with fade
    # Base bed starts at the restricted sign so the mood turns before entry.
    # If a dev jump lands here directly, start it as a fallback.
    if "base_ambient.mp3" not in (renpy.music.get_playing(channel="music") or ""):
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
    narrator "A whole wall of personnel files. Every face blacked out. Clearances you'll never have."
    show gigachad wall at clav_body with dissolve
    narrator "Except one. No redaction. A silhouette so clean it stops reading like a person and starts reading like a decision the universe made on a good day."
    narrator "{b}⬛ LEVEL: GIGACHAD — CLEARANCE BEYOND THIS FACILITY{/b}"
    p "...okay. Who is that?"
    hide gigachad with dissolve
    show clav stern at clav_body
    c "Wrong question. That's not a who. That's the ceiling."
    c "Top of the scale. The number they don't let people be."
    p "Has anyone ever actually—"
    c "No."
    pause 0.3
    c "A handful get close. Ever. In the whole history of the program."
    narrator "For half a second something moves behind his face. Not pride. Closer to a bruise."
    c "...I got close."
    hide clav
    narrator "He says it flat, like a weather report, and walks off before you can pull the thread."
    narrator "You look back at the silhouette. And somewhere deep in your skull — a desk. A window full of city. A file set down on a stack of files exactly like it."
    narrator "You have no idea why it feels like you've already met him."
    pause 0.8

    # ── SCENE 6.5 — THE NATURAL MOGGERS ──
    scene bg ch3_corridor with fade
    narrator "The next corridor is darker. Warmer. Glass displays line both walls, each one lit from below in gold."
    narrator "No names. No plaques. Just silhouettes."
    narrator "All of them at once: a small figure in a soccer kit, frozen mid-cut; a skater hanging calm in the air; a giant rising above a rim; a marble-built man under a cape-shaped shadow."
    narrator "Different bodies. Different worlds. Same impossible feeling — like gravity has quietly agreed to help them."
    p "Are these... famous people?"
    show clav thinking at clav_body
    c "No names in the facility."
    p "Why?"
    c "Names make people think this is celebrity."
    c "It isn't."
    show clav stern at clav_body
    c "It's gravity."
    narrator "You look again. Not posters. Specimens."
    c "Some people mog without trying. Without knowing. Without caring."
    c "They walk into the world already carrying something everyone else has to build."
    p "So what, they're the goal?"
    c "No."
    c "They're proof."
    c "Brain gets you through a test. Controlled conditions. Paper. Definitions."
    c "But Brayden isn't a worksheet."
    c "He doesn't beat people by being smarter. He beats them by making the room agree with him before anyone speaks."
    c "That's Frame. That's Aura."
    p "And Gigachad?"
    pause 0.4
    c "Those people mog in one direction. Movement. Body. Presence. Myth."
    c "Gigachad is what happens when nothing is missing."
    pause 0.4
    c "You won't reach that."
    p "...Oh."
    c "Neither did I."
    narrator "He says it too fast. Like the sentence bit him on the way out."
    show clav smirk at clav_body
    c "But you don't need the ceiling."
    c "You need one step."
    c "One step is the difference between a room forgetting you and a room checking where you're standing."
    c "So."
    c "Training wing."
    hide clav
    pause 0.6


# ── SCENE 7 — THE TRAINING WING (battle tutorial + montage + spar) ──
label ch3_training:
    scene bg ch3_gym with fade
    show gigachad wall at clav_body
    play music "audio/training_montage.mp3" fadeout 1.5 fadein 1.0 volume persistent.vol_music
    narrator "The training wing. Different people run each station. Nobody introduces themselves. Nobody has to."
    narrator "In the back, half in shadow — that same massive figure, leaning on the wall. Not training. Just existing, like the room belongs to him."
    pause 0.5
    show clav thinking at clav_body
    c "Everything so far was observation. Brain. Frame. Aura. The scan at the door."
    c "This is where it turns into something you can point at people."
    hide clav

    # ── HOW A MOG BATTLE WORKS ──
    narrator "Across the gym, two trainees square off. No fists. No words. One of them just... sets his jaw and stands a half-inch taller."
    narrator "The other one's shoulders fold. He looks at the floor. And somehow the whole room knows exactly who won."
    show clav stern at clav_body
    c "That's a Mog Battle. You're going to fight a lot of them."
    c "Every rep you've banked is a move — vocab, posture, aura. Read your opponent, spend the right one, and he breaks. Spend the wrong one and it's your shoulders that fold."
    c "Watch one. Then you're in."
    hide clav

    # ═══════════════════════════════════════════════════════════
    # [ POKÉMON-STYLE BATTLE TUTORIAL GOES HERE ]
    #   Teaches the core loop: pick a move (Brain / Frame / Aura) →
    #   resolve vs the opponent → effectiveness → win/lose.
    #   Tutorial outcome is a scripted win.
    # ═══════════════════════════════════════════════════════════
    show text "{size=48}{color=#88ff88}MOG BATTLE TUTORIAL - IN DEVELOPMENT{/color}" at truecenter with dissolve
    pause 1.6
    hide text with dissolve
    narrator "Your first one is ugly. But the other guy looks away first — and that's the only stat that gets recorded."

    # ── THE MONTAGE (stations) ──
    narrator "Then they run you through all of it. Hours of it."

    narrator "The first station is a steel chair facing an anatomy terminal. Two skulls stare back at you. One weak. One classified."
    show clav smirk at clav_body
    c "Mewing Geometry. Four positions. Miss the window and the machine rejects your palate."
    p "The machine can reject my palate?"
    c "It can do worse."
    hide clav
    $ reset_mewing_minigame()
    $ mewing_score = renpy.call_screen("mewing_minigame")

    if mewing_score == 100:
        narrator "The terminal flashes green on the first sequence. Somewhere behind the glass, a technician slowly removes his sunglasses."
        show clav thinking at clav_body
        c "Beginner's luck. Extremely classified beginner's luck."
        hide clav
    elif mewing_score >= 80:
        narrator "The terminal makes you reset, then accepts the lock with a deep mechanical thunk."
        show clav smirk at clav_body
        c "Messy. But your palate has clearance."
        hide clav
    else:
        narrator "By the time the terminal finally turns green, your tongue feels like it has completed basic training."
        show clav stern at clav_body
        c "Nobody saw the first attempts. The cameras are classified."
        hide clav

    narrator "A curtain jerks open at the next station. Behind it sits an arcade cabinet bolted to the floor, connected to a giant mechanical jaw on a rail."
    show clav smirk at clav_body
    c "Aura Harvester 6000."
    p "Why does it have teeth?"
    c "Improves retention."
    c "Green outline adds aura. Red outline drains whatever you've built. Catch enough to reach one hundred."
    p "So I can't run out of lives?"
    c "No. You can only watch the number go back down."
    p "That feels worse."
    c "Correct."
    hide clav

    $ reset_aura_harvester()
    $ aura_result = renpy.call_screen("aura_harvester")
    $ aura_training_score = aura_score

    narrator "The jaw slams shut hard enough to shake the cabinet. Green lights race across the machine: {color=#69ff9a}AURA STABILIZED.{/color}"
    show clav thinking at clav_body
    c "One hundred. The federal minimum for entering a room like you belong there."
    p "That cannot be a real measurement."
    c "It has a number. Of course it's real."
    hide clav

    # ═══════════════════════════════════════════════════════════
    # [ REMAINING TRAINING MONTAGE MINIGAMES GO HERE ]
    #   Station stubs: PUSHUP PROTOCOL · HEEL INSERTION ·
    #   SIGMA VOCAB DRILL
    # ═══════════════════════════════════════════════════════════
    show text "{size=48}{color=#88ff88}REMAINING TRAINING STATIONS - IN DEVELOPMENT{/color}" at truecenter with dissolve
    pause 1.6
    hide text with dissolve
    narrator "Your jaw aches in a muscle you didn't know existed. The sensor band on your wrist keeps flashing the same read no matter what they make you do: {color=#88ff88}AURA: RISING.{/color}"

    # ── THE GRADUATION SPAR ──
    show clav smirk at clav_body
    c "One more thing. You don't walk out of here until you can prove it in a real one."
    c "Spar. Now. Everything you've got."
    hide clav
    # ═══════════════════════════════════════════════════════════
    # [ GRADUATION SPAR BATTLE GOES HERE ]
    #   A full Mog Battle vs a trainer (or Clav). Scripted win —
    #   this is the "you graduated" gate into the party chapter.
    # ═══════════════════════════════════════════════════════════
    show text "{size=48}{color=#88ff88}GRADUATION SPAR - IN DEVELOPMENT{/color}" at truecenter with dissolve
    pause 1.6
    hide text with dissolve
    narrator "It's close. It is not clean. But when it's over, you're the one still standing up straight."
    pause 0.4
    show clav smirk at clav_body
    c "Adequate."
    hide clav
    # The figure on the wall shifts once — then he's gone.
    show gigachad wall at clav_body with hpunch
    pause 0.6
    hide gigachad with dissolve
    narrator "By the side door, the wall is bare. The figure is gone. He was never introduced. He will not be explained."
    stop music fadeout 1.5
    pause 0.6


# ── SCENE 8 — EUGENE (THE FIRST CHOICE THAT LOGS) ──
label ch3_eugene:
    stop music fadeout 0.5  # silent scene — clear inherited music (audio-hardening)
    scene bg ch3_janitor with fade
    narrator "On the way out, a mop squeaks in a side corridor. You almost keep walking. You don't."
    show eugene neutral at clav_body
    narrator "Folded-in shoulders. Eyes down. A lanyard that just says INTERN. You know that exact posture — you wore it for years."
    p "...Eugene?"
    eu "Oh. Hey."
    p "What are you doing here?"
    eu "Internship. Unpaid. But the wi-fi's honestly insane, so."
    narrator "He keeps mopping. He isn't waiting for you to stick around. Nobody ever does."
    pause 0.4
    show clav smirk at clav_body
    c "(quiet, right at your shoulder) Go on. You earned this one."
    c "First person you've ever met who's actually below you. Feels good, doesn't it. It's supposed to."
    hide clav
    narrator "And that's the ugly part — there's a pull in your chest that agrees with him. A little voice going {i}finally. someone under me.{/i}"
    menu:
        "Eugene mops, waiting for you to be like everyone else who's come through."
        "Mog him. Just once — see what it feels like from the top.":
            $ mogged_eugene = True
            $ helped_eugene = False
            narrator "You straighten. You let everything you built settle onto him, full weight — the way it used to settle onto you."
            narrator "Eugene's shoulders drop another inch. He nods. Small, unsurprised. Like he always figured you'd end up here too."
            eu "...yeah. 'Course."
            narrator "It feels incredible for about a second and a half. Then it just feels familiar. Then it feels like the cafeteria."
            show clav smirk at clav_body
            c "There he is."
            hide clav
        "Lift him. You know exactly what nobody ever said to you.":
            $ helped_eugene = True
            $ mogged_eugene = False
            narrator "You crouch down, so you're not looking at him from above."
            p "For what it's worth — the wi-fi bit was actually funny. And nobody who grinds this quiet stays invisible forever. I'd know."
            narrator "Eugene stops mopping. Looks at you properly — the first time anyone's really looked at him all day."
            eu "...huh. Most people who come through here don't even see me."
            narrator "He stands a little straighter. Something quiet passes between you. Behind you, for once, Clav says absolutely nothing."
    hide eugene with dissolve
    pause 0.6


# ── SCENE 9 — THE DRIVE BACK / THE INVITE ──
label ch3_return:
    # Reuse the daytime desert road, tinted dark-navy for night (same road =
    # continuity, and guaranteed people-free). The night_tint clears on the
    # scene change to black at the end.
    scene bg ch3_road with fade
    show expression Solid("#0a1430cc") as night_tint
    play music "audio/desert_ambient.mp3" fadein 1.0 volume persistent.vol_bed
    narrator "Night. The desert unspools backward outside the window. You've been quiet a long time."
    p "So what was that, actually. All of it."
    show clav stern at clav_body
    c "Proof. That the grind isn't a phone thing. It's old, it's real, and it works."
    c "You walked in an LTN. You're walking out a problem."
    hide clav
    narrator "You catch your reflection in the side mirror and sit up without deciding to. Even the glass has an opinion about you now."
    pause 0.5
    play sound "audio/text_buzz.mp3" volume persistent.vol_sfx
    narrator "Your phone lights up. The class group chat — the one you've been muted in since freshman year."
    narrator "{i}FRIDAY. Brayden's place. Open invite. Whole school's going.{/i}"
    pause 0.4
    narrator "Open invite. Which has always, always meant {i}everyone except you.{/i} You read it three times."
    show clav smirk at clav_body
    c "Don't sit there wondering if you should go."
    c "You're going to walk in like your name's on the lease."
    hide clav
    pause 0.6
    play sound "audio/text_buzz.mp3" volume persistent.vol_sfx
    narrator "{color=#7ab8ff}BRAYDEN{/color}"
    narrator "{i}\"yo heard you're coming friday\"{/i}"
    pause 0.4
    narrator "{i}\"just don't make it weird\"{/i}"
    pause 0.6
    narrator "You stare at the second message longer than the first."
    narrator "For once, Brayden texted first."
    narrator "Not to invite you. To make sure he still owned the frame before you walked in."
    pause 1.0

    stop music fadeout 2.0
    scene bg black with fade
    pause 0.4

    # Stacked end card — same family as the merged Ch1 BRAINMAXXED card.
    show expression Text("END OF CHAPTER 3", style="story_card_text", size=42, color="#aeb8b2") as endline_top at Transform(xalign=0.5, yalign=0.38) with dissolve
    pause 0.5
    show expression Text("THE MOGBENDER", style="story_card_text", size=120, color="#79c98b") as endline_bot at Transform(xalign=0.5, yalign=0.52) with dissolve
    pause 2.8
    hide endline_top with dissolve
    hide endline_bot with dissolve
    pause 0.4

    # TODO (Phase 3): swap `jump roll_credits` for `jump chapter4_start` (the
    # party / Auramaxxing) once that chapter exists. For now the Mogbender
    # still ends into the credits.
    $ persistent.chapter3_complete = True
    $ credits_from_chapter = 3
    jump roll_credits
