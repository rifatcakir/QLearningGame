## Game play explanation
![image](https://user-images.githubusercontent.com/9320341/120070561-d1f2ae00-c093-11eb-88d5-b8b595db9b0b.png)

Consider the environment above. There are three agentsin the environment. C1 and C2 are
the chasers and R is trying to run away from them.The initial positions of the agents are
given in the figure. In each turn first R is goingto make a move and then C1 and lastly C2.
Certainly, the X positions cannot be used by the agents.The game ends if R is in the same
cell with one of the chasers.

## Game Board Design

## Board Creation

Board constructed on array lists like:
map = np.array([ [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0],
[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ])

## Main Menu

There are questions about creating a board, placingthe initial position of chasers,runners
and blocks in the game.


## Mapping Objects on Board

### createBoardList: this function converts every pieceinto a relation tuple.

For example, Assume that on map[3][5] and [3][6] thereis no X block. We convert this
blocks like (35, 36) and (36,35). With this way wecan say moving 35 to 36 and 36 to 35 is
valid.
Note that, I have added +1 for x value. Otherwise,map[0][10] and map[1][0] are equal and it
creates a hack jump point for our chasers.

Vısual wiev of Map
This part is coded in _printBoard_ function that convertsthe mathematical view of map into
char map list.

# How Runner and Chasers Works

**Runner** has two options to run. The first one is manuallychanging the position of it. We
enter position per each turn by an input. Second wayof moving is a runner which is trying to
be just as far away from the chasers by calculatingthe range and Manhattan distance. In
this way, every turn our function decides the farestposition and moves on that area.

**Chasers** have a few steps to work.
● **playChaser** : this function takes the chaser numberas an input and moves the
chaser on the game board.
● **trainModel:** This function takes the chaser numberas parameter and trains a model
to find the shortest path about accessing the Runner.It returns a Q matrix which help
us to find shortest path on map.
● **createBoardList:** this function converts every pieceinto a relation tuple and returns
a list of tuples.
○ For example, Assume that on map[3][5] and [3][6] thereis no X block. We
convert these blocks like (35, 36) and (36,35). Withthis way we can say
moving 35 to 36 and 36 to 35 is valid.
○ Note that, I have added +1 for x value. Otherwise,map[0][10] and map[1][0]
are equal and it creates a hack jump point for ourchasers.
**● createGraph:** This method takes the boardlist responseand creates a graph of
possible paths.


```
● initializeRewardMatrix : this function takes ‘G’ as graph and targetPosition which is
Runner. it returns a matrix by creating a reward map.
● initializeQMatrix : this function takes ‘G’ as graphand returns a Q matrix.
● learner : this function takes exploration rate, learningrate, discount factor of learning,
G as Graph, Q as Q matrix and R as rewarding matrix.Then it fills the Q matrix
based on the learning process.
○ Note: For our chasers we have different learning rateson the project.
Therefore, we expect different behaviour when moving.
● shortest_path : When we have trained Q matrix basedon the chaser type, we call
shortest_path function with the current position ofchaser, current position of runner
and Q matrix which is created by trainModel function.This function returns the
shortest path steps. This response has numbers like30 - 20 -10 -11. These nodes
exist on our graph. Then, we have a matrix where itshows the real coordinates of the
returned number. We take the real x and y coordinatesand move the chasers.
● calculateEarnedPoint : calculates the Manhattan distancebetween chaser and
runner and sets the chaser's point.
```
# References

```
● Finding Shortest Path using Q-Learning Algorithm
https://towardsdatascience.com/finding-shortest-path-using-q-learning-algorithm-1c1f
39e
```
```
● Q Learning - Reinforcement Learning
https://www.youtube.com/watch?v=yMk_XtIEzH
```

