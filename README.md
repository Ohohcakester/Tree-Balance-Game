Tree Balance
=================

Use rotations to keep the binary tree in balance! Made using PyGame.

The initial game was made in three days.
[Write-up + videos](http://localhost/webpage/?page=treebalance)


Gameplay
=================
There is a tutorial within the game.

Nodes are constantly added and removed from the tree, which can cause the tree to go out of balance.
The player navigates around the tree and performs "rotations" to keep the tree balanced.
The player's HP drains faster the more out of balance the tree is. HP can regenerate when the tree is balanced.

* Standard Mode
 * A fixed queue of add / delete operations. Survive until the queue runs out.
* Endless Mode
 * An endless queue of operations. Survive for as many operations as you can. Scoring is by the number of operations (Ops) survived.


Controls
================
* Movement:
 - UP: Move to parent node
 - RIGHT: Move to right child
 - LEFT: Move to left child
* Rotation:
 - A: Rotate left about current node
 - D: Rotate right about current node
 
 
Details
===============
Made using Python 3.4.2 / Pygame.
 
[Precompiled version](http://www.mediafire.com/download/4p5d3476bv1n0za/TreeBalance.rar)
