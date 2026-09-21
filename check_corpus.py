#!/usr/bin/env python3
"""check_corpus.py  -  eval-leakage guardrail for the Class 4 custom LLM assignment.

Run BEFORE every training run:   python3 check_corpus.py
Exit code 0 = safe to train.  Exit code 1 = fix corpus/ first.

What it checks (stricter than the notebook's own exact-match guard):
 1. evals/language_evals.json is byte-identical to the pinned checksum in custom_llm.py.
 2. CORPUS_FOLDER in custom_llm.py is exactly "corpus".
 3. Every .txt/.md/.pdf under corpus/ (recursively) passes the notebook's exact-prompt check.
 4. FUZZY: 4+ consecutive tokens of any eval prompt = error; 3 with 2 content words = warning.
 5. FUZZY: any passage that contains 3+ distinct content words from one eval case
    (prompt + answer, stopwords removed). Catches paraphrases like "ava bought milk".
 6. Any eval proper name (ava, maya, leo, finn, omar, nina, ella) in corpus/.
 7. WARNING when an eval answer appears next to a content word of its own prompt.
 8. Nothing under corpus/ was copied from examples/ (hash compare with examples/reference/corpus.txt).
Prints a DO-NOT-USE list you can hand to whoever writes teaching sentences.
"""
import hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SUITE = ROOT / "evals" / "language_evals.json"
CORPUS = ROOT / "corpus"
STOP = set("the a an is are was were am of to in at and or it its he she they them his her we our you your "
           "this that these those for from with by on into up down not did do does who which what be been "
           "then after before . , ? ! ' one first last".split())

def tokens(t):
    return re.findall(r"\w+(?:['’]\w+)*|[^\w\s]", t.lower())

def passages(text):
    return [u for u in re.split(r"(?<=[.!?])\s+|\n+", text) if u.strip()]

def read_text(p):
    if p.suffix.lower() == ".pdf":
        try:
            from pypdf import PdfReader
            return "\n".join((pg.extract_text() or "") for pg in PdfReader(str(p)).pages)
        except Exception as e:
            return f"[[PDF NOT READABLE: {e}]]"
    return p.read_text(encoding="utf-8", errors="replace")

def ngrams(tk, n):
    return {tuple(tk[i:i+n]) for i in range(len(tk)-n+1)}

problems, warnings = [], []
def bad(msg): problems.append(msg)
def warn(msg): warnings.append(msg)

# 1. suite integrity
src = (ROOT / "custom_llm.py").read_text(encoding="utf-8") if (ROOT / "custom_llm.py").exists() else ""
m = re.search(r"'evals/language_evals\.json':\s*'([0-9a-f]{64})'", src)
suite_sha = hashlib.sha256(SUITE.read_bytes()).hexdigest()
if m and m.group(1) != suite_sha:
    bad(f"evals/language_evals.json checksum {suite_sha[:12]} != pinned {m.group(1)[:12]}. Restore the original suite.")
# 2. corpus folder setting
cf = re.search(r'^CORPUS_FOLDER\s*=\s*"([^"]+)"', src, re.M)
if cf and cf.group(1) != "corpus":
    bad(f'CORPUS_FOLDER is "{cf.group(1)}". It must be "corpus".')

suite = json.load(open(SUITE, encoding="utf-8"))["cases"]
names = {"ava", "maya", "leo", "finn", "omar", "nina", "ella"}
case_info = []
for c in suite:
    ptk = tokens(c["prompt"])
    content = {t for t in ptk + [c["answer"]] if t not in STOP and t.isalpha()}
    case_info.append((c["id"], ptk, c["answer"], content, ngrams(ptk, 3), ngrams(ptk, 4)))

# 8. examples copy check
ref = ROOT / "examples" / "reference" / "corpus.txt"
ref_sha = hashlib.sha256(ref.read_bytes()).hexdigest() if ref.exists() else None

files = [p for p in CORPUS.rglob("*") if p.is_file() and p.suffix.lower() in {".txt", ".md", ".pdf"}
         and p.name != "README.md" and not p.name.startswith(".")]
if not files:
    print("corpus/ has no files yet (that is fine for the starter experiment).")
for f in files:
    if ref_sha and hashlib.sha256(f.read_bytes()).hexdigest() == ref_sha:
        bad(f"{f.relative_to(ROOT)} is a copy of examples/reference/corpus.txt. Delete it.")
    text = read_text(f)
    if text.startswith("[[PDF NOT READABLE"):
        bad(f"{f.relative_to(ROOT)}: {text}")
        continue
    for i, ps in enumerate(passages(text), 1):
        tk = tokens(ps)
        tkset = set(tk)
        tri = ngrams(tk, 3)
        hit_names = names & tkset
        if hit_names:
            bad(f"{f.name} passage {i}: uses eval name(s) {sorted(hit_names)}: \"{ps.strip()[:80]}\"")
        for cid, ptk, ans, content, ptri, pquad in case_info:
            norm = " " + " ".join(tk) + " "
            snippet = f"{f.name} passage {i}"
            if " " + " ".join(ptk) + " " in norm:
                bad(f"{snippet}: EXACT eval prompt {cid}: \"{ps.strip()[:80]}\"")
            elif ngrams(tk, 4) & pquad:
                bad(f"{snippet}: 4+ consecutive tokens of {cid}: \"{ps.strip()[:80]}\"")
            elif len(content & tkset) >= 3:
                bad(f"{snippet}: paraphrase of {cid}, shares {sorted(content & tkset)}: \"{ps.strip()[:80]}\"")
            else:
                strong_tri = [t for t in (tri & ptri) if sum(w not in STOP for w in t) >= 2]
                if strong_tri:
                    warn(f"{snippet}: 3 consecutive tokens of {cid} ({' '.join(strong_tri[0])}): \"{ps.strip()[:80]}\"")
                elif ans in tkset and len((content - {ans}) & tkset) >= 1:
                    warn(f"{snippet}: answer '{ans}' of {cid} next to its prompt word(s) {sorted((content - {ans}) & tkset)}: \"{ps.strip()[:80]}\"")

print("=" * 70)
print("DO-NOT-USE while writing teaching sentences:")
print("  names:", ", ".join(sorted(names)))
print("  exact prompts (never write these token sequences):")
for cid, ptk, ans, _, _, _ in case_info:
    print(f"    {cid}: {' '.join(ptk)}  ->  {ans}")
print("  Teach the PATTERN with other subjects, objects, names and places.")
print("=" * 70)
if warnings:
    print(f"\n{len(warnings)} WARNING(S), review by hand (allowed if wording and situation are clearly different):")
    for w in warnings: print(" ~", w)
if problems:
    print(f"\n{len(problems)} PROBLEM(S). DO NOT TRAIN.\n")
    for p in problems: print(" -", p)
    sys.exit(1)
print(f"\nOK: {len(files)} corpus file(s) checked, suite intact, CORPUS_FOLDER=corpus. Safe to train.")
