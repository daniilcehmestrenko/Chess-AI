import pygame
import sys

from const import *
from game import Game


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
            game.show_moves(screen)
            game.show_pieces(screen)

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
                        board.calc_moves(piece, clicked_row, clicked_col)
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(piece)
                        #показываем доску
                        game.show_bg(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)

                #движение мышью
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        #показываем доску
                        game.show_bg(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        dragger.update_blit(screen)

                #отпускание клавиши мыши
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragger.undrag_piece()

                #закрытие окна
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()

main = Main()
main.mainloop()
