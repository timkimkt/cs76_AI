# README.md
 
- Class: COSC 81 
- Assignment: PA 2
- Date: Sep 30, 2021
- Name: Tim (Kyoung Tae) Kim 
- Year: '22
 
## How to execute the program

1. In terminal, run `python _filename_` or open the python files using an IDE such as PyCharm. 
2. First run MazeworldProblem.py if you wish to test that the `get_successors`, `valid_state` and `goal_test` function works for the MazeworldProblem. You could choose to do the same for the functions in SensorlessProblem. 
3. Run test\_mazeworld.py to run the A* algorithm on the multiple robot problem. Note that astar_search.py makes use of SearchSolution class to store the solution and print out problem name, search method, path, cost and node visited. 
4. Run test\_sensorless.py to run the A* algorithm on the blind robot problem. Similary, print out the SearchSolution object to see more information about the search.  
5. Each problem also contains the animate_path method that can simulate the movement or change in potential belief states of the robot. You can also change the maze map by selecting any of the .maz files in the directory. 

## Testing & Design

Please refer to PA2_report.md for more details. 
