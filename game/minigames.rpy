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
default aura_time_left = 30.0
default aura_time_limit = 30.0
default aura_mode = "normal"

default acne_training_score = 0
default acne_score = 0
default acne_time_left = 6.0
default acne_mode = "normal"
default acne_targets = []
default acne_spawn_timer = 0.4
default acne_next_id = 0
default acne_spawned = 0
default acne_cleared = 0
default acne_wave = 1
default acne_wave_cleared = 0
default acne_pressure_used = False
default acne_mistakes = 0
default acne_expired = 0
default acne_pimples_spawned = 0
default acne_combo = 0
default acne_best_combo = 0
default acne_combo_flash = 0.0
default acne_burst_cooldown = 0.0
default acne_game_state = "intro"
default acne_feedback = "DERMAL SCAN READY"
default acne_feedback_good = True
default acne_flash_time = 0.0
default acne_allow_quit = False


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
    AURA_PREMIUM_ITEMS = frozenset(("GOLD DUMBBELL", "CAPE"))
    AURA_DIFFICULTY_PROFILES = {
        "normal": {
            "time_limit": 30.0,
            "good_values": {5: 10, 10: 15, 15: 20},
            "bad_values": {10: 3, 15: 4, 20: 5, 25: 6},
            "jaw_speed": 1750.0,
            "fall_base": 138.0,
            "fall_ramp": 112.0,
            "catch_window": 120.0,
            "premium_window": 90.0,
            "precision_window": 78.0,
            "catch_line": 548.0,
            "catch_bottom": 600.0,
        },
        "hard": {
            "time_limit": 30.0,
            "good_values": {},
            "bad_values": {},
            "jaw_speed": 1450.0,
            "fall_base": 138.0,
            "fall_ramp": 112.0,
            "catch_window": 78.0,
            "premium_window": 78.0,
            "precision_window": 78.0,
            "catch_line": 548.0,
            "catch_bottom": 600.0,
        },
    }

    def _aura_rules():
        return AURA_DIFFICULTY_PROFILES.get(renpy.store.aura_mode, AURA_DIFFICULTY_PROFILES["normal"])

    def reset_aura_harvester(mode="normal"):
        s = renpy.store
        if mode not in AURA_DIFFICULTY_PROFILES:
            mode = "normal"
        s.aura_mode = mode
        rules = AURA_DIFFICULTY_PROFILES[mode]
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
        s.aura_time_limit = rules["time_limit"]
        s.aura_time_left = s.aura_time_limit

    def _aura_move(direction):
        s = renpy.store
        if s.aura_game_state != "playing":
            return
        new_lane = max(0, min(4, s.aura_lane + direction))
        _aura_set_lane(new_lane)

    def _aura_set_lane(lane):
        s = renpy.store
        if s.aura_game_state != "playing":
            return
        lane = max(0, min(4, int(lane)))
        s.aura_lane = lane
        s.aura_jaw_target_x = AURA_LANE_CENTERS[lane] - 110.0

    def _aura_make_item(label, value, good, lane, y=102.0):
        rules = _aura_rules()
        if good and label != "GIGA BUST":
            value = rules["good_values"].get(int(value), int(value))
        elif not good:
            value = -rules["bad_values"].get(abs(int(value)), abs(int(value)))
        if label == "GIGA BUST":
            catch_window = rules["precision_window"]
        elif good and label in AURA_PREMIUM_ITEMS:
            catch_window = rules["premium_window"]
        elif good:
            catch_window = rules["catch_window"]
        else:
            catch_window = rules["precision_window"]
        return {
            "label": label,
            "value": value,
            "good": good,
            "asset": AURA_ITEM_ASSETS[label],
            "lane": lane,
            "x": AURA_LANE_CENTERS[lane] - 62.0,
            "y": y,
            "catch_window": catch_window,
            "precision": good and catch_window < rules["catch_window"],
        }

    def _aura_random_good(pool):
        return renpy.random.choice(pool)

    def _aura_make_bad(lane, label=None, drain=None):
        if label is None:
            source = renpy.random.choice(AURA_BAD_ITEMS)
            label = source["label"]
            drain = source["drain"]
        return _aura_make_item(label, -int(drain), False, lane)

    def _aura_pick_safe_lane(min_step=2):
        s = renpy.store
        choices = [
            lane for lane in range(5)
            if lane != s.aura_last_safe_lane
            and abs(lane - s.aura_lane) >= min_step
        ]
        choices = choices or [lane for lane in range(5) if lane != s.aura_last_safe_lane]
        safe_lane = renpy.random.choice(choices)
        s.aura_last_safe_lane = safe_lane
        return safe_lane

    def _aura_spawn_pattern():
        s = renpy.store
        score = s.aura_score
        items = []

        if score < 20:
            safe_lane = _aura_pick_safe_lane(2)
            good = _aura_random_good(AURA_GOOD_ITEMS[:2])
            items.append(_aura_make_item(good["label"], good["value"], True, safe_lane))
            bad_lanes = [lane for lane in range(5) if lane != safe_lane]
            renpy.random.shuffle(bad_lanes)
            for bad_lane in bad_lanes[:2]:
                items.append(_aura_make_bad(bad_lane))
            interval = 1.65

        elif score < 45:
            safe_lane = _aura_pick_safe_lane(2)
            good = _aura_random_good(AURA_GOOD_ITEMS[:4])
            items.append(_aura_make_item(good["label"], good["value"], True, safe_lane))
            bad_lanes = [lane for lane in range(5) if lane != safe_lane]
            renpy.random.shuffle(bad_lanes)
            for bad_lane in bad_lanes[:3]:
                items.append(_aura_make_bad(bad_lane))
            interval = 1.50

        elif score < 70:
            safe_lane = _aura_pick_safe_lane(2)
            good = _aura_random_good(AURA_GOOD_ITEMS[2:6])
            for lane in range(5):
                if lane == safe_lane:
                    items.append(_aura_make_item(good["label"], good["value"], True, lane))
                else:
                    items.append(_aura_make_bad(lane))
            interval = 1.38

        elif score < 90:
            safe_lane = _aura_pick_safe_lane(2)
            remaining = max(5, 90 - score)
            value = min(10, remaining)
            good = _aura_random_good(AURA_GOOD_ITEMS[:4])
            for lane in range(5):
                if lane == safe_lane:
                    items.append(_aura_make_item(good["label"], value, True, lane))
                else:
                    items.append(_aura_make_bad(lane))
            interval = 1.22

        else:
            safe_lane = _aura_pick_safe_lane(2)
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

    def _aura_fail():
        s = renpy.store
        s.aura_time_left = 0.0
        s.aura_game_state = "failed"
        s.aura_feedback = "TIME EXPIRED // AURA UNSTABLE"
        s.aura_feedback_good = False
        s.aura_flash_time = 0.8
        renpy.music.play("audio/mew_reject.mp3", channel="sound", loop=False)

    def _aura_retry():
        mode = renpy.store.aura_mode
        reset_aura_harvester(mode)
        renpy.store.aura_intro_visible = False
        renpy.store.aura_feedback = "HARVEST ACTIVE"

    def _aura_tick():
        s = renpy.store
        if s.aura_game_state != "playing":
            return

        dt = 0.02
        rules = _aura_rules()
        difficulty = min(1.0, s.aura_score / 100.0)
        fall_speed = rules["fall_base"] + (rules["fall_ramp"] * difficulty)

        s.aura_time_left = max(0.0, s.aura_time_left - dt)
        if s.aura_time_left <= 0.0:
            _aura_fail()
            return

        jaw_delta = s.aura_jaw_target_x - s.aura_jaw_x
        jaw_step = rules["jaw_speed"] * dt
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
            catch_window = item.get("catch_window", rules["precision_window"])
            reached_jaw = item["y"] + AURA_ITEM_HEIGHT >= rules["catch_line"]
            inside_jaw = abs(item_center - jaw_center) <= catch_window

            if reached_jaw and item["y"] < rules["catch_bottom"] and inside_jaw:
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

    ACNE_SPAWN_POINTS = (
        (514, 142), (578, 128), (642, 138), (706, 128), (770, 146),
        (502, 206), (566, 196), (642, 210), (718, 196), (782, 212),
        (492, 314), (540, 342), (518, 400), (548, 458),
        (736, 340), (786, 314), (766, 402), (730, 462),
        (614, 330), (668, 350), (638, 404),
        (570, 512), (620, 536), (674, 538), (716, 506),
    )

    ACNE_STAGE_ASSETS = {
        "small": "images/minigames/acne_small.png",
        "medium": "images/minigames/acne_medium.png",
        "cyst": "images/minigames/acne_cyst.png",
    }

    ACNE_MARK_ASSETS = {
        "MOLE": "images/minigames/acne_mole.png",
        "FRECKLE": "images/minigames/acne_freckle.png",
        "BEAUTY MARK": "images/minigames/acne_beauty.png",
    }

    ACNE_INITIAL_TIME = 6.0
    ACNE_MAX_TIME = 6.5
    ACNE_TOTAL_WAVES = 3
    ACNE_WAVE_GOAL = 8
    ACNE_CLEAR_GOAL = ACNE_TOTAL_WAVES * ACNE_WAVE_GOAL
    ACNE_WRONG_TIME = 1.75
    ACNE_EXPIRE_TIME = 0.40
    ACNE_BURST_LOCKOUT = 1.50
    ACNE_BURST_GRACE = 1.35
    ACNE_REVEAL_DELAY = 0.34

    ACNE_LIFETIMES = {
        "small": 3.15,
        "medium": 3.80,
        "cyst": 5.40,
    }

    ACNE_TIME_BONUSES = {
        "small": 0.55,
        "medium": 0.45,
        "cyst": 0.30,
    }
    ACNE_DIFFICULTY_PROFILES = {
        "normal": {
            "initial_time": 8.5,
            "max_time": 10.0,
            "wave_floor": 8.0,
            "clear_recovery": 0.45,
            "time_bonuses": {
                "small": 0.85,
                "medium": 1.00,
                "cyst": 0.65,
            },
        },
        "hard": {
            "initial_time": ACNE_INITIAL_TIME,
            "max_time": 6.5,
            "wave_floor": 5.0,
            "clear_recovery": 0.0,
            "time_bonuses": ACNE_TIME_BONUSES,
        },
    }

    def _acne_rules():
        return ACNE_DIFFICULTY_PROFILES.get(renpy.store.acne_mode, ACNE_DIFFICULTY_PROFILES["normal"])

    def reset_acne_minigame(mode="normal", allow_quit=False):
        s = renpy.store
        if mode not in ACNE_DIFFICULTY_PROFILES:
            mode = "normal"
        s.acne_mode = mode
        rules = ACNE_DIFFICULTY_PROFILES[mode]
        s.acne_allow_quit = bool(allow_quit)
        s.acne_score = 0
        s.acne_time_left = rules["initial_time"]
        s.acne_targets = []
        s.acne_spawn_timer = 0.4
        s.acne_next_id = 0
        s.acne_spawned = 0
        s.acne_cleared = 0
        s.acne_wave = 1
        s.acne_wave_cleared = 0
        s.acne_pressure_used = False
        s.acne_mistakes = 0
        s.acne_expired = 0
        s.acne_pimples_spawned = 0
        s.acne_combo = 0
        s.acne_best_combo = 0
        s.acne_combo_flash = 0.0
        s.acne_burst_cooldown = 0.0
        s.acne_game_state = "intro"
        s.acne_feedback = "DERMAL SCAN READY"
        s.acne_feedback_good = True
        s.acne_flash_time = 0.0

    def _acne_start():
        s = renpy.store
        s.acne_game_state = "playing"
        s.acne_feedback = "MOVE FAST // CORRECT CLICKS ADD TIME"
        _acne_spawn(force_stage="small")
        _acne_spawn(force_stage="medium", life_bonus=0.40)
        _acne_spawn(force_stage="cyst", life_bonus=0.80)

    def _acne_retry():
        mode = renpy.store.acne_mode
        allow_quit = renpy.store.acne_allow_quit
        reset_acne_minigame(mode, allow_quit)
        _acne_start()

    def _acne_stage(target):
        if target["age"] < 1.8:
            return "small"
        if target["age"] < 3.6:
            return "medium"
        return "cyst"

    def _acne_open_point():
        s = renpy.store
        points = list(ACNE_SPAWN_POINTS)
        renpy.random.shuffle(points)
        for x, y in points:
            if all(((x - target["x"]) ** 2 + (y - target["y"]) ** 2) >= 2800 for target in s.acne_targets):
                return x, y
        return None

    def _acne_spawn(force_stage=None, force_mark=False, life_scale=1.0, life_bonus=0.0, temporary_mark=False):
        s = renpy.store
        point = _acne_open_point()
        if point is None:
            s.acne_spawn_timer = 0.35
            return False

        marks = sum(1 for target in s.acne_targets if target["kind"] == "mark")
        make_mark = force_mark or (force_stage is None and s.acne_spawned > 1 and marks < 6 and renpy.random.randrange(100) < 26)
        x, y = point

        if make_mark:
            mark_name = renpy.random.choice(tuple(ACNE_MARK_ASSETS.keys()))
            target = {
                "id": s.acne_next_id,
                "kind": "mark",
                "mark": mark_name,
                "x": x,
                "y": y,
                "age": 0.0,
                "visible_age": 0.0,
                "life_left": (2.6 if temporary_mark else None),
                "life_max": (2.6 if temporary_mark else None),
                "hits": 0,
            }
        else:
            if force_stage is None:
                if s.acne_pimples_spawned >= 2 and s.acne_pimples_spawned % 3 == 2:
                    force_stage = "cyst"
                elif s.acne_pimples_spawned > 0 and renpy.random.randrange(100) < 35:
                    force_stage = "medium"
                else:
                    force_stage = "small"

            start_age = 0.0 if force_stage == "small" else 2.0 if force_stage == "medium" else 3.7
            lifetime = (ACNE_LIFETIMES[force_stage] * life_scale) + life_bonus + (renpy.random.random() * 0.45)
            target = {
                "id": s.acne_next_id,
                "kind": "pimple",
                "mark": None,
                "x": x,
                "y": y,
                "age": start_age,
                "visible_age": 0.0,
                "life_left": lifetime,
                "life_max": lifetime,
                "hits": 0,
            }
            s.acne_pimples_spawned += 1

        s.acne_targets = s.acne_targets + [target]
        s.acne_next_id += 1
        s.acne_spawned += 1
        s.acne_spawn_timer = 0.38 + renpy.random.random() * 0.16
        return True

    def _acne_pressure_wave():
        s = renpy.store
        spawned = 0
        for _index in range(3):
            if _acne_spawn(force_mark=True, temporary_mark=True):
                spawned += 1

        pressure_stage = renpy.random.choice(("small", "medium"))
        if _acne_spawn(force_stage=pressure_stage, life_scale=0.78):
            spawned += 1

        s.acne_pressure_used = True
        s.acne_spawn_timer = 1.25
        s.acne_feedback = "PRESSURE WAVE // THREE MARKS, ONE PULSE"
        s.acne_feedback_good = False
        s.acne_flash_time = 0.22
        renpy.music.play("audio/ui_click.ogg", channel="sound", loop=False)

    def _acne_finish(success):
        s = renpy.store
        s.acne_game_state = "passed" if success else "failed"
        s.acne_feedback_good = success
        if success:
            s.acne_feedback = "CLEAR SKIN // +100 AURA"
            renpy.music.play("audio/mew_complete.mp3", channel="sound", loop=False)
        else:
            s.acne_feedback = "TIME EXPIRED // WAVE %d // %d / %d TOTAL" % (s.acne_wave, s.acne_cleared, ACNE_CLEAR_GOAL)
            renpy.music.play("audio/mew_reject.mp3", channel="sound", loop=False)

    def _acne_complete_wave():
        s = renpy.store
        s.acne_game_state = "wave_clear"
        s.acne_targets = []
        s.acne_spawn_timer = 0.4
        s.acne_feedback = "WAVE %d CLEARED" % s.acne_wave
        s.acne_feedback_good = True
        s.acne_flash_time = 0.35
        renpy.music.play("audio/mew_step.mp3", channel="sound", loop=False)

    def _acne_next_wave():
        s = renpy.store
        s.acne_wave += 1
        s.acne_wave_cleared = 0
        s.acne_pressure_used = False
        s.acne_burst_cooldown = 0.0
        s.acne_time_left = max(_acne_rules()["wave_floor"], s.acne_time_left)
        s.acne_game_state = "playing"
        s.acne_feedback = "WAVE %d ACTIVE // FIND THE PULSE" % s.acne_wave
        s.acne_feedback_good = True
        _acne_spawn(force_stage="small")
        _acne_spawn(force_stage="medium", life_bonus=0.40)
        _acne_spawn(force_stage="cyst", life_bonus=0.80)
        renpy.restart_interaction()

    def _acne_click(target_id):
        s = renpy.store
        if s.acne_game_state != "playing":
            return

        next_targets = []
        clicked = None
        for target in s.acne_targets:
            if target["id"] == target_id:
                clicked = dict(target)
            else:
                next_targets.append(target)

        if clicked is None:
            return

        if clicked["kind"] == "mark":
            s.acne_score = max(0, s.acne_score - 10)
            s.acne_time_left = max(0.0, s.acne_time_left - ACNE_WRONG_TIME)
            s.acne_mistakes += 1
            s.acne_combo = 0
            s.acne_combo_flash = 0.0
            s.acne_feedback = "%s IS STRUCTURAL  -%.2f SEC" % (clicked["mark"], ACNE_WRONG_TIME)
            s.acne_feedback_good = False
            s.acne_flash_time = 0.22
            renpy.music.play("audio/mew_reject.mp3", channel="sound", loop=False)
        else:
            stage = _acne_stage(clicked)
            required_hits = 3 if stage == "cyst" else 1
            clicked["hits"] += 1
            s.acne_combo += 1
            s.acne_best_combo = max(s.acne_best_combo, s.acne_combo)
            s.acne_combo_flash = 0.18
            recovery_scale = 0.65 if s.acne_combo < 3 else 0.85 if s.acne_combo < 5 else 1.0
            rules = _acne_rules()
            time_bonus = rules["time_bonuses"][stage] * recovery_scale
            s.acne_time_left = min(rules["max_time"], s.acne_time_left + time_bonus)

            if clicked["hits"] < required_hits:
                clicked["life_left"] = min(clicked["life_max"], clicked["life_left"] + 1.10)
                next_targets.append(clicked)
                s.acne_feedback = "CYST PRESSURE  %d / %d  +%.2f SEC" % (clicked["hits"], required_hits, time_bonus)
                s.acne_feedback_good = True
                renpy.music.play("audio/ui_click.ogg", channel="sound", loop=False)
            else:
                clear_recovery = rules["clear_recovery"]
                s.acne_time_left = min(rules["max_time"], s.acne_time_left + clear_recovery)
                points = 5 if stage == "small" else 10 if stage == "medium" else 25
                s.acne_score += points
                s.acne_cleared += 1
                s.acne_wave_cleared += 1
                s.acne_feedback = "%s CLEARED  +%.2f SEC" % (stage.upper(), time_bonus + clear_recovery)
                s.acne_feedback_good = True
                s.acne_flash_time = 0.14
                renpy.music.play("audio/mew_step.mp3", channel="sound", loop=False)

        s.acne_targets = next_targets
        if s.acne_wave_cleared >= ACNE_WAVE_GOAL:
            if s.acne_wave >= ACNE_TOTAL_WAVES:
                _acne_finish(True)
            else:
                _acne_complete_wave()
        elif s.acne_time_left <= 0.0:
            _acne_finish(False)
        renpy.restart_interaction()

    def _acne_tick():
        s = renpy.store
        if s.acne_game_state != "playing":
            return

        dt = 0.05
        s.acne_time_left = max(0.0, s.acne_time_left - dt)
        s.acne_spawn_timer -= dt
        s.acne_flash_time = max(0.0, s.acne_flash_time - dt)
        s.acne_combo_flash = max(0.0, s.acne_combo_flash - dt)
        s.acne_burst_cooldown = max(0.0, s.acne_burst_cooldown - dt)

        aged_targets = []
        expired_ids = []
        for old_target in s.acne_targets:
            target = dict(old_target)
            target["visible_age"] = target.get("visible_age", 0.0) + dt
            if target["kind"] == "pimple":
                target["age"] += dt
                target["life_left"] = max(0.0, target["life_left"] - dt)
                if target["life_left"] <= 0.0:
                    expired_ids.append(target["id"])
            elif target.get("life_left") is not None:
                target["life_left"] = max(0.0, target["life_left"] - dt)
                if target["life_left"] <= 0.0:
                    continue
            aged_targets.append(target)
        s.acne_targets = aged_targets

        if expired_ids and s.acne_burst_cooldown <= 0.0:
            burst_id = min(expired_ids)
            protected_targets = []
            for old_target in s.acne_targets:
                if old_target["id"] == burst_id:
                    continue
                target = dict(old_target)
                if target["kind"] == "pimple":
                    target["life_left"] = max(target["life_left"], ACNE_BURST_GRACE)
                protected_targets.append(target)
            s.acne_targets = protected_targets

            s.acne_time_left = max(0.0, s.acne_time_left - ACNE_EXPIRE_TIME)
            s.acne_expired += 1
            s.acne_combo = 0
            s.acne_combo_flash = 0.0
            s.acne_burst_cooldown = ACNE_BURST_LOCKOUT
            s.acne_feedback = "TARGET BURST  -%.2f SEC // OTHERS PROTECTED" % ACNE_EXPIRE_TIME
            s.acne_feedback_good = False
            s.acne_flash_time = 0.28
            renpy.music.play("audio/mew_reject.mp3", channel="sound", loop=False)
        elif expired_ids:
            held_targets = []
            for old_target in s.acne_targets:
                target = dict(old_target)
                if target["kind"] == "pimple" and target["life_left"] <= 0.0:
                    target["life_left"] = 0.20
                held_targets.append(target)
            s.acne_targets = held_targets

        if s.acne_wave_cleared >= 4 and not s.acne_pressure_used:
            _acne_pressure_wave()
        elif s.acne_spawn_timer <= 0.0:
            _acne_spawn()

        if s.acne_time_left <= 0.0:
            _acne_finish(False)


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

    on "show" action SetVariable("quick_menu", False)
    on "hide" action SetVariable("quick_menu", True)

    add "bg ch2_gym"
    add Solid("#020706e8")

    if not aura_intro_visible:
        timer 0.02 repeat True action Function(_aura_tick)
        key "K_LEFT" action Function(_aura_move, -1)
        key "repeat_K_LEFT" action Function(_aura_move, -1)
        key "K_RIGHT" action Function(_aura_move, 1)
        key "repeat_K_RIGHT" action Function(_aura_move, 1)
        key "K_a" action Function(_aura_move, -1)
        key "K_d" action Function(_aura_move, 1)
        key "K_1" action Function(_aura_set_lane, 0)
        key "K_2" action Function(_aura_set_lane, 1)
        key "K_3" action Function(_aura_set_lane, 2)
        key "K_4" action Function(_aura_set_lane, 3)
        key "K_5" action Function(_aura_set_lane, 4)

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

    text ("TIME  %04.1f" % aura_time_left):
        xpos 950
        ypos 16
        size 22
        color ("#ff6969" if aura_time_left <= 8.0 else "#eeeeee")
        bold True

    text ("%s // %s" % (aura_mode.upper(), aura_phase)):
        xpos 950
        ypos 49
        size 12
        color "#d5ddd9"
        bold True

    text ("COMBO x%d" % aura_combo):
        xpos 1150
        ypos 49
        size 12
        color ("#69ff9a" if aura_combo > 0 else "#68736d")
        bold True

    add Solid("#173125"):
        xpos 28
        ypos 89
        xysize (1224, 6)

    add Solid("#69ff9a" if aura_time_left > 8.0 else "#ff5f5f"):
        xpos 28
        ypos 89
        xysize (int(1224 * aura_time_left / aura_time_limit), 6)

    add Solid("#224438"):
        xpos 28
        ypos 97
        xysize (1224, 2)

    for lane_edge in range(1, 5):
        add Solid("#24433842"):
            xpos (lane_edge * 256)
            ypos 100
            xysize (2, 430)

    if not aura_intro_visible:
        for lane_index in range(5):
            button:
                xpos (lane_index * 256)
                ypos 100
                xysize (256, 430)
                background Solid("#00000000")
                hover_background Solid("#69ff9a0d")
                action Function(_aura_set_lane, lane_index)

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

                if falling_item.get("precision", False):
                    add Solid("#ffcf55"):
                        xysize (124, 4)

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
        for lane_index in range(5):
            textbutton ("LANE %d" % (lane_index + 1)):
                xpos int(AURA_LANE_CENTERS[lane_index] - 58)
                ypos 646
                xysize (116, 58)
                background Solid("#1e6f43" if aura_lane == lane_index else "#11251d")
                hover_background Solid("#2a9c5f")
                text_size 15
                text_color ("#ffffff" if aura_lane == lane_index else "#69ff9a")
                text_bold True
                action Function(_aura_set_lane, lane_index)

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

    if aura_game_state == "failed":
        add Solid("#130605e8")
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 18

            text "AURA UNSTABLE":
                size 50
                color "#ff6969"
                bold True
                xalign 0.5

            text ("HARVESTED %d / 100" % aura_score):
                size 19
                color "#dbe5df"
                xalign 0.5

            textbutton "RETRY HARVEST":
                xalign 0.5
                xysize (300, 64)
                background Solid("#8a2929")
                hover_background Solid("#b73a3a")
                text_size 21
                text_color "#ffffff"
                text_bold True
                action Function(_aura_retry)

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

            text ("%s PROTOCOL" % aura_mode.upper()):
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

            text ("Wide catch window. High-value drops keep the tighter center catch." if aura_mode == "normal" else "They add Aura. Every catch uses the precision window."):
                xpos 245
                ypos 165
                size 14
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

            text ("Small Aura drain. They do not end the run." if aura_mode == "normal" else "Full Aura drain. They do not end the run."):
                xpos 245
                ypos 263
                size 16
                color "#d6ded9"

            add Transform("images/minigames/aura_jaw.png", xysize=(150, 62), fit="contain"):
                xpos 85
                ypos 329

            text "SELECT ANY LANE":
                xpos 245
                ypos 326
                size 22
                color "#f1f3f2"
                bold True

            text ("Click its lane button, or use arrows / A-D. Reach 100 Aura in %d seconds." % int(aura_time_limit)):
                xpos 245
                ypos 359
                size 15
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


screen acne_pop_minigame():
    modal True

    on "show" action SetVariable("quick_menu", False)
    on "hide" action SetVariable("quick_menu", True)

    if acne_allow_quit:
        key "game_menu" action Return("quit")
        key "K_ESCAPE" action Return("quit")

    add Transform("images/minigames/acne_face.png", xysize=(1280, 720), fit="cover")
    add Solid("#02050432")

    if acne_game_state == "playing":
        timer 0.05 repeat True action Function(_acne_tick)

    add Solid("#080c0beF"):
        xysize (1280, 86)

    text ("DERMAL PURGE // WAVE %d/%d" % (acne_wave, ACNE_TOTAL_WAVES)):
        xpos 34
        ypos 24
        size 25
        color "#f0f2f1"
        bold True

    text ("TIME  %04.1f" % acne_time_left):
        xalign 0.5
        ypos 23
        size 27
        color ("#ff6262" if acne_time_left <= 2.0 else "#e3e7e5")
        bold True

    text ("SCORE  %03d" % acne_score):
        xpos 1240
        xanchor 1.0
        ypos 20
        size 19
        color "#69e4ad"
        bold True

    text ("WAVE %02d/%02d   TOTAL %02d/%02d   ERRORS %02d   MISSED %02d" % (acne_wave_cleared, ACNE_WAVE_GOAL, acne_cleared, ACNE_CLEAR_GOAL, acne_mistakes, acne_expired)):
        xpos 1240
        xanchor 1.0
        ypos 48
        size 13
        color "#89948f"
        bold True

    if acne_allow_quit:
        textbutton "QUIT":
            xpos 1124
            ypos 96
            xysize (118, 42)
            background Solid("#101513dd")
            hover_background Solid("#702f2f")
            text_size 15
            text_color "#d8e0dc"
            text_hover_color "#ffffff"
            text_bold True
            action Return("quit")

    if acne_combo > 0 and acne_game_state == "playing":
        $ combo_rank = "CLEAN" if acne_combo < 4 else "SHARP" if acne_combo < 7 else "BRUTAL" if acne_combo < 10 else "FLAWLESS"

        fixed:
            xpos 1000
            ypos 112
            xysize (238, 112)

            text ("%02d" % acne_combo):
                xpos 0
                ypos -8
                size (62 if acne_combo_flash > 0.0 else 56)
                color ("#fff0a8" if acne_combo_flash > 0.0 else "#ffcf55")
                bold True
                outlines [(3, "#210a05", 0, 0)]

            text "HIT":
                xpos 78
                ypos 5
                size 25
                color "#f3f0e7"
                bold True
                outlines [(2, "#210a05", 0, 0)]

            text "KOMBO":
                xpos 78
                ypos 34
                size 22
                color "#ff5f4a"
                bold True
                outlines [(2, "#210a05", 0, 0)]

            text combo_rank:
                xpos 2
                ypos 70
                size 18
                color ("#ff5f4a" if acne_combo >= 7 else "#69e4ad")
                bold True
                outlines [(2, "#07100d", 0, 0)]

    add Solid("#1b2823"):
        ypos 82
        xysize (1280, 4)

    add Solid("#69e4ad" if acne_time_left > 2.0 else "#ff6262"):
        ypos 82
        xysize (int(1280 * acne_time_left / _acne_rules()["max_time"]), 4)

    for target in acne_targets:
        if target["kind"] == "pimple":
            $ acne_stage = _acne_stage(target)
            $ acne_fresh = target.get("visible_age", 0.0) < ACNE_REVEAL_DELAY
            $ acne_pulsing = not acne_fresh and (target.get("visible_age", 0.0) % 0.52) < 0.13
            $ acne_asset = ACNE_MARK_ASSETS["MOLE"] if acne_fresh else ACNE_STAGE_ASSETS[acne_stage]
            $ acne_size = 34 if acne_fresh else 38 if acne_stage == "small" else 56 if acne_stage == "medium" else 82
            $ acne_life_ratio = target["life_left"] / target["life_max"]
        else:
            $ acne_stage = "mark"
            $ acne_fresh = False
            $ acne_pulsing = False
            $ acne_asset = ACNE_MARK_ASSETS[target["mark"]]
            $ acne_size = 34 if target["mark"] == "MOLE" else 24 if target["mark"] == "FRECKLE" else 40

        if target["kind"] == "pimple" and not acne_fresh:
            text "○":
                xpos target["x"]
                ypos target["y"]
                xanchor 0.5
                yanchor 0.52
                size int((acne_size + 42) * acne_life_ratio + acne_size)
                color ("#fff0a8f2" if acne_pulsing else "#ff5f4a9e")
                font "DejaVuSans.ttf"

        imagebutton:
            idle Transform(acne_asset, zoom=(1.12 if acne_pulsing else 1.0))
            hover Transform(acne_asset, zoom=(1.16 if acne_pulsing else 1.08))
            xpos int(target["x"] - acne_size / 2)
            ypos int(target["y"] - acne_size / 2)
            focus_mask True
            action Function(_acne_click, target["id"])

        if acne_stage == "cyst" and target["hits"]:
            text ("%d/3" % target["hits"]):
                xpos target["x"]
                ypos target["y"] + 30
                xanchor 0.5
                size 12
                color "#ffffff"
                bold True
                outlines [(2, "#210a0d", 0, 0)]

    frame:
        xpos 300
        ypos 646
        xysize (680, 52)
        background Solid("#101513ed")
        padding (18, 11)

        text acne_feedback:
            xalign 0.5
            yalign 0.5
            size 17
            color ("#69e4ad" if acne_feedback_good else "#ff6969")
            bold True

    if acne_flash_time > 0.0:
        add Solid("#69e4ad20" if acne_feedback_good else "#ff35352b")

    if acne_game_state == "intro":
        add Solid("#020504ed")

        vbox:
            xalign 0.5
            yalign 0.48
            spacing 14

            text "DERMAL PURGE":
                xalign 0.5
                size 44
                color "#f1f3f2"
                bold True

            text ("%s MODE" % acne_mode.upper()):
                xalign 0.5
                size 14
                color ("#ffcf55" if acne_mode == "hard" else "#69e4ad")
                bold True

            text ("3 WAVES // CLEAR %d TARGETS PER WAVE" % ACNE_WAVE_GOAL):
                xalign 0.5
                size 17
                color "#8ca297"
                bold True

            text "PIMPLES BEGIN DARK LIKE MARKS // WAIT FOR THE PULSE":
                xalign 0.5
                size 14
                color "#69e4ad"
                bold True

            text "ONE TARGET CAN BURST AT A TIME // OTHERS GET 1.35 SEC PROTECTION":
                xalign 0.5
                size 13
                color "#ffcf55"
                bold True

            text ("5+ KOMBO UNLOCKS FULL TIME RECOVERY // MARKS COST 1.75 SECONDS" if acne_mode == "hard" else "NORMAL: BIGGER CLOCK // COMBOS GIVE MORE RECOVERY"):
                xalign 0.5
                size 13
                color "#ffcf55"
                bold True

            text "PRESSURE WAVE: THREE MARKS, ONE PULSING TARGET":
                xalign 0.5
                size 13
                color "#ff6969"
                bold True

            text ("FULL CLEAR ADDS +0.45 SEC RECOVERY" if acne_mode == "normal" else "HARD MODE: NO FULL-CLEAR RECOVERY"):
                xalign 0.5
                size 13
                color ("#69e4ad" if acne_mode == "normal" else "#ffcf55")
                bold True

            null height 8

            hbox:
                xalign 0.5
                spacing 46

                vbox:
                    spacing 8
                    add "images/minigames/acne_small.png":
                        xalign 0.5
                    text ("SMALL  +0.85 MAX" if acne_mode == "normal" else "SMALL  +0.55 MAX"):
                        xalign 0.5
                        size 15
                        color "#e7ebe9"
                        bold True

                vbox:
                    spacing 8
                    add "images/minigames/acne_medium.png":
                        xalign 0.5
                    text ("MEDIUM  +1.00 MAX" if acne_mode == "normal" else "MEDIUM  +0.45 MAX"):
                        xalign 0.5
                        size 15
                        color "#e7ebe9"
                        bold True

                vbox:
                    spacing 8
                    add "images/minigames/acne_cyst.png":
                        xalign 0.5
                    text ("CYST  +0.65 / HIT" if acne_mode == "normal" else "CYST  +0.30 / HIT"):
                        xalign 0.5
                        size 15
                        color "#e7ebe9"
                        bold True

                vbox:
                    spacing 8
                    add "images/minigames/acne_mole.png":
                        xalign 0.5
                    text "MARK  -1.75 SEC":
                        xalign 0.5
                        size 15
                        color "#ff6969"
                        bold True

            null height 12

            textbutton "BEGIN SCAN":
                xalign 0.5
                xysize (290, 62)
                background Solid("#19754f")
                hover_background Solid("#249b69")
                text_size 20
                text_color "#ffffff"
                text_bold True
                action Function(_acne_start)

    if acne_game_state == "wave_clear":
        add Solid("#04110be8")
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 10

            text ("WAVE %d CLEARED" % acne_wave):
                xalign 0.5
                size 50
                color "#69e4ad"
                bold True
                outlines [(2, "#000000", 0, 0)]

            text ("%d / %d TOTAL TARGETS PURGED" % (acne_cleared, ACNE_CLEAR_GOAL)):
                xalign 0.5
                size 19
                color "#e2e7e4"
                bold True

            text "NEXT WAVE INCOMING":
                xalign 0.5
                size 16
                color "#ffcf55"
                bold True

        timer 1.0 action Function(_acne_next_wave)

    if acne_game_state == "failed":
        add Solid("#050706e8")
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 13

            text "SCAN INCOMPLETE":
                xalign 0.5
                size 42
                color "#ff6969"
                bold True

            text acne_feedback:
                xalign 0.5
                size 18
                color "#cbd0cd"

            textbutton "RETRY":
                xalign 0.5
                xysize (250, 56)
                background Solid("#8d3636")
                hover_background Solid("#b34848")
                text_size 19
                text_color "#ffffff"
                text_bold True
                action Function(_acne_retry)

    if acne_game_state == "passed":
        add Solid("#04110be8")
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 8

            text "CLEAR SKIN":
                xalign 0.5
                size 58
                color "#69e4ad"
                bold True
                outlines [(2, "#000000", 0, 0)]

            text "+100 AURA":
                xalign 0.5
                size 26
                color "#ffffff"
                bold True

            text ("PURGE SCORE  %03d" % acne_score):
                xalign 0.5
                size 16
                color "#93a19a"

        timer 1.4 action Return(acne_score)
