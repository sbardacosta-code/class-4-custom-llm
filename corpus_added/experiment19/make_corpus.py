"""Experiment 19: about twice the Experiment 14 generated corpus (higher sampling rates) restricted to the Experiment 6 vocabulary.

Run from the repository root:  python corpus_added/experiment14/make_corpus.py
Builds about 5,000 sentences by combining sentence frames with word lists. Every word
is checked against the Experiment 6 vocabulary (runs/experiment6_coverage/checkpoint.json),
so the run adds no new word types and the 509-type cap cuts nothing that E6 kept.
Frames reuse the eight teaching categories; the do-not-use names and prompt sequences
are never produced (check_corpus.py verifies the output before training). The eight
Experiment 6 files are written alongside, so the corpus is E6 plus this file.
"""
import itertools, json, random, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
tok = lambda t: re.findall(r"\w+(?:['’]\w+)*|[^\w\s]", t.lower())
VOC = set(json.load(open(ROOT / "runs/experiment6_coverage/checkpoint.json", encoding="utf-8"))["vocabulary"])
rng = random.Random(19)

people = ["the boy", "the girl", "the nurse", "the farmer", "the driver", "the teacher", "my uncle",
          "my aunt", "my sister", "the student", "the child", "the cook"]
pron = {"the boy": "he", "the girl": "she", "the nurse": "she", "the farmer": "he", "the driver": "he",
        "the teacher": "she", "my uncle": "he", "my aunt": "she", "my sister": "she", "the student": "he",
        "the child": "she", "the cook": "he"}
places = ["at the market", "at the station", "in the garden", "by the river", "at the school",
          "in the kitchen", "at the bank", "in the park", "at the beach", "in the barn", "at the office",
          "on the roof"]
things = ["cup", "plate", "hat", "shirt", "coat", "bag", "box", "key", "book", "letter", "ball", "lamp",
          "spoon", "shoe", "pillow", "scarf", "kite", "chair"]
colors = ["red", "blue", "green", "white", "black", "brown", "grey", "yellow"]
sizes = [("big", "small"), ("heavy", "light"), ("wet", "dry"), ("hot", "cold"), ("full", "empty"),
         ("noisy", "quiet"), ("clean", "dirty"), ("old", "new"), ("long", "short"), ("open", "closed")]
foods = ["bread", "cheese", "rice", "soup", "coffee", "juice", "beans", "grapes", "apples", "fish", "cake"]
animals = [("cat", "cats"), ("dog", "dogs"), ("horse", "horses"), ("cow", "cows"), ("goat", "goats"),
           ("duck", "ducks"), ("frog", "frogs"), ("bird", "birds")]
past = [("walk", "walked"), ("cook", "cooked"), ("play", "played"), ("visit", "visited"),
        ("paint", "painted"), ("talk", "talked"), ("clean", "cleaned"), ("wash", "washed")]
objects_for = {"walk": "to the market", "cook": "dinner", "play": "football", "visit": "the museum",
               "paint": "the fence", "talk": "about rivers", "clean": "the kitchen", "wash": "the car"}

out = []
# grammar: singular/plural agreement and past tense
for (s, p), place in itertools.product(animals, places):
    if s == "bird" or p == "dogs":
        out += [f"a {s} is {place} .", f"two {p} are {place} .", f"three {p} were {place} ."]
    else:
        out += [f"one {s} is {place} .", f"the {s} is {place} .", f"the {p} are {place} .",
                f"two {p} were {place} ."]
for who, (v, vd) in itertools.product(people, past):
    o = objects_for[v]
    out += [f"yesterday {who} {vd} {o} .", f"today {who} {v}s {o} and yesterday {who} {vd} {o} too ."]
# opposites in contrast frames and "the opposite of" frames with safe pairs
for (a, b), t1, t2 in itertools.product(sizes, things, things):
    if t1 != t2 and rng.random() < 0.8:
        out += [f"the {t1} is {a} but the {t2} is {b} ."]
for a, b in [("big", "small"), ("fast", "slow"), ("tall", "short"), ("young", "old"), ("strong", "weak"),
             ("soft", "hard"), ("wide", "narrow"), ("clean", "dirty"), ("high", "low"), ("thick", "thin"),
             ("sweet", "sour"), ("happy", "sad"), ("near", "far"), ("early", "late"), ("rich", "poor"),
             ("wet", "dry"), ("day", "night"), ("loud", "silent"), ("warm", "cool"), ("heavy", "light")]:
    out += [f"the opposite of {a} is {b} .", f"the opposite of {b} is {a} .", f"{a} and {b} are opposites .",
            f"when it is not {a} it is {b} .", f"if a thing is not {b} then it is {a} ."]
# negation with colors and properties
for t, (c1, c2) in itertools.product(things, itertools.permutations(colors, 2)):
    if t not in {"box"} and rng.random() < 0.6:
        out += [f"the {t} is not {c1} , it is {c2} , so the {t} is {c2} .", f"the {t} is {c2} , not {c1} ."]
for who, (f1, f2) in itertools.product(people, itertools.permutations(foods, 2)):
    if rng.random() < 0.45:
        out += [f"{who} did not buy {f1} , {pron[who]} bought {f2} , so {pron[who]} bought {f2} .",
                f"{who} bought {f2} , not {f1} ."]
# sequence
steps = [("fill the cup", "drink the water", "drink"), ("open the bag", "pack the shirt", "pack"),
         ("wash the plate", "put it away", "put"), ("read the letter", "sign it", "sign"),
         ("lock the gate", "feed the goat", "feed"), ("clean the brush", "paint the wall", "paint"),
         ("peel the fruit", "cut it", "cut"), ("light the fire", "cook the rice", "cook")]
for (a, b, last), who in itertools.product(steps, people):
    out += [f"first {who} must {a} , then {b} , the last step is {last} .",
            f"{who} did {a} first and {b} second , so the later action is {last} ."]
for late, early in [("dinner", "lunch"), ("evening", "morning"), ("spring", "winter"), ("night", "day"),
                    ("supper", "lunch")]:
    for who in people:
        out += [f"{who} eats {late} after {early} , the earlier one is {early} ."
                if late in {"dinner", "supper", "lunch"} else f"{late} comes after {early} , the earlier one is {early} ."]
# spatial
spatial_things = [t for t in things if t not in {"ball", "bag", "book", "lamp", "box"}]
for t1, t2 in itertools.permutations(spatial_things, 2):
    if rng.random() < 0.7:
        out += [f"the {t1} is inside the {t2} , so the {t2} contains the {t1} .",
                f"the {t1} is above the {t2} , so the {t2} is below the {t1} .",
                f"the {t1} is to the left of the {t2} , so the {t2} is to the right of the {t1} ."]
# knowledge and categories in simple frames
facts = ["the lake freezes in winter .", "wood is hard .", "the dog is hungry .", "we turn on the lamp when it is dark .",
         "the room is dark at night .", "a cow eats grass .", "the road is wet after the rain .", "the ice is cold ."]
for f, who in itertools.product(facts, people):
    out += [f"{who} said that {f}", f"{who} saw that {f}"]
for y, a in [("lamb", "sheep"), ("calf", "cow"), ("foal", "horse"), ("chick", "hen"), ("cub", "bear"),
             ("kitten", "cat"), ("puppy", "dog")]:
    for who in people:
        out += [f"{who} saw a {y} , a {y} is a young {a} ."]
for kind, members in [("bird", ["eagle", "robin"]), ("fish", ["tuna", "cod"]),
                      ("tool", ["saw", "wrench"]), ("vegetable", ["pepper", "bean", "carrot"]),
                      ("fruit", ["pear", "peach", "mango", "apple"]), ("vehicle", ["truck", "taxi", "bus", "boat"])]:
    for m, who in itertools.product(members, people):
        out += [f"{who} said a {m} is a kind of {kind} ."]

# keep only sentences whose every word is in the E6 vocabulary
kept, dropped = [], set()
for s in dict.fromkeys(out):
    bad = [w for w in tok(s) if w not in VOC]
    if bad:
        dropped.update(bad)
    else:
        kept.append(s)
rng.shuffle(kept)
print("generated", len(out), "unique kept", len(kept), "| words outside E6 vocabulary that were dropped:", sorted(dropped))
for folder in [ROOT / "corpus", HERE]:
    folder.mkdir(parents=True, exist_ok=True)
    for old in list(folder.glob("*.txt")) + list(folder.glob("*.pdf")):
        old.unlink()
    for f in (ROOT / "corpus_added/experiment6").glob("*.txt"):
        shutil.copy(f, folder / f.name)
    (folder / "generated_10k.txt").write_text("\n".join(kept) + "\n", encoding="utf-8")
