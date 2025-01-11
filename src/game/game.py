from .board import Board
from .ship import Ship

class Game:
    def __init__(self):
        self.player1_board = Board()
        self.player2_board = Board()
        self.current_player = 1
        self.game_over = False

    def switch_player(self):
        """Switch the current player"""
        self.current_player = 3 - self.current_player  # Alterne entre 1 et 2

    def play_turn(self, x, y):
        """Process a player's turn"""
        target_board = self.player2_board if self.current_player == 1 else self.player1_board
        hit = target_board.receive_shot(x, y)
        
        if target_board.is_game_over():
            self.game_over = True
            
        if not hit:
            self.switch_player()
            
        return hit
