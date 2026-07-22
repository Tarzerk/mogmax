# Reusable telegraph-intent battle system for MOGMAX.

default mog_battle = {}
default mog_battle_aura_kept = 100
default mog_battle_last_result = None


init python:
    renpy.music.register_channel("battle_sfx", mixer="sfx", loop=False)
    renpy.music.register_channel("battle_impact", mixer="sfx", loop=False)
    renpy.music.register_channel("battle_warning", mixer="sfx", loop=False)

    MOG_MOVES = {
        "aura": {
            "name": "Aura Blast",
            "mark": "A",
            "description": "Pressure. Spends 3 Momentum for Giga damage.",
            "color": "#a21d50",
            "verbal": True,
        },
        "frame": {
            "name": "Hold Frame",
            "mark": "F",
            "description": "Brace. Correct reads build Momentum.",
            "color": "#23a57c",
            "verbal": False,
        },
        "cringe": {
            "name": "Cringe Check",
            "mark": "C",
            "description": "Apply Cringe. Third stack detonates.",
            "color": "#d45122",
            "verbal": True,
        },
        "mew": {
            "name": "Mew",
            "mark": "M",
            "description": "Silence + heal. 2-round cooldown.",
            "color": "#13a88a",
            "verbal": False,
        },
    }

    MOG_INTENTS = {
        "ATTACK": {"mark": "!", "color": "#c84a35", "answer": "frame"},
        "BLOCK": {"mark": "#", "color": "#3e8ec7", "answer": "cringe"},
        "YAP": {"mark": ">", "color": "#b8752a", "answer": "mew"},
        "ANALYZE": {"mark": "?", "color": "#9a65d1", "answer": None},
    }

    MOG_VARIANTS = {
        "heavy": {
            "label": "HEAVY",
            "clue": "Shoulders square. Full commitment.",
            "color": "#e34d3c",
            "tells": (
                "Both feet plant. One shoulder loads.",
                "His fist tightens and his hips turn in.",
                "He leans forward with his whole frame.",
            ),
        },
        "pressure": {
            "label": "PRESSURE",
            "clue": "He crowds the pocket.",
            "color": "#e87936",
            "tells": (
                "He closes the distance without blinking.",
                "Your space disappears one step at a time.",
                "He crowds your stance and keeps advancing.",
            ),
        },
        "feint": {
            "label": "FEINT",
            "clue": "His weight stays on the back foot.",
            "color": "#f0b84a",
            "tells": (
                "His shoulder twitches, but his weight stays back.",
                "The first motion is fast. His feet never commit.",
                "He shows an opening and watches you react.",
            ),
        },
        "guard": {
            "label": "GUARD",
            "clue": "Elbows close. He is absorbing.",
            "color": "#4c9ed4",
            "tells": (
                "His elbows tuck and his chin disappears.",
                "He closes every opening and waits.",
                "His stance shrinks behind a sealed frame.",
            ),
        },
        "counter": {
            "label": "COUNTER",
            "clue": "One hand waits for your swing.",
            "color": "#8c74d8",
            "tells": (
                "One hand hangs back, waiting for your swing.",
                "He leaves bait open and tracks your shoulders.",
                "His guard looks loose. His eyes do not.",
            ),
        },
        "rant": {
            "label": "RANT",
            "clue": "He inhales like a podcast started.",
            "color": "#d98935",
            "tells": (
                "His chest fills like a podcast is starting.",
                "He points at your jaw and takes a huge breath.",
                "He is visibly preparing a twelve-step explanation.",
            ),
        },
        "bait": {
            "label": "BAIT",
            "clue": "The silence feels rehearsed.",
            "color": "#c2669f",
            "tells": (
                "He goes suspiciously quiet and watches your mouth.",
                "The rant never starts. He studies your lips instead.",
                "He pretends to inhale, then waits for silence.",
            ),
        },
        "repeat": {
            "label": "PATTERN READ",
            "clue": "He has memorized your repetition.",
            "color": "#a56cdb",
            "tells": (
                "He mirrors your last move before you make it.",
                "His eyes follow the pattern you keep repeating.",
                "He mouths the name of your favorite move.",
            ),
        },
    }

    MOG_CRINGE_LINES = (
        "Negative canthal tilt.",
        "Your mewing streak got interrupted.",
        "That ramus is fighting for its life.",
        "Bro got mogged by overhead lighting.",
        "Your facial thirds filed a complaint.",
        "The hunter eyes are in another save file.",
        "Your side profile needs a patch note.",
        "The jaw trainer requested a transfer.",
        "Looksmaxxing status: maintenance required.",
        "The PSL scale just blue-screened.",
        "Your masseters are on airplane mode.",
        "That buccal fat has tenure.",
        "The mirror lowered its brightness.",
        "Your gonial angle went nonverbal.",
        "The symmetry filter clocked out.",
        "Bro is softmaxxing involuntarily.",
        "Your cheekbones missed the update.",
        "The face card entered cooldown.",
        "Mog rating: participation aura.",
        "Your eye area needs a balance patch.",
        "The front camera won the exchange.",
        "Your phenotype got ratioed.",
        "Bone structure has left the chat.",
        "The canthal tilt is purely theoretical.",
        "Your jawline is still buffering.",
    )

    MOG_VARIANT_POOLS = {
        "basic": {
            "ATTACK": (("heavy", 65), ("pressure", 35)),
            "BLOCK": (("guard", 100),),
            "YAP": (("rant", 100),),
            "ANALYZE": (("repeat", 100),),
        },
        "basic_plus": {
            "ATTACK": (("heavy", 48), ("pressure", 42), ("feint", 10)),
            "BLOCK": (("guard", 85), ("counter", 15)),
            "YAP": (("rant", 85), ("bait", 15)),
            "ANALYZE": (("repeat", 100),),
        },
        "medium": {
            "ATTACK": (("heavy", 40), ("pressure", 35), ("feint", 25)),
            "BLOCK": (("guard", 65), ("counter", 35)),
            "YAP": (("rant", 65), ("bait", 35)),
            "ANALYZE": (("repeat", 100),),
        },
        "hard": {
            "ATTACK": (("heavy", 34), ("pressure", 31), ("feint", 35)),
            "BLOCK": (("guard", 50), ("counter", 50)),
            "YAP": (("rant", 55), ("bait", 45)),
            "ANALYZE": (("repeat", 100),),
        },
    }

    MOG_TUTORIAL = (
        {
            "forcedIntent": "ATTACK",
            "forcedVariant": "heavy",
            "allowedHint": "frame",
            "coachLine": "I'm about to hit hard. Brace.",
        },
        {
            "forcedIntent": "BLOCK",
            "forcedVariant": "guard",
            "allowedHint": "cringe",
            "coachLine": "I'm closing up. Say something permanent.",
        },
        {
            "forcedIntent": "YAP",
            "forcedVariant": "rant",
            "allowedHint": "mew",
            "coachLine": "I'm about to talk. Seal the mouth.",
        },
    )

    MOG_BATTLE_CONFIGS = {
        "kai_tutorial": {
            "title": "FIRST CONTACT",
            "enemy_name": "COACH KAI",
            "enemy_short": "KAI",
            "enemy_asset": None,
            "enemy_crop": None,
            "enemy_hp": 100,
            "player_hp": 100,
            "tutorial": MOG_TUTORIAL,
            "tutorial_rounds": 3,
            "sparring": True,
            "stop_at": 0,
            "intent_weights": (("ATTACK", 40), ("BLOCK", 30), ("YAP", 30)),
            "fake_chance": 0,
            "double_tell": False,
            "variant_profile": "basic",
            "adapt_after": 0,
            "phase_thresholds": (),
            "attack_damage": 22,
            "yap_damage": 12,
            "feint_damage": 14,
            "counter_damage": 6,
            "bait_damage": 3,
            "bait_heal": 4,
            "attack_names": ("PLATE SLAM", "Chest Bump", "Lift Different"),
        },
        "kai_graduation": {
            "title": "GRADUATION SPAR",
            "enemy_name": "COACH KAI",
            "enemy_short": "KAI",
            "enemy_asset": None,
            "enemy_crop": None,
            "enemy_hp": 110,
            "player_hp": 100,
            "tutorial": (),
            "tutorial_rounds": 0,
            "sparring": False,
            "stop_at": 0,
            "intent_weights": (("ATTACK", 40), ("BLOCK", 30), ("YAP", 30)),
            "fake_chance": 0,
            "double_tell": False,
            "variant_profile": "basic",
            "adapt_after": 3,
            "phase_thresholds": (0.50,),
            "attack_damage": 23,
            "yap_damage": 13,
            "feint_damage": 16,
            "counter_damage": 8,
            "bait_damage": 4,
            "bait_heal": 6,
            "attack_names": ("PLATE SLAM", "Chest Bump", "Lift Different"),
        },
        "brayden": {
            "title": "HALLWAY TITLE MATCH",
            "enemy_name": "BRAYDEN",
            "enemy_short": "B",
            "enemy_asset": "images/characters/brayden/brayden smirk.png",
            "enemy_crop": (500, 0, 380, 520),
            "enemy_hp": 125,
            "player_hp": 100,
            "tutorial": (),
            "tutorial_rounds": 0,
            "sparring": False,
            "stop_at": 0,
            "intent_weights": (("ATTACK", 45), ("BLOCK", 30), ("YAP", 25)),
            "fake_chance": 0,
            "double_tell": False,
            "variant_profile": "medium",
            "adapt_after": 2,
            "phase_thresholds": (0.60,),
            "attack_damage": 27,
            "yap_damage": 15,
            "feint_damage": 28,
            "counter_damage": 20,
            "bait_damage": 12,
            "bait_heal": 12,
            "attack_names": ("VARSITY CHECK", "Tray Drive", "Public Ratio"),
        },
        "clav": {
            "title": "FINAL EXAM",
            "enemy_name": "CLAV",
            "enemy_short": "C",
            "enemy_asset": "images/characters/clav/clav stern.png",
            "enemy_crop": (470, 0, 340, 540),
            "enemy_hp": 150,
            "player_hp": 100,
            "tutorial": (),
            "tutorial_rounds": 0,
            "sparring": False,
            "stop_at": 0,
            "intent_weights": (("ATTACK", 30), ("BLOCK", 25), ("YAP", 25), ("ANALYZE", 20)),
            "fake_chance": 0,
            "double_tell": True,
            "variant_profile": "hard",
            "adapt_after": 2,
            "phase_thresholds": (0.65, 0.30),
            "attack_damage": 31,
            "yap_damage": 18,
            "feint_damage": 36,
            "counter_damage": 25,
            "bait_damage": 14,
            "bait_heal": 16,
            "attack_names": ("MIRROR TEST", "Measured Disappointment", "Curriculum Correction"),
        },
    }

    def _mog_weighted_pick(weighted):
        total = sum(item[1] for item in weighted)
        roll = renpy.random.randrange(total)
        for value, weight in weighted:
            if roll < weight:
                return value
            roll -= weight
        return weighted[-1][0]

    def _mog_play_cue(path, volume=1.0, channel="battle_sfx"):
        if renpy.loader.loadable(path):
            renpy.music.play(
                path,
                channel=channel,
                loop=False,
                relative_volume=persistent.vol_sfx * volume,
            )

    def _mog_variant_profile(state):
        battle_id = state["battle_id"]
        boss_phase = state.get("boss_phase", 1)
        if battle_id == "kai_graduation" and boss_phase >= 2:
            return "basic_plus"
        if battle_id == "brayden":
            return "medium" if boss_phase >= 2 else "basic_plus"
        if battle_id == "clav":
            return "hard" if boss_phase >= 2 else "medium"
        return state["config"]["variant_profile"]

    def _mog_adapt_after(state):
        configured = state["config"].get("adapt_after", 0)
        if state["battle_id"] == "brayden" and state.get("boss_phase", 1) == 1:
            return max(3, configured)
        return configured

    def _mog_repeated_move(state):
        count = _mog_adapt_after(state)
        history = state.get("move_history", [])
        if not count or len(history) < count:
            return None
        recent = history[-count:]
        if all(move == recent[0] for move in recent):
            return recent[0]
        return None

    def pickIntent(state, forced=None, forced_variant=None):
        intent = forced or _mog_weighted_pick(state["config"]["intent_weights"])
        profile = _mog_variant_profile(state)
        variant = forced_variant or _mog_weighted_pick(MOG_VARIANT_POOLS[profile][intent])
        return {
            "shown": intent,
            "actual": intent,
            "fake": False,
            "variant": variant,
            "variant_data": MOG_VARIANTS[variant],
            "tell": renpy.random.choice(MOG_VARIANTS[variant]["tells"]),
        }

    def say(state, text):
        state["message"] = text

    def _mog_tutorial_step(state):
        tutorial = state["config"]["tutorial"]
        index = state["round"] - 1
        if index < len(tutorial):
            return tutorial[index]
        return None

    def _mog_intent_for_round(state):
        tutorial_step = _mog_tutorial_step(state)
        repeated_move = None if tutorial_step else _mog_repeated_move(state)
        state["adapt_target"] = repeated_move

        if tutorial_step:
            state["intent"] = pickIntent(
                state,
                tutorial_step["forcedIntent"],
                tutorial_step["forcedVariant"],
            )
        elif repeated_move:
            state["intent"] = pickIntent(state, "ANALYZE", "repeat")
        elif state["config"]["double_tell"] and state.get("next_intent"):
            state["intent"] = state["next_intent"]
        else:
            state["intent"] = pickIntent(state)

        if state["config"]["double_tell"]:
            state["next_intent"] = pickIntent(state)
        else:
            state["next_intent"] = None
        state["intent_serial"] += 1

    def start_mog_battle(battle_id):
        global mog_battle
        config = dict(MOG_BATTLE_CONFIGS[battle_id])
        mog_battle = {
            "battle_id": battle_id,
            "config": config,
            "player_hp": config["player_hp"],
            "player_max_hp": config["player_hp"],
            "enemy_hp": config["enemy_hp"],
            "enemy_max_hp": config["enemy_hp"],
            "guard": False,
            "off_balance": False,
            "mewing": False,
            "sealed": False,
            "seal_next": False,
            "cringe_stacks": 0,
            "momentum": 0,
            "mew_cooldown": 0,
            "move_history": [],
            "move_usage": dict((move_id, 0) for move_id in MOG_MOVES),
            "adapt_target": None,
            "boss_phase": 1,
            "locked_move": None,
            "locked_rounds": 0,
            "phase_shift": None,
            "low_health_warned": False,
            "intent": None,
            "next_intent": None,
            "intent_serial": 0,
            "round": 1,
            "phase": "player",
            "selected_move": None,
            "previous_move": None,
            "message": "Read the intent. Answer it.",
            "impact": None,
            "result": None,
        }
        _mog_intent_for_round(mog_battle)
        tutorial_step = _mog_tutorial_step(mog_battle)
        if tutorial_step:
            say(mog_battle, tutorial_step["coachLine"])
        renpy.restart_interaction()

    def _mog_damage(state, target, amount):
        hp_key = "%s_hp" % target
        floor = 1 if state["config"]["sparring"] else 0
        dealt = min(amount, max(0, state[hp_key] - floor))
        state[hp_key] = max(floor, state[hp_key] - amount)
        state["impact"] = target
        if target == "player" and state[hp_key] > 0:
            hp_ratio = state[hp_key] / float(state["player_max_hp"])
            if hp_ratio <= 0.25 and not state["low_health_warned"]:
                state["low_health_warned"] = True
                _mog_play_cue("audio/battle_low_health.mp3", 0.75, "battle_warning")
        return dealt

    def resolvePlayerMove(state, move):
        intent = state["intent"]["actual"]
        variant = state["intent"]["variant"]
        state["selected_move"] = move

        if move == "aura":
            damage = 28 if intent == "YAP" else 8 if intent == "BLOCK" else 30 if variant == "feint" else 18
            giga = state["momentum"] >= 3
            if giga:
                damage += 18
                state["momentum"] = 0
            dealt = _mog_damage(state, "enemy", damage)
            _mog_play_cue("audio/battle_aura_beam.mp3", 0.85)
            if dealt and (intent == "YAP" or variant == "feint" or giga):
                _mog_play_cue("audio/battle_super_effective.mp3", 0.65, "battle_impact")
            giga_text = " GIGA MOMENTUM detonates." if giga else ""
            if intent == "YAP":
                return "Aura Blast catches him mid-inhale.%s (-%d)" % (giga_text, dealt)
            if intent == "BLOCK":
                return "Aura Blast folds against the block.%s (-%d)" % (giga_text, dealt)
            if variant == "feint":
                return "You call the feint and blast the opening.%s (-%d)" % (giga_text, dealt)
            return "Aura Blast lands without discussion.%s (-%d)" % (giga_text, dealt)

        if move == "frame":
            if intent == "ATTACK" and variant != "feint":
                state["guard"] = True
                state["momentum"] = min(3, state["momentum"] + 1)
                dealt = _mog_damage(state, "enemy", 6)
                _mog_play_cue("audio/battle_block_scan.mp3", 0.8)
                return "Perfect frame. The impact feeds Momentum %d/3. Riposte (-%d)" % (state["momentum"], dealt)
            if variant == "feint":
                state["off_balance"] = True
                return "You brace early. He sees your weight commit."
            return "You hold frame against a threat that never arrives."

        if move == "cringe":
            cringe_line = renpy.random.choice(MOG_CRINGE_LINES)
            stacks_added = 2 if intent == "BLOCK" else 1
            state["cringe_stacks"] += stacks_added
            dealt = _mog_damage(state, "enemy", 4)
            _mog_play_cue("audio/battle_cringe.mp3", 0.9)
            if state["cringe_stacks"] >= 3:
                burst = _mog_damage(state, "enemy", 26)
                state["cringe_stacks"] = 0
                return "\"%s\" Third Cringe detonates. (-%d)" % (cringe_line, dealt + burst)
            if intent == "BLOCK":
                return "\"%s\" Bypasses guard. Cringe %d/3. (-%d)" % (cringe_line, state["cringe_stacks"], dealt)
            return "\"%s\" Cringe %d/3. (-%d)" % (cringe_line, state["cringe_stacks"], dealt)

        if move == "mew":
            state["mewing"] = True
            state["mew_cooldown"] = 2
            heal_amount = 12 if intent == "YAP" and variant == "rant" else 8
            healed = min(heal_amount, state["player_max_hp"] - state["player_hp"])
            state["player_hp"] += healed
            if healed:
                renpy.music.stop(channel="battle_warning", fadeout=0.15)
                _mog_play_cue("audio/battle_health_recharge.mp3", 0.85)
                return "You seal your mouth and recover composure. (+%d, cooldown 2)" % healed
            return "You seal your mouth at maximum structural integrity."

        return "Nothing happens. This is recorded."

    def resolveEnemyTurn(state):
        config = state["config"]
        intent = state["intent"]["actual"]
        variant = state["intent"]["variant"]
        enemy_name = config["enemy_name"].title()

        if intent == "ATTACK":
            attack_name = renpy.random.choice(config["attack_names"])
            if variant == "feint":
                amount = config["feint_damage"] if state["off_balance"] else 8
                dealt = _mog_damage(state, "player", amount)
                if state["off_balance"]:
                    return "The feint pulls you out of frame, then snaps back. (-%d)" % dealt
                return "The feint finds no commitment and only grazes you. (-%d)" % dealt

            amount = 7 if state["guard"] else config["attack_damage"]
            if variant == "pressure" and not state["guard"]:
                amount = max(1, amount - 5)
                if state["momentum"]:
                    state["momentum"] -= 1
                    momentum_text = " Momentum drops to %d/3." % state["momentum"]
                else:
                    momentum_text = ""
            else:
                momentum_text = ""
            dealt = _mog_damage(state, "player", amount)
            if state["guard"]:
                return "%s hits the frame and loses most of its meaning. (-%d)" % (attack_name, dealt)
            return "%s lands at full institutional force. (-%d)%s" % (attack_name, dealt, momentum_text)

        if intent == "BLOCK":
            if variant == "counter" and state["selected_move"] in ("aura", "cringe"):
                dealt = _mog_damage(state, "player", config["counter_damage"])
                return "%s catches the aggressive answer and sends it back. (-%d)" % (enemy_name, dealt)
            if variant == "counter":
                return "%s waits to counter a swing that never comes." % enemy_name
            return "%s walls up and absorbs the exchange." % enemy_name

        if intent == "YAP":
            if variant == "bait":
                if state["mewing"]:
                    healed = min(config["bait_heal"], state["enemy_max_hp"] - state["enemy_hp"])
                    state["enemy_hp"] += healed
                    dealt = _mog_damage(state, "player", config["bait_damage"])
                    return "The silence was bait. Your Mew gives %s room to reset. (enemy +%d, you -%d)" % (enemy_name, healed, dealt)
                if state["selected_move"] == "aura":
                    return "You refuse the rehearsed silence and blast the opening. The bait fails."
                dealt = _mog_damage(state, "player", max(6, config["yap_damage"] - 6))
                return "The bait turns into a short jab at your composure. (-%d)" % dealt
            if state["mewing"]:
                return "The rant washes over your sealed silence and does nothing."
            dealt = _mog_damage(state, "player", config["yap_damage"])
            return "His training split becomes psychically painful. (-%d)" % dealt

        if intent == "ANALYZE":
            if state["adapt_target"] and state["selected_move"] == state["adapt_target"]:
                adapt_damage = 18 if state["battle_id"] == "kai_graduation" else 23 if state["battle_id"] == "brayden" else 28
                dealt = _mog_damage(state, "player", adapt_damage)
                return "%s predicts the repetition before you finish it. (-%d)" % (enemy_name, dealt)
            return "%s reads the old pattern, but you give a new answer." % enemy_name

        return "The opponent does nothing with unusual confidence."

    def checkEnd(state):
        if state["enemy_hp"] <= state["config"]["stop_at"]:
            return "win"
        if state["player_hp"] <= 0:
            return "loss"
        if state["config"]["tutorial_rounds"] and state["round"] >= state["config"]["tutorial_rounds"]:
            return "tutorial"
        return None

    def _mog_finish(state, outcome):
        global mog_battle_aura_kept, mog_battle_last_result
        renpy.music.stop(channel="battle_warning", fadeout=0.2)
        state["phase"] = "complete"
        kept = max(0, state["player_hp"])
        result = {
            "battle_id": state["battle_id"],
            "outcome": outcome,
            "aura_kept": kept,
            "rounds": state["round"],
        }
        state["result"] = result
        mog_battle_aura_kept = kept
        mog_battle_last_result = result
        state["impact"] = None
        if outcome == "loss":
            say(state, "Your frame collapses. The lesson remains available.")
        elif outcome == "tutorial":
            say(state, "Three reads confirmed. Training protocol complete.")
        else:
            say(state, "%s breaks eye contact first." % state["config"]["enemy_name"].title())

    def _mog_phase_for_hp(state):
        ratio = state["enemy_hp"] / float(state["enemy_max_hp"])
        phase = 1
        for threshold in state["config"].get("phase_thresholds", ()):
            if ratio <= threshold:
                phase += 1
        return phase

    def _mog_most_used_move(state):
        highest = max(state["move_usage"].values())
        if highest <= 0:
            return None
        return next(move_id for move_id in MOG_MOVES if state["move_usage"][move_id] == highest)

    def _mog_update_boss_phase(state):
        new_phase = _mog_phase_for_hp(state)
        if new_phase <= state["boss_phase"]:
            return None

        state["boss_phase"] = new_phase
        if state["battle_id"] == "kai_graduation":
            return "PHASE 2 // Kai adds feints and counters. Read the specific tell."
        if state["battle_id"] == "brayden":
            return "PHASE 2 // Brayden speeds up and adapts after two repeats."
        if state["battle_id"] == "clav" and new_phase >= 3:
            state["locked_move"] = _mog_most_used_move(state)
            state["locked_rounds"] = 1 if state["locked_move"] else 0
            move_name = MOG_MOVES[state["locked_move"]]["name"] if state["locked_move"] else "your favorite move"
            return "FINAL PHASE // Clav bans %s for one turn." % move_name
        if state["battle_id"] == "clav":
            return "PHASE 2 // Clav stops teaching and starts countering."
        return "The opponent changes cadence."

    def _mog_end_round(state):
        outcome = checkEnd(state)
        if outcome:
            _mog_finish(state, outcome)
            return

        state["previous_move"] = state["selected_move"]
        state["round"] += 1
        state["guard"] = False
        state["off_balance"] = False
        state["mewing"] = False
        state["sealed"] = False
        state["seal_next"] = False
        if state["selected_move"] != "mew" and state["mew_cooldown"]:
            state["mew_cooldown"] -= 1
        if state["locked_rounds"]:
            state["locked_rounds"] -= 1
            if not state["locked_rounds"]:
                state["locked_move"] = None
        state["selected_move"] = None

        phase_message = _mog_update_boss_phase(state)
        _mog_intent_for_round(state)

        state["phase"] = "player"
        tutorial_step = _mog_tutorial_step(state)
        if tutorial_step:
            say(state, tutorial_step["coachLine"])
        elif state["round"] == 4 and state["config"]["tutorial"]:
            say(state, "No more hints. Read the icon. Answer it.")
        elif phase_message:
            say(state, phase_message)
        elif state["intent"]["actual"] == "ANALYZE" and state["adapt_target"]:
            say(state, "PATTERN READ // Switch away from %s." % MOG_MOVES[state["adapt_target"]]["name"])
        else:
            say(state, "The next intent locks in.")

    def _mog_move_locked_reason(state, move):
        if state.get("sealed") and MOG_MOVES[move]["verbal"]:
            return "SEALED"
        if move == "mew" and state.get("mew_cooldown", 0):
            return "COOLDOWN %d" % state["mew_cooldown"]
        if move == state.get("locked_move") and state.get("locked_rounds", 0):
            return "BANNED BY CLAV"
        return None

    def _mog_choose(move):
        state = mog_battle
        if state.get("phase") != "player":
            return
        if _mog_move_locked_reason(state, move):
            return
        state["move_history"].append(move)
        state["move_usage"][move] += 1
        state["phase"] = "player_result"
        say(state, resolvePlayerMove(state, move))
        renpy.music.play("audio/ui_click.ogg", channel="sound", loop=False)
        renpy.restart_interaction()

    def _mog_advance():
        state = mog_battle
        phase = state.get("phase")

        if phase == "player_result":
            outcome = checkEnd(state)
            if outcome and outcome != "tutorial":
                _mog_finish(state, outcome)
            else:
                state["phase"] = "enemy_result"
                say(state, resolveEnemyTurn(state))

        elif phase == "enemy_result":
            outcome = checkEnd(state)
            if outcome:
                _mog_finish(state, outcome)
            else:
                _mog_end_round(state)

        elif phase == "status_result":
            _mog_end_round(state)

        renpy.restart_interaction()

    def _mog_clear_impact():
        if mog_battle:
            mog_battle["impact"] = None
            renpy.restart_interaction()

    def _mog_retry():
        start_mog_battle(mog_battle["battle_id"])

    def _mog_hp_color(value, maximum):
        ratio = float(value) / maximum
        if ratio > 0.55:
            return "#20ad83"
        if ratio > 0.25:
            return "#d39a31"
        return "#d94d4d"

    def _mog_statuses(state, target):
        tags = []
        if target == "enemy" and state["cringe_stacks"]:
            tags.append(("CRINGE x%d" % state["cringe_stacks"], "#d45122"))
        if target == "player":
            tags.append(("MOMENTUM %d/3" % state["momentum"], "#f0b84a" if state["momentum"] < 3 else "#69e4ad"))
            if state["guard"]:
                tags.append(("FRAMED UP", "#23a57c"))
            if state["mewing"]:
                tags.append(("MEWING", "#13a88a"))
            elif state["mew_cooldown"]:
                tags.append(("MEW CD %d" % state["mew_cooldown"], "#68736e"))
            if state["locked_move"]:
                tags.append(("BANNED: %s" % MOG_MOVES[state["locked_move"]]["name"].upper(), "#9a65d1"))
        return tags

    def _mog_move_description(state, move_id, locked_reason=None):
        if locked_reason:
            return locked_reason
        if move_id == "aura" and state["momentum"] >= 3:
            return "GIGA READY // Spend 3 Momentum for +18."
        if move_id == "frame":
            return "Counter committed attacks. Build Momentum."
        if move_id == "cringe":
            return "Cringe %d/3 // +2 vs guard. Third detonates." % state["cringe_stacks"]
        if move_id == "mew":
            return "Silence rants + heal. Bait punishes it."
        return MOG_MOVES[move_id]["description"]


transform mog_intent_pop:
    zoom 0.88
    alpha 0.5
    easeout 0.18 zoom 1.0 alpha 1.0


transform mog_hit_shake:
    xoffset 0
    linear 0.04 xoffset -9
    linear 0.04 xoffset 8
    linear 0.04 xoffset -5
    linear 0.04 xoffset 0


transform mog_hint_pulse:
    alpha 0.55
    linear 0.55 alpha 1.0
    linear 0.55 alpha 0.55
    repeat


transform mog_turn_drop:
    yoffset -18
    alpha 0.0
    easeout 0.22 yoffset 0 alpha 1.0


screen mog_battle_legacy_screen():
    modal True

    on "show" action SetVariable("quick_menu", False)
    on "hide" action SetVariable("quick_menu", True)

    $ state = mog_battle
    $ config = state["config"]
    $ phase = state["phase"]
    $ player_turn = phase == "player"
    $ player_active = phase in ("player", "player_result")
    $ enemy_active = phase in ("enemy_result", "status_result")
    $ intent_name = state["intent"]["shown"]
    $ intent_data = MOG_INTENTS[intent_name]
    $ variant_data = state["intent"]["variant_data"]
    $ tutorial_step = _mog_tutorial_step(state)
    $ explicit_telegraph = state["battle_id"] in ("kai_tutorial", "kai_graduation")
    $ hint_move = tutorial_step["allowedHint"] if tutorial_step and player_turn else None
    $ turn_color = "#6657d9" if player_active else "#d94d4d" if enemy_active else "#23a57c"
    $ player_ratio = state["player_hp"] / float(state["player_max_hp"])
    $ enemy_ratio = state["enemy_hp"] / float(state["enemy_max_hp"])

    add "bg ch2_gym"
    add Solid("#050807dc")
    add Solid("#443a9d20"):
        ypos 70
        xysize (640, 350)
    add Solid(intent_data["color"] + "16"):
        xpos 640
        ypos 70
        xysize (640, 350)

    add Solid("#6657d9"):
        ypos 70
        xysize (640, 3)
    add Solid(intent_data["color"]):
        xpos 640
        ypos 70
        xysize (640, 3)

    for arena_line in range(1, 8):
        add Solid("#dfe5e008"):
            xpos (arena_line * 160)
            ypos 73
            xysize (1, 347)

    if phase in ("player_result", "enemy_result", "status_result"):
        $ result_hold = 1.6 if phase == "player_result" else 1.35
        timer result_hold repeat True action Function(_mog_advance)

    if state["impact"]:
        timer 0.22 action Function(_mog_clear_impact)

    add Solid("#111413f5"):
        xysize (1280, 70)

    add Solid(turn_color):
        ypos 67
        xysize (1280, 3)

    text ("ROUND %d" % state["round"]):
        xpos 42
        yalign 0.048
        size 20
        color "#b7bdb9"
        bold True

    hbox:
        xpos 42
        ypos 61
        spacing 4
        for round_pip in range(5):
            add Solid(turn_color if round_pip < min(5, state["round"]) else "#343a37"):
                xysize (20, 3)

    frame:
        xalign 0.5
        ypos 14
        xysize (430, 44)
        background Solid("#edeaff" if player_active else "#4e2424" if enemy_active else "#173b2d")
        padding (12, 7)
        at mog_turn_drop

        text ("YOUR TURN - PICK A MOVE" if player_active else "ENEMY'S TURN" if enemy_active else "COMPLETE"):
            xalign 0.5
            yalign 0.5
            size 20
            color ("#3f3597" if player_active else "#ffffff")
            bold True

    text config["title"]:
        xpos 1234
        xanchor 1.0
        yalign 0.047
        size 15
        color "#8f9993"
        bold True

    text ("PHASE %d" % state["boss_phase"]):
        xpos 1074
        xanchor 1.0
        yalign 0.047
        size 12
        color variant_data["color"]
        bold True

    # Enemy field.
    fixed:
        xpos 642
        ypos 88
        xysize (580, 295)
        at (mog_hit_shake if state["impact"] == "enemy" else Transform())

        if state["impact"] == "enemy":
            add Solid("#ff49332b"):
                xpos -12
                ypos -10
                xysize (592, 290)

        text config["enemy_name"]:
            xpos 0
            ypos 0
            size 27
            color "#f1f2f1"
            bold True

        text "OPPONENT // AURA":
            xpos 0
            ypos 29
            size 10
            color intent_data["color"]
            bold True

        text ("%d / %d" % (state["enemy_hp"], state["enemy_max_hp"])):
            xpos 485
            ypos 8
            xanchor 1.0
            size 14
            color "#b7bdb9"

        add Solid("#28302c"):
            xpos 0
            ypos 40
            xysize (485, 14)

        add Solid(_mog_hp_color(state["enemy_hp"], state["enemy_max_hp"])):
            xpos 0
            ypos 40
            xysize (int(485 * state["enemy_hp"] / float(state["enemy_max_hp"])), 14)

        for hp_cut in range(1, 10):
            add Solid("#070a09"):
                xpos (hp_cut * 48)
                ypos 40
                xysize (3, 14)

        hbox:
            xpos 0
            ypos 62
            spacing 7
            for tag, tag_color in _mog_statuses(state, "enemy"):
                frame:
                    background Solid(tag_color + "44")
                    padding (8, 3)
                    text tag size 11 color tag_color bold True

        fixed:
            xpos 352
            ypos 76
            xysize (208, 202)
            at Transform(alpha=(1.0 if enemy_active or phase == "complete" else 0.45))
            add Solid(intent_data["color"])
            add Solid("#0b0f0d"):
                xpos 4
                ypos 4
                xysize (200, 194)

            if config["enemy_asset"]:
                add Transform(config["enemy_asset"], crop=config["enemy_crop"], xysize=(196, 190), fit="contain"):
                    xpos 6
                    ypos 6
            else:
                add Solid(intent_data["color"] + "1f"):
                    xpos 6
                    ypos 6
                    xysize (196, 190)
                text config["enemy_short"]:
                    xalign 0.5
                    yalign 0.46
                    size 68
                    color "#d4d6d5"
                    bold True
                text "TRAINER":
                    xalign 0.5
                    ypos 153
                    size 11
                    color intent_data["color"]
                    bold True

        frame:
            xpos 20
            ypos 112
            xysize (320, 108)
            background Solid(intent_data["color"] + "28")
            padding (14, 9)
            at mog_intent_pop

            fixed:
                add Solid(intent_data["color"]):
                    xysize (6, 90)
                text ("TRAINING TELEGRAPH" if explicit_telegraph else "READ THE BODY"):
                    xpos 20
                    ypos 2
                    size 11
                    color "#aeb5b1"
                    bold True
                if explicit_telegraph:
                    text intent_data["mark"]:
                        xpos 20
                        ypos 21
                        size 38
                        color intent_data["color"]
                        bold True
                    text intent_name:
                        xpos 67
                        ypos 30
                        size 25
                        color "#f2f4f3"
                        bold True
                    text variant_data["label"]:
                        xpos 68
                        ypos 60
                        size 10
                        color variant_data["color"]
                        bold True
                    text variant_data["clue"]:
                        xpos 127
                        ypos 59
                        xmaximum 168
                        size 9
                        color "#c0c6c2"
                    if hint_move:
                        text ("COACH READ: %s" % MOG_MOVES[hint_move]["name"].upper()):
                            xpos 68
                            ypos 79
                            size 10
                            color "#69e4ad"
                            bold True
                    else:
                        text "LEARN THE TELL // CHOOSE THE ANSWER":
                            xpos 68
                            ypos 79
                            size 9
                            color "#9da5a0"
                            bold True
                else:
                    text state["intent"]["tell"]:
                        xpos 20
                        ypos 25
                        xmaximum 272
                        size 16
                        color "#f2f4f3"
                        bold True
                    text "NO ICON // INFER THE INTENT":
                        xpos 20
                        ypos 80
                        size 9
                        color variant_data["color"]
                        bold True

        if state["next_intent"]:
            $ preview_name = state["next_intent"]["shown"]
            $ preview_data = MOG_INTENTS[preview_name]
            $ preview_variant = state["next_intent"]["variant_data"]
            frame:
                xpos 20
                ypos 228
                xysize (320, 45)
                background Solid("#171a19")
                padding (10, 6)
                hbox:
                    xalign 0.5
                    spacing 8
                    text "THEN:" size 13 color "#707773" bold True
                    text state["next_intent"]["tell"]:
                        xmaximum 245
                        size 9
                        color preview_variant["color"]
                        bold True

    # Player field.
    fixed:
        xpos 58
        ypos 205
        xysize (565, 215)
        at (mog_hit_shake if state["impact"] == "player" else Transform())

        if state["impact"] == "player":
            add Solid("#ff49332b"):
                xpos -12
                ypos -12
                xysize (590, 220)

        fixed:
            xpos 0
            ypos 0
            xysize (166, 140)
            clipping True
            at Transform(alpha=(1.0 if player_active or phase == "complete" else 0.45))
            add Solid("#6657d9")
            add Solid("#090d0b"):
                xpos 4
                ypos 4
                xysize (158, 132)
            add Transform("images/minigames/acne_face.png", crop=(460, 135, 360, 360), xysize=(154, 128), fit="cover"):
                xpos 6
                ypos 6
            add Solid("#6657d929"):
                xpos 6
                ypos 6
                xysize (154, 128)
            text "FACELESS":
                xpos 10
                ypos 111
                size 10
                color "#d9d5ff"
                bold True

        text "YOU":
            xpos 0
            ypos 140
            size 25
            color "#f1f2f1"
            bold True

        text "PLAYER // AURA":
            xpos 78
            ypos 151
            size 10
            color "#9d93ff"
            bold True

        text ("%d / %d" % (state["player_hp"], state["player_max_hp"])):
            xpos 560
            ypos 146
            xanchor 1.0
            size 14
            color "#b7bdb9"

        add Solid("#28302c"):
            xpos 0
            ypos 178
            xysize (560, 14)

        add Solid(_mog_hp_color(state["player_hp"], state["player_max_hp"])):
            xpos 0
            ypos 178
            xysize (int(560 * state["player_hp"] / float(state["player_max_hp"])), 14)

        for hp_cut in range(1, 10):
            add Solid("#070a09"):
                xpos (hp_cut * 56)
                ypos 178
                xysize (3, 14)

        hbox:
            xpos 0
            ypos 198
            spacing 7
            for tag, tag_color in _mog_statuses(state, "player"):
                frame:
                    background Solid(tag_color + "44")
                    padding (8, 3)
                    text tag size 11 color tag_color bold True

    frame:
        xpos 58
        ypos 432
        xysize (1164, 68)
        background Solid("#2a2d2bf2")
        padding (22, 15)

        add Solid(turn_color):
            xysize (7, 38)

        text state["message"]:
            xpos 18
            yalign 0.5
            size 19
            color "#f0f1f0"
            bold True

    # Move grid.
    grid 2 2:
        xpos 58
        ypos 514
        xspacing 14
        yspacing 10

        for move_id in ("aura", "frame", "cringe", "mew"):
            $ move = MOG_MOVES[move_id]
            $ locked_reason = _mog_move_locked_reason(state, move_id)
            $ move_locked = locked_reason is not None
            $ move_enabled = player_turn and not move_locked
            $ move_description = _mog_move_description(state, move_id, locked_reason)
            $ hinted = move_id == hint_move

            button:
                xysize (575, 88)
                background Solid(move["color"] + "32" if hinted or state.get("selected_move") == move_id else move["color"] + "16")
                hover_background Solid(move["color"] + "3f")
                insensitive_background Solid(move["color"] + "2b" if state.get("selected_move") == move_id else "#101211")
                padding (18, 11)
                sensitive move_enabled
                action Function(_mog_choose, move_id)
                if hinted:
                    at mog_hint_pulse

                fixed:
                    add Solid(move["color"]):
                        xysize (6, 66)

                    frame:
                        xpos 18
                        ypos 12
                        xysize (42, 42)
                        background Solid(move["color"] + "33")
                        padding (0, 0)
                        text move["mark"]:
                            xalign 0.5
                            yalign 0.5
                            size 22
                            color move["color"]
                            bold True

                    vbox:
                        xpos 76
                        ypos 6
                        spacing 2
                        text move["name"]:
                            size 22
                            color ("#f0f1f0" if move_enabled else "#666b68")
                            bold True
                        text move_description:
                            size 14
                            color ("#69e4ad" if move_id == "aura" and state["momentum"] >= 3 and not move_locked else "#b8bdb9" if move_enabled else "#777d79" if move_locked else "#535754")
                            bold move_locked or (move_id == "aura" and state["momentum"] >= 3)

                    if hinted or state.get("selected_move") == move_id:
                        text ("EXECUTING" if state.get("selected_move") == move_id else "COACH READ"):
                            xpos 454
                            ypos 7
                            size 10
                            color "#69e4ad"
                            bold True

    if phase == "complete":
        add Solid("#050706dc")
        frame:
            xalign 0.5
            yalign 0.5
            xysize (560, 310)
            background Solid("#111614")
            padding (36, 28)

            vbox:
                xalign 0.5
                spacing 12

                text ("FRAME BROKEN" if state["result"]["outcome"] == "loss" else "TRAINING COMPLETE" if state["result"]["outcome"] == "tutorial" else "MOG CONFIRMED"):
                    xalign 0.5
                    size 38
                    color ("#d94d4d" if state["result"]["outcome"] == "loss" else "#69e4ad")
                    bold True

                text state["message"]:
                    xalign 0.5
                    text_align 0.5
                    xmaximum 480
                    size 17
                    color "#cbd0cd"

                text ("AURA KEPT: %d / %d" % (state["result"]["aura_kept"], state["player_max_hp"])):
                    xalign 0.5
                    size 21
                    color "#f0f1f0"
                    bold True

                null height 8

                if state["result"]["outcome"] == "loss":
                    textbutton "TRY AGAIN":
                        xalign 0.5
                        xysize (260, 56)
                        background Solid("#8d3636")
                        hover_background Solid("#b34848")
                        text_size 19
                        text_color "#ffffff"
                        text_bold True
                        action Function(_mog_retry)
                else:
                    textbutton "CONTINUE":
                        xalign 0.5
                        xysize (260, 56)
                        background Solid("#19754f")
                        hover_background Solid("#249b69")
                        text_size 19
                        text_color "#ffffff"
                        text_bold True
                        action Return(state["result"])


# Future chapters can call these labels directly while sharing the same engine.
label battle_brayden:
    $ start_mog_battle("brayden")
    $ mog_battle_last_result = renpy.call_screen("mog_battle_screen")
    return


label battle_clav:
    $ start_mog_battle("clav")
    $ mog_battle_last_result = renpy.call_screen("mog_battle_screen")
    return
