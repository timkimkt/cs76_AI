# Report
- Tim (Kyoung Tae) Kim
- COSC 76
- PA 6
- Nov 12, 2021
- '22

# Description 

_(a) Description: How do your implemented algorithms work? What design decisions did you make? How you laid out the problems? In particular, for this specific assignment, explain your model precisely, and explain exactly how you compute each new distribution of possible states._

For this problem, I used a matrix (row, col) convention as the probabilities were created with numpy arrays. Thus, for this problem, I assume that the top left corner of the maze is (0, 0) and all robot positions and movements follow this assumption. As with previous problems, the colors are assigned integer values and converted back to strings for printing. 

Once the maze has been loaded and each cell is randomly assigned a color, I create a uniform distribution of the probabilities given the maze dimension and number of walls. Then, the `move_robot` function moves the robot in random directions, staying in place if there is an obstacle or is out of bounds. The sensor measurements are also recorded with the provided accuracy of 0.88. This color sequence is provided as the parameter for the filtering algorithm. 

The filtering algorithm computes the probability distribution for each iteration as follows. First, I compute the probabilities based on the sensor measurements. Given a color, the probability of being a particular cell is 0.88 if the sensor measurement matches the true color of the cell and 0.04 otherwise (as the sensor could be wrong). Thus, the prediction matrix is a 4 x 4 matrix comprised of 0.88 and 0.04. Then for each cell of the maze, I compute the transition matrix by adding 0.25 to the neighboring cells if the robot can move. This means that 0.25 is added to the current cell if the robot is at a corner or next to the wall. Thus, the transition matrix is a 4 x 4 matrix comprised of 0.25 and 0.5. The transition matrix for each cell is multiplied by the probability of the cell from teh distribution at that iteration, where the new probabilities for each cell is stored in an intermediate matrix. Finally, we add this intermediate matrix to the prediction matrix to calculate the new probability distribution, which is then normalized before being used in the next iteration. 

# Evaluation 

_(b) Evaluation: Do your implemented algorithms actually work? How well? If it doesn’t work, can you tell why not? What partial successes did you have that deserve partial credit?_

As shown below, the filtering algorithm works as intended. To test the filtering algorithm, I added several print statements for each iteration. First, the probability distribution and difference compared to the previous distribution can be examined to see how the probabilities change with each step. After each iteration, the probabilities accumulate over time in certain locations of the maze, although it never reaches certainty. 

By displaying the actual robot location, we can see that areas of the highest probability correspond to the actual location of the robot. To make this observation clear, I added an additional display of the maze with `$` placed in cells that have probabilities equal to or geater than the third highest probability value in the cell. 

Finally, the sensed and true color value of the current cell, as well as the current path in terms of colors, have been added to show that the robot is in one of the cells in the highest probabilities except for cases when the sensor has made an erroneous measurement. For example, in the third iteration, the robot is not in one of the cells marked by `$` because of the wrong sensor measurement. This is corrected after a few steps, provided that the measurements are correct and indeed we see that the robot is in one of the `$` from the fifth iteration. 

Although the addition of walls in the maze does not necessarily make it easier to show that the filtering works, it is possible to use mazes such as maze4.maz that contains walls or any other maze that uses `#` to denote walls. 

## Output

```
-----------------------------------------------------------------
Hidden Markov Model Filtering: 
-----------------------------------------------------------------
Intial distribution: 
[[0.0625 0.0625 0.0625 0.0625]
 [0.0625 0.0625 0.0625 0.0625]
 [0.0625 0.0625 0.0625 0.0625]
 [0.0625 0.0625 0.0625 0.0625]]
....
.R..
....
....

Initial Location
(r, c) = (1, 1)
-----------------------------------------------------------------
Prob Distribution after 1 x filter
[[0.015 0.141 0.141 0.015]
 [0.015 0.141 0.141 0.015]
 [0.015 0.015 0.015 0.015]
 [0.141 0.141 0.015 0.015]]
Difference w/ previous distriubtion: 
[[-0.047  0.079  0.079 -0.047]
 [-0.047  0.079  0.079 -0.047]
 [-0.047 -0.047 -0.047 -0.047]
 [ 0.079  0.079 -0.047 -0.047]]
Robot location in maze
.R..
....
....
....

Locations w/ high prob
.$$.
.$$.
....
$$..

location:  (0, 1)
Sensed color: Blue // Actual color: Blue
Current path:  ['Blue']
[['G' 'B' 'B' 'R']
 ['G' 'B' 'B' 'G']
 ['G' 'G' 'R' 'G']
 ['B' 'B' 'R' 'Y']]
-----------------------------------------------------------------
Prob Distribution after 2 x filter
[[0.013 0.148 0.148 0.013]
 [0.013 0.143 0.143 0.013]
 [0.013 0.018 0.013 0.008]
 [0.148 0.143 0.013 0.008]]
Difference w/ previous distriubtion: 
[[-0.002  0.007  0.007 -0.002]
 [-0.002  0.002  0.002 -0.002]
 [-0.002  0.002 -0.002 -0.007]
 [ 0.007  0.002 -0.002 -0.007]]
Robot location in maze
..R.
....
....
....

Locations w/ high prob
.$$.
....
....
$...

location:  (0, 2)
Sensed color: Blue // Actual color: Blue
Current path:  ['Blue', 'Blue']
[['G' 'B' 'B' 'R']
 ['G' 'B' 'B' 'G']
 ['G' 'G' 'R' 'G']
 ['B' 'B' 'R' 'Y']]
-----------------------------------------------------------------
Prob Distribution after 3 x filter
[[0.035 0.062 0.062 0.035]
 [0.035 0.049 0.048 0.034]
 [0.035 0.048 0.035 0.02 ]
 [0.062 0.049 0.034 0.359]]
Difference w/ previous distriubtion: 
[[ 0.022 -0.086 -0.086  0.022]
 [ 0.022 -0.095 -0.095  0.021]
 [ 0.022  0.03   0.022  0.012]
 [-0.086 -0.095  0.021  0.35 ]]
Robot location in maze
....
..R.
....
....

Locations w/ high prob
..$.
....
....
$..$

location:  (1, 2)
Sensed color: Yellow // Actual color: Blue
Current path:  ['Blue', 'Blue', 'Yellow']
[['G' 'B' 'B' 'R']
 ['G' 'B' 'B' 'G']
 ['G' 'G' 'R' 'G']
 ['B' 'B' 'R' 'Y']]
-----------------------------------------------------------------
Prob Distribution after 4 x filter
[[0.012 0.139 0.139 0.012]
 [0.012 0.139 0.138 0.011]
 [0.013 0.012 0.012 0.023]
 [0.14  0.139 0.024 0.035]]
Difference w/ previous distriubtion: 
[[-0.023  0.078  0.078 -0.023]
 [-0.023  0.09   0.09  -0.023]
 [-0.023 -0.035 -0.023  0.002]
 [ 0.078  0.09  -0.01  -0.324]]
Robot location in maze
....
.R..
....
....

Locations w/ high prob
.$$.
....
....
$...

location:  (1, 1)
Sensed color: Blue // Actual color: Blue
Current path:  ['Blue', 'Blue', 'Yellow', 'Blue']
[['G' 'B' 'B' 'R']
 ['G' 'B' 'B' 'G']
 ['G' 'G' 'R' 'G']
 ['B' 'B' 'R' 'Y']]
-----------------------------------------------------------------
Prob Distribution after 5 x filter
[[0.138 0.022 0.022 0.013]
 [0.138 0.017 0.017 0.139]
 [0.138 0.143 0.013 0.135]
 [0.022 0.018 0.014 0.01 ]]
Difference w/ previous distriubtion: 
[[ 0.126 -0.117 -0.117  0.   ]
 [ 0.127 -0.122 -0.121  0.128]
 [ 0.126  0.131  0.002  0.112]
 [-0.117 -0.121 -0.01  -0.025]]
Robot location in maze
....
....
.R..
....

Locations w/ high prob
....
...$
$$..
....

location:  (2, 1)
Sensed color: Green // Actual color: Green
Current path:  ['Blue', 'Blue', 'Yellow', 'Blue', 'Green']
[['G' 'B' 'B' 'R']
 ['G' 'B' 'B' 'G']
 ['G' 'G' 'R' 'G']
 ['B' 'B' 'R' 'Y']]
-----------------------------------------------------------------
Prob Distribution after 6 x filter
[[0.036 0.022 0.014 0.223]
 [0.036 0.029 0.021 0.028]
 [0.036 0.021 0.23  0.027]
 [0.022 0.021 0.215 0.02 ]]
Difference w/ previous distriubtion: 
[[-0.102 -0.    -0.008  0.21 ]
 [-0.103  0.012  0.004 -0.111]
 [-0.102 -0.122  0.217 -0.107]
 [-0.     0.004  0.201  0.009]]
Robot location in maze
....
....
..R.
....

Locations w/ high prob
...$
....
..$.
..$.

location:  (2, 2)
Sensed color: Red // Actual color: Red
Current path:  ['Blue', 'Blue', 'Yellow', 'Blue', 'Green', 'Red']
[['G' 'B' 'B' 'R']
 ['G' 'B' 'B' 'G']
 ['G' 'G' 'R' 'G']
 ['B' 'B' 'R' 'Y']]
-----------------------------------------------------------------
Prob Distribution after 7 x filter
[[0.017 0.016 0.026 0.241]
 [0.018 0.016 0.028 0.028]
 [0.016 0.029 0.229 0.028]
 [0.016 0.026 0.241 0.027]]
Difference w/ previous distriubtion: 
[[-0.019 -0.006  0.012  0.018]
 [-0.018 -0.013  0.007 -0.   ]
 [-0.02   0.008 -0.001  0.   ]
 [-0.006  0.005  0.026  0.007]]
Robot location in maze
....
....
....
..R.

Locations w/ high prob
...$
....
..$.
..$.

location:  (3, 2)
Sensed color: Red // Actual color: Red
Current path:  ['Blue', 'Blue', 'Yellow', 'Blue', 'Green', 'Red', 'Red']
[['G' 'B' 'B' 'R']
 ['G' 'B' 'B' 'G']
 ['G' 'G' 'R' 'G']
 ['B' 'B' 'R' 'Y']]
-----------------------------------------------------------------
Prob Distribution after 8 x filter
[[0.014 0.014 0.028 0.244]
 [0.014 0.015 0.028 0.029]
 [0.014 0.027 0.231 0.028]
 [0.014 0.028 0.243 0.029]]
Difference w/ previous distriubtion: 
[[-0.004 -0.002  0.002  0.003]
 [-0.004 -0.001 -0.     0.001]
 [-0.002 -0.002  0.002  0.   ]
 [-0.002  0.002  0.002  0.002]]
Robot location in maze
....
....
..R.
....

Locations w/ high prob
...$
....
..$.
..$.

location:  (2, 2)
Sensed color: Red // Actual color: Red
Current path:  ['Blue', 'Blue', 'Yellow', 'Blue', 'Green', 'Red', 'Red', 'Red']
[['G' 'B' 'B' 'R']
 ['G' 'B' 'B' 'G']
 ['G' 'G' 'R' 'G']
 ['B' 'B' 'R' 'Y']]
-----------------------------------------------------------------
Prob Distribution after 9 x filter
[[0.013 0.014 0.028 0.244]
 [0.013 0.015 0.028 0.029]
 [0.014 0.027 0.231 0.029]
 [0.014 0.028 0.243 0.029]]
Difference w/ previous distriubtion: 
[[-7.810e-04 -2.328e-04  1.853e-04  5.516e-04]
 [-6.321e-04 -4.585e-04  3.158e-04  2.750e-04]
 [-5.820e-04  1.027e-04  3.407e-05  4.015e-04]
 [-2.036e-04  4.528e-05  5.398e-04  4.388e-04]]
Robot location in maze
....
....
....
..R.

Locations w/ high prob
...$
....
..$.
..$.

location:  (3, 2)
Sensed color: Red // Actual color: Red
Current path:  ['Blue', 'Blue', 'Yellow', 'Blue', 'Green', 'Red', 'Red', 'Red', 'Red']
[['G' 'B' 'B' 'R']
 ['G' 'B' 'B' 'G']
 ['G' 'G' 'R' 'G']
 ['B' 'B' 'R' 'Y']]
-----------------------------------------------------------------
Prob Distribution after 10 x filter
[[0.013 0.014 0.029 0.244]
 [0.013 0.015 0.028 0.029]
 [0.014 0.027 0.231 0.029]
 [0.014 0.028 0.244 0.03 ]]
Difference w/ previous distriubtion: 
[[-1.458e-04 -7.734e-05  4.927e-05  9.396e-05]
 [-1.474e-04 -2.683e-05  2.160e-06  9.278e-05]
 [-7.902e-05 -5.776e-05  8.172e-05  6.907e-05]
 [-5.672e-05  2.910e-05  6.358e-05  1.093e-04]]
Robot location in maze
....
....
..R.
....

Locations w/ high prob
...$
....
..$.
..$.

location:  (2, 2)
Sensed color: Red // Actual color: Red
Current path:  ['Blue', 'Blue', 'Yellow', 'Blue', 'Green', 'Red', 'Red', 'Red', 'Red', 'Red']
[['G' 'B' 'B' 'R']
 ['G' 'B' 'B' 'G']
 ['G' 'G' 'R' 'G']
 ['B' 'B' 'R' 'Y']]
-----------------------------------------------------------------
Colors sequence [3, 3, 2, 3, 1, 0, 0, 0, 0, 0]
Robot positions [(1, 1), (0, 1), (0, 2), (1, 2), (1, 1), (2, 1), (2, 2), (3, 2), (2, 2), (3, 2), (2, 2)]
```
