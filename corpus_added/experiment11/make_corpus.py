"""Experiment 11: the Experiment 6 corpus with every sentence that check_corpus.py
flags as a WARNING removed (an answer word next to a content word of its own prompt, or
3 consecutive prompt tokens with 2 content words). Run from the repository root:
python corpus_added/experiment11/make_corpus.py
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
STOP = set("the a an is are was were am of to in at and or it its he she they them his her we our you your "
           "this that these those for from with by on into up down not did do does who which what be been "
           "then after before . , ? ! ' one first last".split())
tok = lambda t: re.findall(r"\w+(?:['’]\w+)*|[^\w\s]", t.lower())
suite = json.load(open(ROOT / "evals/language_evals.json", encoding="utf-8"))["cases"]
cases = []
for c in suite:
    pt = tok(c["prompt"])
    content = {t for t in pt + [c["answer"]] if t not in STOP and t.isalpha()}
    cases.append((c["answer"], content, {tuple(pt[i:i+3]) for i in range(len(pt)-2)}))

def warned(sentence):
    tk = tok(sentence); tkset = set(tk); tri = {tuple(tk[i:i+3]) for i in range(len(tk)-2)}
    for ans, content, ptri in cases:
        if any(sum(w not in STOP for w in t) >= 2 for t in tri & ptri):
            return True
        if ans in tkset and (content - {ans}) & tkset:
            return True
    return False

kept = removed = 0
for folder in [ROOT / "corpus", HERE]:
    for old in folder.glob("*.txt"):
        old.unlink()
for f in sorted((ROOT / "corpus_added/experiment6").glob("*.txt")):
    lines = [l for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
    keep = [l for l in lines if not warned(l)]
    removed += len(lines) - len(keep); kept += len(keep)
    for folder in [ROOT / "corpus", HERE]:
        (folder / f.name).write_text("\n".join(keep) + "\n", encoding="utf-8")
    print(f.name, len(lines), "->", len(keep))
print("kept", kept, "removed", removed)
