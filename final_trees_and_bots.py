"""This module runs using final_display.py and final_game.py to allow the player to
play against bots that control one specific side.  This module additionally has
the codes for all of the bots, as well as game tress and methods to make,
export, and import them.

Copyright Nathan Wootton 2021"""
from time import sleep
from typing import Optional
from math import inf
import random
import final_display
import final_game


class CheckersGameTree:
    """A decision tree for a CheckersGame"""
    move: final_game.Move
    white_turn: bool
    subtrees: list

    def __init__(self, move: final_game.Move, white_turn: bool) -> None:
        """Initialize this ChessGameTree"""
        self.move = move
        self.white_turn = white_turn
        self.subtrees = []


class Bot:
    """Template for a bot player"""
    def make_move(self, game: final_game.CheckersGame) -> None:
        """Make a move
        """
        raise NotImplementedError


class RandomBot(Bot):
    """This bot picks a random move from the possible moves"""

    def make_move(self, game: final_game.CheckersGame) -> None:
        """make a random move
        """
        moves = game.find_legal_moves()
        move_to_make = random.choice(moves)
        game.make_move(move_to_make)


class MinimaxBot(Bot):
    """This bot uses the minimax algorithm with no pruning to calculate the best
    possible move for the bot to make

    Instance Attributes:
        - tree: The tree with which the bot makes moves, that represents the game state
        - tree_depth: The depth of the tree that this bot uses.  Larger depths will take
        significantly more time to make moves"""

    tree: CheckersGameTree
    tree_depth: int

    def __init__(self, game: final_game.CheckersGame, tree_depth: int) -> None:
        """Initialize a minimax bot"""
        self.tree = generate_game_tree(tree_depth, game, final_game.Move('', False))
        self.tree_depth = tree_depth

    def make_move(self, game: final_game.CheckersGame) -> None:
        """Make a move based on what the bot does.  Assumes that the subtree only has legal moves"""
        self.update_tree(game)
        best_move = self.calc_best_move(game, self.tree)
        game.make_move(best_move[0])

    def calc_best_move(self, game: final_game.CheckersGame, tree: CheckersGameTree)\
            -> (final_game.Move, int):
        """Uses minimax algorithm to decide the best move based on the value of each
        gamestate the tree corresponds to.  Value based on white pieces minus black pieces"""
        if tree.subtrees == []:
            white_pieces = game.return_all_pieces_location('white')
            black_pieces = game.return_all_pieces_location('black')
            return (tree.move, len(white_pieces) - len(black_pieces))
        elif tree.move.move != '':
            subtree_moves = []
            for subtree in tree.subtrees:
                game_copy = game.make_copy_game()
                game_copy.make_move(subtree.move)
                subtree_moves.append(self.calc_best_move(game_copy, subtree))
            if game.is_white_move:
                best_move = subtree_moves[0]
                for possible_move in subtree_moves:  # max score
                    if possible_move[1] > best_move[1]:
                        best_move = possible_move
                return (tree.move, best_move[1])
            else:
                best_move = subtree_moves[0]
                for possible_move in subtree_moves:  # min score
                    if possible_move[1] < best_move[1]:
                        best_move = possible_move
                return (tree.move, best_move[1])
        else:
            subtree_moves = []
            for subtree in tree.subtrees:
                game_copy = game.make_copy_game()
                game_copy.make_move(subtree.move)
                subtree_moves.append(self.calc_best_move(game_copy, subtree))
            if game.is_white_move:
                best_move = subtree_moves[0]
                for possible_move in subtree_moves:  # max score
                    if possible_move[1] > best_move[1]:
                        best_move = possible_move
                return best_move
            else:
                best_move = subtree_moves[0]
                for possible_move in subtree_moves:  # min score
                    if possible_move[1] < best_move[1]:
                        best_move = possible_move
                return best_move

    def update_tree(self, game: final_game.CheckersGame) -> None:
        """Updates the bot's subtree to reflect the game by generating a new subtree"""
        self.tree = generate_game_tree(self.tree_depth, game, final_game.Move('', False))


class MinimaxPruneBot(Bot):
    """This bot uses the minimax algorithm with no pruning to calculate the best
    possible move for the bot to make.  Additionally, speeds up tree search time by
    implementing alpha-beta pruning to eliminate useless searches"""
    tree: CheckersGameTree
    tree_depth: int

    def __init__(self, game: final_game.CheckersGame, tree_depth: int) -> None:
        """Initialize a minimax bot"""
        self.tree = generate_game_tree(tree_depth, game, final_game.Move('', False))
        self.tree_depth = tree_depth

    def make_move(self, game: final_game.CheckersGame) -> None:
        """Make a move based on what the bot does.  Assumes that the subtree only has legal moves"""
        self.update_tree(game)
        best_move = self.calc_best_move(game, self.tree, -inf, inf)
        game.make_move(best_move[0])

    def calc_best_move(self, game: final_game.CheckersGame, tree: CheckersGameTree,
                       alpha: float, beta: float) -> (final_game.Move, int):
        """Uses minimax algorithm to decide the best move based on the value of each
        gamestate the tree corresponds to.  Value based on white pieces minus black pieces.
        Alpha is the best score for white, and beta is the best score for black"""
        if tree.subtrees == []:
            white_pieces = game.return_all_pieces_location('white')
            black_pieces = game.return_all_pieces_location('black')
            return (tree.move, len(white_pieces) - len(black_pieces))

        else:
            if game.is_white_move:
                best_move = (final_game.Move('', False), -inf)
                for subtree in tree.subtrees:
                    game_copy = game.make_copy_game()
                    game_copy.make_move(subtree.move)
                    potential_move = self.calc_best_move(game_copy, subtree, alpha, beta)
                    if potential_move[1] > best_move[1]:
                        best_move = potential_move
                    alpha = max(alpha, best_move[1])

                    if beta <= alpha:  # only returns the best move if the others will be bad
                        if tree.move.move == '':
                            return best_move
                        else:
                            return (tree.move, best_move[1])
                if tree.move.move == '':
                    return best_move
                else:
                    return (tree.move, best_move[1])

            else:
                best_move = (final_game.Move('', False), inf)
                for subtree in tree.subtrees:
                    game_copy = game.make_copy_game()
                    game_copy.make_move(subtree.move)
                    potential_move = self.calc_best_move(game_copy, subtree, alpha, beta)
                    if potential_move[1] < best_move[1]:
                        best_move = potential_move
                    beta = min(beta, best_move[1])

                    if beta <= alpha:  # only returns the best move if the others will be bad
                        if tree.move.move == '':
                            return best_move
                        else:
                            return (tree.move, best_move[1])
                if tree.move.move == '':
                    return best_move
                else:
                    return (tree.move, best_move[1])

    def update_tree(self, game: final_game.CheckersGame) -> None:
        """Updates the bot's subtree to reflect the game"""
        self.tree = generate_game_tree(self.tree_depth, game, final_game.Move('', False))


def generate_subtrees(game: final_game.CheckersGame, tree: CheckersGameTree) -> CheckersGameTree:
    """Generates subtrees for the given tree"""
    possible_moves = game.find_legal_moves()
    for possible_move in possible_moves:
        tree.subtrees.append(CheckersGameTree(possible_move, game.is_white_move))
    return tree


def generate_game_tree(depth: int, game: final_game.CheckersGame,
                       root: final_game.Move) -> CheckersGameTree:
    """Generates a complete game tree up to a maximum depth

    >>> d5_tree = generate_game_tree(5, final_game.CheckersGame(), final_game.Move('', False))
    """
    if depth == 0:
        self_tree = CheckersGameTree(root, game.is_white_move)
        return self_tree
    else:
        self_tree = CheckersGameTree(root, game.is_white_move)
        possible_moves = game.find_legal_moves()
        for possible_move in possible_moves:
            copy_game = game.make_copy_game()
            copy_game.make_move(possible_move)
            self_tree.subtrees.append(generate_game_tree(depth - 1, copy_game, possible_move))
        return self_tree


def print_trees(tree: CheckersGameTree, d: int = 1) -> None:
    """Print the entire tree given, with indents for subtrees"""
    print(tree.move.move)
    for st in tree.subtrees:
        for _ in range(0, d):
            print('  ', end='')
        print_trees(st, d + 1)


def run_game(white: Optional[Bot], black: Optional[Bot],
             cg: final_game.CheckersGame = None, fps: int = 10) -> None:
    """Runs the game based on how many human players that there are and what colour they play.
    Also removes the option to move pieces when a bot is playing

    >>> run_game(None, None)
    """
    if cg is None:
        cg = final_game.CheckersGame()
    if white is None and black is None:
        final_display.begin_display()
        highlight = []
        while True:
            highlight = final_display.update_display(cg, highlight)
            sleep(1 / fps)
    elif white is None:
        final_display.begin_display()
        highlight = []
        while True:
            if not cg.is_white_move and cg.gamestate == 'GAME':
                black.make_move(cg)
                highlight = []
            highlight = final_display.update_display(cg, highlight)
            sleep(1 / fps)
    elif black is None:
        final_display.begin_display()
        highlight = []
        while True:
            if cg.is_white_move and cg.gamestate == 'GAME':
                white.make_move(cg)
                highlight = []
            highlight = final_display.update_display(cg, highlight)
            sleep(1 / fps)
    else:
        final_display.begin_display()
        highlight = []
        while True:
            final_display.update_display(cg, highlight)
            if cg.is_white_move and cg.gamestate == 'GAME':
                white.make_move(cg)
            elif not cg.is_white_move and cg.gamestate == 'GAME':
                black.make_move(cg)
            sleep(1 / fps)


def export_tree(filename: str, tree: CheckersGameTree) -> None:
    """Exports the given subtree into a .txt file.   Uses a format of where the move is followed by
    two numbers representing true or false for turn and piece captured, and then a comma an another
     number representative of the number of subtrees that tree has. For example,
    '223101,7' is the move of 2, 2 to 3, 1, where no pieces are taken, it's white's turn
     and this move has 7 subtrees.

    >>> my_tree = CheckersGameTree(final_game.Move('2231', False), True)
    >>> export_tree('my_tree', my_tree)
    """
    file = open(filename + '.txt', mode='a')
    file.write(tree.move.move)  # write actual move

    if tree.move.piece_captured:  # writes 1 or 0 based on if a piece was captured
        file.write('1')
    else:
        file.write('0')

    if tree.white_turn:  # writes 1 or 0 based on if it is white's move
        file.write('1')
    else:
        file.write('0')

    file.write(',' + str(len(tree.subtrees)) + '\n')

    for subtree in tree.subtrees:
        export_tree(filename, subtree)


def import_tree(filename: str) -> CheckersGameTree:
    """Imports a file based on the format described in the export_tree function.
    Do not include the .txt in the name, as it is added on later

    >>> cg = import_tree('tree1')
    """
    all_tree_nodes = []
    file = open(filename + '.txt', mode='r')
    for row in file:
        all_tree_nodes.append(row.split(','))

    all_tree_nodes.reverse()

    final_tree = import_compile(all_tree_nodes)

    return final_tree[0]


def import_compile(imported_data: list[list[str, int]]) -> (CheckersGameTree, int):
    """Helper function for import_tree that recursively complies the import data"""
    root_tree = CheckersGameTree(final_game.Move(imported_data[0][0][0:-2],
                                                 bool(int(imported_data[0][0][-2]))),
                                 bool(int(imported_data[0][0][-1])))
    data_index = 1
    subtrees_added = 0
    while data_index < len(imported_data) and subtrees_added < int(imported_data[0][1]):
        if int(imported_data[data_index][1]) == 0:
            root_tree.subtrees.append(
                CheckersGameTree(final_game.Move(imported_data[data_index][0][0:-2],
                                                 bool(int(imported_data[data_index][0][-2]))),
                                 bool(int(imported_data[data_index][0][-1])))
            )
            subtrees_added += 1
            data_index += 1
        else:
            value_and_skip = import_compile(imported_data[data_index:])
            root_tree.subtrees.append(value_and_skip[0])
            data_index += value_and_skip[1]
            subtrees_added += 1
    return (root_tree, data_index)


# if __name__ == '__main__':
#     import python_ta
#     python_ta.check_all(config={
#         'extra-imports': ['math', 'typing', 'time', 'final_game', 'final_display', 'random'],
#         'allowed-io': ['import_tree', 'export_tree', 'print_trees'],
#         'max-line-length': 100,
#         'disable': ['R0912', 'R1702', 'E1136']
#     })
