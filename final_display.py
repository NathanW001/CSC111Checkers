"""This module is responsible for displaying the game of checkers on the screen.
Additionally, it deals with mouse interaction on the screen, such as a player making moves

Copyright Nathan Wootton 2021"""
import pygame
import final_game

MENU_IMAGE = pygame.image.load('assets/menu.png')
START_IDLE = pygame.image.load('assets/start_normal.png')
START_HOVER = pygame.image.load('assets/start_hover.png')
BOARD_IMAGE = pygame.image.load('assets/board.png')
WHITE_KING = pygame.image.load('assets/pieces/wk.png')
WHITE_PIECE = pygame.image.load('assets/pieces/w.png')
BLACK_KING = pygame.image.load('assets/pieces/bk.png')
BLACK_PIECE = pygame.image.load('assets/pieces/b.png')
HL_SQUARE = pygame.image.load('assets/hl_square.png')
WWIN = pygame.image.load('assets/wwin.png')
BWIN = pygame.image.load('assets/bwin.png')
DRAW = pygame.image.load('assets/draw.png')


def begin_display() -> None:
    """Initialize the pygame display window
    """
    if not pygame.display.get_init():
        pygame.display.init()
    pygame.display.set_mode((800, 800))
    pygame.display.set_caption('Checkers')
    surface = pygame.display.get_surface()
    surface.fill((255, 255, 255))
    pygame.display.flip()


def update_display(game: final_game.CheckersGame, moves: list[final_game.Move])\
        -> list[final_game.Move]:
    """Updates the pygame diplay window and calls to handle any events
    that may occur"""
    mouse_pos = pygame.mouse.get_pos()
    if game.gamestate == 'MENU':
        draw_menu(mouse_pos)
        moves = handle_events(game, moves)
    elif game.gamestate == 'GAME':
        draw_current_game(game, moves)
        moves = handle_events(game, moves)
    elif game.gamestate == 'END':
        draw_game_over(game.white_win, game.is_draw)
        moves = handle_events(game, moves)

    pygame.display.update()
    return moves


def handle_events(game: final_game.CheckersGame, old_moves: list[final_game.Move])\
        -> list[final_game.Move]:
    """Handles all events, including mouse click events and moving pieces, as
    well as exiting the window"""
    moves = old_moves
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and game.gamestate == 'GAME':
            moves = []
            legal_moves = game.find_legal_moves()
            raw_pos = event.pos
            pos = (raw_pos[0] // 100, (7 - raw_pos[1] // 100))
            if old_moves != []:
                for old_move in old_moves:
                    if int(old_move.move[-1]) == pos[0] and int(old_move.move[-2]) == pos[1]:
                        game.make_move(old_move)  # if someone wins the game, special case
            elif game.board[pos[1]][pos[0]] is not None:
                pos_moves = game.find_legal_moves_one_piece(((pos[1], pos[0]),
                                                             game.board[pos[1]][pos[0]]))
                for move in pos_moves:
                    for check_move in legal_moves:
                        if move.move == check_move.move:
                            moves.append(move)
            # elif old_highlight is not None:
            #     for possible_pos in old_highlight:
            #         if pos == possible_pos:
            #
            else:
                moves = []
        elif event.type == pygame.MOUSEBUTTONDOWN and game.gamestate == 'MENU':
            pos = event.pos
            if 100 <= pos[0] <= 700 and 400 <= pos[1] <= 500:
                game.gamestate = 'GAME'
    return moves


###################################################
# screens
###################################################

def draw_menu(pos: (int, int)) -> None:
    """Draw the menu screen"""
    screen = pygame.display.get_surface()
    screen.blit(MENU_IMAGE, (0, 0))
    if 100 <= pos[0] <= 700 and 400 <= pos[1] <= 500:
        screen.blit(START_HOVER, (100, 400))
    else:
        screen.blit(START_IDLE, (100, 400))


def draw_current_game(game: final_game.CheckersGame, moves: list[final_game.Move]) -> None:
    """Draw the current game being played"""
    screen = pygame.display.get_surface()
    screen.blit(BOARD_IMAGE, (0, 0))
    for value in game.return_all_pieces_location():
        if value[1].is_white and value[1].is_king:
            screen.blit(WHITE_KING, (100 * value[0][1], 700 - (100 * value[0][0])))
        elif value[1].is_white and not value[1].is_king:
            screen.blit(WHITE_PIECE, (100 * value[0][1], 700 - (100 * value[0][0])))
        elif not value[1].is_white and value[1].is_king:
            screen.blit(BLACK_KING, (100 * value[0][1], 700 - (100 * value[0][0])))
        elif not value[1].is_white and not value[1].is_king:
            screen.blit(BLACK_PIECE, (100 * value[0][1], 700 - (100 * value[0][0])))

    for move in moves:
        screen.blit(HL_SQUARE, (100 * int(move.move[-1]), 700 - (100 * int(move.move[-2]))))


def draw_game_over(white_win: bool, stalemate: bool) -> None:
    """Draws the game over screen"""
    screen = pygame.display.get_surface()
    if stalemate:
        screen.blit(DRAW, (0, 0))
    elif white_win:
        screen.blit(WWIN, (0, 0))
    else:
        screen.blit(BWIN, (0, 0))


# if __name__ == '__main__':
#     import python_ta
#     python_ta.check_all(config={
#         'extra-imports': ['pygame', 'final_game'],
#         'allowed-io': ['import_tree', 'export_tree', 'print_trees'],
#         'max-line-length': 100,
#         'disable': ['R0912', 'R1702', 'E1136', 'E1101']
#     })
