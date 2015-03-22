Tree Balance
=================
![screenshot](/../screenshot/screenshot/endless1.png?raw=true "Endless Mode")

Use rotations to keep the binary tree in balance! Made using PyGame.

The initial game was made in three days.
[Write-up + videos](http://ohoh.byethost7.com/?page=treebalance)

Go to the [Release Page](https://github.com/Ohohcakester/Tree-Balance-Game/releases) to download the game.

Setup
=================
1. Install [Python 3](https://www.python.org/downloads/) and [PyGame](http://pygame.org/download.shtml) (Python 3.4.2 recommended, might work with earlier versions of Python 3)
2. Run ```python main.py``` in the src directory.

Alternatively, a pre-compiled version is also available in the release page.


Gameplay
=================
There is a tutorial within the game.

In the Standard and Endless modes, nodes are constantly added and removed from the tree, which can cause the tree to go out of balance.
The player navigates around the tree and performs "rotations" to keep the tree balanced.
The player's HP drains faster the more out of balance the tree is. HP can regenerate when the tree is balanced.

* Standard Mode
 * A fixed queue of add / delete operations. Survive until the queue runs out.
* Endless Mode
 * An endless queue of operations. Survive for as many operations as you can. Scoring is by the number of operations (Ops) survived.
* Puzzle Mode
 * No time limit or health bar. Use rotations to solve an increasingly difficult series of tasks. Scoring is by the number of rotations used to solve the puzzle.


Controls
================
* Movement:
 - UP: Move to parent node
 - RIGHT: Move to right child
 - LEFT: Move to left child
* Rotation:
 - A: Rotate left about current node
 - D: Rotate right about current node
 
