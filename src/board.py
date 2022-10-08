from const import *
from piece import *
from square import Square
from move import Move


class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        #обновление ходов
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        if isinstance(piece, Pawn):
            self.check_promotion(piece, final)
        
        #королевская рокировка
        if isinstance(piece, King):
            if self.castling(initial, final):
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        #меняем статус фигуры
        piece.moved = True
        
        #очищаем список ходов
        piece.clear_moves()

        #указываем последний ход
        self.last_move = move

    #логика метода сравнения указа в методах __eq__ (Square, Move)
    def valid_move(self, piece, move):
        return move in piece.moves

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

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
                        #выбираем поля для нового хода
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
            possible_move_cols = [col-1, col+1]
            #проверяем на наличие пешки другого цвета если есть то ходить по диагонали можно
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                        #указываем кординаты начала и конца хода
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        #делаем ход
                        move = Move(initial, final)
                        #добавляем ход
                        piece.add_move(move)

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

        def king_moves():
            adjs = [
                (row-1, col+0), #вверх
                (row-1, col+1), #вверх вправо
                (row+0, col+1), #вправо
                (row+1, col+1), #вниз вправо
                (row+1, col+0), #вниз
                (row+1, col-1), #вниз влево
                (row+0, col-1), #влево
                (row-1, col-1), #вверх влево
            ]

            for possible_move in adjs:
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
            
            #рокировка
            if not piece.moved:

                #рокировка в сторону ферзя
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1,4):
                            #если между королем и ладьей есть фигуры то рокировка невозможна
                            if self.squares[row][c].has_piece(): 
                                break

                            if c == 3:
                                #сохраняем левую ладью у короля
                                piece.left_rook = left_rook

                                #перемещаем ладью
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                move = Move(initial, final)
                                left_rook.add_move(move)

                                #перемещаем короля
                                initial = Square(row, col)
                                final = Square(row, 2)
                                move = Move(initial, final)
                                piece.add_move(move)
                
                #рокировка в сторону короля
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            #если между королем и ладьей есть фигуры то рокировка невозможна
                            if self.squares[row][c].has_piece(): 
                                break

                            if c == 6:
                                #сохраняем правую ладью у короля
                                piece.right_rook = right_rook

                                #перемещаем ладью
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                move = Move(initial, final)
                                right_rook.add_move(move)

                                #перемещаем короля
                                initial = Square(row, col)
                                final = Square(row, 6)
                                move = Move(initial, final)
                                piece.add_move(move)

        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):

                        #выбираем поля для возможного нового хода
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)

                        #делаем новый возможный ход
                        move = Move(initial, final)

                        #если путь пустой мы не завершаем цикл
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            #добавляем новый ход
                            piece.add_move(move)

                        #если на пути есть противник
                        if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                            #добавляем новый ход
                            piece.add_move(move)
                            break

                        #если на пути есть союзная фигура
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                    
                    #за пределами доски
                    else: break

                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        if isinstance(piece, Pawn):
            pawn_moves()
        
        elif isinstance(piece, Knight):
            khight_moves()

        elif isinstance(piece, Bishop):
            straightline_moves([
                (-1, 1), #верхняя правая диагональ
                (-1, -1), #верхняя левая диагональ
                (1, 1), #нижняя правая диагональ
                (1, -1) #нижняя левая диагональ
            ])

        elif isinstance(piece, Rook):
            straightline_moves([
                (-1, 0), #вверх
                (1, 0), #вниз
                (0, 1), #вправо
                (0, -1) #влево
            ])

        elif isinstance(piece, Queen):
            straightline_moves([
                (-1, 1), #верхняя правая диагональ
                (-1, -1), #верхняя левая диагональ
                (1, 1), #нижняя правая диагональ
                (1, -1), #нижняя левая диагональ
                (-1, 0), #вверх
                (1, 0), #вниз
                (0, 1), #вправо
                (0, -1) #влево
            ])

        elif isinstance(piece, King):
            king_moves()

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

