from const import *
from piece import *
from square import Square
from move import Move


class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]

        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def calc_moves(self, piece, row, col):
        '''Расчитывает все возможные ходы выбранной фигуры в ее позиции'''

        def pawn_moves():
            #проверка на количество ходов у пешки
            steps = 1 if piece.moved else 2

            #вертикальные ходы
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))

            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        #выбираем поля для новго хода
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        #делаем новый ход
                        move = Move(initial, final)
                        piece.add_move(move)
                    #завершаем цикл потому что клетка впереди не пуста
                    else: break
                #завершаем цикл потому что клетка вне окна
                else: break

            #диагональные ходы
            possible_move_row = row + piece.dir

        def khight_moves():
            #8 возможных ходов
            possible_moves = [
                (row-2, col+1),
                (row-1, col +2),
                (row+1, col +2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        #выбираем поля для нового хода
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)#piece=piece
                        #создаем новый ход
                        move = Move(initial, final)
                        #делаем новый ход который прошел все проверки
                        piece.add_move(move)

        if isinstance(piece, Pawn): pawn_moves()
        
        elif isinstance(piece, Knight): khight_moves()

        elif isinstance(piece, Bishop): pass

        elif isinstance(piece, Rook): pass

        elif isinstance(piece, Queen): pass

        elif isinstance(piece, King): pass

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        #пешки
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        #кони
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        #слоны
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        #ладьи
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        #ферзь
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        #король
        self.squares[row_other][4] = Square(row_other, 4, King(color))

