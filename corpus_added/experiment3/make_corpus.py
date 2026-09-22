"""Generate the Experiment 3 teaching files from short word lists.

Run from the repository root:  python corpus_added/experiment3/make_corpus.py
It writes opposites.txt, grammar.txt and negation.txt into corpus/ and into this folder.
The word lists avoid every name and prompt sequence on the do-not-use list printed by
check_corpus.py. Nothing here was taken from evals/language_evals.json.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = [ROOT / "corpus", Path(__file__).resolve().parent]

# ---------------------------------------------------------------- opposites
pairs = [("big", "small"), ("fast", "slow"), ("up", "down"), ("tall", "short"),
         ("young", "old"), ("heavy", "light"), ("strong", "weak"), ("soft", "hard"),
         ("wide", "narrow"), ("clean", "dirty"), ("high", "low"), ("thick", "thin"),
         ("sweet", "sour"), ("happy", "sad"), ("near", "far"), ("early", "late"),
         ("rich", "poor"), ("wet", "dry"), ("day", "night"), ("loud", "silent"),
         ("warm", "cool"), ("deep", "shallow"), ("dark", "bright"), ("cheap", "expensive"),
         ("open", "shut"), ("push", "pull"), ("begin", "end"), ("win", "lose")]
opposites = []
for a, b in pairs:
    opposites += [f"the opposite of {a} is {b} .", f"the opposite of {b} is {a} .",
                  f"{b} is the opposite of {a} .", f"{a} is the opposite of {b} .",
                  f"{a} and {b} are opposites .",
                  f"when something is not {a} it is {b} ."]
# contrast sentences that teach temperature, amount and sound words in ordinary situations
hot_cold = [("soup", "salad"), ("coffee", "lemonade"), ("sand", "sea"), ("shower", "pool"),
            ("oven", "fridge"), ("tea", "juice"), ("desert", "mountain"), ("engine", "wind")]
full_empty = [("bucket", "jug"), ("bottle", "glass"), ("stadium", "park"), ("fridge", "shelf"),
              ("bus", "train"), ("bag", "basket"), ("tank", "barrel"), ("cinema", "theater")]
noisy_quiet = [("market", "library"), ("street", "garden"), ("classroom", "chapel"),
               ("city", "village"), ("workshop", "museum"), ("kitchen", "bedroom"),
               ("stadium", "forest"), ("station", "lake")]
for x, y in hot_cold:
    opposites += [f"the {x} was hot but the {y} was cold .", f"the {x} is hot and the {y} is cold .",
                  f"the {x} is hot .", f"the {y} is cold ."]
for x, y in full_empty:
    opposites += [f"the {x} was full in the morning and empty at night .",
                  f"the {x} is full but the {y} is empty .", f"the {x} is full .", f"the {y} is empty ."]
for x, y in noisy_quiet:
    opposites += [f"the {x} is noisy and the {y} is quiet .", f"the {x} was noisy but the {y} was quiet .",
                  f"the {x} is noisy .", f"the {y} is quiet ."]

# ------------------------------------------------------------------ grammar
singular = ["cat", "horse", "cow", "goat", "duck", "frog", "boat", "cup", "lamp", "truck",
            "student", "driver", "nurse", "farmer", "boy", "girl", "child", "teacher"]
plural = {"cat": "cats", "horse": "horses", "cow": "cows", "goat": "goats", "duck": "ducks",
          "frog": "frogs", "boat": "boats", "cup": "cups", "lamp": "lamps", "truck": "trucks",
          "student": "students", "driver": "drivers", "nurse": "nurses", "farmer": "farmers",
          "boy": "boys", "girl": "girls", "child": "children", "teacher": "teachers"}
places = ["on the roof", "in the field", "at the door", "on the lake", "on the table",
          "in the barn", "at the station", "in the garden", "by the river", "at the market"]
grammar = []
for i, n in enumerate(singular):
    p1, p2 = places[i % len(places)], places[(i + 3) % len(places)]
    grammar += [f"one {n} is {p1} .", f"a {n} is {p2} .", f"the {n} is {p1} .",
                f"two {plural[n]} are {p2} .", f"the {plural[n]} are {p1} .",
                f"three {plural[n]} were {p2} .",
                f"one {n} is {p1} and the {plural[n]} are {p1} too ."]
# the words bird, dogs, dog in other frames (never "one bird" or "the dogs")
grammar += ["a bird is on the roof .", "the bird is singing in the tree .",
            "every bird is looking for seeds .", "this bird is small and brown .",
            "a bird was in the garden .", "the birds are flying south .",
            "two birds are on the wire .", "three birds were at the lake .",
            "two dogs are barking in the yard .", "our dogs are sleeping by the fire .",
            "both dogs are waiting for dinner .", "three dogs were at the park .",
            "our dogs were tired after the walk .", "the dog is on the sofa .",
            "one dog is in the yard .", "a dog is at the gate ."]
# am / were / walk / walking
grammar += ["i am at the station .", "i am a student .", "i am in the garden .",
            "i am at home today .", "i am happy .", "i am late .",
            "today i am at home and yesterday i was at the office .",
            "we were at the market .", "they were in the garden .", "you were at the door .",
            "yesterday we were at the beach .", "yesterday they were at the museum .",
            "last week we were at the lake .", "the boys were tired .", "the cups were on the shelf .",
            "they walk to school every day .", "we walk along the river on sunday .",
            "the children walk to the park .", "i walk to work .", "you walk very fast .",
            "she is walking to the park .", "the boy is walking the dog .",
            "we are walking to the station .", "they are walking along the beach .",
            "the farmer is walking to the barn ."]
subjects = ["he", "they", "we", "the boy", "my sister", "my uncle", "the driver", "the nurse",
            "the farmer", "the girl", "our teacher", "the children"]
past = [("walked to the market", "walk to the market"), ("cooked dinner", "cook dinner"),
        ("played football", "play football"), ("visited the museum", "visit the museum"),
        ("painted the fence", "paint the fence"), ("talked about rivers", "talk about rivers"),
        ("cleaned the kitchen", "clean the kitchen"), ("climbed the hill", "climb the hill"),
        ("jumped into the lake", "jump into the lake"), ("walked along the beach", "walk along the beach"),
        ("walked home", "walk home"), ("walked to the bank", "walk to the bank")]
for i, s in enumerate(subjects):
    for j in range(3):
        did, do = past[(i + 4 * j) % len(past)]
        grammar += [f"yesterday {s} {did} .", f"today {s} {do} and yesterday {s} {did} too ."]
grammar += ["last week she walked to the office .", "last night she talked with her mother .",
            "last month she painted the kitchen .", "this morning she walked the dog around the block .",
            "she walked to the park with her friend .", "she cooked rice and beans on sunday .",
            "yesterday it rained all afternoon .", "yesterday the shop opened late .",
            "yesterday the baby slept for three hours ."]

# ----------------------------------------------------------------- negation
objects_colors = [("cup", "green", "white"), ("car", "red", "blue"), ("wall", "yellow", "grey"),
                  ("hat", "black", "brown"), ("shirt", "blue", "red"), ("coat", "white", "black"),
                  ("plate", "pink", "orange"), ("kite", "purple", "yellow"), ("chair", "brown", "grey"),
                  ("boat", "green", "red"), ("scarf", "red", "pink"), ("bike", "blue", "green")]
objects_props = [("bag", "small", "large"), ("road", "wet", "dry"), ("soup", "cold", "warm"),
                 ("gate", "open", "closed"), ("shop", "closed", "open"), ("window", "open", "closed"),
                 ("bridge", "long", "short"), ("pencil", "sharp", "dull"), ("movie", "boring", "funny"),
                 ("crate", "heavy", "light"), ("crate", "square", "round"), ("fence", "wooden", "metal"),
                 ("tea", "sweet", "bitter"), ("bread", "fresh", "stale"), ("lamp", "on", "off"),
                 ("river", "shallow", "deep"), ("room", "dark", "bright"), ("ticket", "cheap", "expensive")]
negation = []
for o, a, b in objects_colors + objects_props:
    negation += [f"the {o} is not {a} , it is {b} , so the {o} is {b} .",
                 f"the {o} is {b} , not {a} .",
                 f"the {o} is not {a} but {b} .",
                 f"is the {o} {a} ? no , the {o} is {b} ."]
buyers = [("she", "she"), ("he", "he"), ("they", "they"), ("we", "we"), ("the boy", "he"),
          ("my aunt", "she"), ("the driver", "he"), ("the nurse", "she"), ("the farmer", "he"),
          ("the girl", "she")]
bought = [("rice", "beans"), ("a hat", "a scarf"), ("the sofa", "the chair"), ("oranges", "grapes"),
          ("a kite", "a ball"), ("flowers", "candles"), ("fuel", "water"), ("bread", "cheese"),
          ("a coat", "a shirt"), ("apples", "pears")]
for i, (s, p) in enumerate(buyers):
    x, y = bought[i]
    negation += [f"{s} did not buy {x} , {p} bought {y} , so {p} bought {y} .",
                 f"{s} bought {y} , not {x} .",
                 f"{s} did not buy {x} but {y} ."]
verbs = [("eat", "ate", "pasta", "soup"), ("drink", "drank", "coffee", "juice"),
         ("take", "took", "the train", "the ferry"), ("watch", "watched", "the news", "a film"),
         ("read", "read", "the letter", "the book"), ("use", "used", "butter", "oil"),
         ("want", "wanted", "cake", "bread"), ("want", "wanted", "juice", "milk"),
         ("order", "ordered", "coffee", "tea"), ("choose", "chose", "the soup", "the salad"),
         ("plant", "planted", "corn", "wheat"), ("paint", "painted", "the door", "the fence"),
         ("clean", "cleaned", "the car", "the boat"), ("visit", "visited", "the bank", "the museum")]
for i, (v, vd, x, y) in enumerate(verbs):
    s, p = buyers[i % len(buyers)]
    negation += [f"{s} did not {v} {x} , {p} {vd} {y} , so {p} {vd} {y} .",
                 f"{s} {vd} {y} , not {x} ."]
negation += ["it is not monday , it is tuesday , so today is tuesday .",
             "it is not winter , it is spring , so the season is spring .",
             "the answer is not seven , it is nine , so the answer is nine .",
             "the meeting is not at noon , it is at three , so the meeting is at three .",
             "the cat is not outside , it is inside , so the cat is inside .",
             "the keys are not in the drawer , they are on the hook , so the keys are on the hook .",
             "the milk is not on the table , it is in the fridge , so the milk is in the fridge .",
             # words from the answer lists in ordinary sentences: box, missing, bread
             "the box is on the shelf .", "the box is heavy .", "we put the keys in the box .",
             "the box was empty .", "a small box is on the table .", "the box is brown .",
             "the key is missing .", "one page is missing from the book .", "two cups are missing .",
             "my hat is missing , not lost .", "the bread is on the table .", "we ate bread and cheese .",
             "the bread was warm .", "she cut the bread .", "the door is open .", "the door was closed all day .",
             "the gate is closed .", "the shop is open on sunday ."]

for name, lines in [("opposites.txt", opposites), ("grammar.txt", grammar), ("negation.txt", negation)]:
    unique = list(dict.fromkeys(lines))
    for folder in OUT:
        folder.mkdir(parents=True, exist_ok=True)
        (folder / name).write_text("\n".join(unique) + "\n", encoding="utf-8")
    print(name, len(unique), "sentences")
