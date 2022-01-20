"""This module is responsible for all of the mechanics of the game of checkers.
This includes data classes for moves, the game, and pieces, as well as mutations
to the game board to play the game.

Copyright Nathan Wootton 2021"""

from typing import Optional, Any
from copy import deepcopy


class Move:
    """This class represents a move made in the game

        Instance Attributes:
            - move: the string representation of the move.  The length of the string varies with
            the move complexity, for example a double capture will have a length of 6
            - piece_captured: whether the a capture happened

        Representation Invariants:
            - len(move) % 2 == 0
            - all(isnumeric(number) for number in move)"""

    move: str
    piece_captured: bool

    def __init__(self, move: str, piece_captured: bool) -> None:
        """Initialize a new move"""
        self.move = move
        self.piece_captured = piece_captured


class Piece:
    """This class represents a piece in the game

    Instance Attributes:
        - is_white: whether the piece belongs to the white player
        - is_king: whether the piece has been turned into a king piece"""
    is_white: bool
    is_king: bool

    def __init__(self, is_white: bool) -> None:
        """Initialize a new checkers piece"""
        self.is_white = is_white
        self.is_king = False


DEFAULT_BOARD_SETUP = [[Piece(True), None, Piece(True), None, Piece(True), None, Piece(True), None],
                       [None, Piece(True), None, Piece(True), None, Piece(True), None, Piece(True)],
                       [Piece(True), None, Piece(True), None, Piece(True), None, Piece(True), None],
                       [None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None],
                       [None, Piece(False), None, Piece(False), None, Piece(False), None, Piece(False)],
                       [Piece(False), None, Piece(False), None, Piece(False), None, Piece(False), None],
                       [None, Piece(False), None, Piece(False), None, Piece(False), None, Piece(False)]]


class CheckersGame:
    """This class is responsible for carrying the data for the game and running the game by applying the
    moves made by bots and players alike.

    Instance Attributes:
        - board: a list of all the spaces on the board that keeps track of where pieces are on it
        - is_white_move: whether it is the white players move
        - gamestate: the game state that will be drawn on the screen, for example when a game
        is being played the gamestate is 'GAME'.
        - white_win: whether or not the white player won the game
        - moves_since_cap: tracks the amount of moves since a capture.  If this is 50,
        then the game ends in a tie.
        - is_draw: whether or not the game ended in a tie

    Representation Invariants:
        - gamestate in {'GAME', 'END', 'MENU'}
        """

    board: list[list[Optional[Piece]]]
    is_white_move: bool
    gamestate: str
    white_win: bool
    moves_since_cap: int
    is_draw: bool
    main_game: bool

    def __init__(self, is_white_move: bool = True, board: list[list[Optional[Piece]]] = None,
                 gamestate: str = 'MENU') -> None:
        """Initialize a new checkers game.  If given no input for the board, use the default setup."""
        if board is None:
            self.board = DEFAULT_BOARD_SETUP
        else:
            self.board = board
        self.is_white_move = is_white_move
        self.gamestate = gamestate
        self.white_win = True
        self.player_turn = True
        self.moves_since_cap = 0
        self.is_draw = False
        self.main_game = True

    def return_all_pieces_location(self, colour: str = 'any') -> list[((int, int), Piece)]:
        """Returns a list of tuples, containing the pieces coordinate on the board and the piece itself

        Representation Invariants:
            - colour in {'any', 'black', 'white'}

        >>> cg = CheckersGame()
        >>> pieces = cg.return_all_pieces_location()
        >>> len(pieces)
        24
        """
        pieces_so_far = []
        for row in range(0, 8):
            for col in range(0, 8):
                if self.board[row][col] is not None and colour == 'any':
                    pieces_so_far.append(((row, col), self.board[row][col]))
                elif self.board[row][col] is not None and colour == 'white' \
                        and self.board[row][col].is_white:
                    pieces_so_far.append(((row, col), self.board[row][col]))
                elif self.board[row][col] is not None and colour == 'black' \
                        and not self.board[row][col].is_white:
                    pieces_so_far.append(((row, col), self.board[row][col]))
        return pieces_so_far

    def make_copy_game(self) -> Any:
        """Copy the current game using deepcopy, so that the game's pieces are also
        copies
        """
        copy_game = CheckersGame(deepcopy(self.is_white_move), deepcopy(self.board))
        copy_game.moves_since_cap = 0
        copy_game.main_game = False
        return copy_game

    def find_legal_moves(self) -> list:
        """Find all legal moves that the current player can make

        >>> cg = CheckersGame()
        >>> moves = cg.find_legal_moves()
        >>> len(moves)
        7
        """
        normal_moves = []
        capture_moves = []
        if self.is_white_move:
            pieces_to_check = self.return_all_pieces_location('white')
            for piece_info in pieces_to_check:
                normal_moves.extend(self.check_tl(self.is_white_move, piece_info[0], piece_info[1]))
                normal_moves.extend(self.check_tr(self.is_white_move, piece_info[0], piece_info[1]))
                if piece_info[1].is_king:
                    normal_moves.extend(self.check_bl(self.is_white_move, piece_info[0], piece_info[1]))
                    normal_moves.extend(self.check_br(self.is_white_move, piece_info[0], piece_info[1]))
            for possible_move in normal_moves:
                if possible_move.piece_captured:
                    capture_moves.append(possible_move)
        else:
            pieces_to_check = self.return_all_pieces_location('black')
            for piece_info in pieces_to_check:
                normal_moves.extend(self.check_bl(self.is_white_move, piece_info[0], piece_info[1]))
                normal_moves.extend(self.check_br(self.is_white_move, piece_info[0], piece_info[1]))
                if piece_info[1].is_king:
                    normal_moves.extend(self.check_tl(self.is_white_move, piece_info[0], piece_info[1]))
                    normal_moves.extend(self.check_tr(self.is_white_move, piece_info[0], piece_info[1]))
            for possible_move in normal_moves:
                if possible_move.piece_captured:
                    capture_moves.append(possible_move)

        if capture_moves != []:
            return capture_moves
        else:
            return normal_moves

    def find_legal_moves_one_piece(self, piece_info: ((int, int), Piece)) -> list:
        """Find all legal moves that the given piece can make
        """
        normal_moves = []
        capture_moves = []
        if self.is_white_move:
            normal_moves.extend(self.check_tl(self.is_white_move, piece_info[0], piece_info[1]))
            normal_moves.extend(self.check_tr(self.is_white_move, piece_info[0], piece_info[1]))
            if piece_info[1].is_king:
                normal_moves.extend(self.check_bl(self.is_white_move, piece_info[0], piece_info[1]))
                normal_moves.extend(self.check_br(self.is_white_move, piece_info[0], piece_info[1]))
            for possible_move in normal_moves:
                if possible_move.piece_captured:
                    capture_moves.append(possible_move)
        if not self.is_white_move:
            normal_moves.extend(self.check_bl(self.is_white_move, piece_info[0], piece_info[1]))
            normal_moves.extend(self.check_br(self.is_white_move, piece_info[0], piece_info[1]))
            if piece_info[1].is_king:
                normal_moves.extend(self.check_tl(self.is_white_move, piece_info[0], piece_info[1]))
                normal_moves.extend(self.check_tr(self.is_white_move, piece_info[0], piece_info[1]))
            for possible_move in normal_moves:
                if possible_move.piece_captured:
                    capture_moves.append(possible_move)

        if capture_moves != []:
            return capture_moves
        else:
            return normal_moves

    def _check_additional_capture(self, og_loc: (int, int), loc: (int, int), piece_used: Piece) -> list[Move]:
        """Checks all appropriate directions to find if an additional capture is available.
        This function works recursively with the other four check functions to find
        all multi-captures"""
        moves_list = []

        test_game = self.make_copy_game()
        test_game.board[int((og_loc[0] + loc[0]) / 2)][int((og_loc[1] + loc[1]) / 2)] = None

        if self.is_white_move and not piece_used.is_king:
            moves_list.extend(test_game.check_tl(self.is_white_move, loc, piece_used, True))
            moves_list.extend(test_game.check_tr(self.is_white_move, loc, piece_used, True))
        elif not self.is_white_move and not piece_used.is_king:
            moves_list.extend(test_game.check_bl(self.is_white_move, loc, piece_used, True))
            moves_list.extend(test_game.check_br(self.is_white_move, loc, piece_used, True))
        else:
            moves_list.extend(test_game.check_tl(self.is_white_move, loc, piece_used, True))
            moves_list.extend(test_game.check_tr(self.is_white_move, loc, piece_used, True))
            moves_list.extend(test_game.check_bl(self.is_white_move, loc, piece_used, True))
            moves_list.extend(test_game.check_br(self.is_white_move, loc, piece_used, True))
        for possible_move in moves_list:
            possible_move.move = str(og_loc[0]) + str(og_loc[1]) + possible_move.move

        return moves_list

    def check_tl(self, white: bool, loc: (int, int), piece_used: Piece, double: bool = False) -> list[Move]:
        """Checks the top left of the piece for possible moves, and returns a list of those moves.
        Returns an empty list if there are no moves."""
        if loc[1] != 0 and loc[0] != 7 and white:
            if self.board[loc[0] + 1][loc[1] - 1] is None and not double:
                return [Move(str(loc[0]) + str(loc[1]) + str(loc[0] + 1) + str(loc[1] - 1), False)]
            elif self.board[loc[0] + 1][loc[1] - 1] is None and double:
                return []
            elif not self.board[loc[0] + 1][loc[1] - 1].is_white and \
                    loc[1] > 1 and loc[0] < 6 and self.board[loc[0] + 2][loc[1] - 2] is None:
                legal_moves = [Move(str(loc[0]) + str(loc[1]) + str(loc[0] + 2) + str(loc[1] - 2), True)]
                legal_moves.extend(self._check_additional_capture(
                    (loc[0], loc[1]), (loc[0] + 2, loc[1] - 2), piece_used))
                return legal_moves
            else:
                return []
        elif loc[1] != 0 and loc[0] != 7 and not white:
            if self.board[loc[0] + 1][loc[1] - 1] is None and not double:
                return [Move(str(loc[0]) + str(loc[1]) + str(loc[0] + 1) + str(loc[1] - 1), False)]
            elif self.board[loc[0] + 1][loc[1] - 1] is None and double:
                return []
            elif self.board[loc[0] + 1][loc[1] - 1].is_white and \
                    loc[1] > 1 and loc[0] < 6 and self.board[loc[0] + 2][loc[1] - 2] is None:
                legal_moves = [Move(str(loc[0]) + str(loc[1]) + str(loc[0] + 2) + str(loc[1] - 2), True)]
                legal_moves.extend(self._check_additional_capture(
                    (loc[0], loc[1]), (loc[0] + 2, loc[1] - 2), piece_used))
                return legal_moves
            else:
                return []
        else:
            return []

    def check_tr(self, white: bool, loc: (int, int), piece_used: Piece, double: bool = False) -> list[Move]:
        """Checks the top right of the piece for possible moves, and returns a list of those moves.
        Returns an empty list if there are no moves."""
        if loc[1] != 7 and loc[0] != 7 and white:
            if self.board[loc[0] + 1][loc[1] + 1] is None and not double:
                return [Move(str(loc[0]) + str(loc[1]) + str(loc[0] + 1) + str(loc[1] + 1), False)]
            elif self.board[loc[0] + 1][loc[1] + 1] is None and double:
                return []
            elif not self.board[loc[0] + 1][loc[1] + 1].is_white and \
                    loc[1] < 6 and loc[0] < 6 and self.board[loc[0] + 2][loc[1] + 2] is None:
                legal_moves = [Move(str(loc[0]) + str(loc[1]) + str(loc[0] + 2) + str(loc[1] + 2), True)]
                legal_moves.extend(self._check_additional_capture(
                    (loc[0], loc[1]), (loc[0] + 2, loc[1] + 2), piece_used))
                return legal_moves
            else:
                return []
        elif loc[1] != 7 and loc[0] != 7 and not white:
            if self.board[loc[0] + 1][loc[1] + 1] is None and not double:
                return [Move(str(loc[0]) + str(loc[1]) + str(loc[0] + 1) + str(loc[1] + 1), False)]
            elif self.board[loc[0] + 1][loc[1] + 1] is None and double:
                return []
            elif self.board[loc[0] + 1][loc[1] + 1].is_white and \
                    loc[1] < 6 and loc[0] < 6 and self.board[loc[0] + 2][loc[1] + 2] is None:
                legal_moves = [Move(str(loc[0]) + str(loc[1]) + str(loc[0] + 2) + str(loc[1] + 2), True)]
                legal_moves.extend(self._check_additional_capture(
                    (loc[0], loc[1]), (loc[0] + 2, loc[1] + 2), piece_used))
                return legal_moves
            else:
                return []
        else:
            return []

    def check_bl(self, white: bool, loc: (int, int), piece_used: Piece, double: bool = False) -> list[Move]:
        """Checks the bottom left of the piece for possible moves, and returns a list of those moves.
        Returns an empty list if there are no moves."""
        if loc[1] != 0 and loc[0] != 0 and white:
            if self.board[loc[0] - 1][loc[1] - 1] is None and not double:
                return [Move(str(loc[0]) + str(loc[1]) + str(loc[0] - 1) + str(loc[1] - 1), False)]
            elif self.board[loc[0] - 1][loc[1] - 1] is None and double:
                return []
            elif not self.board[loc[0] - 1][loc[1] - 1].is_white and \
                    loc[1] > 1 and loc[0] > 1 and self.board[loc[0] - 2][loc[1] - 2] is None:
                legal_moves = [Move(str(loc[0]) + str(loc[1]) + str(loc[0] - 2) + str(loc[1] - 2), True)]
                legal_moves.extend(self._check_additional_capture(
                    (loc[0], loc[1]), (loc[0] - 2, loc[1] - 2), piece_used))
                return legal_moves
            else:
                return []
        elif loc[1] != 0 and loc[0] != 0 and not white:
            if self.board[loc[0] - 1][loc[1] - 1] is None and not double:
                return [Move(str(loc[0]) + str(loc[1]) + str(loc[0] - 1) + str(loc[1] - 1), False)]
            elif self.board[loc[0] - 1][loc[1] - 1] is None and double:
                return []
            elif self.board[loc[0] - 1][loc[1] - 1].is_white and \
                    loc[1] > 1 and loc[0] > 1 and self.board[loc[0] - 2][loc[1] - 2] is None:
                legal_moves = [Move(str(loc[0]) + str(loc[1]) + str(loc[0] - 2) + str(loc[1] - 2), True)]
                legal_moves.extend(self._check_additional_capture(
                    (loc[0], loc[1]), (loc[0] - 2, loc[1] - 2), piece_used))
                return legal_moves
            else:
                return []
        else:
            return []

    def check_br(self, white: bool, loc: (int, int), piece_used: Piece, double: bool = False) -> list[Move]:
        """Checks the bottom right of the piece for possible moves, and returns a list of those moves.
        Returns an empty list if there are no moves."""
        if loc[1] != 7 and loc[0] != 0 and white:
            if self.board[loc[0] - 1][loc[1] + 1] is None and not double:
                return [Move(str(loc[0]) + str(loc[1]) + str(loc[0] - 1) + str(loc[1] + 1), False)]
            elif self.board[loc[0] - 1][loc[1] + 1] is None and double:
                return []
            elif not self.board[loc[0] - 1][loc[1] + 1].is_white and \
                    loc[1] < 6 and loc[0] > 1 and self.board[loc[0] - 2][loc[1] + 2] is None:
                legal_moves = [Move(str(loc[0]) + str(loc[1]) + str(loc[0] - 2) + str(loc[1] + 2), True)]
                legal_moves.extend(self._check_additional_capture(
                    (loc[0], loc[1]), (loc[0] - 2, loc[1] + 2), piece_used))
                return legal_moves
            else:
                return []
        elif loc[1] != 7 and loc[0] != 0 and not white:
            if self.board[loc[0] - 1][loc[1] + 1] is None and not double:
                return [Move(str(loc[0]) + str(loc[1]) + str(loc[0] - 1) + str(loc[1] + 1), False)]
            elif self.board[loc[0] - 1][loc[1] + 1] is None and double:
                return []
            elif self.board[loc[0] - 1][loc[1] + 1].is_white and \
                    loc[1] < 6 and loc[0] > 1 and self.board[loc[0] - 2][loc[1] + 2] is None:
                legal_moves = [Move(str(loc[0]) + str(loc[1]) + str(loc[0] - 2) + str(loc[1] + 2), True)]
                legal_moves.extend(self._check_additional_capture(
                    (loc[0], loc[1]), (loc[0] - 2, loc[1] + 2), piece_used))
                return legal_moves
            else:
                return []
        else:
            return []

    def make_move(self, move: Move) -> None:
        """Mutate the game to change the board according to the move passed in"""
        if not move.piece_captured:
            self.board[int(move.move[0])][int(move.move[1])], \
                self.board[int(move.move[2])][int(move.move[3])] = \
                None, self.board[int(move.move[0])][int(move.move[1])]
        else:
            self.moves_since_cap = -1  # reset, since we add one in the same call it totals to 0
            for submove_num in range(0, int((len(move.move) / 2) - 1)):
                self.board[int(move.move[submove_num * 2])][int(move.move[(submove_num * 2) + 1])], \
                    self.board[int(move.move[(submove_num * 2) + 2])][int(move.move[(submove_num * 2) + 3])] = \
                    None, self.board[int(move.move[submove_num * 2])][int(move.move[(submove_num * 2) + 1])]

                self.board[int((int(move.move[submove_num * 2]) + int(move.move[(submove_num * 2) + 2])) / 2)]\
                    [int((int(move.move[(submove_num * 2) + 1]) + int(move.move[(submove_num * 2) + 3])) / 2)] = None
        self.is_white_move = not self.is_white_move

        self._update_pieces()

        self.moves_since_cap += 1

        if self.find_legal_moves() == [] and self.is_white_move and self.main_game:
            self.white_win = False
            self.gamestate = 'END'
        elif self.find_legal_moves() == [] and not self.is_white_move and self.main_game:
            self.white_win = True
            self.gamestate = 'END'
        elif self.moves_since_cap >= 50 and self.main_game:
            self.white_win = True
            self.is_draw = True
            self.gamestate = 'END'

    def _update_pieces(self) -> None:
        """Turns pieces into kings if they reach the ends of the board"""
        locations = self.return_all_pieces_location()
        for piece_loc in locations:
            if piece_loc[1].is_white and piece_loc[0][0] == 7:
                piece_loc[1].is_king = True
            elif not piece_loc[1].is_white and piece_loc[0][0] == 0:
                piece_loc[1].is_king = True


# if __name__ == '__main__':
#     import python_ta
#     python_ta.check_all(config={
#         'extra-imports': ['copy', 'typing'],
#         'allowed-io': [],
#         'max-line-length': 100,
#         'disable': ['R0912', 'R1702', 'E1136']
#     })
