"""Experiment 4 teaching files: sequence, spatial relations, everyday knowledge, categories.

Run from the repository root:  python corpus_added/experiment4/make_corpus.py
Writes four .txt files into corpus/ and into this folder. Written from the category
names and the do-not-use list of check_corpus.py only. Multi-clause passages use commas
because the notebook splits training text at every period.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = [ROOT / "corpus", Path(__file__).resolve().parent]

# -------------------------------------------------------------- sequence
steps = [("peel the fruit", "slice it", "slice"), ("fill the pot", "boil the water", "boil"),
         ("open the bag", "pack the shirt", "pack"), ("mix the flour", "bake the cake", "bake"),
         ("hang the shirt", "dry it", "dry"), ("read the letter", "sign it", "sign"),
         ("lock the gate", "feed the goat", "feed"), ("light the fire", "cook the rice", "cook"),
         ("clean the brush", "paint the wall", "paint"), ("wash the car", "park it", "park")]
sequence = []
for a, b, last in steps:
    sequence += [f"first {a} , then {b} , the last step is {last} .",
                 f"first {a} , then {b} , the final action is {last} .",
                 f"{a} first and {b} second , so the later action is {last} .",
                 f"first {a} and then {b} , in that order ."]
order = [("dinner", "lunch"), ("evening", "morning"), ("spring", "winter"), ("friday", "monday"),
         ("dessert", "soup"), ("sunset", "sunrise"), ("supper", "lunch"), ("night", "day")]
for late, early in order:
    sequence += [f"{late} comes after {early} , the earlier one is {early} .",
                 f"{early} comes before {late} , the later one is {late} .",
                 f"{late} happens after {early} .", f"{early} happens before {late} ."]
arrivals = [("taxi", "truck"), ("boat", "ferry"), ("teacher", "student"), ("nurse", "doctor"),
            ("car", "bicycle"), ("letter", "package")]
for a, b in arrivals:
    sequence += [f"the {a} arrived before the {b} , the one that came later was the {b} .",
                 f"the {a} arrived first and the {b} arrived later .",
                 f"the {b} arrived after the {a} , so the {a} was earlier ."]
sequence += ["a truck is a vehicle .", "a taxi is a vehicle .", "every vehicle needs fuel .",
             "breakfast is the morning meal .", "the meal was warm .", "we cooked a big meal .",
             "lunch is at noon .", "we ate lunch at the market .", "the cup is on the shelf .",
             "the train is at the station .", "the bus is at the station .", "wash the plate .", "we wash the car on sunday .", "the cup is clean .",
             "an action has a result .", "the first action was to open the door ."]

# ---------------------------------------------------------- spatial relations
inside = [("coin", "jar"), ("key", "drawer"), ("shirt", "suitcase"), ("letter", "envelope"),
          ("apple", "basket"), ("pencil", "case"), ("ring", "pocket"), ("toy", "crate")]
spatial = []
for x, y in inside:
    spatial += [f"the {x} is inside the {y} , so the {y} contains the {x} .",
                f"the {y} contains the {x} , the {x} is inside the {y} .",
                f"the {x} is in the {y} .", f"the {y} holds the {x} ."]
above = [("picture", "sofa"), ("clock", "door"), ("shelf", "sink"), ("roof", "wall"),
         ("bird", "tree"), ("cloud", "hill"), ("sign", "gate"), ("light", "table")]
for x, y in above:
    spatial += [f"the {x} is above the {y} , so the {y} is below the {x} .",
                f"the {y} is below the {x} , the {x} is above the {y} .",
                f"the {x} is above the {y} .", f"the {y} is below the {x} ."]
side = [("cup", "plate"), ("chair", "table"), ("truck", "car"), ("shop", "bank"),
        ("boy", "girl"), ("cat", "dog"), ("lamp", "sofa"), ("gate", "fence")]
for x, y in side:
    spatial += [f"the {x} is to the left of the {y} , so the {y} is to the right of the {x} .",
                f"the {y} is to the right of the {x} , the {x} is to the left .",
                f"the {x} is on the left and the {y} is on the right .",
                f"the {y} is beside the {x} ."]
spatial += ["she read the book .", "the book is on the table .", "the bag is large .",
            "we put the bag on the floor .", "the lamp is on .", "the desk is wooden .",
            "the ball is round .", "the boy kicked the ball .", "the box is on the shelf .",
            "the box is heavy .", "the ball is under the table .", "the lamp is beside the desk .",
            "the cat is under the chair .", "the dog is behind the gate ."]

# -------------------------------------------------------- everyday knowledge
knowledge = ["ice is frozen water .", "the lake freezes in winter .", "the pond freezes when it is cold .",
             "snow melts into water .", "steam rises from the hot soup .", "steam comes from boiling water .",
             "the ice melts in the sun .", "we drink water every day .", "the river water is cold .",
             "wood burns in the fire .", "the table is made of wood .", "the fence is made of wood .",
             "an umbrella keeps you dry in the rain .", "she opened an umbrella when it rained .",
             "the rain made the road wet .", "we stay inside when it rains .", "the coat keeps you warm .",
             "a hat keeps the sun off your face .", "a person uses a map to find the road .",
             "a person uses a key to open the door .", "a person uses a spoon to eat soup .",
             "a person uses a pen to write .", "every person needs water .", "the baby is asleep .",
             "the cat is asleep on the sofa .", "the dog is hungry .", "we were hungry after the walk .",
             "the room is dark at night .", "the room was dark so i turned on the lamp .",
             "we turn on the lamp when it is dark .", "i turn on the light to read .",
             "the light is on .", "the light is off .", "we see the road by day .",
             "we cannot see in the dark .", "at night we need a light to see .",
             "the pillow is on the bed .", "she sleeps on a soft pillow .", "the spoon is in the cup .",
             "the shoe is under the bed .", "he lost one shoe .", "the sun gives light .",
             "the moon gives a little light at night .", "fire gives heat and light .",
             "the kettle boils water .", "milk comes from cows .", "bread is made from flour .",
             "an egg comes from a hen .", "an apple grows on a tree .", "an orange is a fruit .",
             "a fish lives in water .", "a bird lives in a tree .", "a cow eats grass .",
             "a dog needs a walk every day .", "the sky is blue by day .", "the sky is dark at night ."]

# ------------------------------------------------------------ categories
birds = ["eagle", "sparrow", "owl", "parrot", "crow", "pigeon"]
fishes = ["trout", "shark", "tuna", "cod", "carp"]
tools = ["hammer", "saw", "drill", "wrench"]
vegs = ["beet", "onion", "potato", "pepper", "bean"]
fruits = ["pear", "peach", "mango", "banana", "grape"]
fabrics = ["cotton", "wool", "silk", "linen"]
vehicles = ["truck", "taxi", "bus", "boat"]
categories = []
for b in birds:
    categories += [f"an {b} is a kind of bird ." if b[0] in "aeiou" else f"a {b} is a kind of bird .",
                   f"the {b} is a bird that flies ."]
for f in fishes:
    categories += [f"a {f} is a kind of fish .", f"the {f} is a fish that swims ."]
for t in tools:
    categories += [f"a {t} is a kind of tool .", f"the {t} is a tool ."]
for v in vegs:
    categories += [f"a {v} is a kind of vegetable .", f"the {v} is a vegetable we cook ."]
for f in fruits:
    categories += [f"a {f} is a kind of fruit .", f"the {f} is a sweet fruit ."]
for f in fabrics:
    categories += [f"{f} is a kind of fabric .", f"the shirt is made of {f} ."]
for v in vehicles:
    categories += [f"a {v} is a kind of vehicle .", f"the {v} is a vehicle on the road ."]
young = [("lamb", "sheep"), ("calf", "cow"), ("foal", "horse"), ("chick", "hen"),
         ("cub", "bear"), ("duckling", "duck"), ("piglet", "pig"), ("kid", "goat")]
for y, a in young:
    categories += [f"a {y} grows up to be a {a} .", f"a {y} is a young {a} .",
                   f"the {y} becomes a {a} .", f"a {a} was once a {y} ."]
categories += ["the robin is a small bird with a red chest .", "we saw a robin in the garden .",
               "the salmon is a big fish .", "we ate salmon for dinner .", "the puppy is a young dog .",
               "the puppy plays in the yard .", "the kitten is a young cat .", "the kitten sleeps all day .",
               "the carrot is an orange vegetable .", "we cooked a carrot with the soup .",
               "the apple is a red fruit .", "she ate an apple .", "a goat eats grass .",
               "the goat is in the barn .", "a robin sings in the morning .", "a salmon swims up the river .",
               "an owl is a bird of the night .", "an eagle is a large bird .", "an onion is a kind of vegetable .",
               "birds fly and fish swim .", "a bird has wings and a fish has fins ."]

for name, lines in [("sequence.txt", sequence), ("spatial.txt", spatial),
                    ("knowledge.txt", knowledge), ("categories.txt", categories)]:
    unique = list(dict.fromkeys(lines))
    for folder in OUT:
        folder.mkdir(parents=True, exist_ok=True)
        (folder / name).write_text("\n".join(unique) + "\n", encoding="utf-8")
    print(name, len(unique), "sentences")
