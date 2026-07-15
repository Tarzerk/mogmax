# MOGMAX training minigames.

default mewing_score = 0
default mew_step = 0
default mew_cursor = 0.0
default mew_direction = 1.0
default mew_holding = False
default mew_hold_progress = 0.0
default mew_visual_progress = 0.0
default mew_misses = 0
default mew_feedback = "WAIT FOR THE WINDOW"
default mew_complete = False

default aura_training_score = 0
default aura_score = 0
default aura_combo = 0
default aura_best_combo = 0
default aura_lane = 2
default aura_jaw_x = 530.0
default aura_jaw_target_x = 530.0
default aura_falling_items = []
default aura_spawn_timer = 0.55
default aura_wave_index = 0
default aura_last_safe_lane = 2
default aura_game_state = "playing"
default aura_feedback = "HARVEST READY"
default aura_feedback_good = True
default aura_flash_time = 0.0
default aura_intro_visible = True


init python:
    MEW_STEPS = (
        {
            "name": "SEAL",
            "instruction": "CLOSE YOUR LIPS",
            "target": (0.68, 0.82),
        },
        {
            "name": "ALIGN",
            "instruction": "LET YOUR TEETH TOUCH LIGHTLY",
            "target": (0.30, 0.44),
        },
        {
            "name": "ANCHOR",
            "instruction": "PLACE THE TIP JUST BEHIND YOUR UPPER TEETH",
            "target": (0.54, 0.68),
        },
        {
            "name": "LOCK",
            "instruction": "LIFT THE WHOLE TONGUE TO THE ROOF",
            "target": (0.40, 0.56),
        },
    )

    def reset_mewing_minigame():
        s = renpy.store
        renpy.music.stop(channel="sound", fadeout=0.08)
        s.mew_step = 0
        s.mew_cursor = 0.0
        s.mew_direction = 1.0
        s.mew_holding = False
        s.mew_hold_progress = 0.0
        s.mew_visual_progress = 0.0
        s.mew_misses = 0
        s.mew_feedback = "WAIT FOR THE WINDOW"
        s.mew_complete = False

    def _mew_play_sfx(path):
        renpy.music.play(path, channel="sound", loop=False)

    def _mew_in_target():
        s = renpy.store
        start, end = MEW_STEPS[s.mew_step]["target"]
        return start <= s.mew_cursor <= end

    def _mew_tick():
        s = renpy.store

        if s.mew_complete:
            s.mew_visual_progress += (1.0 - s.mew_visual_progress) * 0.18
            return

        if s.mew_holding:
            s.mew_hold_progress = min(1.0, s.mew_hold_progress + 0.012)
            visual_target = 0.42 + (0.58 * s.mew_hold_progress)
            s.mew_visual_progress += (visual_target - s.mew_visual_progress) * 0.22
            if s.mew_hold_progress >= 1.0:
                s.mew_complete = True
                s.mew_feedback = "PALATE LOCK CONFIRMED"
                _mew_play_sfx("audio/mew_complete.mp3")
            return

        visual_targets = (0.0, 0.10, 0.24, 0.42)
        visual_target = visual_targets[s.mew_step]
        s.mew_visual_progress += (visual_target - s.mew_visual_progress) * 0.16

        s.mew_cursor += 0.012 * s.mew_direction

        if s.mew_cursor >= 1.0:
            s.mew_cursor = 1.0
            s.mew_direction = -1.0
        elif s.mew_cursor <= 0.0:
            s.mew_cursor = 0.0
            s.mew_direction = 1.0

    def _mew_press():
        s = renpy.store

        if s.mew_complete or s.mew_holding:
            return

        if not _mew_in_target():
            s.mew_misses += 1
            s.mew_feedback = "MISALIGNED - RESET"
            _mew_play_sfx("audio/mew_reject.mp3")
            return

        if s.mew_step == len(MEW_STEPS) - 1:
            s.mew_holding = True
            s.mew_hold_progress = 0.0
            s.mew_feedback = "HOLD. DO NOT BREAK FRAME."
            _mew_play_sfx("audio/mew_charge.mp3")
            return

        s.mew_step += 1
        s.mew_cursor = 0.0
        s.mew_direction = 1.0
        s.mew_feedback = "LOCKED - NEXT POSITION"
        _mew_play_sfx("audio/mew_step.mp3")

    def _mew_release():
        s = renpy.store

        if s.mew_complete or not s.mew_holding:
            return

        s.mew_holding = False
        s.mew_hold_progress = 0.0
        s.mew_misses += 1
        s.mew_feedback = "FRAME BROKEN - HOLD LONGER"
        _mew_play_sfx("audio/mew_reject.mp3")

    AURA_GOOD_ITEMS = (
        {"label": "SHADES", "value": 5},
        {"label": "PROTEIN", "value": 5},
        {"label": "BLACK FIT", "value": 10},
        {"label": "PHONE DOWN", "value": 10},
        {"label": "GOLD DUMBBELL", "value": 15},
        {"label": "CAPE", "value": 15},
        {"label": "GIGA BUST", "value": 25},
    )

    AURA_BAD_ITEMS = (
        {"label": "DOUBLE TEXT", "drain": 15},
        {"label": "PODCAST SHIRT", "drain": 10},
        {"label": "FAKE LUXURY", "drain": 10},
        {"label": "ALPHA IN 7 DAYS", "drain": 20},
        {"label": "RATE MY FIT", "drain": 15},
        {"label": "SELFIE STICK", "drain": 10},
        {"label": "FEDORA", "drain": 25},
        {"label": "SEEN AT 2 AM", "drain": 10},
        {"label": "RING LIGHT", "drain": 10},
        {"label": "COMMENT SECTION", "drain": 20},
    )

    AURA_ITEM_ASSETS = {
        "SHADES": "images/minigames/aura_items/sunglasses.png",
        "PROTEIN": "images/minigames/aura_items/protein_shaker.png",
        "BLACK FIT": "images/minigames/aura_items/fitted_shirt.png",
        "PHONE DOWN": "images/minigames/aura_items/phone_down.png",
        "GOLD DUMBBELL": "images/minigames/aura_items/dumbbell.png",
        "CAPE": "images/minigames/aura_items/cape.png",
        "GIGA BUST": "images/minigames/aura_items/marble_bust.png",
        "DOUBLE TEXT": "images/minigames/aura_items/double_text.png",
        "PODCAST SHIRT": "images/minigames/aura_items/podcast_shirt.png",
        "FAKE LUXURY": "images/minigames/aura_items/fake_luxury.png",
        "ALPHA IN 7 DAYS": "images/minigames/aura_items/alpha_7_days.png",
        "RATE MY FIT": "images/minigames/aura_items/rate_my_fit.png",
        "SELFIE STICK": "images/minigames/aura_items/selfie_stick.png",
        "FEDORA": "images/minigames/aura_items/fedora.png",
        "SEEN AT 2 AM": "images/minigames/aura_items/seen_2am.png",
        "RING LIGHT": "images/minigames/aura_items/ring_light.png",
        "COMMENT SECTION": "images/minigames/aura_items/comment_section.png",
    }

    AURA_LANE_CENTERS = (130.0, 385.0, 640.0, 895.0, 1150.0)
    AURA_ITEM_HEIGHT = 112.0

    def reset_aura_harvester():
        s = renpy.store
        renpy.music.stop(channel="sound", fadeout=0.08)
        s.aura_score = 0
        s.aura_combo = 0
        s.aura_best_combo = 0
        s.aura_lane = 2
        s.aura_jaw_x = 530.0
        s.aura_jaw_target_x = 530.0
        s.aura_falling_items = []
        s.aura_spawn_timer = 0.55
        s.aura_wave_index = 0
        s.aura_last_safe_lane = 2
        s.aura_game_state = "playing"
        s.aura_feedback = "HARVEST READY"
        s.aura_feedback_good = True
        s.aura_flash_time = 0.0
        s.aura_intro_visible = True

    def _aura_move(direction):
        s = renpy.store
        if s.aura_game_state != "playing":
            return
        new_lane = max(0, min(4, s.aura_lane + direction))
        if new_lane == s.aura_lane:
            return
        s.aura_lane = new_lane
        s.aura_jaw_target_x = AURA_LANE_CENTERS[new_lane] - 110.0

    def _aura_make_item(label, value, good, lane, y=102.0):
        return {
            "label": label,
            "value": value,
            "good": good,
            "asset": AURA_ITEM_ASSETS[label],
            "lane": lane,
            "x": AURA_LANE_CENTERS[lane] - 62.0,
            "y": y,
        }

    def _aura_random_good(pool):
        return renpy.random.choice(pool)

    def _aura_make_bad(lane, label=None, drain=None):
        if label is None:
            source = renpy.random.choice(AURA_BAD_ITEMS)
            label = source["label"]
            drain = source["drain"]
        return _aura_make_item(label, -int(drain), False, lane)

    def _aura_pick_safe_lane():
        s = renpy.store
        distant = [lane for lane in range(5) if abs(lane - s.aura_last_safe_lane) >= 2]
        choices = distant or [lane for lane in range(5) if lane != s.aura_last_safe_lane]
        safe_lane = renpy.random.choice(choices)
        s.aura_last_safe_lane = safe_lane
        return safe_lane

    def _aura_spawn_pattern():
        s = renpy.store
        score = s.aura_score
        items = []

        if score < 20:
            safe_lane = renpy.random.randrange(5)
            good = _aura_random_good(AURA_GOOD_ITEMS[:2])
            items.append(_aura_make_item(good["label"], good["value"], True, safe_lane))
            interval = 2.15

        elif score < 45:
            lanes = list(range(5))
            renpy.random.shuffle(lanes)
            safe_lane, bad_lane = lanes[:2]
            good = _aura_random_good(AURA_GOOD_ITEMS[:4])
            items.append(_aura_make_item(good["label"], good["value"], True, safe_lane))
            items.append(_aura_make_bad(bad_lane))
            interval = 2.00

        elif score < 70:
            lanes = list(range(5))
            renpy.random.shuffle(lanes)
            safe_lane = lanes[0]
            good = _aura_random_good(AURA_GOOD_ITEMS[2:6])
            items.append(_aura_make_item(good["label"], good["value"], True, safe_lane))
            for bad_lane in lanes[1:4]:
                items.append(_aura_make_bad(bad_lane))
            interval = 1.88

        elif score < 90:
            safe_lane = _aura_pick_safe_lane()
            remaining = max(5, 90 - score)
            value = min(10, remaining)
            good = _aura_random_good(AURA_GOOD_ITEMS[:4])
            for lane in range(5):
                if lane == safe_lane:
                    items.append(_aura_make_item(good["label"], value, True, lane))
                else:
                    items.append(_aura_make_bad(lane))
            interval = 2.05

        else:
            safe_lane = _aura_pick_safe_lane()
            for lane in range(5):
                if lane == safe_lane:
                    items.append(_aura_make_item("GIGA BUST", 25, True, lane))
                else:
                    items.append(_aura_make_bad(lane, label="FEDORA", drain=25))
            s.aura_feedback = "FINAL WAVE // FEDORA RAIN"
            s.aura_feedback_good = True
            interval = 2.20

        s.aura_falling_items = s.aura_falling_items + items
        s.aura_wave_index += 1
        s.aura_spawn_timer = interval

    def _aura_pass():
        s = renpy.store
        s.aura_score = 100
        s.aura_game_state = "passed"
        s.aura_feedback = "AURA STABILIZED"
        s.aura_feedback_good = True
        s.aura_flash_time = 0.8
        renpy.music.play("audio/mew_complete.mp3", channel="sound", loop=False)

    def _aura_tick():
        s = renpy.store
        if s.aura_game_state != "playing":
            return

        dt = 0.02
        difficulty = min(1.0, s.aura_score / 100.0)
        fall_speed = 118.0 + (102.0 * difficulty)

        jaw_delta = s.aura_jaw_target_x - s.aura_jaw_x
        jaw_step = 620.0 * dt
        if abs(jaw_delta) <= jaw_step:
            s.aura_jaw_x = s.aura_jaw_target_x
        elif jaw_delta > 0:
            s.aura_jaw_x += jaw_step
        else:
            s.aura_jaw_x -= jaw_step

        if s.aura_flash_time > 0.0:
            s.aura_flash_time = max(0.0, s.aura_flash_time - dt)

        s.aura_spawn_timer -= dt
        if s.aura_spawn_timer <= 0.0:
            _aura_spawn_pattern()

        next_items = []
        jaw_center = s.aura_jaw_x + 110.0

        for old_item in s.aura_falling_items:
            item = dict(old_item)
            item["y"] += fall_speed * dt
            item_center = item["x"] + 62.0
            reached_jaw = item["y"] + AURA_ITEM_HEIGHT >= 548.0
            inside_jaw = abs(item_center - jaw_center) <= 78.0

            if reached_jaw and item["y"] < 600.0 and inside_jaw:
                if item["good"]:
                    s.aura_combo += 1
                    s.aura_best_combo = max(s.aura_best_combo, s.aura_combo)
                    if item["label"] == "GIGA BUST":
                        _aura_pass()
                        break
                    s.aura_score = min(90, s.aura_score + item["value"])
                    s.aura_feedback = "%s  +%d AURA" % (item["label"], item["value"])
                    s.aura_feedback_good = True
                    s.aura_flash_time = 0.18
                    renpy.music.play("audio/mew_step.mp3", channel="sound", loop=False)
                else:
                    drain = abs(item["value"])
                    s.aura_score = max(0, s.aura_score - drain)
                    s.aura_combo = 0
                    s.aura_feedback = "%s  -%d AURA" % (item["label"], drain)
                    s.aura_feedback_good = False
                    s.aura_flash_time = 0.28
                    renpy.music.play("audio/mew_reject.mp3", channel="sound", loop=False)
                continue

            if item["y"] <= 666.0:
                next_items.append(item)
            elif item["good"]:
                if s.aura_combo > 0:
                    s.aura_feedback = "GREEN MISSED // COMBO RESET"
                    s.aura_feedback_good = False
                s.aura_combo = 0

        s.aura_falling_items = next_items


transform mew_target_pulse:
    alpha 0.35
    yoffset 4
    linear 0.45 alpha 1.0 yoffset 0
    linear 0.45 alpha 0.35 yoffset 4
    repeat


transform aura_playfield_clip:
    crop (0, 0, 1280, 495)


screen mewing_minigame():
    modal True

    add Transform("images/minigames/mewing_single_start.png", xysize=(1280, 720))
    add Transform("images/minigames/mewing_single_finish.png", xysize=(1280, 720), alpha=mew_visual_progress)

    timer 0.016 repeat True action Function(_mew_tick)
    key "mousedown_1" action Function(_mew_press)
    key "mouseup_1" action Function(_mew_release)

    $ stage = MEW_STEPS[mew_step]
    $ target_start = int(1050 * stage["target"][0])
    $ target_width = int(1050 * (stage["target"][1] - stage["target"][0]))
    $ cursor_x = min(1040, int(1050 * mew_cursor))

    vbox:
        xalign 0.5
        yalign 0.035
        spacing 4

        text "MEWING GEOMETRY":
            size 30
            color "#eeeeee"
            bold True
            xalign 0.5
            outlines [(2, "#000000", 0, 0)]

        text "PALATE CALIBRATION // STAGE [mew_step + 1] OF 4":
            size 14
            color "#789b8a"
            xalign 0.5

    hbox:
        xalign 0.5
        yalign 0.13
        spacing 44

        for index, item in enumerate(MEW_STEPS):
            vbox:
                spacing 3

                text ("DONE" if index < mew_step else ("NOW" if index == mew_step else "--")):
                    size 15
                    color ("#88ff88" if index <= mew_step else "#555c58")
                    xalign 0.5

                text item["name"]:
                    size 13
                    color ("#d9e4de" if index <= mew_step else "#555c58")
                    bold (index == mew_step)
                    xalign 0.5

    if mew_step == 0:
        text "<":
            xpos 817
            ypos 324
            size 42
            color "#88ff88"
            bold True
            at mew_target_pulse
    elif mew_step == 1:
        text "<":
            xpos 770
            ypos 331
            size 42
            color "#88ff88"
            bold True
            at mew_target_pulse
    elif mew_step == 2:
        text "<":
            xpos 737
            ypos 350
            size 42
            color "#88ff88"
            bold True
            at mew_target_pulse
    else:
        text "UP":
            xpos 630
            ypos 300
            size 30
            color "#88ff88"
            bold True
            at mew_target_pulse

    add Solid("#050807ed"):
        xysize (1280, 190)
        ypos 530

    vbox:
        xalign 0.5
        ypos 542
        spacing 8

        text stage["instruction"]:
            size 22
            color "#f0f0f0"
            bold True
            xalign 0.5

        fixed:
            xysize (1050, 30)

            add Solid("#1c2420"):
                xysize (1050, 24)
                ypos 3

            add Solid("#2c8a5566"):
                xpos target_start
                xysize (target_width, 24)
                ypos 3

            add Solid("#8affaa"):
                xpos target_start
                xysize (2, 30)

            add Solid("#8affaa"):
                xpos (target_start + target_width - 2)
                xysize (2, 30)

            add Solid("#f4f4f4"):
                xpos cursor_x
                xysize (10, 30)

        if mew_step == len(MEW_STEPS) - 1:
            fixed:
                xysize (1050, 12)

                add Solid("#1c2420"):
                    xysize (1050, 8)
                    ypos 2

                add Solid("#88ff88"):
                    xysize (int(1050 * mew_hold_progress), 8)
                    ypos 2

        else:
            null height 12

        text ("PRESS AND HOLD IN THE GREEN" if mew_step == len(MEW_STEPS) - 1 else "CLICK WHEN THE MARKER ENTERS THE GREEN"):
            size 15
            color "#aab5af"
            xalign 0.5

        text mew_feedback:
            size 17
            color ("#88ff88" if ("LOCKED" in mew_feedback or "CONFIRMED" in mew_feedback) else "#dd7777" if ("MISALIGNED" in mew_feedback or "BROKEN" in mew_feedback) else "#b7c3bd")
            bold True
            xalign 0.5

    if mew_complete:
        add Solid("#07150ddd")
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 8

            text "PALATE LOCK CONFIRMED":
                size 44
                color "#88ff88"
                bold True
                xalign 0.5
                outlines [(2, "#000000", 0, 0)]

            text "FRAME INTEGRITY: STABLE":
                size 18
                color "#d8e1dc"
                xalign 0.5

        timer 0.8 action Return(max(50, 100 - (mew_misses * 10)))


screen aura_harvester():
    modal True

    add "bg ch3_gym"
    add Solid("#020706e8")

    if not aura_intro_visible:
        timer 0.02 repeat True action Function(_aura_tick)
        key "K_LEFT" action Function(_aura_move, -1)
        key "repeat_K_LEFT" action Function(_aura_move, -1)
        key "K_RIGHT" action Function(_aura_move, 1)
        key "repeat_K_RIGHT" action Function(_aura_move, 1)

    $ aura_phase = ("CALIBRATION" if aura_score < 20 else "CHOICE PAIRS" if aura_score < 45 else "CROSSFIRE" if aura_score < 70 else "RED WALLS" if aura_score < 90 else "FEDORA RAIN")

    add Solid("#050908"):
        xysize (1280, 96)

    text "AURA HARVESTER 6000":
        xpos 34
        ypos 30
        size 30
        color "#eeeeee"
        bold True

    fixed:
        xpos 374
        ypos 29
        xysize (532, 38)

        add Solid("#173125"):
            xysize (532, 38)

        add Solid("#07100c"):
            xpos 3
            ypos 3
            xysize (526, 32)

        add Solid("#69ff9a"):
            xpos 5
            ypos 5
            xysize (int(522 * aura_score / 100.0), 28)

        text ("AURA  %d / 100" % aura_score):
            xalign 0.5
            yalign 0.5
            size 17
            color "#ffffff"
            bold True
            outlines [(2, "#000000", 0, 0)]

    text ("PHASE: %s" % aura_phase):
        xpos 950
        ypos 27
        size 14
        color "#d5ddd9"
        bold True

    text ("COMBO  x%d" % aura_combo):
        xpos 950
        ypos 53
        size 15
        color ("#69ff9a" if aura_combo > 0 else "#68736d")
        bold True

    add Solid("#224438"):
        xpos 28
        ypos 97
        xysize (1224, 2)

    for lane_center in AURA_LANE_CENTERS:
        add Solid("#24433842"):
            xpos int(lane_center)
            ypos 100
            xysize (2, 430)

    fixed:
        ypos 100
        xysize (1280, 495)
        at aura_playfield_clip

        for falling_item in aura_falling_items:
            $ item_outline = "#69ff9a" if falling_item["good"] else "#ff5f5f"
            $ item_asset = falling_item.get("asset", AURA_ITEM_ASSETS[falling_item["label"]])
            $ item_label = falling_item["label"]
            $ item_value = falling_item["value"]

            fixed:
                xpos int(falling_item["x"])
                ypos int(falling_item["y"] - 100)
                xysize (124, 112)

                add Solid(item_outline):
                    xysize (124, 112)

                add Solid("#07100d"):
                    xpos 4
                    ypos 4
                    xysize (116, 104)

                add Transform(item_asset, xysize=(108, 72), fit="contain"):
                    xpos 8
                    ypos 5

                text item_label:
                    xalign 0.5
                    ypos 77
                    xmaximum 110
                    text_align 0.5
                    size 11
                    color "#f1f3f2"
                    bold True

                text (("+%d" % item_value) if falling_item["good"] else ("%d" % item_value)):
                    xalign 0.5
                    ypos 94
                    size 13
                    color ("#69ff9a" if falling_item["good"] else "#ff6969")
                    bold True

    text aura_feedback:
        xalign 0.5
        ypos 606
        size 18
        color ("#69ff9a" if aura_feedback_good else "#ff6969")
        bold True
        outlines [(2, "#000000", 0, 0)]

    $ jaw_y = 528 if aura_flash_time > 0.0 else 535
    add Transform("images/minigames/aura_jaw.png", xysize=(220, 91)):
        xpos int(aura_jaw_x)
        ypos jaw_y

    if not aura_intro_visible:
        textbutton "<":
            xpos 485
            ypos 640
            xysize (140, 70)
            background Solid("#11251d")
            hover_background Solid("#1c4834")
            text_size 48
            text_color "#69ff9a"
            text_hover_color "#ffffff"
            text_bold True
            action Function(_aura_move, -1)

        textbutton ">":
            xpos 655
            ypos 640
            xysize (140, 70)
            background Solid("#11251d")
            hover_background Solid("#1c4834")
            text_size 48
            text_color "#69ff9a"
            text_hover_color "#ffffff"
            text_bold True
            action Function(_aura_move, 1)

    if aura_flash_time > 0.0:
        add Solid("#48ff7a20" if aura_feedback_good else "#ff35352b")

    if aura_game_state == "passed":
        add Solid("#06150ddd")
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 9

            text "AURA STABILIZED":
                size 52
                color "#69ff9a"
                bold True
                xalign 0.5
                outlines [(2, "#000000", 0, 0)]

            text "HARVEST QUOTA: 100 / 100":
                size 18
                color "#dbe5df"
                xalign 0.5

        timer 1.0 action Return("passed")

    if aura_intro_visible:
        add Solid("#020504f2")
        key "K_RETURN" action [SetVariable("aura_intro_visible", False), SetVariable("aura_feedback", "HARVEST ACTIVE")]
        key "K_SPACE" action [SetVariable("aura_intro_visible", False), SetVariable("aura_feedback", "HARVEST ACTIVE")]

        fixed:
            xpos 210
            ypos 92
            xysize (860, 536)

            add Solid("#69ff9a")
            add Solid("#07100d"):
                xpos 4
                ypos 4
                xysize (852, 528)

            text "AURA HARVESTER 6000":
                xalign 0.5
                ypos 30
                size 38
                color "#f1f3f2"
                bold True

            text "TRAINING PROTOCOL":
                xalign 0.5
                ypos 78
                size 15
                color "#789b8a"
                bold True

            add Transform("images/minigames/aura_items/sunglasses.png", xysize=(112, 78), fit="contain"):
                xpos 105
                ypos 128

            text "CATCH GREEN OBJECTS":
                xpos 245
                ypos 132
                size 22
                color "#69ff9a"
                bold True

            text "They add Aura to your score.":
                xpos 245
                ypos 165
                size 16
                color "#d6ded9"

            add Transform("images/minigames/aura_items/fedora.png", xysize=(112, 78), fit="contain"):
                xpos 105
                ypos 226

            text "AVOID RED OBJECTS":
                xpos 245
                ypos 230
                size 22
                color "#ff6969"
                bold True

            text "They drain Aura but do not end the run.":
                xpos 245
                ypos 263
                size 16
                color "#d6ded9"

            add Transform("images/minigames/aura_jaw.png", xysize=(150, 62), fit="contain"):
                xpos 85
                ypos 329

            text "MOVE THE JAW WITH  <  >":
                xpos 245
                ypos 326
                size 22
                color "#f1f3f2"
                bold True

            text "Use the arrow keys or the buttons. Reach 100 Aura.":
                xpos 245
                ypos 359
                size 16
                color "#d6ded9"

            textbutton "START HARVEST":
                xalign 0.5
                ypos 432
                xysize (310, 66)
                background Solid("#1e6f43")
                hover_background Solid("#2a9c5f")
                text_size 22
                text_color "#ffffff"
                text_bold True
                action [SetVariable("aura_intro_visible", False), SetVariable("aura_feedback", "HARVEST ACTIVE")]
