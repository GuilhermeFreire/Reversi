# -*- coding: utf-8 -*-
import numpy as np
from models.board import Board


class State:
	EMPTY, BLACK, WHITE, OUTER = '.', '□', '■', '?'

	def __init__(self, board):
		self.board = board
		self.children = []
		self.pos_values = [[100, -1, 5, 2, 2, 5, -1, 100],
						   [-1, -20, 1, 1, 1, 1, -20, -1],
						   [5, 1, 1, 1, 1, 1, 1, 5],
						   [2, 1, 1, 0, 0, 1, 1, 2],
						   [2, 1, 1, 0, 0, 1, 1, 2],
						   [5, 1, 1, 1, 1, 1, 1, 5],
						   [-1, -20, 1, 1, 1, 1, -20, -1],
						   [100, -1, 5, 2, 2, 5, -1, 100]]

	def score(self):
		white = 0
		black = 0
		for i in range(1, 9):
			for j in range(1, 9):
				if self.board.get_square_color(i, j) == State.WHITE:
					white += self.pos_values[i - 1][j - 1]
				elif self.board.get_square_color(i, j) == State.BLACK:
					black += self.pos_values[i - 1][j - 1]

		return [white, black]

	def make_children(self, color):
		valid_moves = self.board.valid_moves(color)
		for move in valid_moves:
			new_board = self.board.get_clone()
			new_state = State(new_board)
			new_board.play(move, color)
			self.children.append(new_state)

	def get_board(self):
		return self.board

	def get_children(self):
		return self.children

	def mobility_score(self, color):
		opponent_color = self.board._opponent(color)
		max_player_number_of_moves = len(self.board.valid_moves(color))
		min_player_number_of_moves = len(self.board.valid_moves(opponent_color))

		sum_of_plays = max_player_number_of_moves + min_player_number_of_moves
		dif_of_plays = max_player_number_of_moves - min_player_number_of_moves

		if sum_of_plays != 0:
			heuristic = 100*(dif_of_plays)/sum_of_plays
		else:
			heuristic = 0
		return heuristic