"""The main program used to run my CSC111 final project

Copyright Nathan Wootton 2021"""
import final_game
import final_trees_and_bots
from time import sleep
from typing import Optional


def make_new_game() -> final_game.CheckersGame:
    """Makes a new checkers game

    >>> cg = make_new_game()
    """
    return final_game.CheckersGame()


def make_current_game_tree(depth: int, game: final_game.CheckersGame,
                           root: final_game.Move) -> final_trees_and_bots.CheckersGameTree:
    """Generates a game tree based on the current game state, up to a depth of
    the depth provided

    >>> new_game = make_new_game()
    >>> new_game.make_move(final_game.Move('2031', False))
    >>> new_game.make_move(final_game.Move('5140', False))
    >>> make_current_game_tree(5, new_game, final_game.Move('5140', False))
    """
    return final_trees_and_bots.generate_game_tree(depth, game, root)


def make_random_bot() -> final_trees_and_bots.RandomBot:
    """Returns a RandomBot bot

    >>> make_random_bot()
    """
    return final_trees_and_bots.RandomBot()


def make_minimax_bot(game: final_game.CheckersGame, depth: int)\
        -> final_trees_and_bots.MinimaxBot:
    """Returns a MinimaxBot bot with a depth as given.  Depths over 4 take noticeably more time,
    but 5 is recommended for the bot to play at it's best without sacrificing much time

    >>> make_minimax_bot(make_new_game(), 5)
    """
    return final_trees_and_bots.MinimaxBot(game, depth)


def make_prune_bot(game: final_game.CheckersGame, depth: int) \
        -> final_trees_and_bots.MinimaxPruneBot:
    """Returns a MinimaxBot bot with a depth as given.  Depths over 4 take noticeably more time,
    but 5 is recommended for the bot to play at it's best without sacrificing much time

    >>> make_prune_bot(make_new_game(), 5)
    """
    return final_trees_and_bots.MinimaxPruneBot(game, depth)


def print_tree(tree: final_trees_and_bots.CheckersGameTree) -> None:
    """Prints out the given game tree"""
    final_trees_and_bots.print_trees(tree)


def export_tree(filename: str, tree: final_trees_and_bots.CheckersGameTree) -> None:
    """Exports the given subtree into a .txt file.   Uses a format of where the move is followed by
    two numbers representing true or false for turn and piece captured, and then a comma an another
    number representative of the number of subtrees that tree has. For example,
    '223101,7' is the move of 2, 2 to 3, 1, where no pieces are taken, it's white's turn
    and this move has 7 subtrees.

    >>> cg = import_tree('tree1')
    """
    final_trees_and_bots.export_tree(filename, tree)


def import_tree(filename: str) -> final_trees_and_bots.CheckersGameTree:
    """Imports a tree from the file, that follow the format given in the
    project report, as well as by export_tree

    >>> my_tree = final_trees_and_bots.CheckersGameTree(final_game.Move('2231', False), True)
    >>> export_tree('my_tree', my_tree)
    """
    return final_trees_and_bots.import_tree(filename)


def run_game(white: Optional[final_trees_and_bots.Bot],
             black: Optional[final_trees_and_bots.Bot],
             game: final_game.CheckersGame = None, fps: int = 10) -> None:
    """Runs the game with the given setup.  Put white or black as None if
    that is a player playing instead of a bot

    >>> new_game = make_new_game()
    >>> white_bot = make_prune_bot(new_game)
    >>> run_game(white_bot, None, new_game, fps = 10)
    """
    final_trees_and_bots.run_game(white, black, game, fps)


#################################################
# Games To Run
#################################################

# # White Player vs Black Player:
# game = make_new_game()
# run_game(None, None, game)


# # White Player vs Black RandomBot:
# game = make_new_game()
# run_game(None, make_random_bot(), game)


# # White Player vs Black MinimaxBot:
# game = make_new_game()
# run_game(None, make_minimax_bot(game, 5), game)
# # Note: you can change the 5 in the bot to change the number of moves it looks ahead.
# # I wouldn't recommend anything over 5, as it takes too long.


# # White Player vs Black MinimaxPruneBot:
# game = make_new_game()
# run_game(None, make_prune_bot(game, 5), game)
# # Note: you can change the 5 in the bot to change the number of moves it looks ahead.
# # I wouldn't recommend anything over 5, as it takes too long.


# # White RandomBot vs Black Player:
# game = make_new_game()
# run_game(make_random_bot(), None, game)


# # White MinimaxBot vs Black Player:
# game = make_new_game()
# run_game(make_minimax_bot(game, 5), None, game)
# # Note: you can change the 5 in the bot to change the number of moves it looks ahead.
# # I wouldn't recommend anything over 5, as it takes too long.


# # White MinimaxPruneBot vs Black Player:
# game = make_new_game()
# run_game(make_prune_bot(game, 5), None, game)
# # Note: you can change the 5 in the bot to change the number of moves it looks ahead.
# # I wouldn't recommend anything over 5, as it takes too long.


# White RandomBot vs Black RandomBot:
# game = make_new_game()
# run_game(make_random_bot(), make_random_bot(), game)


# # White MinimaxBot vs Black MinimaxBot:
# game = make_new_game()
# run_game(make_minimax_bot(game, 5), make_minimax_bot(game, 5), game)
# # Note: you can change the 5 in the bot to change the number of moves it looks ahead.
# # I wouldn't recommend anything over 5, as it takes too long.


# # White MinimaxPruneBot vs Black MinimaxPruneBot:
# game = make_new_game()
# run_game(make_prune_bot(game, 5), make_prune_bot(game, 5), game)
# # Note: you can change the 5 in the bot to change the number of moves it looks ahead.
# # I wouldn't recommend anything over 5, as it takes too long.


# # White MinimaxPruneBot vs Black MinimaxBot:
# game = make_new_game()
# run_game(make_prune_bot(game, 5), make_minimax_bot(game, 5), game)
# # Note: you can change the 5 in the bot to change the number of moves it looks ahead.
# # I wouldn't recommend anything over 5, as it takes too long.


# # White MinimaxPruneBot vs Black RandomBot:
# game = make_new_game()
# run_game(make_prune_bot(game, 5), make_random_bot(), game)
# # Note: you can change the 5 in the bot to change the number of moves it looks ahead.
# # I wouldn't recommend anything over 5, as it takes too long.
