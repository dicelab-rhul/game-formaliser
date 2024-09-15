from enum import Enum


class GameStatus(Enum):
	START = 0
	CORRECT = 1
	FIXED = 2
	FAULTY = 3
