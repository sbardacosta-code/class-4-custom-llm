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

Untrained baselines: E1 9, E2 6, E3 7, E4 6, E5 7 correct (chance on 4 choices).
Starter group = 16/16 in every trained run. Transfer group: E1 4, E2 8, E3 7, E4 8, E5 8 (of 8).

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
