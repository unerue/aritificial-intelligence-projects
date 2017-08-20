import random
import math


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def custom_score(game, player):
    """The evaluation function learned in lecture that outputs a
    score equal to the difference in the number of moves available to the
    two players and add to empirical weight of opponent players.

    Parameters
    ----------
    game, player

    Returns
    -------
    float : The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(abs(own_moves) - 1.5*abs(opp_moves))

def custom_score_2(game, player):
    """This evaluation function that I earned idea from Euclidean distance.
    This is not consider direction but I want to find the distance between two points.

    Parameters
    ----------
    game, player

    Returns
    -------
    float : The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    y1, x1 = game.get_player_location(player)
    y2, x2 = game.get_player_location(game.get_opponent(player))

    return float(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))

def custom_score_3(game, player):
    """This evaluation function that handle in between my moves and
    opponent moves of centrality.

    Parameters
    ----------
    game, player

    Returns
    -------
    float : The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    w, h = game.width / 2., game.height / 2.
    own_y, own_x = game.get_player_location(player)
    opp_y, opp_x = game.get_player_location(game.get_opponent(player))

    return float((h - own_y)**2 + (w - opp_x)**2) + float((h - opp_y)**2 + (w - own_x)**2) # 71.4%



class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.
    ********************  DO NOT MODIFY THIS CLASS  ********************
    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)
    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.
    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    def get_move(self, game, time_left):
        self.time_left = time_left

        best_move = (-1, -1)

        try:
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass

    def min_value(self, game, depth):
        """def max_value(gameState):
               if terminal_test(gameState):
                  return -1  # by assumption 2
               v = float("-inf")
               for m in gameState.get_legal_moves():
                  v = max(v, min_value(gameState.forecast_move(m)))
               return v
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return self.score(game, self)

        legal_moves = game.get_legal_moves()
        if depth == 0:
            return self.score(game, self)

        value = float("inf")

        for move in legal_moves:
            next_move = game.forecast_move(move)
            value = min(value, self.max_value(next_move, depth-1))

        return value


    def max_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return self.score(game, self)

        legal_moves = game.get_legal_moves()
        if depth == 0:
            return self.score(game, self)

        value = float("-inf")

        for move in legal_moves:
            next_move = game.forecast_move(move)
            value = max(value, self.min_value(next_move, depth-1))

        return value

    def minimax(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return self.score(game, self)

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)

        return max(legal_moves, key=lambda move: self.min_value(game.forecast_move(move), depth-1))


class AlphaBetaPlayer(IsolationPlayer):
    def get_move(self, game, time_left):
        self.time_left = time_left

        best_move = (-1, -1)

        for depth in range(1, 100000):
            try:
                best_move = self.alphabeta(game, depth, alpha=float("-inf"), beta=float("inf"))
            except SearchTimeout:
                break

        return best_move

    def min_value(self, game, depth, alpha, beta):
        """def MAX-VALUE(state, alpha, beta):
                if TERMINAL-TEST(state) then return UTILITY(state)
                V := -inf
                for a in ACTIONS(state):
                    V := MAX(v, MIN-VALUE(result(state, a), alpha, beta))
                    if V >= beta then return v
                    alpha := MAX(alpha, V)
                return V
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return self.score(game, self)

        legal_moves = game.get_legal_moves()
        if len(legal_moves) == 0:
            return self.score(game, self)

        value = float("inf")

        for move in legal_moves:
            next_move = game.forecast_move(move)
            value = min(value, self.max_value(next_move, depth-1, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)

        return value

    def max_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            return self.score(game, self)

        legal_moves = game.get_legal_moves()
        if len(legal_moves) == 0:
            return self.score(game, self)

        value = float("-inf")

        for move in legal_moves:
            next_move = game.forecast_move(move)
            value = max(value, self.min_value(next_move, depth-1, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)

        return value



    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()

        if not legal_moves:
            return (-1, -1)

        if depth == 0:
            return (-1, -1)

        max_value = float("-inf")
        beta = float("inf")
        best_move = game.get_legal_moves()[0]

        for move in legal_moves:
            next_move = game.forecast_move(move)
            value = self.min_value(next_move, depth=depth-1, alpha=max_value, beta=beta)
            if value > max_value:
                best_move = move
                max_value = value
            alpha = max(alpha, value)

        return best_move
