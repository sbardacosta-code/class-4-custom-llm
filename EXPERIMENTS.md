# Experiment log

Format per experiment: **H** hypothesis, written in the notebook before the run ·
**T** test and metric · **R** result · **C** one-line conclusion.
Fixed unless stated: seed 42, 3,000 steps, lr 0.001, batch 32, same 48 evals, classroom
corpus always included. n = 1 run per condition unless stated. "scorable" = cases whose
prompt and all 4 choices are in the vocabulary; "correct" = 4-choice score over 48.
E1 and E2 are the required experiments; E3 onward are extras.

| Exp | Added corpus | Vocab | Scorable | Correct | All-case | Val loss | Run |
|---|---|---:|---:|---:|---:|---:|---|
| E1 | none | 136 | 24 | 20 | 41.7% | 0.706 | [runs/experiment1_starter](runs/experiment1_starter/) |
| E2 | 181 sent., opposites+grammar+negation | 424 | 27 | 25 | 52.1% | 0.703 | [runs/experiment2_extended](runs/experiment2_extended/) |
| E3 | 715 sent., same 3 categories | 478 | 31 | 25 | 52.1% | 0.733 | [runs/experiment3_more_corpus](runs/experiment3_more_corpus/) |
| E4 | 391 sent., sequence+spatial+knowledge+categories (E3 files removed) | 418 | 29 | 26 | 54.2% | 0.708 | [runs/experiment4_new_categories](runs/experiment4_new_categories/) |
| E5 | E3 + E4 files together, 1,106 sent., 647 types → cap 509 | 512 | 32 | 29 | 60.4% | 1.258 | [runs/experiment5_all_seven](runs/experiment5_all_seven/) |
| E6 | E5 + coverage.txt (each missing eval word ≥ 8 uses), 1,346 sent., 715 types → cap 509 | 512 | 43 | 30 | 62.5% | 0.888 | [runs/experiment6_coverage](runs/experiment6_coverage/) |
| E7 | E6 corpus, **6,000 steps** | 512 | 43 | 34 | 70.8% | 0.822 | [runs/experiment7_6000steps](runs/experiment7_6000steps/) |
| E8a | E6 corpus, **seed 7** | 512 | 43 | 35 | 72.9% | 1.233 | [runs/experiment8_seed7](runs/experiment8_seed7/) |
| E8b | E6 corpus, **seed 2026** | 512 | 43 | 30 | 62.5% | 0.901 | [runs/experiment8_seed2026](runs/experiment8_seed2026/) |
| E9 | E6 corpus + a whole book (Alice in Wonderland, 34k tokens, 2,534 types) | 512 | 25 | 25 | 52.1% | 1.886 | [runs/experiment9_alice_raw](runs/experiment9_alice_raw/) |
| E10 | E6 corpus + 90 sentences of the same book with ≥ 60% known words (378 new types) | 512 | 42 | 30 | 62.5% | 0.758 | [runs/experiment10_alice_slice](runs/experiment10_alice_slice/) |
| E11 | E6 corpus minus the 194 sentences the guardrail marks as warnings | 512 | 39 | 27 | 56.3% | 0.923 | [runs/experiment11_no_warnings](runs/experiment11_no_warnings/) |

Untrained baselines: E1 9, E2 6, E3 7, E4 6, E5 7, E6 12, E7 12, E8a 12, E8b 11 correct (chance on 4 choices; 43 scorable from E6 on).
Starter group = 16/16 in every trained run. Transfer group: E1 4, E2 8, E3 7, E4 8, E5 8, E6 8, E7 8, E8a 8, E8b 7 (of 8).

**Noise floor (E6, E8a, E8b: same corpus, same steps, seeds 42/7/2026):** correct 30/35/30, extension 6/11/7 of 19, val loss 0.89/1.23/0.90. A single-run difference of up to 5 cases is seed noise. Cases that pass under all three seeds: lang_25, lang_26, lang_27 (grammar) and lang_37 (sequence). Every other extension pass flips with the seed.

## E1 starter corpus
H: val_loss(3000) ∈ [0.5, 1.5]; starter ≥ 12/16; transfer ≈ 4/8; extension = 0/24 with 0 scorable; nearest(customer) = {client, buyer, shopper, consumer, subscriber}.
T: history.json; eval_summary.json by group; cosine over the embedding table.
R: val 0.706; starter 16/16; transfer 4/8; extension 0/24, 0 scorable; nearest = shopper .978, client .977, buyer .977, subscriber .971, consumer .970. PASS, 5/5 claims.
C: templates fully learned; loss flat after step 1500 (0.718 → 0.706); words absent from the corpus cannot be learned by more steps.

## E2 +181 sentences: opposites, grammar, negation
H: vocab ≈ 300; 9 targeted cases scorable; 4 to 6 of 9 pass; other extension = 0; starter ≈ 16/16; val_loss > 0.71.
T: eval_summary.json by category; vocabulary_report.json.
R: vocab 424; scorable 3/9 (opposites only); pass 1/9; starter 16/16; transfer 8/8 (E1: 4/8); val 0.703. FAIL: scorable and pass below H, loss direction wrong.
C: coverage is limited by answer-choice words, not prompt words (am, were, walk, walking, box, bread, missing, ava); transfer jump not explained by the data → suspected initialization noise.

## E3 ×4 corpus: 715 sentences, same 3 categories, missing choice words added
H: +5 scorable (3 grammar, 2 negation); grammar passes; negation fails; vocab ≈ 480.
T: same as E2; per-case choice probabilities.
R: +4 scorable (choice "walks" never written); grammar 1/2 (singular "is" .99 pass; plural fails, "is" .73 vs "are" .23); negation 1/2 (closed .12 vs open .03 pass; colors fail, top choice "green" not in prompt); opposites 1/3 → 0/3; transfer 8/8 → 7/8; correct 25/48 = E2; vocab 478; val 0.733. PARTIAL.
C: more corpus fixes coverage and teaches frequent frames, not pair binding; the E2 opposites hit was luck; ±1 transfer case is noise.

## E4 four new categories only: sequence, spatial, knowledge, categories (E3 files removed)
H: ≥ 8/12 targeted scorable; ≥ 2/12 pass; reference stays 0 scorable (prompt names are banned); opposites, grammar, negation → 0 scorable; vocab ≈ 430.
T: same.
R: 5/12 scorable; 2/12 pass (lang_45 light .0011 vs pillow .0011, near tie; lang_46 fish .0029 vs tree .0015); vocab 418; correct 26/48, 29 scorable; transfer 8/8; val 0.708. FAIL on coverage, PASS on passes, but both passes are marginal.
C: 7 cases unscorable for one missing word each (buy, desk, north, south, sand, wet, metal); "desk" was written twice and both copies fell into the 10% validation split, so it never entered the training vocabulary → a needed word must appear ≥ 5 times to be safe.

## E5 all seven files together: 1,106 sentences, 647 word types against the 509 cap
H: the cap cuts ≈ 148 rarest types → training UNK > 0; ≥ 3 previously scorable cases lost (ice, breakfast, desk); scorable ≈ 33 < 36 (= 31 + 5); correct ≈ 27; val_loss > 0.73.
T: vocabulary_report.json omitted_types; eval_summary; history.
R: 138 types cut; UNK train 0.37%, val 0.74%; scorable 32; correct 29 (best so far); grammar 2/2 (plural now .94 "are", failed in E3); opposites 2/3 (cold .0115 vs warm .0102, marginal; quiet .065); sequence 1/2 (dry .30); negation 0/1 ("missing" cut); train 0.809 vs val 1.258. PASS on cap, coverage and loss direction; correct above H; loss gap far above H.
C: the cap silently removes the rarest words, which are exactly the one-off eval words; first real train/val gap (0.45) → the model starts memorizing the varied text; plural flipped fail → pass with no plural data change → initialization noise again, seed test needed.

## E6 E5 files + coverage.txt: every missing eval word used ≥ 8 times in ordinary sentences
H: no needed word is cut by the cap; scorable ≥ 40 (only 3 reference + 1 name case stay out); correct ≥ 31; val_loss > 1.0.
T: vocabulary_report omitted_types ∩ needed words; eval_summary; history.
R: 193 rare types cut, none needed; scorable 43 (44 possible; "salmon" left out of the coverage list, 2 uses fell in validation); correct 30; extension 6/19; grammar 3/3 (walked .31); opposites 1/3; negation 0/2 (closed case now fails: open .011 vs closed .003); sequence 1/3; spatial 1/3 (book .016); knowledge 0/3 with all four choices ≈ 0.000; categories 0/2; train 0.871, val 0.888. PASS coverage; FAIL correct (30 < 31) and loss (0.89 < 1.0, better than H).
C: coverage is solved by frequency, not by trimming; but on the 19 scorable extension cases the trained model scores 6 while the untrained model scored 8 by chance → the frames teach frequent wrong words as often as right ones; untrained score now 12/48 because chance scales with coverage.

## E7 E6 corpus, 6,000 steps (only change: steps ×2)
H: train loss < 0.80; val loss does not improve (≥ 0.88), overfitting; correct within ±2 of E6's 30.
T: history.json at 3000 vs 6000; eval_summary.
R: train 0.752; val 0.822 (E6: 0.888; this run at step 3000: 0.838); correct 34, extension 10/19; opposites 3/3; spatial 2/3. FAIL on val direction (it improved); correct +4, outside my ±2 band.
C: the varied corpus was under-trained at 3,000 steps, unlike the starter corpus; but +4 is inside the seed spread measured in E8, so it is not evidence by itself.

## E8 E6 corpus, 3,000 steps, seeds 7 and 2026 (with E6 = seed 42, n = 3)
H: correct varies by ≥ 2 across seeds; extension varies by ≥ 2; starter stays 16/16.
T: same corpus, same evals; compare eval_summary across the three runs.
R: correct 30 / 35 / 30 (spread 5); extension 6 / 11 / 7 of 19 (spread 5); starter 16/16 in all; transfer 8/8/7; val loss 0.89 / 1.23 / 0.90; passes common to all three seeds: lang_25, 26, 27, 37. PASS, all three claims.
C: with one run per condition, differences ≤ 5 cases between experiments are not interpretable; grammar agreement and one sequence frame are the only robust learned patterns; the seed also changes the split and the panels, so val loss is not comparable across seeds either.

## E9 E6 corpus + one whole public-domain book ("more corpus" tested literally)
Source: Alice's Adventures in Wonderland, Project Gutenberg #11, header and footer removed, 942 sentences → 1,483 unique passages. Guardrail: 0 problems, 201 warnings. Only 46% of the book's tokens were already in the E6 vocabulary.
H: training UNK > 10%; ≥ 10 of the 43 scorable cases lose a needed word; correct < 28; val_loss > 2.0.
T: vocabulary_report (omitted_types, unknown rates); eval_summary; history; samples.
R: 2,980 types → 2,471 cut; UNK train 8.2%, val 7.3%; scorable 43 → 25 (18 lost; every extension case but one needs a cut word: dogs, walking, warm, yellow, desk, ice, umbrella, kitten...); correct 25 = E2's score; starter 16/16, transfer 8/8; train 1.769, val 1.886; samples at step 3000 contain <UNK> in 2 of 4 lines. PASS on coverage loss and correct; UNK and loss slightly below the thresholds I wrote (8.2% vs 10%, 1.89 vs 2.0).
C: with a 509-word cap, a real book replaces the eval vocabulary with the book's common words; "more corpus" only helps if its word types fit the cap, which no natural text does (best filter: 93 of 942 sentences still add 378 new types).

## E10 E6 corpus + a 90-sentence slice of the same book (dose test)
Slice rule: sentences in which ≥ 60% of the words were already in the E6 vocabulary (90 unique of 942; 2,015 tokens; 378 new types, most used once). Guardrail: 0 problems, 195 warnings.
H: the cap cuts the new rare words, not the needed eval words (≥ 8 uses); UNK train < 2%; scorable stays 43; correct within E6's seed band (25 to 35); val_loss ∈ [0.9, 1.1].
T: same as E9.
R: 1,023 types → 514 cut; UNK train 1.4%, val 2.1%; scorable 42 ("uses" fell under the cut line at 8 uses; the cut line moved up); correct 30, extension 6/18; grammar 3/3; passes lang_25, 26, 27, 37, 45, 48; train 0.839, val 0.758. PASS on UNK, correct and the mechanism; scorable 42 not 43; val loss below the band (better).
C: the E9 damage was proportional to the number of new word types, not to natural text as such; but the cut line rises with every added type, so "≥ 8 uses" is only safe at E6's size; a small slice of natural text neither helped nor hurt the evals.

## E11 E6 corpus minus every guardrail WARNING sentence (does the score depend on near-miss sentences?)
Context: check_corpus.py never blocked a training run in this project (11 runs, 0 blocked; 14 sentences reworded across 3 drafts before their first run; a whole book passed with 0 problems). Its warnings mark sentences where an answer word sits near a content word of its own prompt, e.g. "the soup was hot but the salad was cold". E6 had 195 such sentences (194 unique). This run removes all of them; the guardrail then reports 0 warnings, 0 problems.
H: scorable ≈ 40 (a few eval words lived mostly in warned sentences); correct 25 to 28; lang_27 (yesterday … walked) fails; opposites 0/3; lang_25 and lang_26 still pass.
T: eval_summary; per-case status; compare with E6 (30 correct, 43 scorable).
R: 194 sentences removed (14% of the added corpus); scorable 39 (bird, closed, left, uses fell below the cut line); correct 27, extension 4/15; lang_26 pass, lang_25 unscorable ("bird" lost), lang_27 fails ("walk" over "walked"); opposites 0/3; val 0.923. PASS on 4 of 5 claims; lang_25 was lost to coverage, not to the pattern.
C: the near-miss sentences carried coverage, not score: without them correct drops 3, inside the 5-case seed band; the warnings are a leakage audit trail, not a training constraint.

## What I would do next
Three seeds per condition before claiming any extension gain; a held-out set of new prompts that never guided corpus choices, to test generalization instead of this public development benchmark. "More corpus" in the sense of a book or scraped text (E9) is ruled out by the 509-type cap; more corpus in the sense of more sentences over the same words (E3, E6, E7) is the only version that helps, and it helps coverage more than reasoning.
