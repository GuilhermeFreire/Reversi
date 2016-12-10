# -*- coding: utf-8 -*-
import numpy as np
from models.state import State


class Mobility:
    EMPTY, BLACK, WHITE, OUTER = '.', '□', '■', '?'

    # Construtor precisa apenas da cor do player e o nivel de profundidade
    def __init__(self, color, level=4):
        self.color = color
        self.level = level

    # Constroi a arvore a partir do estado atual do tabuleiro
    def build_tree(self, state, temp_level, color):
        # Caso base, nivel_atual = nivel_maximo
        if temp_level == self.level:
            scores = state.mobility_score(color)
            del state
            return scores

        # Nao sendo o caso base, expandiremos a arvore atraves
        # das possibilidades de jogadas
        state.make_children(color)
        children = state.get_children()

        # Caso nao haja jogada possibilidade de jogada num certo estado
        # retorna o valo apropriado para esse estado. Eu considerei zero
        # Mas poderia colocar um valor negativo...
        if children == []:
            return 0, -1

        # Armazena a cor do oponente
        opponent_color = self._opponent(color)

        # Armazenara as pontuacoes dos filhos
        scores = []

        # Para cada filho, faca a recurssao, aumentando o nivel da arvore
        # e alterando a cor do estado
        for child in children:
            score = self.build_tree(child, temp_level + 1, opponent_color)
            scores.append(score)

        # O jogador que chamou o MINMAX quer obter o maior valor possivel
        # enquanto o oponente quer diminuir a pontuacao do jogador
        if color == self.color:
            idx = np.argmax(scores)
        else:
            idx = np.argmin(scores)

        # Armazena o valor selecionado
        final_score = scores[idx]

        # Livrar memoria
        del state

        # retorna o valor obtido dos filhos e o indice deste array scores
        # pois no final do algortimo, queremos saber qual movimento fazer
        # o indice i do score coincide com o movimento armazenado no indice i
        return final_score, idx

    # SWAP oponente
    def _opponent(self, color):
        return Mobility.BLACK if color is Mobility.WHITE else Mobility.WHITE

    # Faz jogada
    def play(self, board):
        # Estado inicial, configuracao atual do tabuleiro
        root = State(board)
        # Apois contruir a arvore e obtemos o indice do array de movimentos
        # que corresponde a jogada que o minmax decidiu
        _, idx_move = self.build_tree(root, 1, self.color)
        return root.board.valid_moves(self.color)[idx_move]