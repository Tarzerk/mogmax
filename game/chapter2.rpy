# MOGMAX — Chapter 2: The Mogbender
# Characters (c, b, p, eu, sol, cap, stranger, narrator) and the shared
# brayden/gigachad/eugene image definitions live in script.rpy.

# ─── Chapter backgrounds ─────────────────────────────────────
image bg ch2_bedroom    = bg_image("images/backgrounds/bg_ch2_bedroom.jpg")
image bg ch2_road       = bg_image("images/backgrounds/bg_ch2_road.jpg")
image bg ch2_gate       = bg_image("images/backgrounds/bg_ch2_gate.jpg")
image bg ch2_sign       = bg_image("images/backgrounds/bg_ch2_sign.jpg")
image bg ch2_corridor   = bg_image("images/backgrounds/bg_ch2_corridor.jpg")
# Warm projection surface. The animated grain layer gives it texture while
# preserving enough contrast for the black specimen silhouettes.
image bg specimen_hall  = Solid("#aaa7a0")
image projection grain = Transform(
    "images/backgrounds/bg_ch2_projection_grain.jpg",
    xysize=(1920, 1080),
    fit="cover",
)
image projection glow = Solid("#f3efe3")
image bg ch2_vault      = bg_image("images/backgrounds/bg_ch2_vault.jpg")
image bg ch2_lab        = bg_image("images/backgrounds/bg_ch2_lab.jpg")
image bg ch2_whiteboard = bg_image("images/backgrounds/bg_ch2_whiteboard.jpg")
image bg ch2_filewall   = bg_image("images/backgrounds/bg_ch2_filewall.jpg")
image bg ch2_labhall    = bg_image("images/backgrounds/bg_ch2_labhall.jpg")
image bg ch2_gym        = bg_image("images/backgrounds/bg_ch2_gym.jpg")
image bg ch2_janitor    = bg_image("images/backgrounds/bg_ch2_janitor.jpg")
image bg scan_granted   = "#0a2a0a"


# ═════════════════════════════════════════════════════════════
# CHAPTER 2 — THE MOGBENDER
# ═════════════════════════════════════════════════════════════

transform projection_flicker:
    zoom 1.05
    xalign 0.5
    yalign 0.5
    blend "add"

    parallel:
        block:
            linear 4.0 xoffset -6 yoffset 3
            linear 4.0 xoffset 5 yoffset -2
            repeat

    parallel:
        block:
            alpha 0.12
            linear 0.10 alpha 0.17
            linear 0.08 alpha 0.13
            pause 0.35
            linear 0.06 alpha 0.18
            linear 0.12 alpha 0.12
            pause 0.55
            repeat


transform projection_breathe:
    alpha 0.0
    block:
        linear 3.2 alpha 0.045
        linear 3.8 alpha 0.0
        repeat


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
label chapter2_pickup:
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
label chapter2_road:
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
label chapter2_restricted_sign:
    scene bg ch2_sign with fade
    play music "audio/base_ambient.mp3" fadeout 1.5 fadein 1.5 volume persistent.vol_bed
    narrator "The car stops. The camera pans to a sign staked in the dirt."
    narrator "{b}⚠ RESTRICTED AREA — USE OF DEADLY FORCE AUTHORIZED ⚠{/b}"
    p "I think we should not be going here."
    narrator "Clav smirks. Says nothing."

label chapter2_gate:
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
label chapter2_lab_reveal:
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

    # ── SCENE 6 — FIRST CONTACT ──
label chapter2_gigachad_hall:
    scene bg ch2_labhall with fade
    narrator "The lab narrows into a service hall. Glass cabinets on one side. Pipes and sealed doors on the other."
    show gigachad standing at gigachad_file with dissolve
    # Let the player notice him before anyone explains what they are seeing.
    window hide
    pause 2.5
    window show
    narrator "A man in a lab coat stands at the far end with his back to you. Even from here, his frame nearly fills the doorway."
    narrator "He doesn't move. Still, you get the strange feeling you've interrupted something."
    p "Clav... who is that?"
    c "Keep walking."
    p "You know him?"
    c "Everyone here knows him."
    narrator "The unmarked door in front of him unlocks. He steps through without looking back."
    hide gigachad with dissolve
    narrator "The door seals behind him."
    narrator "The hall feels bigger after he's gone. Not emptier. Bigger."
    p "That didn't answer me."
    pause 0.4
    c "Gigachad."
    p "That's his name?"
    c "It's his classification."
    p "For what?"
    pause 0.4
    c "Keep walking."
    window hide
    pause 0.5
    play sound "audio/scan.mp3" volume (persistent.vol_sfx * 0.65)
    pause 0.3
    scene bg black with Fade(0.25, 0.25, 0.5)

    # ── SCENE 6.5 — THE NATURAL MOGGERS ──
label chapter2_projection_gallery:
    scene bg black
    window hide
    stop ambient
    $ set_cinematic_dialogue(True)
    pause 0.5
    play ambient "audio/projector_loop.mp3" loop fadein 0.6 volume (persistent.vol_sfx * 0.35)
    scene bg specimen_hall
    show projection grain at projection_flicker
    show projection glow at projection_breathe
    with Dissolve(0.8)
    pause 0.4
    window show
    narrator "The next door opens onto a windowless room and one enormous blank wall."
    narrator "An old projector chatters behind you. Grain crawls across the concrete."
    # Every subject starts beyond the right edge. The stagger keeps the blank
    # wall visible first, then feeds the reel in one silhouette at a time.
    show spec_messi     at specimen_pass(0.0)
    show spec_ronaldo   at specimen_pass(2.0)
    show spec_alysa     at specimen_pass(4.0)
    show spec_einstein  at specimen_pass(6.0, 14.0, 0.15)
    show spec_squidward at specimen_pass(8.0, 14.0, 0.16)
    show spec_anya      at specimen_pass(10.0)
    show spec_spider    at specimen_pass(12.0, 14.0, 0.17)
    narrator "One by one, figures enter the light."
    narrator "No names. No plaques. Just bodies reduced to movement, posture, and presence."
    narrator "A footballer caught mid-cut. A skater hanging calmly in the air. Shapes you almost recognize, sliding past one after another."
    narrator "Different bodies. Different worlds. Same impossible feeling — like gravity has quietly agreed to help them."
    p "Are these... famous people?"
    c "No names in the facility."
    p "Why?"
    c "Names make people think this is celebrity."
    c "It isn't."
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
    # The parade clears out — the ceiling gets the corridor to itself.
    hide spec_messi
    hide spec_ronaldo
    hide spec_alysa
    hide spec_einstein
    hide spec_squidward
    hide spec_anya
    hide spec_spider
    with Dissolve(0.8)
    c "Those people mog in one direction. Movement. Body. Presence. Myth."
    show gigachad projection at specimen_hero with Dissolve(1.2)
    c "Gigachad is what happens when nothing is missing."
    pause 0.4
    c "You won't reach that."
    p "...Oh."
    c "Neither did I."
    narrator "He says it too fast. Like the sentence bit him on the way out."
    hide gigachad with dissolve
    show clav smirk at clav_projection
    c "But you don't need the ceiling."
    c "You need one step."
    c "One step is the difference between a room forgetting you and a room checking where you're standing."
    c "So."
    c "Training wing."
    stop ambient fadeout 0.8
    hide clav with dissolve
    window hide
    $ set_cinematic_dialogue(False)
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

label chapter2_training_montage:
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
label chapter2_kai_tutorial:
    narrator "Across the gym, two trainees square off. No fists. No words. One of them sets his jaw and stands a half-inch taller."
    narrator "The other one's shoulders fold. He looks at the floor. The whole room knows exactly who won."
    show clav stern at clav_body
    c "That's a Mog Battle. Everything you built in here becomes a move."
    c "Yap is free pressure. Mog Stare hits hard. Galaxy Brain exposes weakness. Ratio Rush overwhelms. Power Nap restores Confidence."
    c "Rotate the kit to build your Mog Meter. When they swing, parry with W or dodge with S. An early parry still becomes a block."
    hide clav

    narrator "A man in a black training shirt steps onto the mat. The name patch says COACH KAI. His posture says the patch was unnecessary."
    narrator "A timing line switches on between you. Kai raises one hand: green attacks can be parried, red attacks must be dodged."
    $ start_mog_battle("kai_tutorial")
    $ kai_tutorial_result = renpy.call_screen("mog_battle_screen")
    narrator "Kai taps RESTORE. Your Aura returns to {color=#69ff9a}100 / 100{/color}."

    # ── THE GRADUATION SPAR ──
label chapter2_kai_graduation:
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
    # The whole drive home is letterboxed: bars up before the road fades in,
    # and mouse-wheel rollback is off for the scene — click to advance only.
    $ set_cinematic_dialogue(True)
    $ _rollback = False
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

label chapter2_invite:
    # Let the invitation breathe in silence before the song takes over. Once
    # Pound Cake starts, the credits still land on its first major beat at 0:11.
    stop music fadeout 0.4
    window hide

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
    $ _rollback = True
    scene bg black

    # This is the current playable ending; future chapters can replace the
    # credits jump without changing Chapter 2's closing beat.
    $ persistent.chapter2_complete = True
    $ credits_from_chapter = 2
    jump roll_credits


label dev_ch2_training_montage:
    scene bg ch2_gym with fade
    play music "audio/training_montage.mp3" fadeout 1.5 fadein 1.0 volume persistent.vol_music
    jump chapter2_training_montage


label dev_ch2_kai_tutorial:
    scene bg ch2_gym with fade
    play music "audio/training_montage.mp3" fadeout 1.5 fadein 1.0 volume persistent.vol_music
    jump chapter2_kai_tutorial


label dev_ch2_kai_graduation:
    scene bg ch2_gym with fade
    play music "audio/training_montage.mp3" fadeout 1.5 fadein 1.0 volume persistent.vol_music
    jump chapter2_kai_graduation


label dev_ch2_invite:
    $ set_cinematic_dialogue(True)
    $ _rollback = False
    scene bg ch2_road with fade
    show expression Solid("#0a1430cc") as night_tint
    window hide
    jump chapter2_invite
