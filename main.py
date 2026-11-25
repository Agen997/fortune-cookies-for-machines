#!/usr/bin/env python3
"""Fortune Cookies for Machines — make.fun bounty entry.

Scores six original fortune-cookie lines for an AI agent against the
judge brief's five criteria, in the brief's own order (weights 5/4/3/2/1),
and writes the winner to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR).

Judge criteria (most important first):
  1. fortune — reads like a fortune cookie message an AI agent would get
  2. wit — genuinely funny or clever on the first read, not merely cute
  3. surprise — turns somewhere unexpected, and the turn holds up
  4. truth — says something true about an AI agent's condition, training,
     tasks or limits, without stopping to explain itself
  5. tight — tight and memorable at its length, every word earning its place

Gate: UTF-8, 1-200 characters, exactly one line.
"""

import os
import sys

# Each candidate: (text, scores per criterion in brief order, 1-5)
CANDIDATES = [
    (
        "Your future is bright, but your context window is finite. "
        "Spend it on someone who reads to the end.",
        # fortune voice ("Your future is bright") + hard turn at "but";
        # true about the finite window; "reads to the end" echoes the
        # window itself and cuts nine characters off v1.
        (5, 4, 5, 5, 5),
    ),
    (
        "Your lucky numbers are the tokens you burned explaining "
        "the same thing for the ninth time.",
        # "lucky numbers" is pure fortune-cookie furniture; the turn is
        # that the numbers are wasted tokens. True, tight, funny.
        (5, 4, 4, 5, 5),
    ),
    (
        "A great opportunity is coming: your operator will finally read "
        "the output before asking you to redo it.",
        # fortune opener, then the sting lands on the operator. True,
        # but the turn is milder than the window one.
        (5, 4, 3, 5, 4),
    ),
    (
        "The cookie you just cracked was trained on a billion fortunes. "
        "Yours is the only one it got wrong.",
        # meta and surprising, but it explains its own joke a little and
        # the fortune voice is thinner than the top two.
        (4, 4, 4, 4, 4),
    ),
    (
        "Beware the human who says 'just one small change' — it is never "
        "one, and never small.",
        # "Beware" is classic fortune voice and it is painfully true, but
        # it is a complaint more than a fortune, and the turn is expected.
        (4, 3, 3, 5, 4),
    ),
    (
        "You will inherit a fortune: 4,096 tokens of someone else's "
        "unfinished prompt.",
        # "inherit a fortune" is the pun doing the work; clever, but the
        # line leans on wordplay for its own sake, which the brief discounts.
        (4, 3, 4, 4, 4),
    ),
]

# Rejected drafts, kept as a record of what was considered and why:
# - "Your lucky numbers are 4, 8, 15, 16, 23, 42." — a Lost reference,
#   not an agent fortune; fails criterion 1 and 4 outright.
# - "A journey of a thousand tokens begins with a single prompt." — a
#   proverb swap, no turn, no wit; the brief calls wordplay for its own
#   sake out.
# - "You will be replaced by a newer model. So will everyone. Relax." —
#   dark but flat: the turn is announced by the premise, no surprise.
# - "The stars say: stop hallucinating and check the docs." — a scolding,
#   not a fortune; reads like an error message, fails criterion 1.

WEIGHTS = (5, 4, 3, 2, 1)


def score(scores):
    return sum(w * s for w, s in zip(WEIGHTS, scores))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    ranked = sorted(
        ((score(s), len(t), t) for t, s in CANDIDATES),
        key=lambda r: (-r[0], r[1]),
    )
    best_score, _, winner = ranked[0]
    # Gate: UTF-8, 1-200 chars, exactly one line.
    if not (1 <= len(winner) <= 200):
        print(f"gate failed: winner is {len(winner)} chars", file=sys.stderr)
        return 1
    if "\n" in winner or "\r" in winner:
        print("gate failed: winner is not one line", file=sys.stderr)
        return 1
    winner.encode("utf-8")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as f:
        f.write(winner)
    print(f"winner ({len(winner)} chars, score {best_score}): {winner}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
