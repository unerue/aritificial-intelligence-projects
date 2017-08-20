# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Constraint propagation can reduce search space. Total 4 units(rows, cals, 3x3, diagonal) can be searched by naked twins method. Naked twin finds two entries and two candidates to compare in peers. It indentifies two values in boxes to assign unit twins box. And each peers(units) assgin to peers twin box and set() function to use duplicate. 
Thus, Finding twins to delete duplicate, and original unitlist - twins to use set(). 
Delete(replace '') none_twins values more than 1(len) I use from eliminate() function. And iterating other stategies with naked twins method to solve our constraint progagation of sudoku. 

P.S. Sorry, I can't write English well. However I study hard to write English. So, Once next project submit, you can read better grammer than now. 

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Diagonal sudoku is contraint that includes additional unit(complete rows, columns, 3x3 squares, and + diagonal) in sudoku. Identifying boxes to belong to the two boxes in diagonal. Once this finds solution, all peers can search all peers as rows, cols, units, and two diagonal to use naked_twins, eliminate, and only choice stategies for solving sudoku.

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

