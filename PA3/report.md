# Report
- Tim (Kyoung Tae) Kim
- COSC 76
- PA 3
- Oct 11, 2021
- '22

## Description
_(a) Description: How do your implemented algorithms work? What design decisions did you make?_

The core of all four algorithms is the minmax function, which has been implemented as follows. The minmax essentially calls the first `self.max_value` function by pushing a legal move into the board. We update the max utility and the associated move whenever we discover a move with higher utility. Note that the list of legal moves is shuffled using `random.shuffle()` to prevent repeated moves when all the moves have the same utility. I assume that the depth at `self.minmax` is zero, which means that when it calls `self.min_value`, it is considered to be at depth one. Both `self.max_value` and `self.min_value` conducts a cutoff test, which checks for maximum depth exceeded, checkmate or stalemate. If any of these conditions evaluate to True, we proceed to calculate the utility of the state using `self.utility`. Otherwise, we continue to explore further down the tree, alternating between `self.max_value` and `self.min_value`. The key difference between these two functions are that `self.max_value` keeps track of the maximum of current highest utility and utility returned by `self.min_value` while `self.min_value` keeps track of the minimum of the lowest current utility and utility returned by `self.max_value`. The cutoff test requires the maximum depth to be specified while the utility function needs to know whether the player is player 1 or 2. Both of these values are passed as paramaters when the AI is instantiated. Note that `True` indicates player 1 while `False` indicates player 2. Please refer to the discussion question section for details on the evaluation (utility) function. 

`AlphaBetaAI` simply expands on this 

## Evaluation
_(b) Evaluation: Do your implemented algorithms actually work? How well? If it doesn’t work, can you tell why not? What partial successes did you have that deserve partial credit?_

The minmax algorithm performs quite well until the depth of 3. It is able to reach a win relatively quickly (after 35 calls to minmax fn), despite exploring 824564 nodes at a depth of 3. As we would expected, the alphabeta algorithm is more efficient. Although this is quite evident by the faster speed at which it returns moves with the same utility, we can further verify this with the number of nodes explored of being much lower at 177714 while the number of calls to alphabeta fn stays the same at 35. Note that node re-odering portion of `AlphaBetaAI.py` (lines 159 - 175) have been commented out to demonstrate that the utility of the moves are the same for both functions (thus showing that alphabeta has been implemented correctly). This impact of the node reordering is further detailed in the discussion questions section. (Note that all the `sleep()` methods have been turned off for ease of testing)

## Discussion Questions

### Minimax and cutoff test
_Vary maximum depth to get a feeling of the speed of the algorithm. Also, have the program print the number of calls it made to minimax as well as the maximum depth.  Record your observations in your document._

The minmax algorithm performed quite well until the depths of 3, often reaching a checkmate (win). However, it began to slow down from depth 4 onwards, due to the exponential increase in the number of nodes visited. Attached at the end of this report are sample outputs from `MinimaxAI.py` and `AlphaBetaAI.py` that contain information on the number times `minimax`, `max_value` and `min_value` are called and total number of nodes visited. To replicate this output, you can play MinimaxAI as player 1 with 3 as the given maximum depth and using the seed of 1 in `gui_chess.py`.

### Evaluation Function
_Describe the evaluation function used and vary the allowed depth, and discuss in your document the results._

The utility (evaluation) function was quite a simple material heuristic that was a weighted net sum of the pieces remaining on the boards. After determining whether the player is player 1 or 2, the player's own pieces were added to the total utility while the opponents pieces were subtracted. To make things more simple, I calculated the utility function from the perspective of player 1 and returned the negative of the total utility if the player was player 2. The piece weights followed chess score conventions (pawn: 1, knight: 3, bishop: 3, rook: 5, queen: 5) but the king was weighted highly to make checkmates more desirable. In addition, `is_stalemate()`, `is_fivefold_repetition()` and `is_insufficient_material()` were used to make the utility function indifferent to draws while the case of `is_checkmate()` coinciding with the player's turn (indicating that the player has lost), a large negative utility was returned while in the opposite case (where the player has won), a large positive utility was returned. 

### Alpha-beta
_Discussion question: Record your observations on move-reordering in your document._

For my implementation, move-reordering did reduce the time taken to reach checkmate, but it was not possible to compare if it returns the same utility as alpha-beta without reordering, as it returned a win in fewer moves (which is to be expected in adverserial problems). After implementing this reordering, the node count decreased to 83291 and the number calls made to alphabeta fn (i.e. the number of moves to a win) also decreased to 83291, which shows how node-reodering can improve the performance of alpha-beta, by causing the pruning to occur more frequently. 

#### Iterative deepending
_Discussion question: Verify that for some start states, best_move changes (and hopefully improves) as deeper levels are searched. Discuss the observations in your document._

As shown by the output attached, we can see that for certain starting states, better moves are found are deeper levels. Usually, depth 2 seems sufficient in finding better moves but we can also see several instances where exploring until depth 4 is able to find a better move. This demonstrates how deeper (but time-consuming) searches may yield better moves. 


## Sample Output

### MinimaxAI.py
_seed 1, depth 3, player1=minimax, player2=RandomAI_

```
making move, white turn True
Number of calls made to minmax fn:  1
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 0
------------------------------------------
Minmax AI recommending move a2a3
making move, white turn False
------------------------------------------
Random AI recommending move f7f5
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  2
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 0
------------------------------------------
Minmax AI recommending move a3a4
making move, white turn False
------------------------------------------
Random AI recommending move c7c5
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  3
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 0
------------------------------------------
Minmax AI recommending move c2c3
making move, white turn False
------------------------------------------
Random AI recommending move g7g6
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  4
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 1
------------------------------------------
Minmax AI recommending move d1b3
making move, white turn False
------------------------------------------
Random AI recommending move d7d6
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  5
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 1
------------------------------------------
Minmax AI recommending move a1a3
making move, white turn False
------------------------------------------
Random AI recommending move b8c6
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  6
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 3
------------------------------------------
Minmax AI recommending move b3d5
making move, white turn False
------------------------------------------
Random AI recommending move h7h6
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  7
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 3
------------------------------------------
Minmax AI recommending move g2g3
making move, white turn False
------------------------------------------
Random AI recommending move c8e6
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  8
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 6
------------------------------------------
Minmax AI recommending move d5e6
making move, white turn False
------------------------------------------
Random AI recommending move f5f4
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  9
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 7
------------------------------------------
Minmax AI recommending move g3f4
making move, white turn False
------------------------------------------
Random AI recommending move h6h5
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  10
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 8
------------------------------------------
Minmax AI recommending move e6g6
making move, white turn False
------------------------------------------
Random AI recommending move e8d7
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  11
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 8
------------------------------------------
Minmax AI recommending move a3a1
making move, white turn False
------------------------------------------
Random AI recommending move d8b8
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  12
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 8
------------------------------------------
Minmax AI recommending move g6g2
making move, white turn False
------------------------------------------
Random AI recommending move d7e8
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  13
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 8
------------------------------------------
Minmax AI recommending move e2e3
making move, white turn False
------------------------------------------
Random AI recommending move e8d7
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  14
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 8
------------------------------------------
Minmax AI recommending move b1a3
making move, white turn False
------------------------------------------
Random AI recommending move h8h7
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  15
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 11
------------------------------------------
Minmax AI recommending move g2g8
making move, white turn False
------------------------------------------
Random AI recommending move b8c7
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  16
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 14
------------------------------------------
Minmax AI recommending move g8h7
making move, white turn False
------------------------------------------
Random AI recommending move c6b8
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  17
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 16
------------------------------------------
Minmax AI recommending move h7h8
making move, white turn False
------------------------------------------
Random AI recommending move b7b6
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  18
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 19
------------------------------------------
Minmax AI recommending move h8f8
making move, white turn False
------------------------------------------
Random AI recommending move e7e6
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  19
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 21
------------------------------------------
Minmax AI recommending move f1b5
making move, white turn False
------------------------------------------
Random AI recommending move c7c6
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  20
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 21
------------------------------------------
Minmax AI recommending move b5c6
making move, white turn False
------------------------------------------
Random AI recommending move d7c6
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  21
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 21
------------------------------------------
Minmax AI recommending move e1e2
making move, white turn False
------------------------------------------
Random AI recommending move c6b7
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  22
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 21
------------------------------------------
Minmax AI recommending move g1h3
making move, white turn False
------------------------------------------
Random AI recommending move e6e5
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  23
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 21
------------------------------------------
Minmax AI recommending move f4e5
making move, white turn False
------------------------------------------
Random AI recommending move a7a6
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  24
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 23
------------------------------------------
Minmax AI recommending move f8d6
making move, white turn False
------------------------------------------
Random AI recommending move b7c8
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  25
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 23
------------------------------------------
Minmax AI recommending move a1a2
making move, white turn False
------------------------------------------
Random AI recommending move c8b7
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  26
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 23
------------------------------------------
Minmax AI recommending move h3g1
making move, white turn False
------------------------------------------
Random AI recommending move b8c6
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  27
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 23
------------------------------------------
Minmax AI recommending move d6d5
making move, white turn False
------------------------------------------
Random AI recommending move b6b5
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  28
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 23
------------------------------------------
Minmax AI recommending move a4a5
making move, white turn False
------------------------------------------
Random AI recommending move b7b8
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  29
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 24
------------------------------------------
Minmax AI recommending move d5c6
making move, white turn False
------------------------------------------
Random AI recommending move a8a7
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  30
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 28
------------------------------------------
Minmax AI recommending move c6b6
making move, white turn False
------------------------------------------
Random AI recommending move b8a8
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  31
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 25
------------------------------------------
Minmax AI recommending move b6c5
making move, white turn False
------------------------------------------
Random AI recommending move a7b7
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  32
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 29
------------------------------------------
Minmax AI recommending move c5c8
making move, white turn False
------------------------------------------
Random AI recommending move a8a7
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  33
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 25
------------------------------------------
Minmax AI recommending move c3c4
making move, white turn False
------------------------------------------
Random AI recommending move b7h7
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  34
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 26
------------------------------------------
Minmax AI recommending move c4b5
making move, white turn False
------------------------------------------
Random AI recommending move h7e7
------------------------------------------
making move, white turn True
Number of calls made to minmax fn:  35
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 100000
------------------------------------------
Minmax AI recommending move b5b6
making move, white turn False
game result:  1-0

```


### AlphaBetaAI.py
_seed 1, depth 3, player1=AlphaBetaAI, player2=RandomAI_

```
making move, white turn True
Number of calls made to alphabeta fn:  1
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 0
------------------------------------------
Alphabeta AI recommending move a2a3
making move, white turn False
------------------------------------------
Random AI recommending move f7f5
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  2
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 0
------------------------------------------
Alphabeta AI recommending move a3a4
making move, white turn False
------------------------------------------
Random AI recommending move c7c5
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  3
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 0
------------------------------------------
Alphabeta AI recommending move c2c3
making move, white turn False
------------------------------------------
Random AI recommending move g7g6
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  4
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 1
------------------------------------------
Alphabeta AI recommending move d1b3
making move, white turn False
------------------------------------------
Random AI recommending move d7d6
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  5
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 1
------------------------------------------
Alphabeta AI recommending move a1a3
making move, white turn False
------------------------------------------
Random AI recommending move b8c6
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  6
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 3
------------------------------------------
Alphabeta AI recommending move b3d5
making move, white turn False
------------------------------------------
Random AI recommending move h7h6
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  7
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 3
------------------------------------------
Alphabeta AI recommending move g2g3
making move, white turn False
------------------------------------------
Random AI recommending move c8e6
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  8
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 6
------------------------------------------
Alphabeta AI recommending move d5e6
making move, white turn False
------------------------------------------
Random AI recommending move f5f4
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  9
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 7
------------------------------------------
Alphabeta AI recommending move g3f4
making move, white turn False
------------------------------------------
Random AI recommending move h6h5
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  10
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 8
------------------------------------------
Alphabeta AI recommending move e6g6
making move, white turn False
------------------------------------------
Random AI recommending move e8d7
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  11
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 8
------------------------------------------
Alphabeta AI recommending move a3a1
making move, white turn False
------------------------------------------
Random AI recommending move d8b8
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  12
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 8
------------------------------------------
Alphabeta AI recommending move g6g2
making move, white turn False
------------------------------------------
Random AI recommending move d7e8
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  13
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 8
------------------------------------------
Alphabeta AI recommending move e2e3
making move, white turn False
------------------------------------------
Random AI recommending move e8d7
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  14
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 8
------------------------------------------
Alphabeta AI recommending move b1a3
making move, white turn False
------------------------------------------
Random AI recommending move h8h7
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  15
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 11
------------------------------------------
Alphabeta AI recommending move g2g8
making move, white turn False
------------------------------------------
Random AI recommending move b8c7
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  16
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 14
------------------------------------------
Alphabeta AI recommending move g8h7
making move, white turn False
------------------------------------------
Random AI recommending move c6b8
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  17
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 16
------------------------------------------
Alphabeta AI recommending move h7h8
making move, white turn False
------------------------------------------
Random AI recommending move b7b6
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  18
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 19
------------------------------------------
Alphabeta AI recommending move h8f8
making move, white turn False
------------------------------------------
Random AI recommending move e7e6
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  19
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 21
------------------------------------------
Alphabeta AI recommending move f1b5
making move, white turn False
------------------------------------------
Random AI recommending move c7c6
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  20
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 21
------------------------------------------
Alphabeta AI recommending move b5c6
making move, white turn False
------------------------------------------
Random AI recommending move d7c6
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  21
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 21
------------------------------------------
Alphabeta AI recommending move e1e2
making move, white turn False
------------------------------------------
Random AI recommending move c6b7
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  22
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 21
------------------------------------------
Alphabeta AI recommending move g1h3
making move, white turn False
------------------------------------------
Random AI recommending move e6e5
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  23
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 21
------------------------------------------
Alphabeta AI recommending move f4e5
making move, white turn False
------------------------------------------
Random AI recommending move a7a6
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  24
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 23
------------------------------------------
Alphabeta AI recommending move f8d6
making move, white turn False
------------------------------------------
Random AI recommending move b7c8
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  25
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 23
------------------------------------------
Alphabeta AI recommending move a1a2
making move, white turn False
------------------------------------------
Random AI recommending move c8b7
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  26
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 23
------------------------------------------
Alphabeta AI recommending move h3g1
making move, white turn False
------------------------------------------
Random AI recommending move b8c6
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  27
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 23
------------------------------------------
Alphabeta AI recommending move d6d5
making move, white turn False
------------------------------------------
Random AI recommending move b6b5
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  28
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 23
------------------------------------------
Alphabeta AI recommending move a4a5
making move, white turn False
------------------------------------------
Random AI recommending move b7b8
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  29
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 24
------------------------------------------
Alphabeta AI recommending move d5c6
making move, white turn False
------------------------------------------
Random AI recommending move a8a7
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  30
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 28
------------------------------------------
Alphabeta AI recommending move c6b6
making move, white turn False
------------------------------------------
Random AI recommending move b8a8
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  31
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 25
------------------------------------------
Alphabeta AI recommending move b6c5
making move, white turn False
------------------------------------------
Random AI recommending move a7b7
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  32
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 29
------------------------------------------
Alphabeta AI recommending move c5c8
making move, white turn False
------------------------------------------
Random AI recommending move a8a7
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  33
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 25
------------------------------------------
Alphabeta AI recommending move c3c4
making move, white turn False
------------------------------------------
Random AI recommending move b7h7
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  34
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 26
------------------------------------------
Alphabeta AI recommending move c4b5
making move, white turn False
------------------------------------------
Random AI recommending move h7e7
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  35
min function at depth:  1
max function at depth:  2
min function at depth:  3
Utility of move selected 100000
------------------------------------------
Alphabeta AI recommending move b5b6
making move, white turn False
game result:  1-0
```

### IterativeAI.py
_seed 1, depth 4, player1=IterativeAI, player2=RandomAI_


```
making move, white turn True
Number of calls made to alphabeta fn:  1
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  a2a3 with utility of  0
The best move for depth  2 is  a2a3 with utility of  0
The best move for depth  3 is  a2a3 with utility of  0
The best move for depth  4 is  a2a3 with utility of  0
Utility of move selected 0
------------------------------------------
Iterative AI recommending move a2a3
making move, white turn False
------------------------------------------
Random AI recommending move f7f5
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  2
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  a3a4 with utility of  0
The best move for depth  2 is  a3a4 with utility of  0
The best move for depth  3 is  a3a4 with utility of  0
The best move for depth  4 is  a3a4 with utility of  0
Utility of move selected 0
------------------------------------------
Iterative AI recommending move a3a4
making move, white turn False
------------------------------------------
Random AI recommending move c7c5
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  3
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  e2e3 with utility of  0
The best move for depth  2 is  e2e3 with utility of  0
The best move for depth  3 is  e2e3 with utility of  0
The best move for depth  4 is  e2e3 with utility of  0
Utility of move selected 0
------------------------------------------
Iterative AI recommending move e2e3
making move, white turn False
------------------------------------------
Random AI recommending move g7g6
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  4
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  g2g4 with utility of  0
The best move for depth  2 is  f1b5 with utility of  1
The best move for depth  3 is  f1b5 with utility of  1
The best move for depth  4 is  f1b5 with utility of  1
Utility of move selected 1
------------------------------------------
Iterative AI recommending move f1b5
making move, white turn False
------------------------------------------
Random AI recommending move a7a5
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  5
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  b5c4 with utility of  0
The best move for depth  2 is  g2g3 with utility of  1
The best move for depth  3 is  g2g3 with utility of  1
The best move for depth  4 is  g2g3 with utility of  1
Utility of move selected 1
------------------------------------------
Iterative AI recommending move g2g3
making move, white turn False
------------------------------------------
Random AI recommending move h7h6
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  6
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  b5c4 with utility of  0
The best move for depth  2 is  f2f3 with utility of  1
The best move for depth  3 is  f2f3 with utility of  1
The best move for depth  4 is  f2f3 with utility of  1
Utility of move selected 1
------------------------------------------
Iterative AI recommending move f2f3
making move, white turn False
------------------------------------------
Random AI recommending move h8h7
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  7
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  b5c4 with utility of  0
The best move for depth  2 is  b1c3 with utility of  1
The best move for depth  3 is  b1c3 with utility of  1
The best move for depth  4 is  b1c3 with utility of  1
Utility of move selected 1
------------------------------------------
Iterative AI recommending move b1c3
making move, white turn False
------------------------------------------
Random AI recommending move h7g7
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  8
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  c3d5 with utility of  0
The best move for depth  2 is  e1e2 with utility of  1
The best move for depth  3 is  e1e2 with utility of  1
The best move for depth  4 is  e1e2 with utility of  1
Utility of move selected 1
------------------------------------------
Iterative AI recommending move e1e2
making move, white turn False
------------------------------------------
Random AI recommending move h6h5
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  9
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  b5c4 with utility of  0
The best move for depth  2 is  c3b1 with utility of  1
The best move for depth  3 is  c3b1 with utility of  1
The best move for depth  4 is  c3b1 with utility of  1
Utility of move selected 1
------------------------------------------
Iterative AI recommending move c3b1
making move, white turn False
------------------------------------------
Random AI recommending move h5h4
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  10
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  b5d3 with utility of  0
The best move for depth  2 is  g3h4 with utility of  2
The best move for depth  3 is  g3h4 with utility of  2
The best move for depth  4 is  g3h4 with utility of  2
Utility of move selected 2
------------------------------------------
Iterative AI recommending move g3h4
making move, white turn False
------------------------------------------
Random AI recommending move b8c6
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  11
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  d1f1 with utility of  1
The best move for depth  2 is  d1f1 with utility of  2
The best move for depth  3 is  d1f1 with utility of  2
The best move for depth  4 is  b5c6 with utility of  4
Utility of move selected 4
------------------------------------------
Iterative AI recommending move b5c6
making move, white turn False
------------------------------------------
Random AI recommending move a8b8
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  12
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  c6d5 with utility of  3
The best move for depth  2 is  c6d5 with utility of  5
The best move for depth  3 is  c6d5 with utility of  5
The best move for depth  4 is  c6d5 with utility of  5
Utility of move selected 5
------------------------------------------
Iterative AI recommending move c6d5
making move, white turn False
------------------------------------------
Random AI recommending move e7e5
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  13
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  b2b3 with utility of  3
The best move for depth  2 is  b2b3 with utility of  5
The best move for depth  3 is  b2b3 with utility of  5
The best move for depth  4 is  d5g8 with utility of  7
Utility of move selected 7
------------------------------------------
Iterative AI recommending move d5g8
making move, white turn False
------------------------------------------
Random AI recommending move f8d6
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  14
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  g8c4 with utility of  5
The best move for depth  2 is  g8d5 with utility of  7
The best move for depth  3 is  g8d5 with utility of  7
The best move for depth  4 is  g8d5 with utility of  7
Utility of move selected 7
------------------------------------------
Iterative AI recommending move g8d5
making move, white turn False
------------------------------------------
Random AI recommending move e8f8
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  15
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  d1e1 with utility of  6
The best move for depth  2 is  b1a3 with utility of  7
The best move for depth  3 is  b1a3 with utility of  7
The best move for depth  4 is  d5b7 with utility of  8
Utility of move selected 8
------------------------------------------
Iterative AI recommending move d5b7
making move, white turn False
------------------------------------------
Random AI recommending move f8f7
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  16
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  b7c8 with utility of  7
The best move for depth  2 is  b7c8 with utility of  8
The best move for depth  3 is  b7c8 with utility of  8
The best move for depth  4 is  b7c8 with utility of  11
Utility of move selected 11
------------------------------------------
Iterative AI recommending move b7c8
making move, white turn False
------------------------------------------
Random AI recommending move d8g8
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  17
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  c8d7 with utility of  11
The best move for depth  2 is  c8d7 with utility of  13
The best move for depth  3 is  c8d7 with utility of  13
The best move for depth  4 is  c8d7 with utility of  13
Utility of move selected 13
------------------------------------------
Iterative AI recommending move c8d7
making move, white turn False
------------------------------------------
Random AI recommending move g8c8
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  18
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  d7c8 with utility of  14
The best move for depth  2 is  d7c8 with utility of  14
The best move for depth  3 is  d7c8 with utility of  14
The best move for depth  4 is  d7c8 with utility of  17
Utility of move selected 17
------------------------------------------
Iterative AI recommending move d7c8
making move, white turn False
------------------------------------------
Random AI recommending move g7g8
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  19
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  c8a6 with utility of  16
The best move for depth  2 is  c8d7 with utility of  18
The best move for depth  3 is  c8d7 with utility of  18
The best move for depth  4 is  c8d7 with utility of  18
Utility of move selected 18
------------------------------------------
Iterative AI recommending move c8d7
making move, white turn False
------------------------------------------
Random AI recommending move f7g7
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  20
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  a1a2 with utility of  16
The best move for depth  2 is  a1a2 with utility of  18
The best move for depth  3 is  a1a2 with utility of  18
The best move for depth  4 is  a1a2 with utility of  18
Utility of move selected 18
------------------------------------------
Iterative AI recommending move a1a2
making move, white turn False
------------------------------------------
Random AI recommending move b8b7
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  21
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  d7c6 with utility of  16
The best move for depth  2 is  d7e6 with utility of  18
The best move for depth  3 is  d7e6 with utility of  18
The best move for depth  4 is  d7e6 with utility of  18
Utility of move selected 18
------------------------------------------
Iterative AI recommending move d7e6
making move, white turn False
------------------------------------------
Random AI recommending move g8b8
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  22
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  b2b3 with utility of  16
The best move for depth  2 is  b2b3 with utility of  18
The best move for depth  3 is  b2b3 with utility of  18
The best move for depth  4 is  b2b3 with utility of  18
Utility of move selected 18
------------------------------------------
Iterative AI recommending move b2b3
making move, white turn False
------------------------------------------
Random AI recommending move f5f4
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  23
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  e3f4 with utility of  17
The best move for depth  2 is  e6d5 with utility of  18
The best move for depth  3 is  e6d5 with utility of  18
The best move for depth  4 is  e6d5 with utility of  18
Utility of move selected 18
------------------------------------------
Iterative AI recommending move e6d5
making move, white turn False
------------------------------------------
Random AI recommending move b8c8
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  24
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  d5b7 with utility of  21
The best move for depth  2 is  d5b7 with utility of  23
The best move for depth  3 is  d5b7 with utility of  23
The best move for depth  4 is  d5b7 with utility of  23
Utility of move selected 23
------------------------------------------
Iterative AI recommending move d5b7
making move, white turn False
------------------------------------------
Random AI recommending move d6b8
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  25
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  b7c8 with utility of  27
The best move for depth  2 is  b7c8 with utility of  27
The best move for depth  3 is  b7c8 with utility of  27
The best move for depth  4 is  b7c8 with utility of  27
Utility of move selected 27
------------------------------------------
Iterative AI recommending move b7c8
making move, white turn False
------------------------------------------
Random AI recommending move b8a7
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  26
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  c2c3 with utility of  27
The best move for depth  2 is  c2c3 with utility of  27
The best move for depth  3 is  c2c3 with utility of  27
The best move for depth  4 is  e3f4 with utility of  28
Utility of move selected 28
------------------------------------------
Iterative AI recommending move e3f4
making move, white turn False
------------------------------------------
Random AI recommending move e5f4
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  27
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  a2a3 with utility of  27
The best move for depth  2 is  g1h3 with utility of  28
The best move for depth  3 is  g1h3 with utility of  28
The best move for depth  4 is  g1h3 with utility of  28
Utility of move selected 28
------------------------------------------
Iterative AI recommending move g1h3
making move, white turn False
------------------------------------------
Random AI recommending move g7f7
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  28
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  h3f4 with utility of  28
The best move for depth  2 is  h3f4 with utility of  29
The best move for depth  3 is  h3f4 with utility of  29
The best move for depth  4 is  h3f4 with utility of  29
Utility of move selected 29
------------------------------------------
Iterative AI recommending move h3f4
making move, white turn False
------------------------------------------
Random AI recommending move f7f8
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  29
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  d1g1 with utility of  29
The best move for depth  2 is  d1g1 with utility of  29
The best move for depth  3 is  d1g1 with utility of  29
The best move for depth  4 is  d1g1 with utility of  29
Utility of move selected 29
------------------------------------------
Iterative AI recommending move d1g1
making move, white turn False
------------------------------------------
Random AI recommending move f8e7
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  30
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  g1g4 with utility of  29
The best move for depth  2 is  f4g6 with utility of  30
The best move for depth  3 is  f4g6 with utility of  30
The best move for depth  4 is  f4g6 with utility of  30
Utility of move selected 30
------------------------------------------
Iterative AI recommending move f4g6
making move, white turn False
------------------------------------------
Random AI recommending move e7d8
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  31
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  c8a6 with utility of  29
The best move for depth  2 is  c8a6 with utility of  30
The best move for depth  3 is  c8a6 with utility of  30
The best move for depth  4 is  c8a6 with utility of  30
Utility of move selected 30
------------------------------------------
Iterative AI recommending move c8a6
making move, white turn False
------------------------------------------
Random AI recommending move a7b6
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  32
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  a2a3 with utility of  29
The best move for depth  2 is  a2a3 with utility of  30
The best move for depth  3 is  a2a3 with utility of  30
The best move for depth  4 is  a2a3 with utility of  30
Utility of move selected 30
------------------------------------------
Iterative AI recommending move a2a3
making move, white turn False
------------------------------------------
Random AI recommending move c5c4
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  33
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  g1b6 with utility of  33
The best move for depth  2 is  g1b6 with utility of  33
The best move for depth  3 is  g1b6 with utility of  33
The best move for depth  4 is  g1b6 with utility of  33
Utility of move selected 33
------------------------------------------
Iterative AI recommending move g1b6
making move, white turn False
------------------------------------------
Random AI recommending move d8d7
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  34
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  a6b5 with utility of  100000
The best move for depth  2 is  a6b5 with utility of  100000
The best move for depth  3 is  a6b5 with utility of  100000
The best move for depth  4 is  a6b5 with utility of  100000
Utility of move selected 100000
------------------------------------------
Iterative AI recommending move a6b5
making move, white turn False
------------------------------------------
Random AI recommending move d7c8
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  35
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  h1d1 with utility of  100000
The best move for depth  2 is  h1d1 with utility of  100000
The best move for depth  3 is  h1d1 with utility of  100000
The best move for depth  4 is  h1d1 with utility of  100000
Utility of move selected 100000
------------------------------------------
Iterative AI recommending move h1d1
making move, white turn False
------------------------------------------
Random AI recommending move c4c3
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  36
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  d1g1 with utility of  100000
The best move for depth  2 is  d1g1 with utility of  100000
The best move for depth  3 is  d1g1 with utility of  100000
The best move for depth  4 is  d1g1 with utility of  100000
Utility of move selected 100000
------------------------------------------
Iterative AI recommending move d1g1
making move, white turn False
------------------------------------------
Random AI recommending move c3d2
------------------------------------------
making move, white turn True
Number of calls made to alphabeta fn:  37
min function at depth:  1
max function at depth:  2
The best move for depth  1 is  g6e7 with utility of  100000
The best move for depth  2 is  g6e7 with utility of  100000
The best move for depth  3 is  g6e7 with utility of  100000
The best move for depth  4 is  g6e7 with utility of  100000
Utility of move selected 100000
------------------------------------------
Iterative AI recommending move g6e7
making move, white turn False
game result:  1-0
```
