# -*- coding: utf-8 -*-
import numpy as np
from models.board import Board


class State:

	def __init__(self, board):
		self.board = board
		self.children = []

	def make_children(self, color):
		if color == self.board.BLACK:
			color = self.board.BLACK 
		else:
			color = self.board.WHITE

		valid_moves = self.board.valid_moves(color)
		self.children = []
		for move in valid_moves:
			new_board = self.board.get_clone()
			new_board.play(move, color)
			new_state = State(new_board)
			self.children.append(new_state)

	def get_board(self):
		return self.board

	def get_children(self):
		return self.children