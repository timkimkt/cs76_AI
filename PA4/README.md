# README.md
 
- Class: COSC 76 
- Assignment: PA 4
- Date: Oct 23, 2021
- Name: Tim (Kyoung Tae) Kim 
- Year: '22
 
## How to execute the program

1. In terminal, run `python _filename` or open the python files using an IDE such as PyCharm. 
2. `CSPSolver.py` contains the back-tracking, heuristic and inference function used for both CSP problems. 
3. The setup and solution for each CSP problem is located in their CSP[problem] file. The setup for the circuit problem is in `CSPCircuit.py` while the map problem is in `CSPMap.py`.
4. To create a problem and solve it, you first create a problem object and solution object (providing the problem object as the parameter). Then, you can call backtrack with the problem domain. 
5. For the circuit problem, you can print out the completed board and for the map problem, you can check the output with a function checks for any constraint violations. 
6. Various test cases for different combinations of heuristics and inference have already been included in each problem file. Note that you can simply modify the boolean parameters for the back-track function to create additional combinations.

## Testing & Design

Please refer to report.md for more details. 
