# Report
- Tim (Kyoung Tae) Kim
- COSC 76
- PA 3
- Oct 2, 2021
- '22

## Description

## Evaluation



## Discussion Questions

#### Minimax and cutoff test

Vary maximum depth to get a feeling of the speed of the algorithm. Also, have the program print the number of calls it made to minimax as well as the maximum depth.  Record your observations in your document.

For the given seed of 1 in `gui_chess.py`, the minmax algorithm performed sufficiently at depths greater than 1. At depth 1, the minmax failed to win and it reached a stalemate. However, at depth 2 and 3, it was able to come to a win quite quickly. The alogrithm became much slower at depth 4 and greater, due to the exponential increase in the number of nodes visited. 

Below is the sample output of number of calls the minimax and maximum depth for depth 3: 

```
Number of calls made to minmax fn:  1
min function at depth:  1
max function at depth:  2
------------------------------------------
Minmax AI recommending move e2e4
making move, white turn False
------------------------------------------
Random AI recommending move g8h6
making move, white turn True
Number of calls made to minmax fn:  2
min function at depth:  1
max function at depth:  2
------------------------------------------
Minmax AI recommending move d1h5
making move, white turn False
------------------------------------------
Random AI recommending move e7e5
making move, white turn True
Number of calls made to minmax fn:  3
min function at depth:  1
max function at depth:  2
------------------------------------------
Minmax AI recommending move h5e5
making move, white turn False
------------------------------------------
Random AI recommending move d8e7
making move, white turn True
Number of calls made to minmax fn:  4
min function at depth:  1
max function at depth:  2
------------------------------------------
Minmax AI recommending move e5f4
making move, white turn False
------------------------------------------
Random AI recommending move e7g5
making move, white turn True
Number of calls made to minmax fn:  5
min function at depth:  1
max function at depth:  2
------------------------------------------
Minmax AI recommending move f4g5
making move, white turn False
------------------------------------------
Random AI recommending move f7f6
making move, white turn True
Number of calls made to minmax fn:  6
min function at depth:  1
max function at depth:  2
------------------------------------------
Minmax AI recommending move g5h5
making move, white turn False
------------------------------------------
Random AI recommending move h6f7
making move, white turn True
Number of calls made to minmax fn:  7
min function at depth:  1
max function at depth:  2
------------------------------------------
Minmax AI recommending move f1c4
making move, white turn False
------------------------------------------
Random AI recommending move f6f5
making move, white turn True
Number of calls made to minmax fn:  8
min function at depth:  1
max function at depth:  2
------------------------------------------
Minmax AI recommending move h5f7
making move, white turn False
------------------------------------------
Random AI recommending move e8d8
making move, white turn True
Number of calls made to minmax fn:  9
min function at depth:  1
max function at depth:  2
------------------------------------------
Minmax AI recommending move e4f5
making move, white turn False
------------------------------------------
Random AI recommending move h8g8
making move, white turn True
Number of calls made to minmax fn:  10
min function at depth:  1
max function at depth:  2
------------------------------------------
Minmax AI recommending move f7g8
making move, white turn False
------------------------------------------
Random AI recommending move a7a6
making move, white turn True
Number of calls made to minmax fn:  11
min function at depth:  1
max function at depth:  2
------------------------------------------
Minmax AI recommending move g8f8
making move, white turn False
game result:  1-0
```

Note that 


Sample output at depth 1, 2, 3


#### Evaluation Function
Describe the evaluation function used and vary the allowed depth, and discuss in your document the results.

#### Alpha-beta
Discussion question: Record your observations on move-reordering in your document.

#### Iterative deepending
Discussion question: Verify that for some start states, best_move changes (and hopefully improves) as deeper levels are searched. Discuss the observations in your document.
