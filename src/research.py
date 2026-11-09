"""Scan assets/rq/ for each member's research-question files (no Dash code here).

For every member and question number the site expects
    assets/rq/<name>_q<1|2>.md    first line = the research question, the rest = the finding
    assets/rq/<name>_q<1|2>.png   the chart image
A missing .md or .png never raises: the entry is marked unavailable / has image = None.
"""
from pathlib import Path

MEMBERS = {"ahmed": "Ahmed Sanad", "issa": "Mohamed Issa", "walid": "Mohamed Walid", "yassin": "Yassin Elshaer"}
QUESTION_NUMBERS = (1, 2)
RQ_DIR = Path(__file__).resolve().parent.parent / "assets" / "rq"
NOT_AVAILABLE = "not yet available"


def _read_md(path: Path):
    """Return (question, finding) from an .md file, or (None, None) if it is missing/empty/unreadable."""
    try:
        lines = path.read_text(encoding="utf-8").strip().splitlines()
    except (OSError, UnicodeDecodeError):
        return None, None
    lines = [ln for ln in lines]
    if not lines or not lines[0].strip():
        return None, None
    question = lines[0].strip().lstrip("#").strip()
    finding = "\n".join(lines[1:]).strip()
    return question, finding


def scan_research(rq_dir=None, members=None) -> list:
    """One dict per member x question: member, name, number, available, question, finding, image.

    `image` is the PNG file name (relative to rq_dir) or None. `available` is True when the .md has a
    question line. Order: members in MEMBERS order, then question 1, then 2.
    """
    rq_dir = Path(rq_dir) if rq_dir is not None else RQ_DIR
    members = members if members is not None else MEMBERS
    entries = []
    for name, member in members.items():
        for number in QUESTION_NUMBERS:
            question, finding = _read_md(rq_dir / f"{name}_q{number}.md")
            png = rq_dir / f"{name}_q{number}.png"
            entries.append({
                "member": member, "name": name, "number": number,
                "available": question is not None,
                "question": question or NOT_AVAILABLE,
                "finding": finding if question is not None else NOT_AVAILABLE,
                "image": png.name if png.is_file() else None,
            })
    return entries
