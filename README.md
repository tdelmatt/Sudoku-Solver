# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: We know that if a subset satisfies the criterion of naked twins, then that means it must contain a set of values which are unique to that subset within the unit.  We
 find this definition/consequence of naked twins by propagating the constraints of the sudoku.  Using induction, if we have s subset of n boxes with n possible values.
 By induction if the first box has n possibilities, the last box has 1. (n,n-1,....1) by the time we get to the end of assigning digits,
 there are no possible digits left.  Since all n possible digits are assigned to those boxes, there will be a box in those boxes with each digit in n.  
 By propagating the constraint that if one box in a unit has a value, no other can, boxes outside of the subset cannot contain values contained within the subset.
 By this constraint propagation we derive the definition/consequences of the naked twins.  
 In summary we derive the solution (definition/implications) of naked twins scenario by propagating constraints of the sudoku puzzle. 

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Elimination and only choice are essentially directly propagating constraints by using rules.
to eliminate possibilities.  Naked twins is more indirect constraint propagation.  By iterating over these
heuristics, we apply constraints/heuristics in a cycle.  This cycle of constraint derived heuristics reduces possibilities, 
which in turn exposes more exploitable constraints to the heuristics which can eliminate further possibilities.  
In other words this creates a self-inducing cycle of solving exposed constraints and reducing possibilities.  The constraint propagation is used as a combination of practical heuristics
to help solve the problem.  The heuristics do not have a guarantee of solving the problem, but they typically solve or vastly reduce the number of possibilities left to iterate through by search.
By definition, the heuristics are much more efficient than brute force search.  So they create a much more efficient algorithm.  


### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

