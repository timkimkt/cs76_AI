# Report
- Tim (Kyoung Tae) Kim
- COSC 76
- PA 2
- Sep 30, 2021
- '22

# Description

## Implement A* Search

#### Implementation 

The A* search algorithm works very similar to the breadth-first search algorithm. The key difference arises from the fact that we are using a priority queue in the form of a heap. By modifying its comparison operator function, we are able to pop the nodes with the lowest total cost, which is calculated by the sum of the heuristic and transition cost. Note that we do not actually pop the node with the higher cost. Instead, we use a dictionary to keep track of nodes visited and their lowest total cost. Thus, for each successor state, if the state has not yet been observed, we pack it into a search node and push it to the priority queue. If the successor has been observed (i.e. in the visited dictionary) and if the successor's total cost is lower than the one in the dictionary, we update the cost and push a new search node into the heap with this lower cost. If we reach the goal state, we update the solution cost and path and return. Otherwise, we will continue in this fashion until the priority queue is empty, skipping any nodes that have already been visited and have a higher cost. 

#### Design

Although the action taken when we find a state that has not been visited and action taken when we find that a visited state can have a lower total cost, the conditions have been separated out to make the thought process more clear. As noted, we do not actually remove a repeated node with the higher cost from the heap so the performance will be affected if the heap becomes too big. 

## MazeworldProblem (Multiple Robot)

#### Modeling the problem

The key to modeling the problem comes from deciding on what the start and successive states will look like. Each state is represented by (robot\_to\_be\_moved, robot1\_coordinates, robot2\_coodinates, etc...). Thus, the starting state is simply initialized as the first robot (indexed from zero) and the starting location of the robot(s) in the maze. Then, the successors function will parse the state to update the robot to be moved next and add a state for every valid direction that it can move in. Note that if a robot is already in the goal location, it will stop moving and skip to the next robot. The goal test function simply checks if all the robots are in the predetermined goal locations.

#### Implementation & Design

Due to the use of tuples to represent each state, it was sometimes necessary to convert the tuple into a list to modify certain coordinates before converting them back into a tuple. While the manhattan heuristics decreases the number of nodes visited compared to the null heuristic, it was actually much more effective to use the square of the manhattan heuristic (although it would not be considered admissible). 

## SensorlessProblem (Blind Robot)

#### Modeling the problem

Again, the key modeling the problem was to understand how one might get from the starting state (all possible locations of the robot) to the goal state (one remaining possible location of the robot). It is important to remember that the robot is 'blind', meaning it cannot tell if it has been moved to a particular direction or stayed in place due to a wall or an obstacle. For each state, there are going to be four successors (East, West, South, North) and we will keep the set of coordinates that are valid (i.e. floors). Since coorindates will be repeated and sets only keep one distinct element, we will be left with one remaining coordinate. 

#### Implementation & Design

The heuristic function in this case was simply the number of coordinates in the successor state since we would want to explore the path that would help us reduce the number of possible coordinates in the shortest time period. The start state is initialized using `create_start_state` function which is called in the constructor. The `animate_path` function was modified to reflect that the fact that the solution returns a list of tuple of tuples, where the outer tuple represents a state and inner tuples represent the robot coordinates. 

## Maze Examples

#### maze4.maz
```
#####
#.#.#
#...#
#.#.#
###.#

\robot 1 1
\robot 3 0
```
```
----
Mazeworld problem: 
attempted with search method Astar with heuristic null_heuristic
number of nodes visited: 86
solution length: 18
cost: 9
path: [(0, 1, 1, 3, 0), (1, 1, 1, 3, 0), (0, 1, 1, 3, 1), (1, 1, 1, 3, 1), (0, 1, 1, 3, 2), (1, 1, 1, 3, 2), (0, 1, 1, 2, 2), (1, 1, 1, 2, 2), (0, 1, 1, 1, 2), (1, 1, 1, 1, 2), (0, 1, 1, 1, 3), (1, 1, 2, 1, 3), (0, 1, 2, 1, 3), (1, 2, 2, 1, 3), (0, 2, 2, 1, 3), (1, 3, 2, 1, 3), (0, 3, 2, 1, 3), (1, 3, 3, 1, 3)]

----
Mazeworld problem: 
attempted with search method Astar with heuristic manhattan_heuristic
number of nodes visited: 66
solution length: 18
cost: 9
path: [(0, 1, 1, 3, 0), (1, 1, 1, 3, 0), (0, 1, 1, 3, 1), (1, 1, 1, 3, 1), (0, 1, 1, 3, 2), (1, 1, 1, 3, 2), (0, 1, 1, 2, 2), (1, 1, 1, 2, 2), (0, 1, 1, 1, 2), (1, 1, 1, 1, 2), (0, 1, 1, 1, 3), (1, 1, 2, 1, 3), (0, 1, 2, 1, 3), (1, 2, 2, 1, 3), (0, 2, 2, 1, 3), (1, 3, 2, 1, 3), (0, 3, 2, 1, 3), (1, 3, 3, 1, 3)]
```

This is a relatively simple 5 x 5 maze, but the goal locations can be set set so that the robots would have to 'cross paths with each other.' The animated path for this maze can be found at the end of the report.

#### maze5.maz
```
###..###
#......#
#..#...#
#...#..#
#..#...#
#...#..#
#..#...#
#...#..#
\robot 1 0
\robot 2 0
\robot 5 0
```
```
----
Mazeworld problem: 
attempted with search method Astar with heuristic null_heuristic
number of nodes visited: 144752
solution length: 61
cost: 39
path: [(0, 1, 0, 2, 0, 5, 0), (1, 1, 0, 2, 0, 5, 0), (2, 1, 0, 2, 1, 5, 0), (0, 1, 0, 2, 1, 5, 0), (1, 1, 0, 2, 1, 5, 0), (2, 1, 0, 2, 2, 5, 0), (0, 1, 0, 2, 2, 5, 0), (1, 1, 0, 2, 2, 5, 0), (2, 1, 0, 2, 3, 5, 0), (0, 1, 0, 2, 3, 5, 1), (1, 1, 0, 2, 3, 5, 1), (2, 1, 0, 2, 4, 5, 1), (0, 1, 0, 2, 4, 5, 2), (1, 1, 0, 2, 4, 5, 2), (2, 1, 0, 2, 5, 5, 2), (0, 1, 0, 2, 5, 5, 3), (1, 1, 0, 2, 5, 5, 3), (2, 1, 0, 2, 6, 5, 3), (0, 1, 0, 2, 6, 5, 4), (1, 1, 1, 2, 6, 5, 4), (2, 1, 1, 3, 6, 5, 4), (0, 1, 1, 3, 6, 5, 5), (1, 1, 2, 3, 6, 5, 5), (2, 1, 2, 4, 6, 5, 5), (0, 1, 2, 4, 6, 5, 6), (1, 1, 3, 4, 6, 5, 6), (2, 1, 3, 4, 5, 5, 6), (0, 1, 3, 4, 5, 4, 6), (1, 1, 4, 4, 5, 4, 6), (2, 1, 4, 4, 5, 4, 6), (0, 1, 4, 4, 5, 3, 6), (1, 1, 5, 4, 5, 3, 6), (2, 1, 5, 4, 5, 3, 6), (0, 1, 5, 4, 5, 2, 6), (1, 1, 6, 4, 5, 2, 6), (2, 1, 6, 4, 5, 2, 6), (0, 1, 6, 4, 5, 2, 5), (1, 2, 6, 4, 5, 2, 5), (2, 2, 6, 4, 5, 2, 5), (0, 2, 6, 4, 5, 2, 5), (1, 3, 6, 4, 5, 2, 5), (2, 3, 6, 4, 5, 2, 5), (0, 3, 6, 4, 5, 2, 5), (1, 4, 6, 4, 5, 2, 5), (2, 4, 6, 4, 5, 2, 5), (0, 4, 6, 4, 5, 2, 4), (1, 5, 6, 4, 5, 2, 4), (2, 5, 6, 4, 5, 2, 4), (0, 5, 6, 4, 5, 2, 3), (1, 5, 5, 4, 5, 2, 3), (2, 5, 5, 4, 5, 2, 3), (0, 5, 5, 4, 5, 2, 2), (1, 5, 4, 4, 5, 2, 2), (2, 5, 4, 4, 5, 2, 2), (0, 5, 4, 4, 5, 2, 1), (1, 5, 3, 4, 5, 2, 1), (2, 5, 3, 4, 5, 2, 1), (0, 5, 3, 4, 5, 2, 0), (1, 4, 3, 4, 5, 2, 0), (2, 4, 3, 4, 5, 2, 0), (0, 4, 3, 4, 5, 1, 0)]

----
Mazeworld problem: 
attempted with search method Astar with heuristic manhattan_heuristic
number of nodes visited: 78589
solution length: 80
cost: 39
path: [(0, 1, 0, 2, 0, 5, 0), (1, 1, 0, 2, 0, 5, 0), (2, 1, 0, 2, 1, 5, 0), (0, 1, 0, 2, 1, 5, 0), (1, 1, 0, 2, 1, 5, 0), (2, 1, 0, 2, 2, 5, 0), (0, 1, 0, 2, 2, 5, 0), (1, 1, 0, 2, 2, 5, 0), (2, 1, 0, 2, 3, 5, 0), (0, 1, 0, 2, 3, 5, 0), (1, 1, 0, 2, 3, 5, 0), (2, 1, 0, 2, 4, 5, 0), (0, 1, 0, 2, 4, 5, 1), (1, 1, 0, 2, 4, 5, 1), (2, 1, 0, 2, 5, 5, 1), (0, 1, 0, 2, 5, 5, 2), (1, 1, 0, 2, 5, 5, 2), (2, 1, 0, 2, 6, 5, 2), (0, 1, 0, 2, 6, 5, 3), (1, 1, 1, 2, 6, 5, 3), (2, 1, 1, 3, 6, 5, 3), (0, 1, 1, 3, 6, 5, 4), (1, 1, 1, 3, 6, 5, 4), (2, 1, 1, 3, 6, 5, 4), (0, 1, 1, 3, 6, 5, 5), (1, 1, 2, 3, 6, 5, 5), (2, 1, 2, 4, 6, 5, 5), (0, 1, 2, 4, 6, 5, 6), (1, 1, 2, 4, 6, 5, 6), (2, 1, 2, 4, 5, 5, 6), (0, 1, 2, 4, 5, 4, 6), (1, 1, 2, 4, 5, 4, 6), (2, 1, 2, 4, 5, 4, 6), (0, 1, 2, 4, 5, 3, 6), (1, 1, 2, 4, 5, 3, 6), (2, 1, 2, 4, 5, 3, 6), (0, 1, 2, 4, 5, 2, 6), (1, 1, 2, 4, 5, 2, 6), (2, 1, 2, 4, 5, 2, 6), (0, 1, 2, 4, 5, 2, 5), (1, 1, 3, 4, 5, 2, 5), (2, 1, 3, 4, 5, 2, 5), (0, 1, 3, 4, 5, 2, 4), (1, 1, 3, 4, 5, 2, 4), (2, 1, 3, 4, 5, 2, 4), (0, 1, 3, 4, 5, 2, 3), (1, 1, 3, 4, 5, 2, 3), (2, 1, 3, 4, 5, 2, 3), (0, 1, 3, 4, 5, 2, 2), (1, 2, 3, 4, 5, 2, 2), (2, 2, 3, 4, 5, 2, 2), (0, 2, 3, 4, 5, 2, 2), (1, 2, 4, 4, 5, 2, 2), (2, 2, 4, 4, 5, 2, 2), (0, 2, 4, 4, 5, 2, 1), (1, 2, 5, 4, 5, 2, 1), (2, 2, 5, 4, 5, 2, 1), (0, 2, 5, 4, 5, 2, 0), (1, 2, 6, 4, 5, 2, 0), (2, 2, 6, 4, 5, 2, 0), (0, 2, 6, 4, 5, 2, 0), (1, 3, 6, 4, 5, 2, 0), (2, 3, 6, 4, 5, 2, 0), (0, 3, 6, 4, 5, 2, 0), (1, 4, 6, 4, 5, 2, 0), (2, 4, 6, 4, 5, 2, 0), (0, 4, 6, 4, 5, 2, 0), (1, 5, 6, 4, 5, 2, 0), (2, 5, 6, 4, 5, 2, 0), (0, 5, 6, 4, 5, 2, 0), (1, 5, 5, 4, 5, 2, 0), (2, 5, 5, 4, 5, 2, 0), (0, 5, 5, 4, 5, 2, 0), (1, 5, 4, 4, 5, 2, 0), (2, 5, 4, 4, 5, 2, 0), (0, 5, 4, 4, 5, 2, 0), (1, 5, 3, 4, 5, 2, 0), (2, 5, 3, 4, 5, 2, 0), (0, 5, 3, 4, 5, 1, 0), (1, 4, 3, 4, 5, 1, 0)]
```

This is a 8 x 8 maze where the robot has the go around the wall that divides the maze in half. The goal locations are (4,3,4,5,1,0) for each respective robot. The animated path has not been included for the brevity of this report but it can be observed by uncommenting the test code.

#### maze6.maz
```
#........######
#..##.........#
#..##.........#
#.............#
#...#...#.....#
#...#...#.....#
#...#####.....#
#.............#
#.............#
#.....#.......#
#....#.#......#
#.....#.......#
#.............#
#.............#
#.#.#.#.#.#####

\robot 1 0
\robot 8 2
\robot 9 5
\robot 12 12
```
This is a 14 x 14 maze that tries to increase the number of wall collision by creating a bucket or teeth that the robots might fall into into. The solution output and animated path have not been included for the brevity of this report. 

#### maze7.maz

```
#............................#
#............................#
###########################..#
#............................#
#..###########################
#............................#
###########################..#
#............................#
#..###########################
#............................#
###########################..#
#............................#
#..###########################
#............................#
###########################..#
#............................#
#..###########################
#............................#
###########################..#
#............................#
#..###########################
#............................#
###########################..#
#............................#
#..###########################
#............................#
###########################..#
#............................#
#..###########################
#............................#

\robot 1 0
\robot 2 0
\robot 3 0
\robot 4 0
\robot 5 0
\robot 6 0
\robot 7 0
\robot 8 0
\robot 9 0
\robot 10 0
```
This is a maze where the robots would have to travel sequentially in order to get from the bottom to the goal locations at the top of the maze. Depending on the starting order of the maze, it may take some time for the robots to rearrange themselves at the top, where there is more room. The solution output and animated path have not been included for the brevity of this report. 

#### maze8.maz

```
#......................................#
#......................................#
#......................................#
#......................................#
#......................................#
#......................................#
#......................................#
#...################################...#
#.................................##...#
#...############################..##...#
#...###...........................##...#
#...##....##########################...#
#...##............................##...#
#...############################..##...#
#...##............................##...#
#...##..############################...#
#...##............................##...#
####################################...#
#......................................#
#....###........#####....###...........#
#...............#####..................#
#...............#####..................#
#.###...........#####..........###.....#
#...............#####..................#
#...............#####..................#
#.........###...#####......###.........#
#...............#####..................#
#....###........#####..................#
#...............#####...###............#
#......###......#####..................#
#...............#####..................#
#.......###.....#####......###.........#
#...............#####..................#
#....###........#####..................#
#...............#####.........###......#
#..###..........#####..................#
#.........###...#####......###.........#
#...............#####..................#
#......................................#
########################################

\robot 38 1
\robot 38 2
\robot 38 3
\robot 38 4
\robot 38 5
\robot 38 6
```
This is a very large maze that would generate a lot of possible states. The size of the maze allows this maze to be the combination of various types of mazes in the above examples. The solution output and animated path have not been included for the brevity of this report. 

# Evaluation

### MazeworldProblem (Multiple Robot)

The A* algorithm appears to work quite well with the null heuristic function and with the manhattan heuristic function. The output below demonstrates the A* algorithm on the MazeworldProblem using Maze3.maz. Since both UCS and A* are optimal, we can observe that the solution length and cost are the same. We can also see that the manhattan heuristic significantly decreases the number of nodes visited, which is a result that we would expect. 

```
----
Mazeworld problem: 
attempted with search method Astar with heuristic null_heuristic
number of nodes visited: 1814
solution length: 16
cost: 10
path: [(0, 1, 0, 1, 1, 2, 1), (1, 1, 0, 1, 1, 2, 1), (2, 1, 0, 1, 2, 2, 1), (0, 1, 0, 1, 2, 2, 1), (1, 1, 1, 1, 2, 2, 1), (2, 1, 1, 2, 2, 2, 1), (0, 1, 1, 2, 2, 2, 1), (1, 1, 2, 2, 2, 2, 1), (2, 1, 2, 2, 2, 2, 1), (0, 1, 2, 2, 2, 2, 1), (1, 1, 3, 2, 2, 2, 1), (2, 1, 3, 1, 2, 2, 1), (0, 1, 3, 1, 2, 2, 2), (1, 1, 4, 1, 2, 2, 2), (2, 1, 4, 1, 3, 2, 2), (2, 1, 4, 1, 3, 1, 2)]

----
Mazeworld problem: 
attempted with search method Astar with heuristic manhattan_heuristic
number of nodes visited: 119
solution length: 16
cost: 10
path: [(0, 1, 0, 1, 1, 2, 1), (1, 1, 0, 1, 1, 2, 1), (2, 1, 0, 1, 2, 2, 1), (0, 1, 0, 1, 2, 2, 1), (1, 1, 1, 1, 2, 2, 1), (2, 1, 1, 2, 2, 2, 1), (0, 1, 1, 2, 2, 2, 1), (1, 1, 2, 2, 2, 2, 1), (2, 1, 2, 2, 2, 2, 1), (0, 1, 2, 2, 2, 2, 1), (1, 1, 3, 2, 2, 2, 1), (2, 1, 3, 1, 2, 2, 1), (0, 1, 3, 1, 2, 1, 1), (1, 1, 4, 1, 2, 1, 1), (2, 1, 4, 1, 3, 1, 1), (2, 1, 4, 1, 3, 1, 2)]
```
You can uncomment other test cases that uses the A* search on different mazes, including the sample mazes that I have created (maze4.maz, maze5.maz, maze6.maz, maze7.maz, maze8.maz). Note the A* was tested with a maze dimensions up to 15 x 15 (maze6.maz) as the runtime becomes quite long at this point. Perhaps the efficiency can be improved by removing duplicate nodes from the heap and better heuristic function. Please refer to the output at the end of this report for the animated path. 


### SensorlessProblem (Blind Robot)

The A* algorithm appears to work quite well with the null heuristic function and with the relatively simple heuristic function. The output below demonstrates the A* algorithm on the MazeworldProblem using Maze3.maz. Again, the solution length and cost are the same for UCS and A* with heuristic function. The heuristic significantly decreases the number of nodes visited, which is what we would expect. 

```
----
Blind robot problem: 
attempted with search method Astar with heuristic null_heuristic
number of nodes visited: 1010
solution length: 9
cost: 8
path: [((1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 1), (2, 2), (2, 4), (2, 5), (3, 1), (3, 2), (3, 3), (3, 4)), ((2, 4), (1, 2), (2, 1), (3, 1), (1, 1), (3, 3), (1, 0), (3, 2), (1, 3)), ((1, 2), (2, 1), (1, 1), (1, 4), (3, 3), (2, 2), (1, 0), (1, 3)), ((1, 2), (3, 4), (1, 1), (1, 4), (2, 2), (1, 3)), ((2, 4), (1, 2), (1, 1), (1, 4), (1, 3)), ((1, 1), (1, 2), (1, 3), (1, 4)), ((1, 2), (1, 3), (1, 4)), ((1, 3), (1, 4)), ((1, 4),)]

----
Blind robot problem: 
attempted with search method Astar with heuristic blind_heuristic_fn
number of nodes visited: 33
solution length: 9
cost: 8
path: [((1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 1), (2, 2), (2, 4), (2, 5), (3, 1), (3, 2), (3, 3), (3, 4)), ((1, 2), (3, 4), (1, 1), (1, 4), (3, 3), (2, 2), (3, 2), (2, 5), (1, 3)), ((1, 2), (3, 4), (1, 4), (3, 3), (2, 2), (2, 5), (1, 3)), ((3, 4), (1, 4), (2, 2), (2, 5), (1, 3)), ((2, 4), (1, 2), (1, 4), (2, 5), (1, 3)), ((2, 5), (1, 3), (1, 4)), ((2, 5), (1, 4)), ((2, 4), (2, 5)), ((2, 5),)]
```
Similarly, conducting the A* search on the SensorlessProblem will take significant time after maze6.maz. Please refer to the output at the end of this report for the animated path. 

For the animated path for maze3, here is how the states would change (which is also what the animated path shows). 
- Starting possible number of coordinates: 13
- Change in belief states: (North, 9), (North, 7), (North, 5), (West, 5), (North, 3), (North, 2), (East, 2), (North, 1) 

# Discussion Questions

### On A*: 

#### 1. If there are k robots, how would you represent the state of the system?

To represent the state, you would need to know the robot that is to be moved and the x,y coordinates of all the robots in the maze. You would need to know the robot to be moved since robots are moving one at a time. For instance, the state would look something like: 

(robot\_to\_be\_moved, robot1\_x, robot1_y, robot2\_x, ... )

Thus, we would need a tuple of size (2*k + 1), where k represents the number of robots.

#### 2. Give an upper bound on the number of states in the system, in terms of n and k.

There are k robots that can be moved and there are n x n coordinates possible for each robot. However, since robots cannot be placed on top of each other, you would need to consider how many ways you can place k robots in a n x n maze. Thus, the upper bound on the number of states can be expressed as: 

k x n<sup>2</sup> Choose k = K*C<sub>k</sub>(n<sup>2</sup>)

#### 3. Give a rough estimate on how many of these states represent collisions if the number of wall squares is w, and n is much larger than k.

If we calculate the number of _possible_ states when the number of wall squares is w, we can use our calculation above to say that it is approximately:

k x (n<sup>2</sup> - w) Choose k = K*C<sub>k</sub>(n<sup>2</sup> - w)

Thus, if we subtract this number from the total number of possible states, we can say that the rough estimate of the number of wall collisions would be: 

KC<sub>k</sub>(n<sup>2</sup>) - KC<sub>k</sub>(n<sup>2</sup> - w)

#### 4. If there are not many walls, n is large (say 100x100), and several  robots (say 10), do you expect a straightforward breadth-first search on the state space to be computationally feasible for all start and goal pairs? Why or why not?

For each robot, the time and space complexity of the search would be O(b<sup>n x n</sup>) since you could potentially be exploring and storing the entire maze. Even if you were to do so, you would have to ensure that the path returned for each robot do not overlap at a given point (i.e. two robots being at the same point). Thus, you would have to keep running dfs until you find the combination of paths that do not overlap. As you have to account for robots moving around each other or getting close, it does not seem computationally feasible. 

#### 5. Describe a useful, monotonic heuristic function for this search space. Show that your heuristic is monotonic. See the textbook for a formal definition of monotonic.

The following equaation holds if the heurisitic is monotonic: 

```h(n) ≤ c(n, a, n') + h(n')
```
First, considering the manhattan heuristic, we can show that it is monotonic by drawing a rectangle that contains the triangle between the starting coordinate (n), end coordinate(n') and a goal location (g). 

![](pictures/fig1.png)

No matter how you try to draw the triangle, the way to maximize the heuristic for n would be to have n and g on the opposite vertices. In this case, the heuristic for n would be the two sides of the rectangle. However, no matter where you place n' on the rectangle, the sum of the cost of moving and heuristic of n' is the remaining two sides of the rectangle. Thus, we can see that monotonicity of the manhattan heuristic holds. We could also use a heuristic that uses the Euclidean distance since the triangle inequality would hold. 

#### 6. Describe why the 8-puzzle in the book is a special case of this problem. Is the heuristic function you chose a good one for the 8-puzzle?

The 8 puzzle is a special case where there is only one 'floor' and the maze is filled with robots that need to shift places with each other to reach the goal state. So we can think of the 8 robots trying to reach a goal state in a 3 x 3 maze. Since this is a special case of the multi-robot problem, the manhattan heuristic would still be admissible. Another admissible heuristic would be to use the number of misplaced tiles.

#### 7. The state space of the 8-puzzle is made of two disjoint sets.  Describe how you would modify your program to prove this.

You could show that it is made of two disjoint sets in a brute-force manner. From a starting state, you could set possible states as the goal state. If you were to keep the set of all successors, you could compare it to another set of successors from another starting state. If the 'and' comparison of these two sets return false, you would know that they are made of two disjoint sets.

### On Blind robot problem: 

#### 1. Describe what heuristic you used for the A* search. Is the heuristic optimistic? Are there other heuristics you might use? 

A simple heuristic that I used was simply the length of the current possible states. This heuristic is not optimistic. For instance, we can consider a 3 x 3 maze that is empty. At the starting state, we would 9 possible locations but we know that it is possible to know the location of the robot in 4 moves. A simple solution to this may be to take the log of the number of possible coordinates so that it will always be less than the number of moves required. 


## Output

### Animate Path for A* on MazeworldProblem

#### Maze: maze3.maz

```
Mazeworld problem: 
##.##
#...#
#.#.#
#...#
#BC.#
#A###

Mazeworld problem: 
##.##
#...#
#.#.#
#...#
#BC.#
#A###

Mazeworld problem: 
##.##
#...#
#.#.#
#B..#
#.C.#
#A###

Mazeworld problem: 
##.##
#...#
#.#.#
#B..#
#.C.#
#A###

Mazeworld problem: 
##.##
#...#
#.#.#
#B..#
#AC.#
#.###

Mazeworld problem: 
##.##
#...#
#.#.#
#.B.#
#AC.#
#.###

Mazeworld problem: 
##.##
#...#
#.#.#
#.B.#
#AC.#
#.###

Mazeworld problem: 
##.##
#...#
#.#.#
#AB.#
#.C.#
#.###

Mazeworld problem: 
##.##
#...#
#.#.#
#AB.#
#.C.#
#.###

Mazeworld problem: 
##.##
#...#
#.#.#
#AB.#
#.C.#
#.###

Mazeworld problem: 
##.##
#...#
#A#.#
#.B.#
#.C.#
#.###

Mazeworld problem: 
##.##
#...#
#A#.#
#B..#
#.C.#
#.###

Mazeworld problem: 
##.##
#...#
#A#.#
#B..#
#C..#
#.###

Mazeworld problem: 
##.##
#A..#
#.#.#
#B..#
#C..#
#.###

Mazeworld problem: 
##.##
#A..#
#B#.#
#...#
#C..#
#.###

Mazeworld problem: 
##.##
#A..#
#B#.#
#C..#
#...#
#.###
```

#### maze4.maz
```
Mazeworld problem: 
#####
#.#.#
#...#
#A#.#
###B#

Mazeworld problem: 
#####
#.#.#
#...#
#A#.#
###B#

Mazeworld problem: 
#####
#.#.#
#...#
#A#B#
###.#

Mazeworld problem: 
#####
#.#.#
#...#
#A#B#
###.#

Mazeworld problem: 
#####
#.#.#
#..B#
#A#.#
###.#

Mazeworld problem: 
#####
#.#.#
#..B#
#A#.#
###.#

Mazeworld problem: 
#####
#.#.#
#.B.#
#A#.#
###.#

Mazeworld problem: 
#####
#.#.#
#.B.#
#A#.#
###.#

Mazeworld problem: 
#####
#.#.#
#B..#
#A#.#
###.#

Mazeworld problem: 
#####
#.#.#
#B..#
#A#.#
###.#

Mazeworld problem: 
#####
#B#.#
#...#
#A#.#
###.#

Mazeworld problem: 
#####
#B#.#
#A..#
#.#.#
###.#

Mazeworld problem: 
#####
#B#.#
#A..#
#.#.#
###.#

Mazeworld problem: 
#####
#B#.#
#.A.#
#.#.#
###.#

Mazeworld problem: 
#####
#B#.#
#.A.#
#.#.#
###.#

Mazeworld problem: 
#####
#B#.#
#..A#
#.#.#
###.#

Mazeworld problem: 
#####
#B#.#
#..A#
#.#.#
###.#

Mazeworld problem: 
#####
#B#A#
#...#
#.#.#
###.#

```

### Animate Path for A* on SensorlessProblem
Maze: maze3.maz

```
Blind robot problem: 
##I##
#EHM#
#D#L#
#CGK#
#BFJ#
#A###

Blind robot problem: 
##H##
#D.B#
#I#E#
#AFG#
#C..#
#.###

Blind robot problem: 
##F##
#C.B#
#G#D#
#AE.#
#...#
#.###

Blind robot problem: 
##D##
#B.A#
#E#.#
#.C.#
#...#
#.###

Blind robot problem: 
##D##
#CA.#
#E#.#
#B..#
#...#
#.###

Blind robot problem: 
##A##
#C..#
#B#.#
#...#
#...#
#.###

Blind robot problem: 
##A##
#B..#
#.#.#
#...#
#...#
#.###

Blind robot problem: 
##B##
#.A.#
#.#.#
#...#
#...#
#.###

Blind robot problem: 
##A##
#...#
#.#.#
#...#
#...#
#.###
```


