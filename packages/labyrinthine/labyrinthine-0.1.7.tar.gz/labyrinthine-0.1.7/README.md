# Labyrinthine

A no-dependency library that generates all the mazes you need.

![maze](https://raw.githubusercontent.com/robertoschiavone/labyrinthine/master/maze.png)

## Installation

```bash
pip install labyrinthine
```

## Usage

```python
import matplotlib.pyplot as plt
import numpy as np

from labyrinthine import depth_first

maze = depth_first(size=(31, 21))
plt.imshow(np.pad(maze, 1, constant_values=1), cmap="binary")
plt.axis("off")
plt.savefig("maze.png", bbox_inches="tight", pad_inches=0)
```

## Parameters

`depth_first` accepts the following parameters:

- `size`: either a pair of `int` specifying width and height of the maze, or a single
  `int` for a square one.
- `start`: a pair of `int` defining the starting point. Default value is `(0, 0)`, the
  top-left corner of the maze.
- `seed`: as of Python 3.11, the seed must be one of the following types: `NoneType`,
  `int`, `float`, `str`, `bytes`, or `bytearray`. Default value is `None`.

The output is an integer matrix of the requested size, where **1** represents a filled
cell, thus a wall, and **0** represents an empty cell, thus a passage.

> :warning: HEADS UP!
>
> Due to the nature of the algorithm, it is warmly recommended to use odd width and
> height values, so that the resulting matrix doesn't have a vertical and horizontal
> border entirely filled with walls.

## Development

`Makefile` is self-explanatory.
