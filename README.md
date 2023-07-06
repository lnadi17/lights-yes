# lights-yes

This is a project about mathematical analysis and solution search for the game originally called "Ligths Out". 
It has the Jupyter Notebook that implements the linear algebra approach to solving this game. 
More about this approach can be found out in [this paper](https://dc.ewu.edu/cgi/viewcontent.cgi?article=1166&context=theses). 
There exists another, shorter [paper](http://buzzard.ups.edu/courses/2007spring/projects/olson-paper-revised.pdf) that I used as a reference.

## Introduction Video

I decided to make a full video about the linear algebra solutions of this game, but I abandoned it after some time. However, intro video (in Georgian language) and all the manim code remains in this repository. Here it is:

https://github.com/lnadi17/lights-yes/assets/19193250/e096e7ad-a296-43e8-a3f2-e7dbda1f11ee


## Implementation Details

This notebook defines `Gameboard` class, which has methods for initializing the board, triggering bulbs, making moves, restarting the game, getting the current state of the board, checking if the game is over, and more.

It also defines a method called `solve_bfs` that solves the game using a breadth-first search algorithm. This is an initial effort to 
solve the game. On 2x2 board it works well, but for larger boards it takes too much time. This part of the notebook also visualizes the lengths of moves distribution for 2x2 board.

Next up, we move on to the linear algebra solution of the game. To keep this short, it turns out that the game has solutions that can be expressed as particular and homogenous solutions of a specific system of linear equations. Notebook defines different methods, such as `rref` (Row Reduced Echelon Form), `exact`, `null_space`, `particular` and eventually `solve_linalg`, which uses previous methods to get all solutions of a single game. Notebook solves these linear system equations in different ways and confirms that they are all equal. 

In addition, different board sizes are considered, which haven't been studied before. Up to the size of 100, all board sizes are checked if they always have a solution or not. This is the result:
```
4x4 not always solvable
5x5 not always solvable
9x9 not always solvable
11x11 not always solvable
14x14 not always solvable
```
Turns out 4, 5, 9, 11 and 14 are not always solvable. This also includes the original board size of 5.

If board has a solution, it is also calculated how many unique solutions it has, by calculating the total combinations of null space vectors. This is the result:
```
2x2: 1
3x3: 1
4x4: 17
5x5: 5
6x6: 1
...
95x95: 4611686018427387905
96x96: 1
97x97: 1
98x98: 1048577
99x99: 65537
100x100: 1
```

Turns out the original 5x5 game has 5 unique solutions. 79x79 had the most unique solutions, reaching `18446744073709551617`, which is the number of estimated possible worlds in Minecraft.
