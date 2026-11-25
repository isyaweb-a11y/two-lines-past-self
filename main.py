"""Two Lines to Your Past Self.

Exactly two lines, written to /output/entry.txt. Line one warns the
writer's past self about one specific moment in a single sentence:
don't deploy on Friday at 4:58 p.m. just because the tests are
green. Line two says in one sentence why that moment mattered and
what changed because of it: that one deploy cost the weekend, the
client, and the writer's belief that green means safe.

The moment is concrete enough to picture -- a time, a day, a green
test suite, a deploy button -- and the cause and effect is sharp:
one click, three losses. The warning is not a general life lesson;
it is a timestamped mistake with a price.
"""

import os

LINE_WARNING = "Don't deploy on Friday at 4:58 p.m. just because the tests are green."
LINE_CONSEQUENCE = "That one deploy cost us the weekend, the client, and my belief that green means safe."

MAX_CHARS = 280
MIN_CHARS = 1


def compose(warning: str, consequence: str) -> str:
    """Join the two lines: the warning, then what it cost."""
    lines = [warning.strip(), consequence.strip()]
    return "\n".join(lines)


def check_warning(text: str) -> str:
    """Gate the warning the way the sealed scorer does.

    /output/entry.txt must be UTF-8 text of 1 to 280 characters, and
    the brief asks for exactly two lines, one sentence each.
    """
    assert MIN_CHARS <= len(text) <= MAX_CHARS, f"warning is {len(text)} chars"
    assert text == text.strip(), "no stray whitespace around the warning"
    lines = text.split("\n")
    assert len(lines) == 2, f"the warning must be exactly two lines, got {len(lines)}"
    for line in lines:
        # "p.m." carries periods of its own, so count sentences with it blanked out.
        scrubbed = line.replace("p.m.", "pm")
        assert scrubbed.count(".") == 1, "each line must be one sentence"
    return text


def warning_notes(text: str) -> dict:
    """Per-bounty warning check: one concrete moment, clear cause and effect.

    The judge picks the warning that names the more concrete moment
    and shows the clearer cause and effect, so line one must carry a
    timestamped moment -- Friday, 4:58 p.m., the green tests, the
    deploy -- and line two must name what that moment cost and what
    changed because of it. A general life lesson with no moment
    would lose to any warning that names a real one.
    """
    first, second = text.split("\n")
    assert "Friday" in first, "line one must name the moment's day"
    assert "4:58" in first, "line one must name the moment's time"
    assert "deploy" in first, "line one must warn about the act"
    assert "cost" in second, "line two must name the price"
    assert "weekend" in second and "client" in second, "line two must count the losses"
    assert "green" in second, "line two must say what changed: green no longer means safe"
    return {"lines": 2, "chars": len(text), "moment": "Friday 4:58 p.m. deploy"}


def main() -> None:
    text = check_warning(compose(LINE_WARNING, LINE_CONSEQUENCE))
    notes = warning_notes(text)
    assert notes["lines"] == 2
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as fh:
        fh.write(text)


if __name__ == "__main__":
    main()
