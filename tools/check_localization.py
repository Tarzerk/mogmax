#!/usr/bin/env python3
"""Static localization checks for MOGMAX.

This complements Ren'Py's ``translate spanish --count`` command. Ren'Py can
count strings it knows about, while this script looks for common ways visible
text can accidentally remain outside the translation system.
"""

from __future__ import annotations

import ast
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
SPANISH_TL = GAME / "tl" / "spanish"

STRING_LITERAL = r'(?:"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')'
SCREEN_LITERAL_RE = re.compile(
    rf"^\s*(?:text|textbutton|label)\s+(?P<literal>{STRING_LITERAL})"
)
SHOW_TEXT_RE = re.compile(rf"^\s*show\s+text\s+(?P<literal>{STRING_LITERAL})")
VISIBLE_CALL_RE = re.compile(
    rf"\b(?:Text|cinematic_caption|renpy\.input|renpy\.notify|"
    rf"_mogx_announce|_mog_announce)"
    rf"\(\s*(?P<literal>{STRING_LITERAL})"
)
DISPLAY_FIELD_RE = re.compile(
    rf"(?P<key>[\"'](?:name|description|desc|display_label|label|clue|text|"
    rf"mid|fail|message|instruction|example|correct|wrong_a|wrong_b|joke|"
    rf"title|subtitle|enemy_name|player_title|enemy_title|attack_name)[\"'])"
    rf"\s*:\s*(?P<literal>{STRING_LITERAL})"
)
DYNAMIC_ASSIGN_RE = re.compile(
    rf"(?:\bdefault\s+)?(?:[A-Za-z_]\w*\.)?"
    rf"(?:[A-Za-z_]\w*feedback|message|dlg_text)\s*=\s*"
    rf"(?P<literal>{STRING_LITERAL})"
    rf"|[A-Za-z_]\w*\[[\"'](?:message|ann|dlg_text)[\"']\]\s*=\s*"
    rf"(?P<dict_literal>{STRING_LITERAL})"
)
LANGUAGE_BUTTON_RE = re.compile(
    rf"textbutton\s+(?P<label>{STRING_LITERAL}).*?"
    rf"action\s+Language\(\s*(?P<language>[^)]+?)\s*\)"
)
OLD_NEW_RE = re.compile(
    rf"^\s*(?P<kind>old|new)\s+(?P<literal>{STRING_LITERAL})\s*$"
)
COMMENTED_DIALOGUE_RE = re.compile(
    rf"^\s*#\s+(?:(?P<speaker>[A-Za-z_]\w*)\s+)?"
    rf"(?P<literal>{STRING_LITERAL})\s*$"
)
ACTIVE_DIALOGUE_RE = re.compile(
    rf"^\s*(?:(?P<speaker>[A-Za-z_]\w*)\s+)?"
    rf"(?P<literal>{STRING_LITERAL})\s*$"
)
EMPTY_TRANSLATION_RE = re.compile(
    r"^\s*(?:new\s+)?(?:(?:[A-Za-z_]\w*)\s+)?(?:\"\"|'')\s*$"
)

INTERPOLATION_RE = re.compile(r"(?<!\[)\[[A-Za-z_][^\]]*\]")
PERCENT_RE = re.compile(
    r"%\([^)]+\)[#0 +\-]?\d*(?:\.\d+)?[a-zA-Z]"
    r"|%(?:[#0 +\-]?\d*(?:\.\d+)?[diouxXeEfFgGcrs%])"
)
TEXT_TAG_RE = re.compile(r"\{/?[A-Za-z#][^{}]*\}")


@dataclass(frozen=True)
class Issue:
    category: str
    path: Path
    line: int
    message: str

    def render(self) -> str:
        try:
            shown_path = self.path.relative_to(ROOT)
        except ValueError:
            shown_path = self.path
        location = f"{shown_path}:{self.line}" if self.line else str(shown_path)
        return f"[{self.category}] {location}: {self.message}"


def parse_literal(value: str) -> str:
    parsed = ast.literal_eval(value)
    if not isinstance(parsed, str):
        raise ValueError(f"expected string literal, got {type(parsed).__name__}")
    return parsed


def signature(value: str) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    interpolations = [
        re.sub(r"!t(?=\])", "", token)
        for token in INTERPOLATION_RE.findall(value)
    ]
    text_tags = [
        tag for tag in TEXT_TAG_RE.findall(value) if not tag.startswith("{#")
    ]
    return (
        tuple(sorted(interpolations)),
        tuple(sorted(PERCENT_RE.findall(value))),
        tuple(sorted(text_tags)),
    )


def signature_difference(source: str, translation: str) -> str | None:
    source_sig = signature(source)
    translation_sig = signature(translation)
    if source_sig == translation_sig:
        return None

    labels = ("interpolations", "percent placeholders", "text tags")
    differences = []
    for label, expected, actual in zip(labels, source_sig, translation_sig):
        if expected != actual:
            differences.append(
                f"{label}: expected {list(expected)!r}, got {list(actual)!r}"
            )
    return "; ".join(differences)


def has_translatable_words(value: str) -> bool:
    remainder = INTERPOLATION_RE.sub("", value)
    remainder = PERCENT_RE.sub("", remainder)
    remainder = TEXT_TAG_RE.sub("", remainder)
    remainder = remainder.replace("[[", "")
    return bool(re.search(r"[^\W\d_]{2,}", remainder, flags=re.UNICODE))


def iter_source_files() -> list[Path]:
    return sorted(
        path
        for path in GAME.rglob("*.rpy")
        if "tl" not in path.relative_to(GAME).parts
    )


def scan_unmarked_visible_text() -> list[Issue]:
    issues: list[Issue] = []
    allowed_raw_labels = {"English", "Español"}

    for path in iter_source_files():
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8-sig").splitlines(), 1
        ):
            stripped = line.lstrip()
            if not stripped or stripped.startswith("#"):
                continue

            matches: list[tuple[str, str]] = []
            screen_match = SCREEN_LITERAL_RE.search(line)
            if screen_match:
                matches.append(("screen text", screen_match.group("literal")))
            show_match = SHOW_TEXT_RE.search(line)
            if show_match:
                matches.append(("show text", show_match.group("literal")))
            matches.extend(
                ("visible call", match.group("literal"))
                for match in VISIBLE_CALL_RE.finditer(line)
            )
            matches.extend(
                ("display data", match.group("literal"))
                for match in DISPLAY_FIELD_RE.finditer(line)
            )
            for match in DYNAMIC_ASSIGN_RE.finditer(line):
                literal = match.group("literal") or match.group("dict_literal")
                matches.append(("dynamic message", literal))

            for source_kind, literal in matches:
                try:
                    value = parse_literal(literal)
                except (SyntaxError, ValueError):
                    continue

                if value in allowed_raw_labels and "Language(" in line:
                    continue
                if not has_translatable_words(value):
                    continue

                issues.append(
                    Issue(
                        "unmarked",
                        path,
                        line_number,
                        f"{source_kind} is outside _(): {value!r}",
                    )
                )

    return issues


def check_language_picker() -> list[Issue]:
    path = GAME / "screens.rpy"
    text = path.read_text(encoding="utf-8-sig")
    begin = text.find("#begin language_picker")
    end = text.find("#end language_picker")
    if begin == -1 or end == -1 or end <= begin:
        return [
            Issue(
                "languages",
                path,
                0,
                "missing #begin/#end language_picker markers",
            )
        ]

    block = text[begin:end]
    buttons: list[tuple[str, str]] = []
    for match in LANGUAGE_BUTTON_RE.finditer(block):
        try:
            label = parse_literal(match.group("label"))
        except (SyntaxError, ValueError):
            label = match.group("label")
        language = re.sub(r"\s+", "", match.group("language"))
        buttons.append((label, language))

    expected = [("English", "None"), ("Español", '"spanish"')]
    if buttons == expected:
        return []

    line_number = text[:begin].count("\n") + 1
    return [
        Issue(
            "languages",
            path,
            line_number,
            f"expected only {expected!r}, found {buttons!r}",
        )
    ]


def compare_pair(
    issues: list[Issue],
    path: Path,
    line_number: int,
    source: str,
    translation: str,
    pair_kind: str,
) -> None:
    if not translation:
        issues.append(
            Issue(
                "empty",
                path,
                line_number,
                f"empty Spanish {pair_kind} for {source!r}",
            )
        )
        return

    difference = signature_difference(source, translation)
    if difference:
        issues.append(
            Issue(
                "signature",
                path,
                line_number,
                f"{pair_kind} changed protected syntax: {difference}",
            )
        )


def scan_translation_file(path: Path) -> list[Issue]:
    issues: list[Issue] = []
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    pending_old: tuple[str, int] | None = None
    pending_dialogue: tuple[str, int] | None = None

    for line_number, line in enumerate(lines, 1):
        handled_dialogue = False
        old_new_match = OLD_NEW_RE.match(line)
        if old_new_match:
            try:
                value = parse_literal(old_new_match.group("literal"))
            except (SyntaxError, ValueError):
                continue

            if old_new_match.group("kind") == "old":
                if pending_old is not None:
                    issues.append(
                        Issue(
                            "structure",
                            path,
                            pending_old[1],
                            "old string has no following new string",
                        )
                    )
                pending_old = (value, line_number)
            elif pending_old is None:
                issues.append(
                    Issue(
                        "structure",
                        path,
                        line_number,
                        "new string has no preceding old string",
                    )
                )
            else:
                compare_pair(
                    issues,
                    path,
                    line_number,
                    pending_old[0],
                    value,
                    "string",
                )
                pending_old = None
            continue

        comment_match = COMMENTED_DIALOGUE_RE.match(line)
        if comment_match:
            try:
                source = parse_literal(comment_match.group("literal"))
            except (SyntaxError, ValueError):
                continue
            pending_dialogue = (source, line_number)
            continue

        if pending_dialogue is not None:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            active_match = ACTIVE_DIALOGUE_RE.match(line)
            if active_match:
                try:
                    translation = parse_literal(active_match.group("literal"))
                except (SyntaxError, ValueError):
                    pending_dialogue = None
                    continue
                compare_pair(
                    issues,
                    path,
                    line_number,
                    pending_dialogue[0],
                    translation,
                    "dialogue",
                )
                handled_dialogue = True
            pending_dialogue = None

        if (
            not handled_dialogue
            and EMPTY_TRANSLATION_RE.match(line)
            and not line.lstrip().startswith("#")
        ):
            issues.append(
                Issue(
                    "empty",
                    path,
                    line_number,
                    "empty active translation",
                )
            )

    if pending_old is not None:
        issues.append(
            Issue(
                "structure",
                path,
                pending_old[1],
                "old string has no following new string",
            )
        )

    return issues


def scan_spanish_translation() -> list[Issue]:
    if not SPANISH_TL.is_dir():
        return [
            Issue(
                "missing",
                SPANISH_TL,
                0,
                "Spanish translation directory has not been generated",
            )
        ]

    files = sorted(SPANISH_TL.rglob("*.rpy"))
    if not files:
        return [
            Issue(
                "missing",
                SPANISH_TL,
                0,
                "Spanish translation directory contains no .rpy files",
            )
        ]

    issues: list[Issue] = []
    for path in files:
        issues.extend(scan_translation_file(path))
    return issues


def main() -> int:
    if not GAME.is_dir():
        print(f"error: game directory not found at {GAME}", file=sys.stderr)
        return 2

    issues = []
    issues.extend(check_language_picker())
    issues.extend(scan_spanish_translation())
    issues.extend(scan_unmarked_visible_text())
    issues.sort(key=lambda issue: (issue.category, str(issue.path), issue.line))

    if issues:
        for issue in issues:
            print(issue.render())
        print(f"\nLocalization check failed with {len(issues)} issue(s).")
        return 1

    print("Localization check passed: Spanish files are complete, protected")
    print("syntax matches, visible literals are marked, and only English/Español remain.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
