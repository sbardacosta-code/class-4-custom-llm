"""Experiment 6: all seven categories, trimmed to fit the 509-type vocabulary cap.

Run from the repository root:  python corpus_added/experiment6/make_corpus.py
1. Loads the Experiment 3 and 4 sentences (corpus_added/experiment3, experiment4).
2. Adds coverage.txt: ordinary sentences that use, at least six times each, the words
   that Experiments 4 and 5 showed missing or cut (walks, north, south, desk, breakfast,
   ice, freezes, steam, wood, stay, umbrella, asleep, hungry, turn, pillow, spoon, shoe,
   robin, kitten, puppy, carrot, fabric, missing, wet, sand, metal, buy).
3. Checks that every needed word has at least 8 uses, so it ranks well above the line
   where the notebook's 509-type cap starts cutting (in Experiment 5 the cut words had
   3 uses or fewer). Rare words that are not needed are allowed to become UNK.
Names and prompt sequences on the do-not-use list are never used. check_corpus.py
verifies the output before training.
"""
import json, re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
tok = lambda t: re.findall(r"\w+(?:['’]\w+)*|[^\w\s]", t.lower())

files = {}
for exp in ["experiment3", "experiment4"]:
    for f in sorted((ROOT / "corpus_added" / exp).glob("*.txt")):
        files[f.name] = [l for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]

W = {  # word to teach -> six ordinary sentences built from words already common in the corpus
 "walks": ["he walks to the office every morning .","she walks the dog at noon .","the girl walks to school .","my uncle walks by the river .","the nurse walks to the hospital .","the boy walks home after lunch ."],
 "north": ["the road goes north to the city .","the birds fly north in spring .","the wind comes from the north .","the farm is north of the village .","the market is north of the station .","we walked north along the river ."],
 "south": ["the river flows south .","the beach is south of the town .","the ducks fly south in winter .","the road goes south to the sea .","our school is south of the park .","we walked south along the beach ."],
 "desk": ["the desk is wooden .","the lamp is beside the desk .","she left the letter on the desk .","the teacher sits at the desk .","the desk is near the window .","my book is on the desk ."],
 "breakfast": ["breakfast is the morning meal .","we ate breakfast at seven .","she cooked eggs for breakfast .","breakfast comes before lunch .","the hotel serves breakfast .","he ate bread for breakfast ."],
 "ice": ["ice is frozen water .","the ice melts in the sun .","we put ice in the juice .","the lake was covered with ice .","the ice is cold and hard .","the road was covered with ice at night ."],
 "freezes": ["the lake freezes in winter .","the pond freezes when it is cold .","the river freezes in winter .","water freezes when it is very cold .","the milk freezes in the fridge .","the garden pond freezes at night ."],
 "steam": ["steam rises from the hot soup .","steam comes from boiling water .","the kettle makes steam .","steam filled the kitchen .","hot tea gives off steam .","we saw steam over the river ."],
 "wood": ["wood burns in the fire .","the table is made of wood .","the fence is made of wood .","we cut wood for the winter .","the boat is made of wood .","the floor is made of wood ."],
 "stay": ["we stay inside when it rains .","they stay at the hotel .","the children stay at school until three .","please stay on the road .","we stay warm by the fire .","the cats stay in the barn ."],
 "umbrella": ["an umbrella keeps you dry in the rain .","she opened an umbrella when it rained .","he forgot his umbrella at the office .","the umbrella is black .","take an umbrella today .","the umbrella is in the car ."],
 "asleep": ["the baby is asleep .","the cat is asleep on the sofa .","the dog fell asleep by the fire .","the children are asleep .","he was asleep at noon .","the town is asleep at night ."],
 "hungry": ["the dog is hungry .","we were hungry after the walk .","the baby is hungry .","a hungry goat eats everything .","the students are hungry at noon .","i am hungry ."],
 "turn": ["we turn on the lamp when it is dark .","i turn on the light to read .","turn left at the bank .","they turn the boat toward the shore .","we turn off the lamp at night .","turn the page ."],
 "pillow": ["the pillow is on the bed .","she sleeps on a soft pillow .","the pillow is white .","he put the pillow on the sofa .","the cat sleeps on the pillow .","a pillow is soft ."],
 "spoon": ["the spoon is in the cup .","a person uses a spoon to eat soup .","the spoon is made of metal .","she washed the spoon .","the spoon is on the plate .","he stirred the tea with a spoon ."],
 "shoe": ["the shoe is under the bed .","he lost one shoe .","the shoe is wet .","her shoe is brown .","the dog took my shoe .","a shoe protects the foot ."],
 "robin": ["the robin is a small bird with a red chest .","we saw a robin in the garden .","a robin sings in the morning .","the robin sat on the fence .","a robin built a nest in the tree .","the robin flew to the roof ."],
 "kitten": ["the kitten is a young cat .","the kitten sleeps all day .","the kitten plays with the ball .","a kitten drinks milk .","the kitten is asleep on the pillow .","our kitten is grey ."],
 "puppy": ["the puppy is a young dog .","the puppy plays in the yard .","a puppy needs a walk .","the puppy is hungry .","our puppy is brown .","the puppy sleeps by the fire ."],
 "carrot": ["the carrot is an orange vegetable .","we cooked a carrot with the soup .","the goat ate the carrot .","she cut the carrot .","a carrot grows in the ground .","the carrot is sweet ."],
 "fabric": ["cotton is a kind of fabric .","the shirt is made of soft fabric .","wool is a warm fabric .","she bought fabric for the dress .","the fabric is blue .","silk is a smooth fabric ."],
 "missing": ["the key is missing .","one page is missing from the book .","two cups are missing .","my hat is missing .","a wheel is missing from the cart .","the last page is missing ."],
 "wet": ["the road is wet .","the shoe is wet after the rain .","the grass is wet in the morning .","the towel is wet .","the dog is wet from the lake .","wet wood does not burn ."],
 "sand": ["the sand is hot in summer .","the children play in the sand .","the beach has white sand .","sand gets into the shoe .","the sand is soft .","we built a castle of sand ."],
 "metal": ["the spoon is made of metal .","the gate is metal .","the roof is metal .","metal is hard and cold .","the fence is metal .","the key is made of metal ."],
 "buy": ["we buy bread at the market .","they buy fruit on saturday .","i buy milk every morning .","she wants to buy a hat .","you can buy fuel at the station .","we buy fish at the harbor ."],
 "fill": ["fill the cup with water .","we fill the tank with fuel .","fill the bucket at the river .","they fill the boxes with apples .","fill the pot and boil the water .","the children fill the bag with sand ."],
 "fish": ["a fish lives in water .","we ate fish for dinner .","the cat wants the fish .","a shark is a big fish .","the fish is in the river .","birds fly and fish swim ."],
 "ball": ["the ball is round .","the boy kicked the ball .","the ball is under the table .","the dog wants the ball .","the ball is red .","she threw the ball to the girl ."],
 "vegetable": ["a beet is a kind of vegetable .","an onion is a kind of vegetable .","the potato is a vegetable we cook .","a bean is a kind of vegetable .","the pepper is a vegetable we cook .","a cabbage is a kind of vegetable ."],
 "tool": ["a hammer is a kind of tool .","a saw is a kind of tool .","the drill is a tool .","the farmer keeps every tool in the barn .","a wrench is a kind of tool .","the tool is made of metal ."],
 "grows": ["a lamb grows up to be a sheep .","a calf grows up to be a cow .","the tree grows by the river .","a foal grows up to be a horse .","the corn grows in summer .","a chick grows up to be a hen ."],
 "action": ["an action has a result .","the first action was to open the door .","the last action was to lock the gate .","every action has a cost .","the final action is to sign the letter .","the next action is to feed the goat ."],
 "wash": ["wash the plate .","we wash the car on sunday .","wash the cup after dinner .","they wash the dog in the yard .","i wash the shirt at night .","wash the apple before you eat it ."],
 "see": ["we see the road by day .","we cannot see in the dark .","at night we need a light to see .","i see a bird on the roof .","they see the lake from the hill .","you see the station from the bank ."],
 "person": ["a person uses a map to find the road .","a person uses a key to open the door .","a person uses a pen to write .","every person needs water .","one person is at the door .","a person walks faster than a goat ."],
 "dogs": ["two dogs are barking in the yard .","our dogs are sleeping by the fire .","both dogs are waiting for dinner .","three dogs were at the park .","our dogs were tired after the walk .","two dogs were at the gate ."],
 "birds": ["the birds are flying south .","two birds are on the wire .","three birds were at the lake .","the birds sing in the morning .","the birds are in the tree .","two birds were on the roof ."],
 "bread": ["the bread is on the table .","we ate bread and cheese .","the bread was warm .","she cut the bread .","we buy bread at the market .","he ate bread for breakfast ."],
}
W["meal"] = ["the meal was warm .", "we cooked a big meal .", "lunch is the midday meal .", "dinner is the evening meal .",
             "the family shared a meal .", "the hotel serves a meal at noon ."]
W["walking"] = ["she is walking to the park .", "the boy is walking the dog .", "we are walking to the station .",
                "they are walking along the beach .", "the farmer is walking to the barn .", "i am walking home ."]
W["north"] += ["the mountain is north of the lake .", "they live north of the river ."]
W["stay"] += ["our dogs stay in the yard .", "we stay at home on sunday ."]
W["walks"] += ["the farmer walks to the barn .", "my aunt walks to the market ."]
coverage = [s for lines in W.values() for s in lines]
files["coverage.txt"] = coverage

# classroom counts from the starter run's checkpoint
ck = json.load(open(ROOT / "runs/experiment1_starter/checkpoint.json", encoding="utf-8"))
classroom = {w: c for w, c in zip(ck["vocabulary"], ck["token_counts"]) if not w.startswith("<")}
needed = set(W) | {"am", "were", "walk", "walking", "box", "closed", "open", "hot", "cold", "empty",
           "full", "noisy", "quiet", "dry", "light", "cat", "fruit", "bus", "below", "right",
           "book", "blue", "is", "are", "walked", "bird", "opposite", "lunch", "meal", "vehicle",
           "later", "arrived", "earlier", "happens", "inside", "contains", "bag", "above", "left",
           "uses", "dark", "room", "dog", "apple", "tree", "cup", "tea", "milk", "red", "green", "yellow",
           "into", "an", "first", "then", "last", "was", "not", "it", "so"}

MIN_USES = 8  # the notebook keeps the 509 most frequent types; E5 cut only words with <= 3 uses
c = Counter(classroom)
for lines in files.values():
    for l in lines:
        c.update(tok(l))
types = [w for w in c if not w.startswith("<")]
ranked = sorted(types, key=lambda w: (-c[w], w))
cut = set(ranked[509:])
print("word types:", len(types), "| would be cut by the 509 cap:", len(cut), "| lowest kept count:", c[ranked[508]])
low = sorted((w, c[w]) for w in needed if c[w] < MIN_USES)
print("needed words below", MIN_USES, "uses:", low or "none")
print("needed words that the cap would cut:", sorted(w for w in needed if w in cut) or "none")
for folder in [ROOT / "corpus", HERE]:
    folder.mkdir(parents=True, exist_ok=True)
    for old in folder.glob("*.txt"):
        old.unlink()
    for name, lines in files.items():
        (folder / name).write_text("\n".join(dict.fromkeys(lines)) + "\n", encoding="utf-8")
        print(name, len(set(lines)))
