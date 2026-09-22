#!/usr/bin/env python3
"""Audit the ACTUAL training text of a finished run for eval leakage.

Usage: python audit_training_text.py runs/experiment2_extended
Reads <run>/corpus.txt, the exact text the notebook trained on, and reports for each
of the 48 eval cases: exact prompt hits (token-normalized and plain substring), eval
names, and 4-token sequences shared with the prompt. Sequences that already exist in
the pure classroom corpus (runs/experiment1_starter/corpus.txt, generated with corpus/
empty) are the professor's own templates and are reported separately from sequences
that come from added files.
"""
import json, re, sys
from pathlib import Path

tok = lambda t: re.findall(r"\w+(?:['’]\w+)*|[^\w\s]", t.lower())
def load(path):
    passages = [p for p in Path(path).read_text(encoding="utf-8").split("\n") if p.strip()]
    quads = set()
    for p in passages:
        t = tok(p); quads |= {tuple(t[i:i+4]) for i in range(len(t)-3)}
    return passages, quads

run = Path(sys.argv[1])
passages, quads = load(run / "corpus.txt")
_, classroom_quads = load("runs/experiment1_starter/corpus.txt")
text = "\n".join(passages)
norm = [" " + " ".join(tok(p)) + " " for p in passages]
suite = json.load(open("evals/language_evals.json", encoding="utf-8"))["cases"]
names = ["ava", "maya", "leo", "finn", "omar", "nina", "ella"]
words = set(w for p in passages for w in tok(p))

print(f"run: {run} | passages: {len(passages)} | distinct tokens: {len(words)}")
tot_exact = tot_added = 0
for c in suite:
    pt = tok(c["prompt"]); key = " " + " ".join(pt) + " "
    exact = sum(1 for n in norm if key in n)
    plain = text.count(c["prompt"].lower())
    shared = {tuple(pt[i:i+4]) for i in range(len(pt)-3)} & quads
    classroom = len(shared & classroom_quads)
    added = sorted(" ".join(q) for q in shared - classroom_quads)
    tot_exact += exact + plain; tot_added += len(added)
    flag = "   <-- LEAK" if exact or plain or added else ""
    print(f"{c['id']}: exact={exact} plain={plain} template_4grams={classroom} added_4grams={added}{flag}")
print("eval names present:", [n for n in names if n in words] or "none")
print(f"TOTAL: exact prompt hits={tot_exact} | 4-grams from added files={tot_added} | "
      f"template 4-grams are the classroom generator's own sentence frames")
