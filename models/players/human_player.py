from models.move import Move
class HumanPlayer:
  def __init__(self, color):
    self.color = color


  def play(self, board):
    while True:
      try:
        rowInp = int(raw_input("Linha: "))
        colInp = int(raw_input("Coluna: "))
        move = Move(rowInp, colInp)
        if move not in board.valid_moves(self.color):
          raise
        break
      except:
        print "Movimento invalido. Insira um valor valido"

    # move = Move(rowInp, colInp)
    # while move not in board.valid_moves(self.color):
    #   print "Movimento invalido.Insira um valido"
    #   print board
    #   rowInp = int(raw_input("Linha: "))
    #   colInp = int(raw_input("Coluna: "))
    #   move = Move(rowInp, colInp)
    return move
