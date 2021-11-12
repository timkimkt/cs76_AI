# README.md
 
- Class: COSC 76 
- Assignment: PA 6
- Date: Nov 12, 2021
- Name: Tim (Kyoung Tae) Kim 
- Year: '22
 
## How to execute the program

1. In terminal, run `python _filename` or open the python files using an IDE such as PyCharm. 
2. `HiddenMarkovModel.py` contains the prediction model, the transition model and the filtering algorithm for the blind robot problem. 
3. There are also four sample maze files that can be given as the paramter to the filtering algorithm. Note that the last maze contains walls. 
4. To create the HMM, pass in the maze file and valid starting position of the robot into the constructor. 
5. Then, by passing in the number of steps, use the `move_robot` function to generate a random sequence of movements, which will generate sensor readings (which reflects its inaccuracy). 
6. Use the color sequence returned by the `move_robot` function to run the filtering algorithm and generate the probability distribution of possible robot locations. 

## Testing & Design

Please refer to report.md for more details. 
