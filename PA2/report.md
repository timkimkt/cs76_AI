# Report
- Tim (Kyoung Tae) Kim
- COSC 76
- PA 2
- Sep 30, 2021
- '22

## Description
- How do your implemented algorithms work? What design decisions did you make? How you laid out the problems?

## Evaluation
- Do your implemented algorithms actually work? How well? If it doesn’t work, can you tell why not? What partial successes did you have that deserve partial credit? 

## Discussion Questions

### On A*: 

#### 1. If there are k robots, how would you represent the state of the system? Hint -- how many numbers are needed to exactly reconstruct the locations of all the robots, if we somehow forgot where all of the robots were? Further hint. Do you need to know anything else to determine exactly what actions are available from this state?

To represent the state, you would need to know the robot that is to be moved and the x,y coordinates of all the robots in the maze. You would need to know the robot to be moved since robots move one at the time. For instance, the state would look something like: 

(robot\_to\_be\_moved, robot1\_x, robot1_y, robot2\_x, ... )


#### 2. Give an upper bound on the number of states in the system, in terms of n and k.

There are k robots that can be moved and there are n x n coorindates possible for each robot. Thus, the upper bound on the number of states can be expressed as: 

n x k x k 

#### 3. Give a rough estimate on how many of these states represent collisions if the number of wall squares is w, and n is much larger than k.

Possible wall collision: 4w?
Possible robot collision: (n - 1) 


#### 4. If there are not many walls, n is large (say 100x100), and several  robots (say 10), do you expect a straightforward breadth-first search on the state space to be computationally feasible for all start and goal pairs? Why or why not?



#### 5. Describe a useful, monotonic heuristic function for this search space. Show that your heuristic is monotonic. See the textbook for a formal definition of monotonic.

Euclidean distance?


#### 6. Describe why the 8-puzzle in the book is a special case of this problem. Is the heuristic function you chose a good one for the 8-puzzle?

The 8 puzzle is a special case where there is only one 'floor' and the tiles must move around each other to the goal state. 

#### 7. The state space of the 8-puzzle is made of two disjoint sets.  Describe how you would modify your program to prove this. (You do not have to implement this.)

### On Blind robot problem: 


