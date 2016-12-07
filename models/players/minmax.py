import numpy as np
from models.state import State



class MinMax:
	def __init__(self, color, level):
		self.color = color
		self.level = level

	def build_tree(self, state, temp_level, color):
		if temp_level == self.level:
			scores = state.score()
			score = scores[0] if color is Board.WHITE else scores[1]
			return score, -1

		state.make_children(color)
		opponent_color = self._opponent(color)
		scores = []
		for child in children:
			score, _ = build_tree(child,temp_level+1,opponent_color)
			scores.append(score)

		if color == self.color:
			idx = np.argmax(scores)
		else:
			idx = np.argmin(scores)

		final_score = scores[idx]
		return final_score, idx


	def play(self, board):
		root = State(board)
		score, idx_move = build_tree(root,1,self.color)
		return root.board.valid_moves(self.color)[idx_move]

	def _opponent(self, color):
		return Board.BLACK if color is Board.WHITE else Board.WHITE
