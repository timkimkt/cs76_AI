# Report
- Tim (Kyoung Tae) Kim
- COSC 76
- PA 3
- Oct 11, 2021
- '22

## Description
_(a) Description: How do your implemented algorithms work? What design decisions did you make?_


### CSPMap.py

In my constructor, I found it helpful to create dictionaries for variable and domain that indicates which integer value maps to which state (variable) or color (domain). The text map that is given by the user (i.e. the map that indicates which states are adjacent to which) is also converted into a dictionary that maps the integer value of variable to integer value of domain. Then, I create a map of constraints, where the key is a tuple (two adjacent states) and the value is a list of possible pair of domains (possible color combination). I also created a function that checks if the most recently assigned variable satisfies the contraint. By utilizing the dictionaries that I have created, I check that if two states are adjacent (i.e. listed as a key in the constraint dictionary) and if so, I check that the pair of domain values are listed in the key of the constraint dictionary. Finally, I created helper functions that checks if assignment is complete and if a variable is unassigned, where -1 indicates an unassigned value. 

### CSPCircuit

Similarly, I created in my constructor a dictionary that maps each variable to the component. Note that the variables are the left-bottom coordinate of the components. I instantiated variables for the board dimension and dictionary of component sizes to use in the class methods. Then, I assigned the domain for each component variable, which is a list of tuples that represent the possible coordinates of the component in the board. I then generate a constraint map, where all the components have a binary constraint with each other. Thus, I map a tuple (two components) to a list of a pair of tuples (possible coordinate of each component). Before appending the coordinate to the list, I make sure that they do not overlap. Similarly to the map problem, I created a function that checks if the most recently assigned variable satisfies the contraint. I also create other functions that are helpful such as functions that check if assignment is complete or if variable is unassigned and also a function that prints the board filled with components according to the CSP solution. 

### CSPSolver.py

## Evaluation

_(b) Evaluation: Do your implemented algorithms actually work? How well? If it doesn’t work, can you tell why not? What partial successes did you have that deserve partial credit?_

First, the constraint satisfaction and back-tracking function works well, returning solutions that are legal for both map and circuit problem. I found the implementation of heuristics quite challenging and while I tried out various combination of the heuristics as well as the inference for both map and circuit problem, I wasn't certain that they are fully functional. As discussed below, the effects of the heuristics was not clear for the map coloring problem, but more pronounced for the circuit problem. 

For the circuit problem, the hueri

## Discussion Questions

### Map coloring test

_Describe the results from the test of your solver with and without heuristic, and with and without inference on the map coloring problem_

As for the map problem, the node count stayed consistent at 8 but the value count (located inside the for-loop inside the back-track function), returned a higher value with the degree heuristic. This was the same with the inference turned on. 


### Circuit-board

1. _In your write-up, describe the domain of a variable corresponding to a component of width w and height h, on a circuit board of width n and height m.  Make sure the component fits completely on the board._

The domain of a variable consists of possible left-bottom coordinates for the circuit piece. Thus, assuming that w <= n and h <= m and that the left-bottom coordinate of the board starts at (0, 0), the possible domain (x, y) of the piece would be all coordinates in the range of:

0 <= x and x + width <= n and 0 <= y and y + height <= m

To demonstrate, here are the domain for the example components and circuit board provided in the instructions: 

```
Domain of  A is  [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)]
Domain of  B is  [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)]
Domain of  C is  [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)]
Domain of  D is  [(0, 2), (1, 2), (2, 2), (3, 2), (0, 1), (1, 1), (2, 1), (3, 1), (0, 0), (1, 0), (2, 0), (3, 0)]
```

2. _Consider components a and b above, on a 10x3 board.  In your write-up, write the constraint that enforces the fact that the two components may not overlap.  Write out legal pairs of locations explicitly._

Since the domain for each component only consists of coordinates where it fits the board, the constraint only need to consider whether two pieces overlap. Let's say that the two components are A and B. Then we would need to check whether any of B's x coordinate in the range of its starting point and its width falls into the range of A's starting point and its width. If this is true, we need to check whether any of B's y coordinate in the range of its starting point and its height falls into the range of A's starting point and its height. 

To demonstrate, here are the constraints for the example components and circuit board provided in the instructions: 

```
Legal pairs of locations for A and B are:  [((0, 1), (3, 1)), ((0, 1), (4, 1)), ((0, 1), (5, 1)), ((0, 1), (3, 0)), ((0, 1), (4, 0)), ((0, 1), (5, 0)), ((1, 1), (4, 1)), ((1, 1), (5, 1)), ((1, 1), (4, 0)), ((1, 1), (5, 0)), ((2, 1), (5, 1)), ((2, 1), (5, 0)), ((5, 1), (0, 1)), ((5, 1), (0, 0)), ((6, 1), (0, 1)), ((6, 1), (1, 1)), ((6, 1), (0, 0)), ((6, 1), (1, 0)), ((7, 1), (0, 1)), ((7, 1), (1, 1)), ((7, 1), (2, 1)), ((7, 1), (0, 0)), ((7, 1), (1, 0)), ((7, 1), (2, 0)), ((0, 0), (3, 1)), ((0, 0), (4, 1)), ((0, 0), (5, 1)), ((0, 0), (3, 0)), ((0, 0), (4, 0)), ((0, 0), (5, 0)), ((1, 0), (4, 1)), ((1, 0), (5, 1)), ((1, 0), (4, 0)), ((1, 0), (5, 0)), ((2, 0), (5, 1)), ((2, 0), (5, 0)), ((5, 0), (0, 1)), ((5, 0), (0, 0)), ((6, 0), (0, 1)), ((6, 0), (1, 1)), ((6, 0), (0, 0)), ((6, 0), (1, 0)), ((7, 0), (0, 1)), ((7, 0), (1, 1)), ((7, 0), (2, 1)), ((7, 0), (0, 0)), ((7, 0), (1, 0)), ((7, 0), (2, 0))]
```

3. _Describe how your code converts constraints, etc, to integer values for use by the generic CSP solver._

The constraints are created in a similar manner to the map coloring problem, except that tuples are used. I created a dictionary to store the constraint between two pieces, where the keys are a pair of integers that represent two different components and the value is a list of possible pair of coordinates for the two pieces. 

## Sample Output

### CSP Map

```
Here are the regions: ['WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T']
here are the colors:  ['red', 'green', 'blue']
Here is the map:  {'WA': ['NT', 'SA'], 'NT': ['WA', 'SA', 'Q'], 'Q': ['NT', 'SA', 'NSW'], 'NSW': ['Q', 'SA', 'V'], 'V': ['NSW', 'SA'], 'SA': ['WA', 'NT', 'Q', 'NSW', 'V'], 'T': []}
-------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------
MRV selected
LCV not selected
Node count:  8
Value count:  11
Assignment:  ['WA: red', 'NT: green', 'Q: red', 'NSW: green', 'V: red', 'SA: blue', 'T: red']
-------------------------------------------------------------------------------------------------------------------------
Degree selected
LCV not selected
Node count:  8
Value count:  15
Assignment:  ['WA: blue', 'NT: green', 'Q: blue', 'NSW: green', 'V: blue', 'SA: red', 'T: red']
-------------------------------------------------------------------------------------------------------------------------
MRV selected with Tiebreak (Degree)
LCV not selected
Node count:  8
Value count:  15
Assignment:  ['WA: blue', 'NT: green', 'Q: blue', 'NSW: green', 'V: blue', 'SA: red', 'T: red']
-------------------------------------------------------------------------------------------------------------------------
No variable heuristic selected
LCV heuristic selected
Node count:  8
Value count:  11
Assignment:  ['WA: red', 'NT: green', 'Q: red', 'NSW: green', 'V: red', 'SA: blue', 'T: red']
-------------------------------------------------------------------------------------------------------------------------
MRV selected with Tiebreak (Degree)
LCV heuristic selected
Node count:  8
Value count:  15
Assignment:  ['WA: blue', 'NT: green', 'Q: blue', 'NSW: green', 'V: blue', 'SA: red', 'T: red']
-------------------------------------------------------------------------------------------------------------------------
Degree selected
LCV heuristic selected
Node count:  8
Value count:  15
Assignment:  ['WA: blue', 'NT: green', 'Q: blue', 'NSW: green', 'V: blue', 'SA: red', 'T: red']
-------------------------------------------------------------------------------------------------------------------------
Inference on
MRV selected with Tiebreak (Degree)
LCV not selected
Node count:  8
Value count:  15
Assignment:  ['WA: blue', 'NT: green', 'Q: blue', 'NSW: green', 'V: blue', 'SA: red', 'T: red']
-------------------------------------------------------------------------------------------------------------------------
Inference on
Degree selected
LCV heuristic selected
Node count:  8
Value count:  15
Assignment:  ['WA: blue', 'NT: green', 'Q: blue', 'NSW: green', 'V: blue', 'SA: red', 'T: red']
```

### CSP Circuit

```
-------------------------------------------------------------------------------------------------------------------------
MRV selected
LCV not selected
Node count:  5
Value count:  23
Assignment:  [(7, 1), (2, 1), (0, 0), (2, 0)]
[['c' 'c' 'b' 'b' 'b' 'b' 'b' 'a' 'a' 'a']
 ['c' 'c' 'b' 'b' 'b' 'b' 'b' 'a' 'a' 'a']
 ['c' 'c' 'e' 'e' 'e' 'e' 'e' 'e' 'e' '.']]
-------------------------------------------------------------------------------------------------------------------------
Degree selected
LCV not selected
Node count:  5
Value count:  23
Assignment:  [(0, 1), (3, 1), (8, 0), (0, 0)]
[['a' 'a' 'a' 'b' 'b' 'b' 'b' 'b' 'c' 'c']
 ['a' 'a' 'a' 'b' 'b' 'b' 'b' 'b' 'c' 'c']
 ['e' 'e' 'e' 'e' 'e' 'e' 'e' '.' 'c' 'c']]
-------------------------------------------------------------------------------------------------------------------------
MRV selected with Tiebreak (Degree)
LCV not selected
Node count:  5
Value count:  23
Assignment:  [(7, 1), (2, 1), (0, 0), (2, 0)]
[['c' 'c' 'b' 'b' 'b' 'b' 'b' 'a' 'a' 'a']
 ['c' 'c' 'b' 'b' 'b' 'b' 'b' 'a' 'a' 'a']
 ['c' 'c' 'e' 'e' 'e' 'e' 'e' 'e' 'e' '.']]
-------------------------------------------------------------------------------------------------------------------------
MRV selected
LCV heuristic selected
Node count:  5
Value count:  10
Assignment:  [(2, 1), (5, 1), (0, 0), (3, 0)]
[['c' 'c' 'a' 'a' 'a' 'b' 'b' 'b' 'b' 'b']
 ['c' 'c' 'a' 'a' 'a' 'b' 'b' 'b' 'b' 'b']
 ['c' 'c' '.' 'e' 'e' 'e' 'e' 'e' 'e' 'e']]
-------------------------------------------------------------------------------------------------------------------------
MRV selected with Tiebreak (Degree)
LCV heuristic selected
Node count:  5
Value count:  10
Assignment:  [(2, 1), (5, 1), (0, 0), (3, 0)]
[['c' 'c' 'a' 'a' 'a' 'b' 'b' 'b' 'b' 'b']
 ['c' 'c' 'a' 'a' 'a' 'b' 'b' 'b' 'b' 'b']
 ['c' 'c' '.' 'e' 'e' 'e' 'e' 'e' 'e' 'e']]
-------------------------------------------------------------------------------------------------------------------------
Degree selected
LCV heuristic selected
Node count:  9
Value count:  61
Assignment:  [(0, 1), (3, 1), (8, 0), (0, 0)]
[['a' 'a' 'a' 'b' 'b' 'b' 'b' 'b' 'c' 'c']
 ['a' 'a' 'a' 'b' 'b' 'b' 'b' 'b' 'c' 'c']
 ['e' 'e' 'e' 'e' 'e' 'e' 'e' '.' 'c' 'c']]
-------------------------------------------------------------------------------------------------------------------------
Inference on
MRV selected with Tiebreak (Degree)
LCV heuristic selected
Node count:  5
Value count:  10
Assignment:  [(2, 1), (5, 1), (0, 0), (3, 0)]
[['c' 'c' 'a' 'a' 'a' 'b' 'b' 'b' 'b' 'b']
 ['c' 'c' 'a' 'a' 'a' 'b' 'b' 'b' 'b' 'b']
 ['c' 'c' '.' 'e' 'e' 'e' 'e' 'e' 'e' 'e']]
-------------------------------------------------------------------------------------------------------------------------
Inference on
Degree selected
LCV heuristic selected
Node count:  8
Value count:  40
Assignment:  [(0, 1), (3, 1), (8, 0), (0, 0)]
[['a' 'a' 'a' 'b' 'b' 'b' 'b' 'b' 'c' 'c']
 ['a' 'a' 'a' 'b' 'b' 'b' 'b' 'b' 'c' 'c']
 ['e' 'e' 'e' 'e' 'e' 'e' 'e' '.' 'c' 'c']]
```