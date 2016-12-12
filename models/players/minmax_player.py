# -*- coding: utf-8 -*-
import numpy as np
from models.state import State



class MinMax:
	EMPTY, BLACK, WHITE, OUTER = '.', '□', '■', '?'

	#Construtor precisa apenas da cor do player e o nivel de profundidade
	def __init__(self, color, level=4, threshold=15):
		self.color = color
		self.level = level
		self.threshold = threshold
		self.turn = 0
		self.pos_values = [[20, -3, 11, 8, 8, 11, -3, 20],
    						[-3, -7, -4, 1, 1, -4, -7, -3],
    						[11, -4, 2, 2, 2, 2, -4, 11],
    						[8, 1, 2, -3, -3, 2, 1, 8],
    						[8, 1, 2, -3, -3, 2, 1, 8],
    						[11, -4, 2, 2, 2, 2, -4, 11],
    						[-3, -7, -4, 1, 1, -4, -7, -3],
    						[20, -3, 11, 8, 8, 11, -3, 20]]


	#Constroi a arvore a partir do estado atual do tabuleiro
	def build_tree(self, state, temp_level, color, cut=None, father=None):
		#Caso base, nivel_atual = nivel_maximo
		if temp_level == self.level:
			score = self.score(state.get_board(), color)

			if abs(score - father) > self.threshold:
				state.make_children(color)
				children = state.get_children()
				if children == []:
					children.append(state)

				scores = []
				for child in children:
					child_score = self.score(state.get_board(), color)
					scores.append(child_score)

				if color == self.color:
					score = max(scores)
				else:
					score = min(scores)

			# print "Final level:", score, scores
			del state
			return score, -1

		#Nao sendo o caso base, expandiremos a arvore atraves
		#das possibilidades de jogadas.
		state.make_children(color)
		children = state.get_children()
		# print "Entrou no level",temp_level
		#Caso nao haja jogada possibilidade de jogada num certo estado
		#Passamos a vez, logo seu filho e ele mesmo so que na vez do
		#oponente.
		if children == []:
			children.append(state)

		#Caso estejamos no estado inicial e so tivermos uma opcao
		#nem vale a pena olhar o resto da arvore, faca a jogada.
		if temp_level == 1 and len(children) == 1:
			# print "uma possibilidade apenas"
			return 0, 0

		#Armazena a cor do oponente.
		opponent_color = self._opponent(color)
		#Armazenara as pontuacoes dos filhos.
		scores = []
		# print "Entrou no level", temp_level
		#Para cada filho, faca a recurssao, aumentando o nivel da arvore
		#e alterando a cor do estado.
		First = True
		ab = None
		if temp_level == self.level -1:
			father = self.score(state.get_board(), color)
			

		for child in children:
			if First == True:
				# print "Chamando primeiro filho"
				score, _ = self.build_tree(child,temp_level+1,opponent_color,None,father)
				scores.append(score)
				ab = score
				First = False
			else:
				# print "Chamando n-esimo filho"
				ab = max(scores) if self.color == color else min(scores)
				score, _ = self.build_tree(child,temp_level+1,opponent_color,ab,father)
				scores.append(score)
			# Se o pai nao tem seu valor para realizar o corte
			# Faca o Minmax normalmente...
			if cut is None: continue
			# Caso ele tenha, significa que um filho ja foi calculado
			# Logo podemos verificar se e possivel descartar este estado
			if self.color == color:
				#Entrando aqui, significa que o pai e beta e o estado atual e alpha
				#entao caso o beta seja menor ou igual ao alpha atual, podemos 
				#encerrar este for, visto que alpha so tende a aumentar e ja temos um
				#valor menor para o beta.
				if score >= cut:
					# print "Cortou:", cut, score
					break
			if self.color == opponent_color:
				#Analogo ao if acima, so que agora o pai e alpha e o estado atual e beta.
				if score <= cut:
					# print "Cortou:", cut, score
					break

		#randomizar para pegar aleatoriamente qualquer maior score.
		# np.random.shuffle(score)
		#O jogador que chamou o MINMAX quer obter o maior valor possivel
		#enquanto o oponente quer diminuir a pontuacao do jogador.
		# print color, self.color

		if color == self.color:
			idx = np.argmax(scores)
		else:
			idx = np.argmin(scores)
		
		#Armazena o valor selecionado.
		final_score = scores[idx]

		#Livrar memoria.
		del state

		# print "Saiu do level",temp_level
		# print scores
		# print "Score:", final_score

		#retorna o valor obtido dos filhos e o indice deste array scores
		#pois no final do algortimo, queremos saber qual movimento fazer
		#o indice i do score coincide com o movimento armazenado no indice i.
		return final_score, idx

	#SWAP oponente.
	#Aqui foi usado o == ao inves do is, pois a cor que recebemos e do
	#objeto board, entao se usarmos o is... da ruim
	#board.WHITE != minmax.WHITE
	def _opponent(self, color):
		return MinMax.BLACK if color == MinMax.WHITE else MinMax.WHITE

	#Calcula a pontuacao de um stado
	def score(self, board, color):
		white = 0
		black = 0
		# moves_black = board.valid_moves(board.BLACK)
		# moves_white = board.valid_moves(board.WHITE)
		# if moves_black == [] and moves_white == []:
		# 	tiles = board.score()
		# 	if color == MinMax.BLACK:
		# 		tiles[0], tiles[1] = tiles[1], tiles[0]
		# 	if tiles[0] > tiles[1]:
		# 		return float("inf")
		# 	elif tiles[0] < tiles[1]:
		# 		return float("-inf")
		for i in range(1, 9):
			for j in range(1, 9):
				if board.get_square_color(i, j) == MinMax.WHITE:
					white += self.pos_values[i - 1][j - 1]
				elif board.get_square_color(i, j) == MinMax.BLACK:
					black += self.pos_values[i - 1][j - 1]

		score = white if color == MinMax.WHITE else black

		return score

	#Faz jogada.
	def play(self, board):
		#Estado inicial, configuracao atual do tabuleiro.
		root = State(board)
		self.turn += 1

		# print tiles, self.level
		if self.turn > 13:
			self.level = 5
		if self.turn > 27:
			self.level = 8
		#Apois contruir a arvore e obtemos o indice do array de movimentos
		#que corresponde a jogada que o minmax decidiu.
		_, idx_move = self.build_tree(root,1,self.color,None,None)
		return root.board.valid_moves(self.color)[idx_move]