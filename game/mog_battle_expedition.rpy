# MOGMAX battle system — port of the mogmaxxing.html prototype (v6.5) gameplay loop.
#
# Preserves the public start_mog_battle()/mog_battle_screen contract used by
# Chapter 2, and the game's existing battle audio. Everything else follows the
# prototype: Aura economy (0-7 bolts), Mog Meter gains/drains, six skill
# minigames (hold-frame, vocab quiz, J/K mash, timing bar, draw-the-M),
# real timing windows for parry/dodge, red/feint/drain attacks, heal and
# cringe intents, skill timeouts, and the mastery-gated tutorial.

init 2 python:
    MOGX_SKILL_ORDER = ("yap", "looks", "brain", "jester", "sleep", "mogmax")

    MOGX_SKILLS = {
        "yap": {
            "key": "1", "name": "YAP", "icon": "🗣️", "cost": 0,
            "kind": "basic", "color": "#6db1ff",
            "desc": "Free instant jab. Small damage, builds +1 Aura.",
        },
        "looks": {
            "key": "2", "name": "MOG STARE", "icon": "😎", "cost": 4,
            "kind": "looksmaxx", "color": "#ffd75e",
            "desc": "The marker whips back and forth — STRIKE it in the gold. Miss = you blink.",
        },
        "brain": {
            "key": "3", "name": "GALAXY BRAIN", "icon": "🧠", "cost": 2,
            "kind": "brainmaxx", "color": "#c07bff",
            "desc": "Vocab quiz, 9 seconds. Correct = big damage + 1 Aura refund.",
        },
        "jester": {
            "key": "4", "name": "RATIO RUSH", "icon": "🤡", "cost": 5,
            "kind": "jestermaxx", "color": "#f15bb5",
            "desc": "Alternate J and K, fast. 8+ hits Embarrasses them. Full bar = MAX RATIO.",
        },
        "sleep": {
            "key": "5", "name": "POWER NAP", "icon": "😴", "cost": 3,
            "kind": "sleepmaxx", "color": "#5eff9d",
            "desc": "Heal Confidence and cure CRINGE. Perfect timing refunds +1⚡.",
        },
        "mogmax": {
            "key": "6", "name": "MOGMAX", "icon": "👑", "cost": 0,
            "kind": "ultimate", "color": "#ffd75e",
            "desc": "Full Mog Meter only. Draw the M. 4 of 5 circles = BREAK.",
        },
    }

    # Grade-school vocab bank for Galaxy Brain (from the prototype).
    MOGX_WORDS = (
        ("RELUCTANT", "unwilling; hesitant to do something"),
        ("ABUNDANT", "existing in large amounts; plentiful"),
        ("FRAGILE", "easily broken or damaged"),
        ("GENUINE", "real; truly what it seems to be"),
        ("OBSTACLE", "something that blocks your way"),
        ("PREDICT", "to say what will happen before it does"),
        ("VACANT", "empty; not being used"),
        ("WEARY", "very tired"),
        ("BRISK", "quick and full of energy"),
        ("CAUTIOUS", "careful to avoid danger"),
        ("EAGER", "excited and ready to do something"),
        ("FEEBLE", "very weak"),
        ("GLOOMY", "dark, sad, or without hope"),
        ("HASTY", "done too quickly, without thinking"),
        ("IMMENSE", "extremely large; huge"),
        ("JUBILANT", "extremely happy and celebrating"),
        ("LOYAL", "always supporting someone; faithful"),
        ("MIMIC", "to copy how someone acts or speaks"),
        ("NIMBLE", "quick and light in movement"),
        ("TIMID", "shy and easily frightened"),
        ("URGENT", "needing attention right away"),
        ("VIVID", "very bright and clear"),
        ("WANDER", "to move around without a plan"),
        ("DROWSY", "sleepy; almost falling asleep"),
        ("SOAR", "to fly high in the air"),
        ("GRUMBLE", "to complain in a low, unhappy voice"),
        ("SLY", "sneaky and clever"),
        ("DAZZLE", "to amaze someone with brightness or skill"),
    )

    # Enemy kits. Attack "w" is the windup in seconds; impact lands at w
    # (+0.45 for feints). red = unparryable, drain = steals 2 Aura on hit.
    MOGX_KITS = {
        "kai_tutorial": {
            "dmg": 5, "heals": 0, "heal_amt": 0, "cringes": 0, "feint": 0.0,
            "patterns": (({"w": 1.25},), ({"w": 1.25}, {"w": 1.0})),
        },
        # Ram notation: P = parryable, D = red dodge-only, ! = fast (short w),
        # ... = long w on the next hit, ~ = "slow" drift ram, F = feint flag.
        # "heavy" = 1.7x damage with a bigger dive and the heavy punch sound.
        #
        # EASY: 1-3 rams, consistent timing, no feints, D only as finisher.
        "kai_graduation": {
            "dmg": 12, "heals": 1, "heal_amt": 15, "cringes": 1, "feint": 0.0,
            "patterns": (
                ({"w": 1.15},),                                          # P /
                ({"w": 0.95}, {"w": 0.95}),                              # P - P /
                ({"w": 0.95}, {"w": 0.95}, {"w": 0.95}),                 # P - P - P /
                ({"w": 0.95}, {"w": 1.35, "red": True, "heavy": True}),  # P ... D /
                ({"w": 0.95}, {"w": 0.95}, {"w": 1.35, "red": True, "heavy": True}),  # signature P - P ... D /
            ),
        },
        # Brayden: fast but FAIR — every combo has a fixed, learnable rhythm
        # (short-short, short-short-LONG, etc). No dirty tells. His windup is
        # a crouch-and-spring, quicker than Kai's lean.
        "brayden": {
            # MEDIUM: acceleration, delayed rams, D anywhere, no feints.
            "dmg": 17, "heals": 1, "heal_amt": 30, "cringes": 2, "feint": 0.0,
            "patterns": (
                ({"w": 0.9}, {"w": 0.45}),                               # P - !P /
                ({"w": 0.45}, {"w": 1.2}),                               # !P ... P /
                ({"w": 0.9}, {"w": 0.7}, {"w": 0.45}),                   # accelerating triple
                ({"w": 1.0, "red": True, "heavy": True}, {"w": 0.8}, {"w": 0.7}),  # D ... P - P heavy opener
                ({"w": 0.8}, {"w": 0.75, "red": True}, {"w": 0.9}),      # P - D - P
                ({"w": 0.8}, {"w": 0.8}, {"w": 1.35}),                   # P - P ... P delayed final
                ({"w": 0.45}, {"w": 0.45}, {"w": 1.2, "red": True, "heavy": True}),  # !P - !P ... D /
                ({"w": 0.8, "drain": True, "windup": "zigzag"}, {"w": 0.62}),  # aura-drain juke
            ),
        },
        # Clav: fast AND a little unfair — "late" hits flash the tell only a
        # blink before impact, and phase-2 "notell" hits never flash at all.
        # His windup barely moves: the glow is most of the warning you get.
        "clav": {
            # HARD: stutters, slow rams, feints, D with fast follow-ups,
            # shared openers with different endings.
            "dmg": 18, "heals": 2, "heal_amt": 35, "cringes": 3, "feint": 0.0,
            "patterns": (
                ({"w": 1.3}, {"w": 0.7}, {"w": 0.45}),                   # P ... P - !P delayed triple
                ({"w": 0.45}, {"w": 0.45}, {"w": 1.0, "slow": True}),    # !P - !P ... ~P
                ({"w": 1.0, "slow": True, "windup": "spin"}, {"w": 0.45}),  # ~P - !P
                ({"w": 0.95, "red": True, "heavy": True}, {"w": 0.45}),  # D - !P wall rebound
                ({"w": 0.7}, {"w": 0.7}, {"w": 1.2, "red": True, "heavy": True}, {"w": 0.45}),  # P - P ... D - !P
                ({"w": 1.15, "feint": True},),                           # F ... P
                ({"w": 0.7, "drain": True, "windup": "spin"}, {"w": 0.55}),
            ),
            "phase2": {
                "dmg": 21, "feint": 0.0,
                "patterns": (
                    # shared opener P - P, three endings:
                    ({"w": 0.7}, {"w": 0.7}, {"w": 1.25, "red": True, "heavy": True}),   # A: delayed heavy D
                    ({"w": 0.7}, {"w": 0.7}, {"w": 0.45}, {"w": 0.45}),                  # B: two fast rams
                    ({"w": 0.7}, {"w": 0.7}, {"w": 1.0, "slow": True}),                  # C: slow ram
                    ({"w": 1.2}, {"w": 1.2}, {"w": 0.45}),                               # stutter charge
                    ({"w": 1.0, "feint": True, "windup": "spin"}, {"w": 0.95, "red": True, "heavy": True}),  # F ... D
                    ({"w": 0.62, "notell": True}, {"w": 0.5}, {"w": 0.8, "red": True, "heavy": True}),
                    ({"w": 0.55, "late": True}, {"w": 0.5}, {"w": 0.9, "heavy": True}),
                ),
            },
        },
    }

    # Timing windows, in seconds relative to impact (negative = early).
    # The dodge window opens once the dive is visibly close — dodging while
    # the attack is still winding up counts as too early.
    MOGX_PARRY_WIN = (-0.21, 0.11)
    MOGX_PERFECT_WIN = (-0.10, 0.075)
    MOGX_DODGE_WIN = (-0.26, 0.13)

    MOGX_AURA_MAX = 7
    MOGX_MASH_FULL = 14
    MOGX_MASH_DUR = 2.2
    MOGX_HOLD_SWEEP = 0.75   # seconds for the stare marker to cross the bar once
    MOGX_HOLD_TIMEOUT = 3.4  # hesitate too long and you blink anyway
    MOGX_QUIZ_DUR = 9.0
    MOGX_NAP_DUR = 1.15
    MOGX_OSU_WIN = 0.9

    def _mogx_stare_pos(elapsed):
        # Triangle wave: the marker ping-pongs across the bar, fast.
        cyc = (elapsed / MOGX_HOLD_SWEEP) % 2.0
        return cyc if cyc <= 1.0 else 2.0 - cyc

    MOGX_COLORS = {
        "gold": "#ffd75e", "red": "#ff5d6c", "blue": "#6db1ff",
        "green": "#5eff9d", "purp": "#c07bff",
    }

    # ------------------------------------------------------------------
    # Tutorial script. Kinds: dlg / teach / guided / real / free.
    # ------------------------------------------------------------------
    MOGX_TUT = (
        {"do": "dlg", "text": "Locker room. Just us and the timing line. Before you mog anyone in these halls, you learn the {b}fundamentals{/b}."},
        {"do": "dlg", "text": "{b}ATTACKING:{/b} every skill is its own minigame — quizzes, stare-downs, mash-offs. But {b}1 · YAP{/b} 🗣️ is the freebie: instant jab, small damage, builds {b}+1⚡ Aura{/b}. Try it on me."},
        {"do": "teach", "skill": "yap"},
        {"do": "dlg", "text": "See the {b}⚡ bolts{/b} under your Confidence? Yap jabs and parries fill them, skills spend them. {b}Aura is everything.{/b}"},
        {"do": "dlg", "text": "{b}DEFENSE:{/b} when I attack, I {b}glow{/b} — {color=#ff5d6c}{b}RED{/b}{/color} or {color=#ffd75e}{b}YELLOW{/b}{/color} — and the hit lands a beat later. Easiest escape first: press {b}S{/b} to {b}DODGE{/b}. For your first two, I'll {b}freeze time{/b} at the exact moment — just press when I say NOW."},
        {"do": "guided", "kind": "dodge", "reps": 2,
         "mid": "THAT moment. Feel it. One more frozen rep."},
        {"do": "dlg", "text": "Real time now — no freeze. Watch the dive, press {b}S{/b} near impact. Dodges earn nothing by themselves — but take {b}zero hits{/b} from an attack and you bank {b}+1⚡ UNTOUCHED{/b}. {b}Dodge 2 swings.{/b}"},
        {"do": "real", "kind": "dodge", "reps": 2,
         "attack": {"w": 1.4, "red": True}, "rep_dmg": 4,
         "mid": "One. Again.",
         "fail": "Too slow — press {b}S{/b} as the swing lands. One more time."},
        {"do": "dlg", "text": "Dodging keeps you safe — but {b}PARRYING{/b} pays. Press {b}W{/b} with {i}tight{/i} timing at impact: you take nothing, gain {b}+1⚡{/b}, heal {b}+5{/b}, feed the {b}Mog Meter{/b}, and {b}counterattack{/b}. There are no half-parries — you land it or you don't. One rule: a {color=#ff5d6c}{b}RED glow{/b}{/color} can NEVER be parried — only dodged. {color=#ffd75e}{b}YELLOW{/b}{/color} = parry or dodge. Two frozen reps."},
        {"do": "guided", "kind": "parry", "reps": 2,
         "mid": "That's the parry window — tighter than the dodge, better rewards. Again."},
        {"do": "dlg", "text": "Now in real time. Watch the swing, press {b}W{/b} at impact. {b}Land 2 parries.{/b}"},
        {"do": "real", "kind": "parry", "reps": 2,
         "attack": {"w": 1.4}, "rep_dmg": 4,
         "mid": "One. Again.",
         "fail": "Almost. Watch for the {color=#ffd75e}{b}yellow glow{/b}{/color}, then {b}W{/b} {i}right as the swing lands{/i} — not when the glow appears. Again."},
        {"do": "dlg", "text": "CLEAN. 🔥 Parries also {b}restore Confidence{/b} and fill your {b}👑 MOG METER{/b} — landed attacks fill it too, and getting hit or flubbing a minigame {b}drains{/b} it. Full meter lights up {b}6 · MOGMAX{/b}."},
        {"do": "dlg", "text": "BRAIN TIME: press {b}3 · GALAXY BRAIN{/b} 🧠 — it quizzes you with a {b}vocab word{/b}. Answer right for a big-brain blast {b}+ a ⚡ refund{/b}. I'll spot you the Aura."},
        {"do": "teach", "skill": "brain",
         "fail": "Wrong one. No stress — new word, {b}run it back{/b}. You proceed when you get one right."},
        {"do": "dlg", "text": "Now the stare-down: {b}2 · MOG STARE{/b} 😎 — the marker {b}whips back and forth{/b}. Press {b}SPACE{/b} or the {b}STRIKE{/b} button while it's in the {b}gold{/b}. Green still counts. Anywhere else — you blink. This is called {b}holding frame{/b}."},
        {"do": "teach", "skill": "looks",
         "fail": "You {b}blinked{/b}. Watch the rhythm of the marker and strike inside the {b}green or gold{/b}. Again."},
        {"do": "dlg", "text": "Chaos lesson: {b}4 · RATIO RUSH{/b} 🤡 — hammer {b}J{/b} and {b}K{/b}, {b}alternating{/b}, fast as you can. Every press is a hit. Get {b}8+ hits{/b} to pass (that also {b}Embarrasses{/b} your opponent)."},
        {"do": "teach", "skill": "jester",
         "fail": "Not enough hits — need {b}8+{/b}. Alternate faster, don't double-tap the same key. Run it back."},
        {"do": "dlg", "text": "Next one you need to {b}feel{/b}, not hear about. Hold still — this is a {b}CRINGE{/b}."},
        {"do": "cringe_hit"},
        {"do": "dlg", "text": "That. 😬 You're {b}CRINGED{/b}: every attack {b}-35%{/b} and you {b}leak 1⚡ every turn{/b} — and look at your Confidence. It hangs on for {b}three turns{/b}, bosses WILL do this to you, and you {b}can't dodge it{/b}. The fast cure: {b}5 · POWER NAP{/b} 😴 — time the bar into the {b}green or gold{/b} to heal up AND clear it now."},
        {"do": "teach", "skill": "sleep",
         "fail": "Restless sleep — you missed the zone. Watch the marker, SPACE in the green. Again."},
        {"do": "dlg", "text": "Last one. I'm filling your {b}👑 MOG METER{/b}. Press {b}6 · MOGMAX{/b}: the room goes dark and you {b}DRAW THE M{/b} — hit the five circles in order as they light. You pass with {b}4 of 5{/b}."},
        {"do": "teach", "skill": "mogmax",
         "fail": "Sloppy M. Click each circle {b}as it glows{/b}, 1 through 5. I'll refill the meter — again."},
        {"do": "dlg", "text": "FULL KIT TOURED. 📈 One last rule: a used skill goes {b}⏳ ON TIMEOUT{/b} for a turn — no spamming. Rotate your kit. (Yap is always available.)"},
        {"do": "dlg", "text": "Final check. I fight back now — gently. {b}Finish me.{/b}"},
        {"do": "free"},
    )

    def _mogx_audio(path, volume=1.0, channel="battle_sfx"):
        if renpy.loader.loadable(path):
            renpy.music.play(path, channel=channel, loop=False,
                relative_volume=persistent.vol_sfx * volume)

    # All clips are short (≤1.9s) — long source files are pre-trimmed
    # (mogging_short, scan_short, quiz_correct, quiz_wrong).
    MOGX_SFX = {
        "click":   ("audio/ui_click.ogg", 0.55),
        "hit":     ("audio/battle_aura_beam.mp3", 0.5),
        "bighit":  ("audio/mogging_short.mp3", 0.8),
        "perfect": ("audio/battle_super_effective.mp3", 0.75),
        # Lists = variants; each play picks one at random so combos don't
        # sound like a stuck sample.
        "parry":   [("audio/parry_block.mp3", 0.95), ("audio/parry_block2.mp3", 0.95), ("audio/parry_block3.mp3", 0.95)],
        "hurt":    [("audio/punch_impact.mp3", 0.9), ("audio/punch_impact2.mp3", 0.9)],
        "hurt_heavy": ("audio/punch_heavy.mp3", 1.0),
        "whoosh":  [("audio/whoosh_dodge.mp3", 0.85), ("audio/whoosh_dodge2.mp3", 0.85), ("audio/whoosh_dodge3.mp3", 0.85)],
        "heal":    ("audio/battle_health_recharge.mp3", 0.8),
        "mog":     ("audio/mogging_short.mp3", 1.0),
        "miss":    ("audio/quiz_wrong.mp3", 0.7),
        "buff":    ("audio/scan_short.mp3", 0.6),
        "win":     ("audio/mew_complete.mp3", 0.9),
        "tap":     ("audio/typewriter-soft-click.mp3", 0.32),
        "step":    ("audio/mew_step.mp3", 0.8),
        "alert":   ("audio/ui_hover.ogg", 0.8),
        "alert_red": ("audio/alert_danger.mp3", 0.6),
        "quiz_ok": ("audio/quiz_correct.mp3", 0.85),
        "quiz_no": ("audio/quiz_wrong.mp3", 0.7),
    }

    def _mogx_sfx(name, channel="battle_sfx"):
        entry = MOGX_SFX[name]
        if isinstance(entry, list):
            entry = renpy.random.choice(entry)
        path, vol = entry
        _mogx_audio(path, vol, channel)

    # ------------------------------------------------------------------
    # Battle construction
    # ------------------------------------------------------------------
    def start_mog_battle(battle_id):
        global mog_battle
        config = dict(MOG_BATTLE_CONFIGS[battle_id])
        kit = MOGX_KITS[battle_id]
        mog_battle = {
            "battle_id": battle_id,
            "config": config,
            "tutorial": battle_id == "kai_tutorial",
            # Player
            "php": config["player_hp"], "pmax": config["player_hp"],
            "aura": 0, "mog": 0,
            "cringe": False, "var_mult": 1.0,
            "cooldown": None, "pending_cooldown": None,
            "counter": 0,
            # Enemy
            "ehp": config["enemy_hp"], "emax": config["enemy_hp"],
            "edmg": kit["dmg"],
            "heals_left": kit["heals"], "heal_amt": kit["heal_amt"],
            "cringes_left": kit["cringes"], "feint": kit["feint"],
            "patterns": [list(p) for p in kit["patterns"]],
            "last_pat": None, "last_action": None,
            "phase2": dict(kit["phase2"]) if kit.get("phase2") else None,
            "in_phase2": False,
            "stunned": False, "embarrassed": False,
            # Flow
            "phase": "player", "round": 1,
            "selected": None, "allowed": None, "result_delay": 0.85,
            "message": "YOUR TURN // Rotate the kit, build the Mog Meter.",
            "last_grade": None,
            # Enemy attack execution
            "queue": [], "queue_idx": 0, "hit": None,
            "turn_hits": 0, "turn_pdodges": 0, "turn_parries": 0,
            "turn_took_hit": False, "cringe_turns": 0,
            "hit_elapsed": 0.0, "impact_at": 0.0, "alert_at": 0.0,
            "alert_on": False, "alert_played": False,
            "def_result": None, "def_lock": 0.0, "def_pose": None,
            "guided_kind": None, "def_focus": None,
            # Minigame clocks
            "qte_elapsed": 0.0,
            "mash_count": 0, "mash_last": None,
            "quiz": None, "word_bag": [],
            "osu_step": 0, "osu_hits": 0, "osu_clock": 0.0, "osu_results": [],
            # Tutorial interpreter
            "tut_idx": 0, "tut_reps": 0, "tut_free": False,
            "dlg_text": None, "dlg_next": None,
            # Juice
            "ann": None, "ann_age": 0.0, "ann_color": "#ffd75e",
            "floaters": [], "flash": None, "flash_age": 0.0,
            "mog_full_announced": False,
            # Stats
            "stats": {"parries": 0, "perfect_parries": 0, "perfects": 0,
                      "hits_taken": 0, "turns": 0},
            "help": False,
            "result": None,
        }
        if mog_battle["tutorial"]:
            _mogx_tut_run()
        else:
            mog_battle["message"] = "YOUR TURN // Spend Aura, rotate skills, build MOGMAX."
        _mogx_sfx("click")
        renpy.restart_interaction()

    def _mogx_hp_color(value, maximum):
        ratio = max(0.0, float(value) / maximum)
        if ratio > 0.55:
            return "#5eff9d"
        if ratio > 0.25:
            return "#ffd75e"
        return "#ff5d6c"

    # ------------------------------------------------------------------
    # Juice: announcer + floaters + flashes
    # ------------------------------------------------------------------
    def _mogx_announce(text, color="gold"):
        S = mog_battle
        S["ann"] = text
        S["ann_age"] = 0.0
        S["ann_color"] = MOGX_COLORS.get(color, color)

    MOGX_ANCHORS = {
        "enemy": (975, 118),
        "player": (255, 305),
        "hp": (275, 492),
        "aura": (255, 515),
    }

    def _mogx_float(anchor, text, color="gold"):
        S = mog_battle
        x, y = MOGX_ANCHORS[anchor]
        stack = sum(1 for f in S["floaters"] if f["anchor"] == anchor and f["age"] < 0.5)
        S["floaters"].append({
            "anchor": anchor, "text": text,
            "color": MOGX_COLORS.get(color, color),
            "x": x, "y": y - stack * 26, "age": 0.0,
        })

    def _mogx_flash(kind):
        S = mog_battle
        S["flash"] = kind
        S["flash_age"] = 0.0

    # ------------------------------------------------------------------
    # Resource changes
    # ------------------------------------------------------------------
    def _mogx_gain_aura(n):
        S = mog_battle
        S["aura"] = max(0, min(MOGX_AURA_MAX, S["aura"] + n))

    def _mogx_gain_mog(n):
        S = mog_battle
        was = S["mog"]
        S["mog"] = max(0, min(100, S["mog"] + n))
        if was < 100 and S["mog"] >= 100 and not S["mog_full_announced"]:
            S["mog_full_announced"] = True
            _mogx_announce("MOG METER FULL 👑", "gold")
            _mogx_sfx("mog")
        if S["mog"] < 100:
            S["mog_full_announced"] = False

    def _mogx_damage_enemy(amount, color="gold", big=False):
        S = mog_battle
        amount = max(0, int(round(amount)))
        S["ehp"] = max(0, S["ehp"] - amount)
        _mogx_float("enemy", "-%d" % amount, color)
        _mogx_flash("enemy")
        _mogx_sfx("bighit" if big else "hit")
        return amount

    def _mogx_enemy_smirk(amount=6):
        # A flubbed action costs the enemy nothing — they gain Ego off your L.
        S = mog_battle
        healed = min(amount, S["emax"] - S["ehp"])
        if healed > 0:
            S["ehp"] += healed
            _mogx_float("enemy", "+%d EGO 😏" % healed, "green")

    def _mogx_damage_player(amount, heavy=False):
        S = mog_battle
        amount = max(0, int(round(amount)))
        if S["tutorial"]:
            amount = min(amount, max(0, S["php"] - 1))
        S["php"] = max(0, S["php"] - amount)
        S["stats"]["hits_taken"] += 1
        _mogx_gain_mog(-6)
        _mogx_float("player", ("💥 -%d" % amount) if heavy else ("-%d" % amount), "red")
        _mogx_flash("player")
        _mogx_sfx("hurt_heavy" if heavy else "hurt")
        if S["php"] <= S["pmax"] * 0.25:
            _mogx_audio("audio/battle_low_health.mp3", 0.55, "battle_warning")
        return amount

    def _mogx_heal_player(amount):
        S = mog_battle
        healed = min(int(round(amount)), S["pmax"] - S["php"])
        S["php"] += healed
        if healed > 0:
            _mogx_float("hp", "+%d" % healed, "green")
        _mogx_sfx("heal")
        return healed

    # ------------------------------------------------------------------
    # Skill locks / selection
    # ------------------------------------------------------------------
    def _mogx_skill_lock(skill_id):
        S = mog_battle
        skill = MOGX_SKILLS[skill_id]
        if S["phase"] != "player":
            return "WAIT"
        if S["allowed"] is not None and skill_id not in S["allowed"]:
            return "LOCKED"
        if skill_id == "mogmax":
            if S["mog"] < 100:
                return "METER %d%%" % S["mog"]
            return None
        if S["cooldown"] == skill_id:
            return "⏳ TIMEOUT"
        if S["aura"] < skill["cost"]:
            return "NEED %d⚡" % skill["cost"]
        return None

    def _mogx_choose(skill_id):
        S = mog_battle
        if S["phase"] != "player" or _mogx_skill_lock(skill_id):
            return
        skill = MOGX_SKILLS[skill_id]
        S["selected"] = skill_id
        S["aura"] = max(0, S["aura"] - skill["cost"])
        if skill_id not in ("yap", "mogmax"):
            S["pending_cooldown"] = skill_id
        # Cringe weakens EVERY attack while active (Power Nap excluded) and
        # only Power Nap clears it — see the per-turn Aura leak in end_round.
        S["var_mult"] = 1.0
        if S["cringe"] and skill_id != "sleep":
            S["var_mult"] = 0.65
            _mogx_float("player", "😬 -35%", "red")
        S["last_grade"] = None
        S["qte_elapsed"] = 0.0
        S["result_delay"] = 0.85
        _mogx_sfx("click")

        if skill_id == "yap":
            _mogx_resolve_yap()
        elif skill_id == "looks":
            S["phase"] = "hold"
            S["message"] = "MOG STARE 😎 // Strike while the marker is in the gold."
        elif skill_id == "brain":
            _mogx_quiz_start()
        elif skill_id == "jester":
            S["phase"] = "mash"
            S["mash_count"] = 0
            S["mash_last"] = None
            S["message"] = "RATIO RUSH 🤡 // Tap the glowing key. Alternate J and K, fast!"
        elif skill_id == "sleep":
            S["phase"] = "nap"
            S["message"] = "POWER NAP 😴 // SPACE at the sweet spot."
        elif skill_id == "mogmax":
            S["mog"] = 0
            S["phase"] = "mogmax"
            S["osu_step"] = 0
            S["osu_hits"] = 0
            S["osu_clock"] = 0.0
            S["osu_results"] = []
            S["message"] = "DRAW THE M // Hit each circle as it glows, 1 through 5."
            _mogx_announce("👑 M O G M A X 👑", "gold")
            _mogx_sfx("mog")
        renpy.restart_interaction()

    # ------------------------------------------------------------------
    # Skill resolutions
    # ------------------------------------------------------------------
    def _mogx_after_attack(landed, perfects, feeds_meter=True):
        S = mog_battle
        S["stats"]["perfects"] += perfects
        if feeds_meter:
            if perfects:
                _mogx_gain_mog(perfects * 8)
            if landed:
                _mogx_gain_mog(6)
        S["phase"] = "player_result"
        renpy.restart_interaction()

    def _mogx_resolve_yap():
        S = mog_battle
        dmg = 7 * S["var_mult"]
        _mogx_damage_enemy(dmg, "blue")
        _mogx_gain_aura(1)
        _mogx_float("aura", "+1⚡", "gold")
        S["last_grade"] = "good"
        S["message"] = "Yap lands. +1⚡ Aura."
        _mogx_after_attack(True, 0)

    def _mogx_hold_press():
        S = mog_battle
        if S["phase"] != "hold":
            return
        p = _mogx_stare_pos(S["qte_elapsed"])
        if 0.82 <= p <= 0.93:
            grade = "perfect"
        elif 0.55 <= p < 0.82:
            grade = "good"
        else:
            grade = "miss"
        _mogx_resolve_hold(grade)

    def _mogx_resolve_hold(grade):
        S = mog_battle
        S["last_grade"] = grade
        if grade == "miss":
            _mogx_announce("YOU BLINKED ❌", "red")
            _mogx_sfx("miss")
            _mogx_float("enemy", "MISS", "blue")
            _mogx_gain_mog(-5)
            _mogx_enemy_smirk()
            S["message"] = "Sloppy stare. Nothing lands — and their Ego grows."
            _mogx_after_attack(False, 0)
            return
        perfects = 0
        if grade == "perfect":
            base = 32
            perfects = 1
            _mogx_announce("FRAME HELD 😎", "gold")
            _mogx_sfx("perfect", "battle_impact")
        else:
            base = 24
        # The short mogging sting plays on a landed stare — let it finish
        # before the enemy turn starts.
        _mogx_damage_enemy(base * S["var_mult"], big=True)
        S["result_delay"] = 1.4
        S["message"] = "%s MOG STARE." % grade.upper()
        _mogx_after_attack(True, perfects)

    def _mogx_quiz_start():
        S = mog_battle
        if not S["word_bag"]:
            S["word_bag"] = list(MOGX_WORDS)
            renpy.random.shuffle(S["word_bag"])
        word, correct = S["word_bag"].pop()
        others = [d for (w, d) in MOGX_WORDS if w != word]
        renpy.random.shuffle(others)
        opts = [correct] + others[:3]
        renpy.random.shuffle(opts)
        S["quiz"] = {
            "word": word, "opts": opts,
            "correct": opts.index(correct), "picked": None,
        }
        S["qte_elapsed"] = 0.0
        S["phase"] = "quiz"
        S["message"] = "GALAXY BRAIN 🧠 // Answer before the bar runs out. Keys 1-4."

    def _mogx_quiz_pick(idx):
        S = mog_battle
        if S["phase"] != "quiz" or S["quiz"] is None:
            return
        S["quiz"]["picked"] = idx
        if idx == S["quiz"]["correct"]:
            _mogx_sfx("quiz_ok")
        else:
            _mogx_sfx("quiz_no")
        S["phase"] = "quiz_reveal"
        S["qte_elapsed"] = 0.0
        renpy.restart_interaction()

    def _mogx_quiz_apply():
        S = mog_battle
        if S["phase"] != "quiz_reveal":
            return
        ok = S["quiz"]["picked"] == S["quiz"]["correct"]
        S["quiz"] = None
        S["last_grade"] = "correct" if ok else "wrong"
        if ok:
            _mogx_announce("GALAXY BRAIN 📈 ACTUALLY SMART", "purp")
            _mogx_gain_aura(1)
            _mogx_float("aura", "+1⚡", "purp")
            _mogx_damage_enemy(20 * S["var_mult"], "purp")
            S["message"] = "Galaxy Brain // correct."
            _mogx_after_attack(True, 1)
        else:
            # Wrong answer: no damage at all — the enemy feeds on your L.
            _mogx_announce("NOT COOKING 📉", "blue")
            _mogx_gain_mog(-5)
            _mogx_enemy_smirk()
            S["message"] = "Galaxy Brain // wrong. Their Ego grows."
            _mogx_after_attack(False, 0)

    def _mogx_mash_press(key):
        S = mog_battle
        if S["phase"] != "mash":
            return
        if key is not None and key == S["mash_last"]:
            _mogx_sfx("miss")
            return
        S["mash_last"] = key
        S["mash_count"] += 1
        _mogx_sfx("tap")
        renpy.restart_interaction()

    def _mogx_resolve_mash():
        S = mog_battle
        count = S["mash_count"]
        S["last_grade"] = count
        dmg = int(round(count * 1.6 * S["var_mult"]))
        if count >= MOGX_MASH_FULL:
            dmg += 10
        perfects = 1 if count >= 12 else 0
        if count > 0:
            _mogx_damage_enemy(dmg, "purp")
        else:
            _mogx_float("enemy", "crickets…", "blue")
            _mogx_sfx("miss")
            _mogx_enemy_smirk()
        if count >= MOGX_MASH_FULL:
            _mogx_announce("MAX RATIO 💥 %d HITS" % count, "gold")
        elif count >= 8:
            _mogx_announce("RATIO'D 📉 %d HITS" % count, "purp")
        if count < 8:
            _mogx_gain_mog(-5)
            if count > 0:
                _mogx_sfx("quiz_no")
        if count >= 8 and S["ehp"] > 0:
            S["embarrassed"] = True
            _mogx_sfx("buff")
        S["message"] = "Ratio Rush // %d hits%s." % (count, " — they're EMBARRASSED 🫣" if count >= 8 and S["ehp"] > 0 else "")
        if perfects:
            _mogx_sfx("perfect")
        _mogx_after_attack(count > 0, perfects)

    def _mogx_nap_press():
        S = mog_battle
        if S["phase"] != "nap":
            return
        p = S["qte_elapsed"] / MOGX_NAP_DUR
        if abs(p - 0.75) <= 0.0475:
            grade = "perfect"
        elif 0.60 <= p <= 0.90:
            grade = "good"
        else:
            grade = "miss"
        _mogx_resolve_nap(grade)

    def _mogx_resolve_nap(grade):
        S = mog_battle
        S["last_grade"] = grade
        if grade == "miss":
            _mogx_gain_mog(-5)
            _mogx_sfx("quiz_no")
        heal = 30 if grade == "perfect" else 20 if grade == "good" else 12
        _mogx_heal_player(heal)
        cured = S["cringe"]
        S["cringe"] = False
        S["cringe_turns"] = 0
        if grade == "perfect":
            _mogx_announce("QUALITY REM 💤", "green")
            _mogx_gain_aura(1)
            _mogx_float("aura", "+1⚡", "green")
        elif cured:
            _mogx_announce("STATUS CURED 😌", "green")
        S["message"] = "Power Nap // +%d Confidence%s." % (heal, ", CRINGE cured" if cured else "")
        if cured:
            _mogx_sfx("buff")
        _mogx_after_attack(True, 0, feeds_meter=False)

    MOGX_OSU_POINTS = ((430, 470), (500, 270), (640, 420), (780, 270), (850, 470))

    def _mogx_osu_press(index):
        S = mog_battle
        if S["phase"] != "mogmax" or index != S["osu_step"]:
            return
        _mogx_osu_advance(True)

    def _mogx_osu_advance(hit):
        S = mog_battle
        if S["phase"] != "mogmax":
            return
        S["osu_results"].append(hit)
        if hit:
            S["osu_hits"] += 1
            _mogx_sfx("step")
        else:
            _mogx_sfx("quiz_no")
        S["osu_step"] += 1
        S["osu_clock"] = 0.0
        if S["osu_step"] >= 5:
            _mogx_resolve_mogmax()
        renpy.restart_interaction()

    def _mogx_resolve_mogmax():
        S = mog_battle
        hits = S["osu_hits"]
        S["last_grade"] = hits
        perfects = 0
        if hits > 0:
            _mogx_damage_enemy(hits * 9, "gold", big=True)
            _mogx_float("enemy", "CRIT ×%d!" % hits, "red")
        else:
            _mogx_float("enemy", "WHIFF", "blue")
            _mogx_sfx("miss")
            _mogx_enemy_smirk()
        if hits == 5:
            perfects = 1
            _mogx_announce("FULL COMBO M! 👑", "gold")
            _mogx_sfx("perfect")
            _mogx_gain_aura(1)
            _mogx_float("aura", "+1⚡", "gold")
        if S["ehp"] > 0:
            if hits >= 4:
                S["stunned"] = True
                _mogx_announce("BROKEN 💫", "purp")
                _mogx_sfx("buff")
                S["message"] = "MOGMAX // %d of 5 — they are BROKEN 💫 and lose their turn." % hits
            else:
                S["message"] = "MOGMAX // %d of 5 — not clean enough, no break." % hits
        else:
            S["message"] = "MOGMAX // %d of 5." % hits
        S["stats"]["perfects"] += perfects
        S["phase"] = "mogmax_impact"
        _mogx_audio("audio/battle_super_effective.mp3", 0.85, "battle_impact")
        renpy.restart_interaction()

    # ------------------------------------------------------------------
    # After a player skill resolves
    # ------------------------------------------------------------------
    def _mogx_after_skill():
        S = mog_battle
        if S["phase"] not in ("player_result", "mogmax_impact"):
            return
        if S["tutorial"] and not S["tut_free"]:
            _mogx_tut_after_skill()
            return
        if S["ehp"] <= 0:
            _mogx_finish("tutorial" if S["tutorial"] else "win")
            return
        _mogx_enemy_turn()

    # ------------------------------------------------------------------
    # Enemy turn: intents, then attack pattern
    # ------------------------------------------------------------------
    def _mogx_enemy_turn():
        S = mog_battle
        name = S["config"]["enemy_name"]

        if S["stunned"]:
            S["stunned"] = False
            S["message"] = "%s is BROKEN 💫 — they can't move!" % name
            _mogx_announce("💫 TOO BROKEN TO ATTACK", "purp")
            S["phase"] = "break_result"
            renpy.restart_interaction()
            return

        # Clav's final form.
        if S["phase2"] and not S["in_phase2"] and S["ehp"] <= S["emax"] * 0.5:
            S["in_phase2"] = True
            p2 = S["phase2"]
            S["edmg"] = p2["dmg"]
            S["feint"] = p2["feint"]
            S["patterns"] = [list(p) for p in p2["patterns"]]
            S["last_pat"] = None
            _mogx_announce("FINAL FORM 👑🔥", "red")
            _mogx_sfx("alert_red")

        # Heal intent: limited charges, only when hurt, never twice in a row.
        if (S["heals_left"] > 0 and S["ehp"] < S["emax"] * 0.5
                and S["last_action"] != "heal" and renpy.random.random() < 0.75):
            S["heals_left"] -= 1
            S["last_action"] = "heal"
            S["message"] = "%s takes a recovery turn! 🥤 Burst or BREAK them to deny heals." % name
            S["phase"] = "enemy_heal"
            renpy.restart_interaction()
            return

        # Cringe taunt: undodgeable status, cured only by Power Nap.
        if (S["cringes_left"] > 0 and not S["cringe"]
                and S["last_action"] != "cringe" and renpy.random.random() < 0.45):
            S["cringes_left"] -= 1
            S["last_action"] = "cringe"
            S["message"] = "%s is posting your L online… 📱" % name
            S["phase"] = "enemy_cringe"
            renpy.restart_interaction()
            return

        S["last_action"] = "attack"
        idxs = list(range(len(S["patterns"])))
        if len(idxs) > 1 and S["last_pat"] is not None:
            idxs = [i for i in idxs if i != S["last_pat"]]
        pi = renpy.random.choice(idxs)
        S["last_pat"] = pi
        pattern = [dict(h) for h in S["patterns"][pi]]
        if S["feint"]:
            for h in pattern:
                if not any(h.get(k) for k in ("red", "feint", "drain", "late", "notell")):
                    if renpy.random.random() < S["feint"]:
                        h["feint"] = True

        S["queue"] = pattern
        S["queue_idx"] = 0
        S["counter"] = 0
        S["turn_hits"] = 0
        S["turn_pdodges"] = 0
        S["turn_parries"] = 0
        S["turn_took_hit"] = False
        # Deliberately does NOT announce the combo length — read the rhythm.
        S["message"] = "%s attacks! W = parry · S = dodge" % name
        S["phase"] = "enemy_intro"
        renpy.restart_interaction()

    def _mogx_apply_enemy_heal():
        S = mog_battle
        if S["phase"] != "enemy_heal":
            return
        healed = min(S["heal_amt"], S["emax"] - S["ehp"])
        S["ehp"] += healed
        _mogx_float("enemy", "+%d" % healed, "green")
        _mogx_announce("🥤 %s RECOVERS" % S["config"]["enemy_name"].upper(), "green")
        _mogx_sfx("heal")
        S["phase"] = "enemy_result"
        renpy.restart_interaction()

    def _mogx_apply_enemy_cringe():
        S = mog_battle
        if S["phase"] != "enemy_cringe":
            return
        S["cringe"] = True
        S["cringe_turns"] = 0
        _mogx_float("player", "😬", "red")
        _mogx_announce("CRINGED 😬 — LEAKING AURA. NAP IT OFF", "red")
        _mogx_sfx("miss")
        S["phase"] = "enemy_result"
        renpy.restart_interaction()

    def _mogx_start_hit(guided=None, focus=None):
        S = mog_battle
        hit = S["queue"][S["queue_idx"]]
        S["hit"] = hit
        S["hit_elapsed"] = 0.0
        w = hit["w"]
        feint = hit.get("feint", False)
        S["impact_at"] = w + (0.45 if feint else 0.0)
        if hit.get("notell"):
            S["alert_at"] = 999.0        # no tell at all (Clav phase 2)
        elif hit.get("late"):
            S["alert_at"] = max(0.0, S["impact_at"] - 0.15)
        else:
            S["alert_at"] = max(0.0, w - (0.80 if feint else 0.36))
        S["alert_on"] = False
        S["alert_played"] = False
        S["def_result"] = None
        S["def_lock"] = 0.0
        S["def_pose"] = None
        S["guided_kind"] = guided
        S["def_focus"] = focus or guided
        S["phase"] = "defense"
        renpy.restart_interaction()

    def _mogx_defend(kind):
        S = mog_battle
        # Frozen-time tutorial rep: the exact press moment, no timer.
        if S["phase"] == "guided_frozen":
            if kind == S["guided_kind"]:
                _mogx_guided_success()
            else:
                if S["guided_kind"] == "parry":
                    _mogx_float("player", "W to parry this one!", "blue")
                else:
                    _mogx_float("player", "that one's a DODGE — S!", "blue")
            return
        if S["phase"] != "defense" or S["def_result"] is not None:
            return
        # During a frozen-time lesson only the freeze moment accepts input —
        # otherwise an early press would resolve through the normal pipeline
        # and end the round mid-tutorial (soft-locking the lesson).
        if S["guided_kind"]:
            _mogx_float("player", "wait for the freeze ❄️", "blue")
            return
        if S["def_lock"] > 0:
            return
        hit = S["hit"]
        dt = S["hit_elapsed"] - S["impact_at"]
        in_parry = MOGX_PARRY_WIN[0] <= dt <= MOGX_PARRY_WIN[1]
        in_perfect = MOGX_PERFECT_WIN[0] <= dt <= MOGX_PERFECT_WIN[1]
        in_dodge = MOGX_DODGE_WIN[0] <= dt <= MOGX_DODGE_WIN[1]
        if kind == "parry":
            if in_parry:
                # A landed parry IS perfect — there's only one tier.
                if hit.get("red"):
                    _mogx_apply_defense("failparry")
                else:
                    _mogx_apply_defense("parry")
            elif dt < MOGX_PARRY_WIN[0]:
                _mogx_float("player", "too early!", "blue")
                _mogx_sfx("miss")
                S["def_lock"] = 0.38
        else:
            if in_dodge:
                _mogx_apply_defense("pdodge" if in_perfect else "dodge")
            elif dt < MOGX_DODGE_WIN[0]:
                _mogx_float("player", "too early!", "blue")
                _mogx_sfx("miss")
                S["def_lock"] = 0.30

    def _mogx_apply_defense(result):
        S = mog_battle
        if S["phase"] != "defense":
            return
        hit = S["hit"]
        S["def_result"] = result
        S["turn_hits"] += 1
        dmg = S.get("rep_dmg_override") or S["edmg"]
        if hit.get("heavy"):
            dmg = int(round(dmg * 1.7))
        if S["embarrassed"]:
            dmg = int(round(dmg * 0.6))

        if result == "parry":
            S["stats"]["parries"] += 1
            S["turn_parries"] += 1
            S["def_pose"] = "parry"
            _mogx_announce("PARRY!", "gold")
            _mogx_sfx("parry")
            _mogx_gain_aura(1)
            _mogx_float("aura", "+1⚡", "gold")
            if S["php"] < S["pmax"]:
                _mogx_heal_player(5)
            _mogx_gain_mog(20)
            S["counter"] += 6
        elif result == "pdodge":
            S["def_pose"] = "dodge"
            S["turn_pdodges"] += 1
            _mogx_announce("PERFECT DODGE 💨✨", "purp")
            # Whoosh + a light chime only — the "super effective" smack reads
            # as taking a hit, which is exactly wrong for a clean dodge.
            # Aura pays out only for a FLAWLESS string (see finish_enemy_turn).
            _mogx_sfx("whoosh")
            _mogx_sfx("step", "battle_impact")
        elif result == "dodge":
            S["def_pose"] = "dodge"
            _mogx_announce("DODGED 💨", "purp")
            _mogx_sfx("whoosh")
        elif result == "failparry":
            S["def_pose"] = "hit"
            S["turn_took_hit"] = True
            _mogx_announce("CAN'T PARRY THAT ❌", "red")
            _mogx_damage_player(dmg, heavy=hit.get("heavy"))
        else:  # hit
            S["def_pose"] = "hit"
            S["turn_took_hit"] = True
            _mogx_damage_player(dmg, heavy=hit.get("heavy"))
            if hit.get("drain") and S["aura"] > 0:
                stolen = min(2, S["aura"])
                S["aura"] -= stolen
                _mogx_float("aura", "-%d⚡ YOINKED" % stolen, "red")
                _mogx_announce("AURA YOINKED ⚡", "red")
        S["phase"] = "defense_result"
        renpy.restart_interaction()

    def _mogx_hit_resolved():
        S = mog_battle
        if S["phase"] != "defense_result":
            return
        # Tutorial real-rep evaluation intercepts the normal flow.
        if S.get("tut_real"):
            _mogx_tut_real_resolved()
            return
        # Safety net: any other defense resolution during a tutorial lesson is
        # a stray — restart the current lesson instead of running enemy turns.
        if S["tutorial"] and not S["tut_free"]:
            _mogx_tut_run()
            return
        if S["php"] <= 0:
            _mogx_finish("loss")
            return
        S["queue_idx"] += 1
        if S["queue_idx"] < len(S["queue"]):
            _mogx_start_hit()
        else:
            _mogx_finish_enemy_turn()

    def _mogx_finish_enemy_turn():
        S = mog_battle
        S["embarrassed"] = False
        # Take ZERO hits across the whole string — by any mix of parries and
        # dodges — and bank +1 Aura.
        if S["turn_hits"] > 0 and not S["turn_took_hit"]:
            _mogx_gain_aura(1)
            _mogx_float("aura", "UNTOUCHED ✨ +1⚡", "purp")
        if S["counter"] > 0 and S["php"] > 0 and S["ehp"] > 0:
            _mogx_announce("COUNTER!", "gold")
            _mogx_damage_enemy(S["counter"], "gold")
            S["counter"] = 0
        S["phase"] = "enemy_result"
        renpy.restart_interaction()

    def _mogx_end_round():
        S = mog_battle
        if S["phase"] not in ("enemy_result", "break_result"):
            return
        # Safety net: rounds only cycle in real fights and the free-form finish.
        if S["tutorial"] and not S["tut_free"]:
            _mogx_tut_run()
            return
        if S["php"] <= 0:
            _mogx_finish("loss")
            return
        if S["ehp"] <= 0:
            _mogx_finish("tutorial" if S["tutorial"] else "win")
            return
        S["cooldown"] = S["pending_cooldown"]
        S["pending_cooldown"] = None
        # Cringe leaks Aura each turn, but fades on its own after 3 turns so
        # a broke player can't get locked out of ever affording the nap.
        if S["cringe"]:
            if S["aura"] > 0:
                S["aura"] -= 1
                _mogx_float("aura", "😬 -1⚡", "red")
            S["cringe_turns"] += 1
            if S["cringe_turns"] >= 3:
                S["cringe"] = False
                S["cringe_turns"] = 0
                _mogx_float("player", "😮‍💨 cringe faded", "green")
        S["round"] += 1
        S["stats"]["turns"] += 1
        S["selected"] = None
        S["def_pose"] = None
        S["phase"] = "player"
        S["message"] = "YOUR TURN // Spend Aura, rotate skills, build MOGMAX."
        renpy.restart_interaction()

    # ------------------------------------------------------------------
    # Tick — drives every clock (0.02s granularity, like the rest of the game)
    # ------------------------------------------------------------------
    def _mogx_tick():
        S = mog_battle
        if S is None:
            return
        dt = 0.02
        phase = S["phase"]

        if S["ann"] is not None:
            S["ann_age"] += dt
            if S["ann_age"] > 1.0:
                S["ann"] = None
        if S["flash"] is not None:
            S["flash_age"] += dt
            if S["flash_age"] > 0.30:
                S["flash"] = None
        if S["floaters"]:
            for f in S["floaters"]:
                f["age"] += dt
            S["floaters"] = [f for f in S["floaters"] if f["age"] < 1.05]

        if phase == "hold":
            S["qte_elapsed"] += dt
            if S["qte_elapsed"] >= MOGX_HOLD_TIMEOUT:
                _mogx_resolve_hold("miss")
        elif phase == "quiz":
            S["qte_elapsed"] += dt
            if S["qte_elapsed"] >= MOGX_QUIZ_DUR:
                S["quiz"]["picked"] = -1
                _mogx_sfx("quiz_no")
                S["phase"] = "quiz_reveal"
                S["qte_elapsed"] = 0.0
        elif phase == "mash":
            S["qte_elapsed"] += dt
            if S["qte_elapsed"] >= MOGX_MASH_DUR:
                _mogx_resolve_mash()
        elif phase == "nap":
            S["qte_elapsed"] += dt
            if S["qte_elapsed"] >= MOGX_NAP_DUR:
                _mogx_resolve_nap("miss")
        elif phase == "mogmax":
            S["osu_clock"] += dt
            if S["osu_clock"] >= MOGX_OSU_WIN:
                _mogx_osu_advance(False)
        elif phase == "defense":
            S["hit_elapsed"] += dt
            if S["def_lock"] > 0:
                S["def_lock"] = max(0.0, S["def_lock"] - dt)
            if not S["alert_on"] and S["hit_elapsed"] >= S["alert_at"]:
                S["alert_on"] = True
                if not S["alert_played"]:
                    S["alert_played"] = True
                    _mogx_sfx("alert_red" if S["hit"].get("red") else "alert")
            if S["guided_kind"]:
                # Freeze time at the exact impact moment and wait for the key.
                if S["hit_elapsed"] >= S["impact_at"]:
                    S["hit_elapsed"] = S["impact_at"]
                    S["phase"] = "guided_frozen"
            elif S["hit_elapsed"] >= S["impact_at"] + 0.16 and S["def_result"] is None:
                # Resolve the hit only after the dodge window (+0.13) has fully
                # closed — otherwise a legit last-instant dodge could be beaten
                # to the punch by this auto-resolve in the same frame.
                _mogx_apply_defense("hit")
        renpy.restart_interaction()

    # ------------------------------------------------------------------
    # Tutorial interpreter
    # ------------------------------------------------------------------
    def _mogx_dlg(text, next_action):
        S = mog_battle
        S["dlg_text"] = text
        S["dlg_next"] = next_action
        S["phase"] = "dialogue"
        renpy.restart_interaction()

    def _mogx_dlg_advance():
        S = mog_battle
        if S["phase"] != "dialogue" or S["dlg_next"] is None:
            return
        action = S["dlg_next"]
        S["dlg_text"] = None
        S["dlg_next"] = None
        _mogx_sfx("click")
        if action == "step":
            S["tut_idx"] += 1
            _mogx_tut_run()
        elif action == "reteach":
            _mogx_tut_run()
        elif action == "guided_rep":
            _mogx_tut_guided_rep()
        elif action == "real_rep":
            _mogx_tut_real_rep()
        renpy.restart_interaction()

    def _mogx_tut_run():
        S = mog_battle
        if S["tut_idx"] >= len(MOGX_TUT):
            return
        step = MOGX_TUT[S["tut_idx"]]
        kind = step["do"]
        if kind == "dlg":
            _mogx_dlg(step["text"], "step")
        elif kind == "teach":
            skill = step["skill"]
            cost = MOGX_SKILLS[skill]["cost"]
            S["aura"] = max(S["aura"], cost)
            S["cooldown"] = None
            S["pending_cooldown"] = None
            S["ehp"] = max(S["ehp"], min(S["emax"], 80))
            S["stunned"] = False
            if skill == "mogmax":
                S["mog"] = 100
            S["allowed"] = [skill]
            S["phase"] = "player"
            S["message"] = "LESSON // Use %s %s." % (
                MOGX_SKILLS[skill]["name"], MOGX_SKILLS[skill]["icon"])
        elif kind == "cringe_hit":
            # Scripted: Kai cringes you and drops your Confidence so the
            # Power Nap lesson has something real to heal and cure.
            S["cringe"] = True
            S["cringe_turns"] = 0
            S["php"] = min(S["php"], 40)
            _mogx_float("player", "😬", "red")
            _mogx_flash("player")
            _mogx_sfx("hurt")
            _mogx_announce("CRINGED 😬", "red")
            S["message"] = "Kai posts your L in the group chat. CRINGE applied."
            S["phase"] = "tut_beat"
        elif kind == "guided":
            S["tut_reps"] = 0
            _mogx_tut_guided_rep()
        elif kind == "real":
            S["tut_reps"] = 0
            _mogx_tut_real_rep()
        elif kind == "free":
            S["allowed"] = None
            S["tut_free"] = True
            S["ehp"] = min(S["ehp"], 45)
            S["emax"] = 45
            S["cooldown"] = None
            S["pending_cooldown"] = None
            S["phase"] = "player"
            S["message"] = "FINAL CHECK // Full kit, live. Finish the spar."
        renpy.restart_interaction()

    def _mogx_tut_guided_rep():
        S = mog_battle
        step = MOGX_TUT[S["tut_idx"]]
        kind = step["kind"]
        S["queue"] = [{"w": 1.35, "red": kind == "dodge"}]
        S["queue_idx"] = 0
        S["message"] = ("FROZEN REP // I'll stop time at the exact %s moment."
                        % ("dodge" if kind == "dodge" else "parry"))
        _mogx_start_hit(guided=kind)

    def _mogx_guided_success():
        S = mog_battle
        kind = S["guided_kind"]
        S["guided_kind"] = None
        S["alert_on"] = False
        if kind == "parry":
            S["stats"]["parries"] += 1
            S["def_pose"] = "parry"
            _mogx_announce("PARRY!", "blue")
            _mogx_sfx("parry")
            _mogx_gain_aura(1)
            _mogx_float("aura", "+1⚡", "blue")
        else:
            S["def_pose"] = "dodge"
            _mogx_announce("DODGED 💨", "purp")
            _mogx_sfx("whoosh")
            _mogx_gain_aura(1)
            _mogx_float("aura", "+1⚡", "purp")
        S["phase"] = "guided_result"
        renpy.restart_interaction()

    def _mogx_tut_beat_done():
        S = mog_battle
        if S["phase"] != "tut_beat":
            return
        S["tut_idx"] += 1
        _mogx_tut_run()

    def _mogx_guided_done():
        S = mog_battle
        if S["phase"] != "guided_result":
            return
        step = MOGX_TUT[S["tut_idx"]]
        S["tut_reps"] += 1
        if S["tut_reps"] < step["reps"]:
            _mogx_dlg(step["mid"], "guided_rep")
        else:
            S["tut_idx"] += 1
            _mogx_tut_run()

    def _mogx_tut_real_rep():
        S = mog_battle
        step = MOGX_TUT[S["tut_idx"]]
        S["tut_real"] = True
        S["rep_dmg_override"] = step.get("rep_dmg", 4)
        S["counter"] = S.get("counter", 0)
        S["queue"] = [dict(step["attack"])]
        S["queue_idx"] = 0
        S["message"] = ("LIVE REP %d of %d // %s"
                       % (S["tut_reps"] + 1, step["reps"],
                          "press S near impact" if step["kind"] == "dodge" else "press W at impact"))
        _mogx_start_hit(focus=step["kind"])

    def _mogx_tut_real_resolved():
        S = mog_battle
        step = MOGX_TUT[S["tut_idx"]]
        res = S["def_result"]
        S["tut_real"] = False
        S["rep_dmg_override"] = None
        if step["kind"] == "dodge":
            passed = res in ("dodge", "pdodge")
        else:
            passed = res in ("parry", "perfect")
        if passed:
            S["tut_reps"] += 1
            if S["tut_reps"] < step["reps"]:
                _mogx_dlg(step["mid"], "real_rep")
            else:
                # Fire any queued counter from the parry reps before moving on.
                if S["counter"] > 0 and S["ehp"] > 0:
                    _mogx_announce("COUNTER!", "gold")
                    _mogx_damage_enemy(S["counter"], "gold")
                    S["counter"] = 0
                S["tut_idx"] += 1
                _mogx_tut_run()
        else:
            _mogx_dlg(step["fail"], "real_rep")

    def _mogx_tut_after_skill():
        S = mog_battle
        step = MOGX_TUT[S["tut_idx"]]
        if step["do"] != "teach":
            return
        skill = step["skill"]
        grade = S["last_grade"]
        passed = True
        fail_text = step.get("fail")
        if skill == "brain":
            passed = grade == "correct"
        elif skill == "looks":
            passed = grade in ("good", "perfect")
            if grade == "oob" and step.get("fail_oob"):
                fail_text = step["fail_oob"]
        elif skill == "jester":
            passed = isinstance(grade, int) and grade >= 8
        elif skill == "sleep":
            passed = grade in ("good", "perfect")
        elif skill == "mogmax":
            passed = isinstance(grade, int) and grade >= 4
            S["stunned"] = False
        if passed:
            S["allowed"] = []
            S["tut_idx"] += 1
            _mogx_tut_run()
        else:
            _mogx_dlg(fail_text, "reteach")

    # ------------------------------------------------------------------
    # Finish
    # ------------------------------------------------------------------
    def _mogx_grade(stats):
        if stats["hits_taken"] == 0:
            return ("💎 GIGAMOGGER — flawless", "#ffd75e")
        if stats["hits_taken"] <= 2 and stats["parries"] >= 2:
            return ("🔥 CERTIFIED MOGGER", "#ffd75e")
        if stats["hits_taken"] <= 5:
            return ("😐 KINDA MID (still won tho)", "#6db1ff")
        return ("🧍 NPC BEHAVIOR — practice your parries", "#ff5d6c")

    def _mogx_finish(outcome):
        global mog_battle_aura_kept, mog_battle_last_result
        S = mog_battle
        renpy.music.stop(channel="battle_warning", fadeout=0.15)
        stats = S["stats"]
        result = {
            "battle_id": S["battle_id"],
            "outcome": outcome,
            "aura_kept": max(0, S["php"]),
            "rounds": S["round"],
            "perfect_attacks": stats["perfects"],
            "perfect_defenses": stats["parries"],
            "parries": stats["parries"],
            "hits_taken": stats["hits_taken"],
        }
        S["result"] = result
        S["phase"] = "complete"
        mog_battle_aura_kept = result["aura_kept"]
        mog_battle_last_result = result
        if outcome == "loss":
            S["message"] = "Your Confidence hit zero. Shake it off — every mogger gets ratio'd sometimes."
            _mogx_audio("audio/battle_low_health.mp3", 0.5)
        elif outcome == "tutorial":
            S["message"] = "Full kit confirmed. The hallway awaits."
            _mogx_sfx("win")
        else:
            S["message"] = "%s breaks eye contact first." % S["config"]["enemy_name"].title()
            _mogx_sfx("win")
        renpy.restart_interaction()

    def _mogx_retry():
        start_mog_battle(mog_battle["battle_id"])

    def _mogx_toggle_help():
        mog_battle["help"] = not mog_battle["help"]
        renpy.restart_interaction()


# Quick-test entry points (console: shift+O, then `jump battle_kai_tutorial`).
label battle_kai_tutorial:
    $ start_mog_battle("kai_tutorial")
    $ mog_battle_last_result = renpy.call_screen("mog_battle_screen")
    return

label battle_kai_graduation:
    $ start_mog_battle("kai_graduation")
    $ mog_battle_last_result = renpy.call_screen("mog_battle_screen")
    return


# ----------------------------------------------------------------------
# Transforms
# ----------------------------------------------------------------------
# Every enemy-state transform opens with a FULL reset (xoffset/yoffset/zoom/
# rotate) — Ren'Py carries unset properties over when transforms swap, which
# left interrupted spins stuck mid-rotation (upside-down enemies).
transform mogx_enemy_idle:
    xoffset 0 yoffset 0 zoom 1.0 rotate 0
    ease 1.2 yoffset -6
    ease 1.2 yoffset 0
    repeat

transform mogx_enemy_windup:
    xoffset 0 yoffset 0 zoom 1.0 rotate 0
    easein 0.45 xoffset 42 yoffset -20 zoom 1.05

# Brayden coils DOWN then springs up — a quicker, bouncier tell than Kai's.
transform mogx_enemy_windup_brayden:
    xoffset 0 yoffset 0 zoom 1.0 rotate 0
    easein 0.16 yoffset 16 zoom 1.09
    easein 0.20 xoffset 30 yoffset -28 zoom 1.05

# Clav barely telegraphs: a slow, subtle coil — read the glow, not the body.
transform mogx_enemy_windup_clav:
    xoffset 0 yoffset 0 zoom 1.0 rotate 0
    easein 0.55 xoffset 10 yoffset -6 zoom 0.985

# Zig-zag windup: jukes side to side before committing.
transform mogx_enemy_windup_zigzag:
    xoffset 0 yoffset 0 zoom 1.0 rotate 0
    block:
        linear 0.09 xoffset -26
        linear 0.09 xoffset 26
        repeat 3
    easein 0.14 xoffset 30 yoffset -16 zoom 1.05

# Spin windup: two full spins, then winds up to full speed.
transform mogx_enemy_windup_spin:
    xoffset 0 yoffset 0 zoom 1.0 rotate 0
    linear 0.26 rotate 360
    rotate 0
    linear 0.26 rotate 360
    rotate 0
    easein 0.20 xoffset 26 yoffset -14 zoom 1.14

# The dive: leaves the windup pose and rams the player's AVATAR head-on
# exactly 0.30s later — the lunge is the parry/dodge timing cue.
transform mogx_enemy_lunge:
    xoffset 42 yoffset -20 zoom 1.05 rotate 0
    easein 0.30 xoffset -795 yoffset 0 zoom 1.32
    pause 0.14
    easeout 0.28 xoffset 0 yoffset 0 zoom 1.0

# Heavy dive: slower and bigger — the weight of the swing is readable.
transform mogx_enemy_lunge_heavy:
    xoffset 42 yoffset -20 zoom 1.05 rotate 0
    easein 0.38 xoffset -795 yoffset 0 zoom 1.48
    pause 0.16
    easeout 0.30 xoffset 0 yoffset 0 zoom 1.0

# Slow ram (~): drifts across the arena — defend when it ARRIVES, not when
# it starts moving.
transform mogx_enemy_lunge_slow:
    xoffset 42 yoffset -20 zoom 1.05 rotate 0
    easein 0.60 xoffset -795 yoffset 0 zoom 1.36
    pause 0.14
    easeout 0.30 xoffset 0 yoffset 0 zoom 1.0

# Frozen-time lesson: held at the moment of contact.
transform mogx_enemy_contact:
    xoffset -795 yoffset 0 zoom 1.32 rotate 0

# Whole player box (avatar + bars) rattles when a hit connects.
transform mogx_box_shake:
    xoffset 0 yoffset 0
    linear 0.04 xoffset -15 yoffset 7
    linear 0.04 xoffset 13 yoffset -6
    linear 0.04 xoffset -10 yoffset 4
    linear 0.04 xoffset 7 yoffset -3
    linear 0.04 xoffset 0 yoffset 0

transform mogx_player_hit:
    xoffset 0
    linear 0.04 xoffset -12
    linear 0.04 xoffset 11
    linear 0.04 xoffset -7
    linear 0.04 xoffset 0

transform mogx_player_dodge:
    alpha 1.0
    xoffset 0
    easeout 0.10 xoffset -80 alpha 0.3
    easein 0.22 xoffset 0 alpha 1.0

# Parry: the player shoves INTO the attack (up-right, toward the enemy).
transform mogx_player_parry:
    xoffset 0 yoffset 0 zoom 1.0
    easeout 0.10 xoffset 48 yoffset -26 zoom 1.07
    ease 0.24 xoffset 0 yoffset 0 zoom 1.0

# ...and the enemy is knocked off the contact point, rocking back past home.
transform mogx_enemy_parried:
    xoffset -795 yoffset 0 zoom 1.32 rotate 0
    easeout 0.24 xoffset 85 yoffset -45 zoom 1.02 rotate 9
    ease 0.22 xoffset 0 yoffset 0 zoom 1.0 rotate 0

transform mogx_impact_flash:
    alpha 0.85
    linear 0.09 alpha 0.0

transform mogx_red_flash:
    alpha 0.55
    linear 0.25 alpha 0.0

transform mogx_mogmax_word:
    alpha 0.0
    zoom 1.5
    easeout 0.32 alpha 1.0 zoom 1.0

transform mogx_mogmax_point:
    zoom 1.0
    linear 0.38 zoom 1.13
    linear 0.38 zoom 1.0
    repeat

transform mogx_mog_ready_pulse:
    alpha 1.0
    linear 0.55 alpha 0.55
    linear 0.55 alpha 1.0
    repeat

transform mogx_freeze_pulse:
    zoom 1.0
    linear 0.3 zoom 1.04
    linear 0.3 zoom 1.0
    repeat

transform mogx_finisher_impact:
    xoffset 0
    linear 0.035 xoffset -18
    linear 0.035 xoffset 16
    linear 0.035 xoffset -12
    linear 0.035 xoffset 10
    linear 0.035 xoffset 0


# ----------------------------------------------------------------------
# The battle screen
# ----------------------------------------------------------------------
screen mog_battle_screen():
    modal True
    zorder 210

    $ S = mog_battle
    $ config = S["config"]
    $ phase = S["phase"]
    $ enemy_asset = config.get("enemy_asset") or "images/characters/harker/harker stopwatch.png"
    $ enemy_crop = config.get("enemy_crop") or (110, 50, 610, 790)
    $ mogx_text_outlines = [(2, "#000000d8", 0, 1), (4, "#00000070", 0, 2)]

    timer 0.02 repeat True action Function(_mogx_tick)

    # Phase auto-advance timers.
    if phase == "player_result":
        timer S["result_delay"] action Function(_mogx_after_skill)
    elif phase == "mogmax_impact":
        timer 1.2 action Function(_mogx_after_skill)
    elif phase == "quiz_reveal":
        timer 0.95 action Function(_mogx_quiz_apply)
    elif phase == "enemy_intro":
        timer 0.55 action Function(_mogx_start_hit)
    elif phase == "enemy_heal":
        timer 0.9 action Function(_mogx_apply_enemy_heal)
    elif phase == "enemy_cringe":
        timer 0.9 action Function(_mogx_apply_enemy_cringe)
    elif phase == "defense_result":
        # Mid-combo the next hit chains fast; only the last hit breathes.
        timer (0.30 if S["queue_idx"] + 1 < len(S["queue"]) else 0.72) action Function(_mogx_hit_resolved)
    elif phase == "guided_result":
        timer 0.75 action Function(_mogx_guided_done)
    elif phase == "tut_beat":
        timer 1.2 action Function(_mogx_tut_beat_done)
    elif phase in ("enemy_result", "break_result"):
        timer 0.85 action Function(_mogx_end_round)

    # Keys.
    if phase == "player":
        for index, skill_id in enumerate(MOGX_SKILL_ORDER):
            key ("K_%s" % (index + 1)) action Function(_mogx_choose, skill_id)
    elif phase == "dialogue":
        key "K_SPACE" action Function(_mogx_dlg_advance)
        key "K_RETURN" action Function(_mogx_dlg_advance)
    elif phase == "hold":
        key "K_SPACE" action Function(_mogx_hold_press)
    elif phase == "quiz":
        for qi in range(4):
            key ("K_%s" % (qi + 1)) action Function(_mogx_quiz_pick, qi)
    elif phase == "mash":
        key "K_j" action Function(_mogx_mash_press, "j")
        key "K_k" action Function(_mogx_mash_press, "k")
    elif phase == "nap":
        key "K_SPACE" action Function(_mogx_nap_press)
    elif phase == "mogmax":
        key "K_SPACE" action Function(_mogx_osu_press, S["osu_step"])
    elif phase in ("defense", "guided_frozen"):
        key "K_w" action Function(_mogx_defend, "parry")
        key "K_SPACE" action Function(_mogx_defend, "parry")
        key "K_s" action Function(_mogx_defend, "dodge")
        key "K_d" action Function(_mogx_defend, "dodge")

    add "images/backgrounds/bg_ch2_gym.jpg"
    add Solid("#030712e8")

    # Header.
    $ header = "%s  //  %s" % (config.get("title", "MOG BATTLE"), config["enemy_name"])
    text header:
        xpos 26 ypos 20 size 13 color "#aab4c5" bold True
        outlines mogx_text_outlines
    textbutton "❓ HOW TO PLAY":
        xpos 1254 xanchor 1.0 ypos 12 padding (10, 6)
        background Solid("#111827c0") hover_background Solid("#1c2740")
        text_size 11 text_color "#d7dceb" text_bold True
        text_outlines mogx_text_outlines
        action Function(_mogx_toggle_help)

    # ── ENEMY (upper right) ─────────────────────────────────────────
    fixed:
        xpos 800 ypos 76 xysize (360, 330)
        # Only the character art travels; name and EGO bar stay anchored.
        $ hit_heavy = S["hit"] is not None and S["hit"].get("heavy")
        $ hit_slow = S["hit"] is not None and S["hit"].get("slow")
        $ lunge_lead = 0.60 if hit_slow else 0.38 if hit_heavy else 0.30
        # Per-hit windup style ("zigzag"/"spin"), else the enemy's default.
        $ windup_style = (S["hit"].get("windup") if S["hit"] else None) or {"brayden": "brayden", "clav": "clav"}.get(S["battle_id"], "lean")
        fixed:
            xysize (360, 210)
            if phase in ("defense_result", "guided_result") and S["def_pose"] == "parry":
                at mogx_enemy_parried
            elif phase in ("defense", "defense_result") and S["hit_elapsed"] >= S["impact_at"] - lunge_lead and hit_slow:
                at mogx_enemy_lunge_slow
            elif phase in ("defense", "defense_result") and S["hit_elapsed"] >= S["impact_at"] - lunge_lead and hit_heavy:
                at mogx_enemy_lunge_heavy
            elif phase in ("defense", "defense_result") and S["hit_elapsed"] >= S["impact_at"] - lunge_lead:
                at mogx_enemy_lunge
            elif phase == "guided_frozen":
                at mogx_enemy_contact
            elif phase in ("defense", "enemy_cringe") and windup_style == "zigzag":
                at mogx_enemy_windup_zigzag
            elif phase in ("defense", "enemy_cringe") and windup_style == "spin":
                at mogx_enemy_windup_spin
            elif phase in ("defense", "enemy_cringe") and windup_style == "brayden":
                at mogx_enemy_windup_brayden
            elif phase in ("defense", "enemy_cringe") and windup_style == "clav":
                at mogx_enemy_windup_clav
            elif phase in ("defense", "enemy_cringe"):
                at mogx_enemy_windup
            else:
                at mogx_enemy_idle
            # Attack tell: the enemy itself glows — RED = unparryable (dodge
            # only), YELLOW = parry or dodge. The glow silhouette sits behind
            # the art and travels with the lunge. Always present (alpha 0 when
            # inactive) so toggling it never restarts the motion transforms.
            $ tell_on = phase in ("defense", "guided_frozen") and S["alert_on"]
            $ tell_color = "#ff5d6c" if (S["hit"] and S["hit"].get("red")) else "#ffd75e"
            # Two-layer glow: a wide soft halo plus a tight bright rim.
            add Transform(enemy_asset, crop=enemy_crop, fit="contain", xysize=(348, 234), matrixcolor=ColorizeMatrix(Color(tell_color), Color(tell_color))):
                xalign 0.5 ypos -17 alpha (0.5 if tell_on else 0.0)
            add Transform(enemy_asset, crop=enemy_crop, fit="contain", xysize=(324, 218), matrixcolor=ColorizeMatrix(Color(tell_color), Color(tell_color))):
                xalign 0.5 ypos -9 alpha (0.95 if tell_on else 0.0)
            add Transform(enemy_asset, crop=enemy_crop, fit="contain", xysize=(300, 200)) xalign 0.5 ypos 0
        text config["enemy_name"]:
            xpos 20 ypos 202 size 20 color "#f7f8fa" bold True
            outlines mogx_text_outlines
        $ etitle = ("PHASE 2" if S["in_phase2"] else "PHASE 1")
        text ("%s  //  %s" % (etitle, S["battle_id"].replace("_", " ").upper())):
            xpos 20 ypos 229 size 10 color "#98a3b8" bold True
            outlines mogx_text_outlines
        text "EGO":
            xpos 20 ypos 252 size 10 color "#98a3b8" bold True
            outlines mogx_text_outlines
        text ("%d/%d" % (S["ehp"], S["emax"])):
            xpos 320 xanchor 1.0 ypos 252 size 10 color "#98a3b8" bold True
            outlines mogx_text_outlines
        add Solid("#222b3b") xpos 20 ypos 270 xysize (300, 9)
        add Solid("#ffb84d") xpos 20 ypos 270 xysize (int(300 * S["ehp"] / float(S["emax"])), 9)
        $ estatus = ("💫 BROKEN  " if S["stunned"] else "") + ("🫣 EMBARRASSED" if S["embarrassed"] else "")
        if estatus:
            text estatus:
                xpos 20 ypos 288 size 14 color "#c07bff" bold True
                outlines mogx_text_outlines

    # Enemy hit flash.
    if S["flash"] == "enemy":
        add Solid("#ffffff") xpos 800 ypos 76 xysize (360, 210) at mogx_impact_flash

    # ── PLAYER (lower left) ─────────────────────────────────────────
    fixed:
        xpos 100 ypos 258 xysize (350, 310)
        if S["flash"] == "player":
            at mogx_box_shake
        fixed:
            xysize (350, 180)
            if S["def_pose"] == "dodge" and phase in ("defense_result", "guided_result"):
                at mogx_player_dodge
            elif S["def_pose"] == "parry" and phase in ("defense_result", "guided_result"):
                at mogx_player_parry
            elif S["flash"] == "player":
                at mogx_player_hit
            add Transform("images/minigames/acne_face.png", crop=(500, 40, 1050, 1050), fit="contain", xysize=(280, 176)) xpos 26 ypos 0
        text "YOU":
            xpos 26 ypos 176 size 20 color "#f7f8fa" bold True
            outlines mogx_text_outlines
        text "ASPIRING MOGGER":
            xpos 26 ypos 202 size 10 color "#98a3b8" bold True
            outlines mogx_text_outlines

        text "CONFIDENCE":
            xpos 0 ypos 226 size 10 color "#98a3b8" bold True
            outlines mogx_text_outlines
        text ("%d/%d" % (S["php"], S["pmax"])):
            xpos 340 xanchor 1.0 ypos 226 size 10 color "#98a3b8" bold True
            outlines mogx_text_outlines
        add Solid("#222b3b") xpos 0 ypos 244 xysize (340, 9)
        add Solid(_mogx_hp_color(S["php"], S["pmax"])) xpos 0 ypos 244 xysize (int(340 * S["php"] / float(S["pmax"])), 9)

        text "⚡ AURA":
            xpos 0 ypos 262 size 10 color "#98a3b8" bold True
            outlines mogx_text_outlines
        for pip in range(MOGX_AURA_MAX):
            if pip < S["aura"]:
                text "⚡" xpos (86 + pip * 28) ypos 258 size 17 outlines mogx_text_outlines
            else:
                text "⚡" xpos (86 + pip * 28) ypos 258 size 17 outlines mogx_text_outlines at Transform(alpha=0.18)
        text ("%d/%d" % (S["aura"], MOGX_AURA_MAX)):
            xpos 340 xanchor 1.0 ypos 262 size 10 color "#98a3b8" bold True
            outlines mogx_text_outlines

        text "👑 MOG":
            xpos 0 ypos 288 size 10 color "#98a3b8" bold True
            outlines mogx_text_outlines
        add Solid("#222b3b") xpos 86 ypos 291 xysize (214, 8)
        add Solid("#f15bb5" if S["mog"] < 100 else "#ffd75e") xpos 86 ypos 291 xysize (int(214 * S["mog"] / 100.0), 8)
        text ("%d%%" % S["mog"]):
            xpos 340 xanchor 1.0 ypos 287 size 10 color ("#ffd75e" if S["mog"] >= 100 else "#98a3b8") bold True
            outlines mogx_text_outlines
        if S["cringe"]:
            text ("😬 CRINGE (%d turns left) — leaking ⚡, nap it off" % max(1, 3 - S["cringe_turns"])):
                xpos 0 ypos 306 size 13 color "#ff5d6c" bold True
                outlines mogx_text_outlines

    # ── Announcer ───────────────────────────────────────────────────
    if S["ann"] is not None:
        $ ann_age = S["ann_age"]
        $ ann_yoff = int(-20 * max(0.0, (ann_age - 0.55) / 0.45))
        $ ann_alpha = 1.0 if ann_age < 0.7 else max(0.0, 1.0 - (ann_age - 0.7) / 0.3)
        text S["ann"]:
            xalign 0.5 ypos (150 + ann_yoff) size 40 italic True bold True
            color S["ann_color"] outlines [(3, "#000000c0", 0, 2)]
            at Transform(alpha=ann_alpha)

    # ── Floaters ────────────────────────────────────────────────────
    for f in S["floaters"]:
        $ f_alpha = 1.0 if f["age"] < 0.55 else max(0.0, 1.0 - (f["age"] - 0.55) / 0.5)
        text f["text"]:
            xpos f["x"] ypos int(f["y"] - f["age"] * 66) size 24 bold True
            color f["color"] outlines [(2, "#000000b0", 0, 1)]
            at Transform(alpha=f_alpha)

    # ── Message band (top center, under the header) ─────────────────
    text S["message"]:
        xalign 0.5 ypos 52 xmaximum 1000 text_align 0.5 size 15 color "#d7dceb" bold True
        outlines mogx_text_outlines

    # ── Skill deck (hidden while defending — the W/S buttons take its
    #    place in the bottom bar so the UI stays focused) ─────────────
    $ defending = phase in ("defense", "guided_frozen", "defense_result", "guided_result", "enemy_intro", "enemy_heal", "enemy_cringe") and S["hit"] is not None
    if not defending:
        hbox:
            xpos 50 ypos 586 spacing 10
            for skill_id in MOGX_SKILL_ORDER:
                $ skill = MOGX_SKILLS[skill_id]
                $ locked = _mogx_skill_lock(skill_id)
                $ mog_ready = skill_id == "mogmax" and S["mog"] >= 100 and locked is None
                button:
                    xysize (188, 118)
                    if mog_ready:
                        background Solid("#3a2f10")
                        at mogx_mog_ready_pulse
                    else:
                        background Solid("#111827e8")
                    hover_background Solid(skill["color"] + "2d")
                    insensitive_background Solid("#0c111bd9")
                    sensitive locked is None
                    action Function(_mogx_choose, skill_id)
                    tooltip skill["desc"]
                    padding (10, 8)
                    fixed:
                        text skill["key"]:
                            xpos 2 ypos 0 size 10 color "#778197" bold True
                            outlines mogx_text_outlines
                        if locked is not None and locked != "WAIT":
                            text skill["icon"] xalign 0.5 ypos 4 size 30 outlines mogx_text_outlines at Transform(alpha=0.3)
                        else:
                            text skill["icon"] xalign 0.5 ypos 4 size 30 outlines mogx_text_outlines
                        text skill["name"]:
                            xalign 0.5 ypos 48 size 14 color ("#f7f8fa" if locked is None else "#606879") bold True
                            outlines mogx_text_outlines
                        text skill["kind"].upper():
                            xalign 0.5 ypos 68 size 9 color "#8791a5" bold True
                            outlines mogx_text_outlines
                        if skill_id == "mogmax":
                            text ("READY!" if mog_ready else (locked if locked not in (None, "WAIT") else "%d%%" % S["mog"])):
                                xalign 0.5 ypos 88 size 11 color ("#ffd75e" if mog_ready else "#5c6473") bold True
                                outlines mogx_text_outlines
                        elif locked not in (None, "WAIT"):
                            text locked:
                                xalign 0.5 ypos 88 size 10 color "#ff9d6c" bold True
                                outlines mogx_text_outlines
                        else:
                            text ("FREE" if skill["cost"] == 0 else "⚡" * skill["cost"]):
                                xalign 0.5 ypos 86 size 12 color "#ffd75e"
                                outlines mogx_text_outlines

    # Skill hover description — sits on the free line just above the deck.
    $ deck_tt = GetTooltip()
    if deck_tt and phase == "player":
        text deck_tt:
            xalign 0.5 ypos 550 size 13 color "#aab4c5" text_align 0.5 xmaximum 1000
            outlines mogx_text_outlines

    # ── Defense buttons (prototype-style, bottom center) ────────────
    if phase in ("defense", "guided_frozen", "defense_result") and S["hit"] is not None:
        use mogx_defense_buttons(S)

    # ── Minigame panels ─────────────────────────────────────────────
    if phase == "hold":
        use mogx_hold_panel(S)
    elif phase in ("quiz", "quiz_reveal"):
        use mogx_quiz_panel(S)
    elif phase == "mash":
        use mogx_mash_panel(S)
    elif phase == "nap":
        use mogx_nap_panel(S)
    elif phase in ("mogmax", "mogmax_impact"):
        use mogx_mogmax_panel(S)

    # ── Tutorial freeze hint ────────────────────────────────────────
    if phase == "guided_frozen":
        use mogx_freeze_hint(S)

    # ── Coach dialogue ──────────────────────────────────────────────
    if phase == "dialogue" and S["dlg_text"] is not None:
        use mogx_dialogue(S)

    # ── Player hurt flash ───────────────────────────────────────────
    if S["flash"] == "player":
        add Solid("#ff5d6c30") at mogx_red_flash

    # ── Help / results ──────────────────────────────────────────────
    if S["help"]:
        use mogx_help_overlay
    if phase == "complete":
        use mogx_results(S)


# ----------------------------------------------------------------------
# Defense buttons — no timing bar. Read the dive, like the prototype:
# wind-up → ❗ flash → the enemy lunges into your face → press at contact.
# ----------------------------------------------------------------------
screen mogx_defense_buttons(S):
    $ hit = S["hit"]
    $ is_red = bool(hit.get("red"))
    $ focus = S["def_focus"]
    # No "DODGE ONLY" banner — the red glow IS the tell.
    # The two defense buttons live where the skill deck normally sits.
    hbox:
        xalign 0.5 ypos 588 spacing 32
        button:
            xysize (300, 110)
            background Solid("#0d1422e0" if focus == "dodge" else "#6db1ff22")
            hover_background Solid("#6db1ff50")
            sensitive focus != "dodge"
            action Function(_mogx_defend, "parry")
            if focus == "parry":
                at mogx_freeze_pulse
            hbox:
                xalign 0.5 yalign 0.5 spacing 14
                frame:
                    xysize (52, 52) padding (0, 0)
                    background Solid("#2a2438" if focus == "parry" else "#1b2236")
                    text "W" xalign 0.5 yalign 0.5 size 24 bold True color ("#ffb347" if focus == "parry" else "#ffffff")
                text "🛡️ PARRY" yalign 0.5 size 20 bold True color ("#525b6e" if focus == "dodge" else "#ffffff")
        button:
            xysize (300, 110)
            background Solid("#0d1422e0" if focus == "parry" else "#c07bff22")
            hover_background Solid("#c07bff50")
            sensitive focus != "parry"
            action Function(_mogx_defend, "dodge")
            if focus == "dodge":
                at mogx_freeze_pulse
            hbox:
                xalign 0.5 yalign 0.5 spacing 14
                frame:
                    xysize (52, 52) padding (0, 0)
                    background Solid("#2a2438" if focus == "dodge" else "#1b2236")
                    text "S" xalign 0.5 yalign 0.5 size 24 bold True color ("#ffb347" if focus == "dodge" else "#ffffff")
                text "💨 DODGE" yalign 0.5 size 20 bold True color ("#525b6e" if focus == "parry" else "#ffffff")


screen mogx_freeze_hint(S):
    $ kind = S["guided_kind"]
    frame:
        xalign 0.5 ypos 96
        background Solid("#0a1428f6")
        padding (28, 18)
        at mogx_freeze_pulse
        vbox:
            xalign 0.5 spacing 8
            if kind == "parry":
                text "❄️ TIME FROZEN — press {color=#ffd75e}W{/color} NOW!" xalign 0.5 size 24 color "#f7f8fa" bold True
            else:
                text "❄️ TIME FROZEN — press {color=#ffd75e}S{/color} NOW!" xalign 0.5 size 24 color "#f7f8fa" bold True
            # Mini WASD keyboard with the target key lit.
            vbox:
                xalign 0.5 spacing 4
                hbox:
                    xalign 0.5
                    frame:
                        xysize (38, 38) padding (0, 0)
                        background Solid("#2a2438" if kind == "parry" else "#1b2236")
                        text "W" xalign 0.5 yalign 0.5 size 15 bold True color ("#ffb347" if kind == "parry" else "#778197")
                hbox:
                    xalign 0.5 spacing 4
                    frame:
                        xysize (38, 38) padding (0, 0) background Solid("#1b2236")
                        text "A" xalign 0.5 yalign 0.5 size 15 bold True color "#778197"
                    frame:
                        xysize (38, 38) padding (0, 0)
                        background Solid("#2a2438" if kind == "dodge" else "#1b2236")
                        text "S" xalign 0.5 yalign 0.5 size 15 bold True color ("#ffb347" if kind == "dodge" else "#778197")
                    frame:
                        xysize (38, 38) padding (0, 0) background Solid("#1b2236")
                        text "D" xalign 0.5 yalign 0.5 size 15 bold True color "#778197"
            text ("this is the exact %s moment" % ("parry" if kind == "parry" else "dodge")):
                xalign 0.5 size 11 color "#98a3b8"


# ----------------------------------------------------------------------
# Minigame panels
# ----------------------------------------------------------------------
screen mogx_hold_panel(S):
    add Solid("#000000a8")
    $ p = _mogx_stare_pos(S["qte_elapsed"])
    frame:
        xalign 0.5 yalign 0.45 xysize (620, 260)
        background Solid("#0d1422f8")
        padding (30, 22)
        vbox:
            xalign 0.5 spacing 13
            text "😎 MOG STARE — HOLD FRAME":
                xalign 0.5 size 22 color "#ffd75e" bold True
            text "STRIKE WHILE THE MARKER IS IN THE GOLD":
                xalign 0.5 size 12 color "#aab4c5" bold True
            fixed:
                xalign 0.5 xysize (540, 34)
                add Solid("#263149") ypos 6 xysize (540, 22)
                add Solid("#5eff9d50") xpos int(540 * 0.55) ypos 6 xysize (int(540 * 0.27), 22)
                add Solid("#ffd75e") xpos int(540 * 0.82) ypos 6 xysize (int(540 * 0.11), 22)
                add Solid("#ffffff") xpos int(534 * min(p, 1.0)) xysize (6, 34)
            hbox:
                xalign 0.5 spacing 18
                text "green = GOOD" size 11 color "#5eff9d" bold True
                text "gold = PERFECT" size 11 color "#ffd75e" bold True
                text "anywhere else = ❌ BLINK" size 11 color "#ff5d6c" bold True
            button:
                xalign 0.5 xysize (240, 54)
                background Solid("#3a2f10") hover_background Solid("#57460f")
                action Function(_mogx_hold_press)
                hbox:
                    xalign 0.5 yalign 0.5 spacing 10
                    frame:
                        xysize (70, 30) padding (0, 0) background Solid("#1b2236")
                        text "SPACE" xalign 0.5 yalign 0.5 size 12 color "#ffd75e" bold True
                    text "STRIKE 😎" yalign 0.5 size 16 color "#ffffff" bold True


screen mogx_quiz_panel(S):
    add Solid("#000000a8")
    $ quiz = S["quiz"]
    $ qleft = max(0.0, 1.0 - S["qte_elapsed"] / MOGX_QUIZ_DUR) if S["phase"] == "quiz" else 0.0
    frame:
        xalign 0.5 yalign 0.46 xysize (640, 330)
        background Solid("#0d1422f8")
        padding (26, 20)
        vbox:
            xalign 0.5 spacing 10
            if S["phase"] == "quiz":
                fixed:
                    xysize (588, 8)
                    add Solid("#263149") xysize (588, 8)
                    add Solid("#c07bff") xysize (max(1, int(588 * qleft)), 8)
            text ("🧠 What does {color=#c07bff}{b}%s{/b}{/color} mean?" % quiz["word"]):
                xalign 0.5 size 19 color "#f7f8fa"
            null height 2
            for qi, opt in enumerate(quiz["opts"]):
                $ q_bg = "#111827"
                if S["phase"] == "quiz_reveal":
                    if qi == quiz["correct"]:
                        $ q_bg = "#14532d"
                    elif qi == quiz["picked"]:
                        $ q_bg = "#5c1a24"
                button:
                    xfill True ysize 44
                    background Solid(q_bg)
                    hover_background Solid("#c07bff28")
                    sensitive S["phase"] == "quiz"
                    action Function(_mogx_quiz_pick, qi)
                    hbox:
                        spacing 10 yalign 0.5
                        text str(qi + 1) size 14 color "#c07bff" bold True yalign 0.5
                        text opt size 14 color "#e8ecf8" yalign 0.5
            text "PRESS 1-4 · ANSWER BEFORE THE BAR RUNS OUT":
                xalign 0.5 size 10 color "#98a3b8" bold True


screen mogx_mash_panel(S):
    add Solid("#000000a8")
    $ mleft = max(0.0, 1.0 - S["qte_elapsed"] / MOGX_MASH_DUR)
    $ mfill = min(1.0, S["mash_count"] / float(MOGX_MASH_FULL))
    frame:
        xalign 0.5 yalign 0.45 xysize (520, 300)
        background Solid("#0d1422f8")
        padding (26, 18)
        vbox:
            xalign 0.5 spacing 10
            text "🤡 RATIO RUSH — ALTERNATE, FAST!":
                xalign 0.5 size 17 color "#f15bb5" bold True
            fixed:
                xysize (468, 7)
                add Solid("#263149") xysize (468, 7)
                add Solid("#6db1ff") xysize (max(1, int(468 * mleft)), 7)
            fixed:
                xysize (468, 28)
                add Solid("#263149") ypos 2 xysize (468, 24)
                add Solid("#ffd75e" if mfill >= 1.0 else "#5eff9d") ypos 2 xysize (max(1, int(468 * mfill)), 24)
                text "FULL = MAX DMG" xpos 460 xanchor 1.0 yalign 0.5 size 9 color "#0d1422" bold True
            text ("%d hits%s" % (S["mash_count"], " — MAX RATIO 💥" if S["mash_count"] >= MOGX_MASH_FULL else "")):
                xalign 0.5 size 18 color "#ffffff" bold True
            hbox:
                xalign 0.5 spacing 30
                $ next_j = S["mash_last"] != "j"
                button:
                    xysize (92, 92)
                    background Solid("#241f38" if next_j else "#151b2c")
                    action Function(_mogx_mash_press, "j")
                    if next_j:
                        at mogx_freeze_pulse
                    text "J" xalign 0.5 yalign 0.5 size 38 bold True color ("#ffb347" if next_j else "#5c6473")
                button:
                    xysize (92, 92)
                    background Solid("#241f38" if not next_j else "#151b2c")
                    action Function(_mogx_mash_press, "k")
                    if not next_j:
                        at mogx_freeze_pulse
                    text "K" xalign 0.5 yalign 0.5 size 38 bold True color ("#ffb347" if not next_j else "#5c6473")


screen mogx_nap_panel(S):
    add Solid("#000000a8")
    button:
        xfill True yfill True background None action Function(_mogx_nap_press)
    $ p = min(1.0, S["qte_elapsed"] / MOGX_NAP_DUR)
    frame:
        xalign 0.5 yalign 0.45 xysize (620, 230)
        background Solid("#0d1422f8")
        padding (30, 22)
        vbox:
            xalign 0.5 spacing 14
            text "😴 POWER NAP — STRIKE AT THE SWEET SPOT":
                xalign 0.5 size 20 color "#5eff9d" bold True
            fixed:
                xalign 0.5 xysize (540, 34)
                add Solid("#263149") ypos 6 xysize (540, 22)
                add Solid("#5eff9d50") xpos int(540 * 0.60) ypos 6 xysize (int(540 * 0.30), 22)
                add Solid("#ffd75e") xpos int(540 * 0.7025) ypos 6 xysize (int(540 * 0.095), 22)
                add Solid("#ffffff") xpos int(534 * p) xysize (6, 34)
            button:
                xalign 0.5 xysize (240, 54)
                background Solid("#123524") hover_background Solid("#1b4d34")
                action Function(_mogx_nap_press)
                hbox:
                    xalign 0.5 yalign 0.5 spacing 10
                    frame:
                        xysize (70, 30) padding (0, 0) background Solid("#1b2236")
                        text "SPACE" xalign 0.5 yalign 0.5 size 12 color "#5eff9d" bold True
                    text "STRIKE 😴" yalign 0.5 size 16 color "#ffffff" bold True


screen mogx_mogmax_panel(S):
    add Solid("#000000f2")
    if S["phase"] == "mogmax":
        text "MOGMAX":
            xalign 0.5 ypos 74 size 58 color "#ffffff" bold True at mogx_mogmax_word
        text "👑 DRAW THE M — HIT THE CIRCLES IN ORDER":
            xalign 0.5 ypos 148 size 14 color "#ffd75e" bold True
        # Connecting strokes of the M.
        add Solid("#ffffff30") xpos 458 ypos 360 xysize (190, 5) rotate -57
        add Solid("#ffffff30") xpos 513 ypos 338 xysize (165, 5) rotate 46
        add Solid("#ffffff30") xpos 653 ypos 338 xysize (165, 5) rotate -46
        add Solid("#ffffff30") xpos 728 ypos 360 xysize (190, 5) rotate 57
        for index, point in enumerate(MOGX_OSU_POINTS):
            $ active = index == S["osu_step"]
            $ done = index < S["osu_step"]
            $ node_hit = done and index < len(S["osu_results"]) and S["osu_results"][index]
            button:
                xpos point[0] ypos point[1] xanchor 0.5 yanchor 0.5 xysize (88, 88)
                background Solid("#ffd75e" if active else "#5eff9d" if node_hit else "#ff5d6c" if done else "#ffffff20")
                hover_background Solid("#ffffff" if active else "#ffffff30")
                sensitive active
                action Function(_mogx_osu_press, index)
                if active:
                    at mogx_mogmax_point
                text (("OK" if node_hit else "NAH ❌") if done else str(index + 1)):
                    xalign 0.5 yalign 0.5 size (22 if not done or node_hit else 16) bold True
                    color ("#0d1422" if active or node_hit else "#ffffff")
        if S["osu_step"] < 5:
            $ ring = max(0.0, 1.0 - S["osu_clock"] / MOGX_OSU_WIN)
            add Solid("#ffd75e"):
                xpos MOGX_OSU_POINTS[S["osu_step"]][0] xanchor 0.5
                ypos (MOGX_OSU_POINTS[S["osu_step"]][1] + 56)
                xysize (max(2, int(88 * ring)), 5)
        text ("HITS %d / 5" % S["osu_hits"]):
            xalign 0.5 ypos 580 size 18 color "#5eff9d" bold True
        text "SPACE or click — each circle lasts under a second":
            xalign 0.5 ypos 612 size 12 color "#98a3b8"
    else:
        fixed at mogx_finisher_impact:
            text "MOGMAX":
                xalign 0.5 yalign 0.42 size 104 color "#ffffff" bold True outlines [(5, "#ff5d6c", 0, 0)]
            text ("%d / 5  //  %s" % (S["osu_hits"], "BREAK 💫" if S["stunned"] else "IMPACT")):
                xalign 0.5 yalign 0.62 size 26 color "#ffd75e" bold True


# ----------------------------------------------------------------------
# Coach dialogue box (tutorial)
# ----------------------------------------------------------------------
screen mogx_dialogue(S):
    # Dim the battlefield so the instruction is the only thing that pops.
    add Solid("#000000b4")
    button:
        xfill True yfill True background None
        action Function(_mogx_dlg_advance)
    button:
        # style "empty" — the project gui pins default buttons to 50px tall,
        # which clipped the card and its clickable area to the header strip.
        style "empty"
        xalign 0.5 ypos 350 xsize 660
        background Solid("#0a0f1ef2")
        hover_background Solid("#111b34f2")
        action Function(_mogx_dlg_advance)
        padding (24, 18)
        vbox:
            spacing 8
            text S["config"]["enemy_name"]:
                size 11 color "#ffd75e" bold True
            text S["dlg_text"]:
                size 17 color "#e8ecf8" line_spacing 4
            frame:
                xalign 1.0 padding (12, 7)
                background Solid("#ffd75e")
                text "TAP TO CONTINUE" size 11 color "#0d1422" bold True


# ----------------------------------------------------------------------
# Help overlay
# ----------------------------------------------------------------------
screen mogx_help_overlay():
    modal True
    zorder 220
    add Solid("#050812ee")
    # Swallow clicks so the battle UI underneath stays inert.
    button:
        xfill True yfill True background None
        action Function(_mogx_toggle_help)
    key "K_ESCAPE" action Function(_mogx_toggle_help)
    frame:
        xalign 0.5 yalign 0.5 xysize (680, 600)
        background Solid("#0d1422")
        padding (32, 24)
        vbox:
            spacing 8
            text "❓ How to play" size 26 color "#f7f8fa" bold True
            text "DEFENSE (their turn)" size 12 color "#ffd75e" bold True
            text "• {b}W = PARRY{/b} — tight timing at impact. Negates the hit: +1⚡, +5 Confidence, feeds the Mog Meter, and counters." size 13 color "#aab4c5"
            text "• {b}S = DODGE{/b} — avoids the hit, earns nothing by itself. Take {b}zero hits{/b} across a whole attack — any mix of parries and dodges — and bank {b}+1⚡{/b}." size 13 color "#aab4c5"
            text "• The enemy {b}glows{/b} before a hit: {color=#ff5d6c}{b}RED{/b}{/color} = can't be parried, dodge only. {color=#ffd75e}{b}YELLOW{/b}{/color} = parry or dodge. Watch for feints (delayed swings)." size 13 color "#aab4c5"
            text "• {b}💥 HEAVY swings{/b} wind up slower, dive bigger, and hit much harder — the deep windup is your warning." size 13 color "#aab4c5"
            text "YOUR SKILLS (keys 1-6)" size 12 color "#ffd75e" bold True
            text "• {b}1 Yap 🗣️{/b} — free jab, +1⚡.  {b}2 Mog Stare 😎{/b} (4⚡) — strike while the fast marker is in the gold." size 13 color "#aab4c5"
            text "• {b}3 Galaxy Brain 🧠{/b} (2⚡) — vocab quiz; correct = big damage +1⚡ back." size 13 color "#aab4c5"
            text "• {b}4 Ratio Rush 🤡{/b} (5⚡) — alternate J/K; 8+ hits Embarrasses them (-40% their damage)." size 13 color "#aab4c5"
            text "• {b}5 Power Nap 😴{/b} (3⚡) — heal + cures 😬 CRINGE.  {b}6 MOGMAX 👑{/b} — full meter; draw the M; 4+ circles = BREAK." size 13 color "#aab4c5"
            text "RULES OF THE HALLWAY" size 12 color "#ffd75e" bold True
            text "• Used skills go {b}⏳ on timeout{/b} for one turn — rotate your kit." size 13 color "#aab4c5"
            text "• The {b}👑 Mog Meter{/b} fills from parries and landed hits — and drains when you get hit or flub a minigame." size 13 color "#aab4c5"
            text "• Enemies heal (deny by bursting or BREAKing them), and some hits YOINK your ⚡. Undodgeable 😬 CRINGE weakens every attack AND leaks 1⚡ per turn — lasts 3 turns, or nap it off early." size 13 color "#aab4c5"
            null height 6
            textbutton "CLOSE":
                xalign 0.5 xysize (200, 46)
                background Solid("#1c2740") hover_background Solid("#26365c")
                text_color "#ffffff" text_size 14 text_bold True
                action Function(_mogx_toggle_help)


# ----------------------------------------------------------------------
# Results
# ----------------------------------------------------------------------
screen mogx_results(S):
    add Solid("#030712ed")
    $ result = S["result"]
    $ won = result["outcome"] != "loss"
    frame:
        xalign 0.5 yalign 0.5 xysize (560, 400)
        background Solid("#0d1422")
        padding (38, 30)
        vbox:
            xalign 0.5 spacing 14
            text ("RATIO'D 💀" if not won else "TRAINING COMPLETE 📈" if result["outcome"] == "tutorial" else "VICTORY 👑"):
                xalign 0.5 size 38 italic True bold True
                color ("#ff5d6c" if not won else "#ffd75e")
            text S["message"]:
                xalign 0.5 text_align 0.5 xmaximum 470 size 14 color "#d7dceb"
            hbox:
                xalign 0.5 spacing 26
                vbox:
                    text "PARRIES" xalign 0.5 size 10 color "#8f9b95" bold True
                    text str(result["parries"]) xalign 0.5 size 26 color "#6db1ff" bold True
                vbox:
                    text "PERFECT STRIKES" xalign 0.5 size 10 color "#8f9b95" bold True
                    text str(result["perfect_attacks"]) xalign 0.5 size 26 color "#5eff9d" bold True
                vbox:
                    text "HITS TAKEN" xalign 0.5 size 10 color "#8f9b95" bold True
                    text str(result["hits_taken"]) xalign 0.5 size 26 color "#ff5d6c" bold True
            if won and result["outcome"] == "win":
                $ grade_text, grade_color = _mogx_grade(S["stats"])
                text ("GRADE: %s" % grade_text):
                    xalign 0.5 size 16 color grade_color bold True
            null height 6
            if not won:
                textbutton "🔄 RUN IT BACK":
                    xalign 0.5 xysize (250, 54)
                    background Solid("#5c1a24") hover_background Solid("#7a2331")
                    text_color "#ffffff" text_size 16 text_bold True
                    action Function(_mogx_retry)
            else:
                textbutton "CONTINUE":
                    xalign 0.5 xysize (250, 54)
                    background Solid("#157a55") hover_background Solid("#20a775")
                    text_color "#ffffff" text_size 16 text_bold True
                    action Return(S["result"])
