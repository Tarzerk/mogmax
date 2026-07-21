# MOGMAX — Chapter 2: The Mogbender
# Characters (c, b, p, eu, sol, cap, stranger, narrator) and the shared
# brayden/gigachad/eugene image definitions live in script.rpy.

# ─── Chapter backgrounds ─────────────────────────────────────
image bg ch2_bedroom    = bg_image("images/backgrounds/bg_ch2_bedroom.jpg")
image bg ch2_road       = bg_image("images/backgrounds/bg_ch2_road.jpg")
image bg ch2_gate       = bg_image("images/backgrounds/bg_ch2_gate.jpg")
image bg ch2_sign       = bg_image("images/backgrounds/bg_ch2_sign.jpg")
image bg ch2_corridor   = bg_image("images/backgrounds/bg_ch2_corridor.jpg")
image bg ch2_vault      = bg_image("images/backgrounds/bg_ch2_vault.jpg")
image bg ch2_lab        = bg_image("images/backgrounds/bg_ch2_lab.jpg")
image bg ch2_whiteboard = bg_image("images/backgrounds/bg_ch2_whiteboard.jpg")
image bg ch2_filewall   = bg_image("images/backgrounds/bg_ch2_filewall.jpg")
image bg ch2_gym        = bg_image("images/backgrounds/bg_ch2_gym.jpg")
image bg ch2_janitor    = bg_image("images/backgrounds/bg_ch2_janitor.jpg")
image bg scan_granted   = "#0a2a0a"


# ═════════════════════════════════════════════════════════════
# CHAPTER 2 — THE MOGBENDER
# ═════════════════════════════════════════════════════════════

label chapter2_start:
    # Fade out the mirror theme carried in from Chapter 1 so the new chapter's
    # ambient bed can take over cleanly.
    stop music fadeout 2.0
    scene bg black with fade
    pause 0.4
    show expression Text("CHAPTER 2 — THE MOGBENDER", style="story_card_text", size=46) as text at truecenter with dissolve
    pause 2.0
    hide text with dissolve

    # ── SCENE 1 — THE PICKUP ──
    scene bg ch2_bedroom with fade
    # Bright stock bedroom -> tint dark for the pre-dawn feel (same trick as
    # the desert night return).
    show expression Solid("#0a1430cc") as night_tint
    narrator "Black. Dead asleep. The kind of sleep that doesn't ask questions."
    pause 0.4
    play sound "audio/honk.mp3" volume persistent.vol_sfx
    narrator "{b}HONK HONK.{/b}"
    narrator "A car horn blares outside your window. You jolt awake."
    c "Get up. We're leaving."
    p "...where exactly?"
    c "I said let's go."
    narrator "No further explanation. The car is already running."
    pause 0.6

    # ── SCENE 2 — THE ROAD ──
    scene bg ch2_road with fade
    play music "audio/desert_ambient.mp3" fadein 1.5 volume persistent.vol_bed
    narrator "At first there are streetlights. Then fewer streetlights. Then the road becomes one long dark line under the headlights."

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

    narrator "Ten minutes becomes forty. Houses turn into gas stations. Gas stations turn into nothing."
    p "Clav, I literally have school tomorrow."
    c "You had school yesterday. Look what it did for you."
    p "Honestly... valid."
    pause 0.5
    call screen ch2_travel_bar

    # ── SCENE 3 — THE SIGN ──
    scene bg ch2_sign with fade
    play music "audio/base_ambient.mp3" fadeout 1.5 fadein 1.5 volume persistent.vol_bed
    narrator "The car stops. The camera pans to a sign staked in the dirt."
    narrator "{b}⚠ RESTRICTED AREA — USE OF DEADLY FORCE AUTHORIZED ⚠{/b}"
    p "I think we should not be going here."
    narrator "Clav smirks. Says nothing."
    scene bg ch2_gate with fade
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
label chapter2_base:
    scene bg ch2_corridor with fade
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
    scene bg ch2_vault with fade
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
    show text "{size=46}{color=#88ff88}👁  WELCOME TO GIGAMAXXING{/color}" at truecenter with dissolve
    pause 1.8
    hide text with dissolve

    # ── SCENE 5 — THE REVEAL ──
    scene bg ch2_lab with fade
    show clav thinking at clav_body
    c "Most people think Area 51 is about aliens. Advanced weapons. Classified tech."
    c "That's exactly what we want them to think."
    c "The real research has been going on for 60 years."
    p "...What research?"
    c "Frame. Brain. Aura. The US government cracked gigamaxxing before the internet even existed."
    hide clav
    scene bg ch2_whiteboard with fade
    narrator "The room opens up. Whiteboards covered in mewing diagrams. Posture charts. Vocabulary trees. A framed photo of a jaw — classified EYES ONLY."
    show clav stern at clav_body
    c "[povname]. With great power comes great responsibility."
    c "Trust the process."
    hide clav
    pause 0.6

    # ── SCENE 6 — THE GIGACHAD FILE ──
    scene bg ch2_filewall with fade
    narrator "A whole wall of personnel files. Every face blacked out. Clearances you'll never have."
    show gigachad wall at gigachad_file with dissolve
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
    scene bg ch2_corridor with fade
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
label chapter2_training:
    scene bg ch2_gym with fade
    play music "audio/training_montage.mp3" fadeout 1.5 fadein 1.0 volume persistent.vol_music
    narrator "The training wing. Different people run each station. Nobody introduces themselves. Nobody has to."
    # Keep the gym stage clear for Clav and future station-specific trainers.
    show clav thinking at clav_body
    c "Everything so far was observation. Brain. Frame. Aura. The scan at the door."
    c "First you build the pieces. Then you learn what they do to someone."
    hide clav

    # ── THE MONTAGE (stations) ──
    narrator "They run you through all of it. Hours of it."

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

    $ reset_aura_harvester("normal")
    $ aura_result = renpy.call_screen("aura_harvester")
    $ aura_training_score = aura_score

    narrator "The jaw slams shut hard enough to shake the cabinet. Green lights race across the machine: {color=#69ff9a}AURA STABILIZED.{/color}"
    show clav thinking at clav_body
    c "One hundred. The federal minimum for entering a room like you belong there."
    p "That cannot be a real measurement."
    c "It has a number. Of course it's real."
    hide clav

    narrator "At the next station, a scanner lowers over a blank anatomical face. It has no eyes. Somehow it still looks judgmental."
    show clav stern at clav_body
    c "Dermal Purge. Clear active inflammation. Leave permanent marks alone."
    p "And if I click a mole?"
    c "The machine documents your lack of restraint."
    hide clav

    $ reset_acne_minigame("normal")
    $ acne_training_score = renpy.call_screen("acne_pop_minigame")
    $ aura += 100

    narrator "The scan turns green: {color=#69e4ad}CLEAR SKIN. +100 AURA.{/color}"
    if acne_mistakes == 0:
        show clav thinking at clav_body
        c "No collateral damage. Unexpectedly civilized."
        hide clav
    else:
        show clav smirk at clav_body
        c "You attacked [acne_mistakes] permanent features. We'll call that enthusiasm."
        hide clav

    # Additional playable stations can slot into this montage without changing
    # the handoff into the battle tutorial.
    narrator "After that, the stations stop feeling separate. The next hour comes back in flashes."
    narrator "A posture harness yanks your shoulders into alignment every time you slouch. By the sixth correction, you start catching yourself before the machine does."
    show clav stern at clav_body
    c "Frame begins before anyone sees your face. Again."
    hide clav
    narrator "A height rig calibrates your stance down to the millimeter. Chin level. Weight balanced. Heels planted like the floor owes you stability."
    narrator "Then a speech terminal throws insults at you through a blown speaker. Your job is not to answer. Your job is to make the silence feel like your decision."
    p "This place spent federal money teaching people how not to reply?"
    show clav smirk at clav_body
    c "Billions. Try to look grateful."
    hide clav
    narrator "By the time the last restraint unlocks, your jaw aches in a muscle you didn't know existed. The sensor on your wrist keeps returning the same verdict: {color=#88ff88}AURA: RISING.{/color}"

    # ── HOW A MOG BATTLE WORKS ──
    narrator "Across the gym, two trainees square off. No fists. No words. One of them sets his jaw and stands a half-inch taller."
    narrator "The other one's shoulders fold. He looks at the floor. The whole room knows exactly who won."
    show clav stern at clav_body
    c "That's a Mog Battle. Everything you built in here becomes a move."
    c "Aura Blast applies pressure. Hold Frame answers force. Cringe slips through a block. Mewing makes yap hit nothing."
    c "Read the tell. Give it the correct answer."
    hide clav

    narrator "A man in a black training shirt steps onto the mat. The name patch says COACH KAI. His posture says the patch was unnecessary."
    narrator "Three lights switch on above him: ATTACK. BLOCK. YAP."
    $ start_mog_battle("kai_tutorial")
    $ kai_tutorial_result = renpy.call_screen("mog_battle_screen")
    narrator "Kai taps RESTORE. Your Aura returns to {color=#69ff9a}100 / 100{/color}."

    # ── THE GRADUATION SPAR ──
    show clav smirk at clav_body
    c "That was instruction. This one is yours."
    c "No answer lights. No help."
    hide clav
    narrator "Coach Kai stays on the mat. Every hint switches off."
    $ start_mog_battle("kai_graduation")
    $ kai_graduation_result = renpy.call_screen("mog_battle_screen")
    narrator "It's close. It is not clean. But when it's over, you're the one still standing up straight with {color=#69ff9a}[kai_graduation_result['aura_kept']] AURA{/color}."
    pause 0.4
    show clav smirk at clav_body
    c "Adequate."
    hide clav
    stop music fadeout 1.5
    pause 0.6


# ── SCENE 8 — EUGENE (THE FIRST CHOICE THAT LOGS) ──
label chapter2_eugene:
    stop music fadeout 0.5  # silent scene — clear inherited music (audio-hardening)
    scene bg ch2_janitor with fade
    narrator "On the way out, a mop squeaks in a side corridor. You almost keep walking. You don't."
    show eugene neutral at eugene_left
    narrator "Folded-in shoulders. Eyes down. A lanyard that just says INTERN. You know that exact posture — you wore it for years."
    p "...Eugene?"
    eu "Oh. Hey."
    p "What are you doing here?"
    eu "Internship. Unpaid. But the wi-fi's honestly insane, so."
    narrator "He keeps mopping. He isn't waiting for you to stick around. Nobody ever does."
    pause 0.4
    narrator "Then you notice the angle: his eyes down, yours up. For once, the room has already decided which of you matters more."
    narrator "No voice tells you what to do. You can keep that advantage and make him feel it — or give it up before it turns you into someone familiar."

    window hide
    $ start_critical_choice()
    show layer master at critical_choice_world

    menu:
        "MOG EUGENE":
            $ stop_critical_choice()
            show layer master at critical_choice_release
            $ mogged_eugene = True
            $ helped_eugene = False
            pause 0.35
            play sound "audio/battle_super_effective.mp3" volume persistent.vol_sfx * 0.9
            show layer master at eugene_mog_impact
            show expression Solid("#fff4df35") as mog_impact_flash onlayer overlay
            pause 0.08
            hide mog_impact_flash onlayer overlay
            show eugene sad at eugene_left
            pause 0.42
            show layer master at critical_choice_release
            narrator "You don't insult him. You don't need to. You straighten, hold his eyes, and let the silence compare you."
            narrator "The hallway changes sides. Eugene's joke dies first. Then his shoulders fold, as if your new frame has actual weight."
            eu "...yeah. 'Course."
            narrator "It lands exactly the way you wanted. That's the worst part. No Clav in your ear. No audience to impress. This one was yours."
        "DON'T MOG EUGENE":
            $ stop_critical_choice()
            show layer master at critical_choice_release
            $ helped_eugene = True
            $ mogged_eugene = False
            narrator "You give up the angle. You crouch down, so you're not looking at him from above."
            p "For what it's worth — the wi-fi bit was actually funny. And nobody who grinds this quiet stays invisible forever. I'd know."
            show eugene happy at eugene_left with dissolve
            narrator "Eugene stops mopping. Looks at you properly — the first time anyone's really looked at him all day."
            eu "...huh. Most people who come through here don't even see me."
            narrator "He stands a little straighter. You did that without an audience. Somehow, that feels more real than anything you proved today."
    hide eugene with dissolve
    pause 0.6


# ── SCENE 9 — THE DRIVE BACK / THE INVITE ──
label chapter2_return:
    # Reuse the daytime desert road, tinted dark-navy for night (same road =
    # continuity, and guaranteed people-free). The night_tint clears on the
    # scene change to black at the end.
    scene bg ch2_road with fade
    show expression Solid("#0a1430cc") as night_tint
    play music "audio/desert_ambient.mp3" fadein 1.0 volume persistent.vol_bed
    narrator "Night. The desert unspools backward outside the window. You've been quiet a long time."
    p "So what was that, actually? All of it."
    show clav smirk at clav_body with dissolve
    c "Proof. None of this started on your phone."
    c "You walked in an LTN. You're walking out a problem."
    hide clav with dissolve
    narrator "You catch your reflection in the side mirror and sit up without deciding to."

    # Let the invitation breathe in silence before the song takes over. Once
    # Pound Cake starts, the credits still land on its first major beat at 0:11.
    stop music fadeout 0.4
    window hide
    $ set_cinematic_dialogue(True)

    pause 0.6
    play sound "audio/text_notification.mp3" volume persistent.vol_sfx
    pause 0.25
    show screen cinematic_caption("{i}FRIDAY @ MY PLACE - 9PM\nOPEN INVITE\nEVERYBODY PULL UP{/i}", "Class Group Chat")
    pause 3.4
    hide screen cinematic_caption
    pause 0.7

    play music "audio/pound_cake.mp3" noloop fadein 0.15 volume persistent.vol_music

    $ _wait_until_music_pos(1.20)
    play sound "audio/text_notification.mp3" volume persistent.vol_sfx
    $ _wait_until_music_pos(1.45)
    show screen cinematic_caption("{i}jus so we clear{/i}", "Brayden")

    $ _wait_until_music_pos(4.75)
    play sound "audio/text_notification.mp3" volume persistent.vol_sfx
    $ _wait_until_music_pos(5.0)
    show screen cinematic_caption("{i}u aint invited{/i}", "Brayden")

    $ _wait_until_music_pos(11.0)
    hide screen cinematic_caption
    $ set_cinematic_dialogue(False)
    scene bg black

    # This is the current playable ending; future chapters can replace the
    # credits jump without changing Chapter 2's closing beat.
    $ persistent.chapter2_complete = True
    $ credits_from_chapter = 2
    jump roll_credits
