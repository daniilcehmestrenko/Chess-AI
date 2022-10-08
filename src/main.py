import pygame
import sys

from const import *
from game import Game
from move import Move
from square import Square


class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('Chess')
        self.game = Game()

    def mainloop(self):

        game = self.game
        screen = self.screen
        board = self.game.board
        dragger = self.game.dragger
        
        while True:
            #показываем доску
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                #зажатие мыши
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    #проверка клика на наличие фигуры
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        #проверяем цвет фигуры с очередью хода
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            #показываем доску
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                #движение мышью
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE

                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        #показываем доску
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)

                #отпускание клавиши мыши
                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        #создаем возможный ход
                        inital = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(inital, final)

                        #проверка валидности хода
                        if board.valid_move(dragger.piece, move):

                            captured = board.squares[released_row][released_col].has_piece()

                            board.move(dragger.piece, move)
                            #звук хода или атаки на фигуру
                            game.play_sound(captured)
                            #рисуем ход на доске
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            #меняем очередь хода
                            game.next_turn()

                    dragger.undrag_piece()

                #меняем тему при нажатии t
                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_t:
                        game.change_theme()
                    
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                #закрытие окна
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()

main = Main()
main.mainloop()
