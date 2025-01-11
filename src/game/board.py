class Board:
    def __init__(self, size=10):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.ships = []

    def place_ship(self, ship, x, y, horizontal=True):
        """Place a ship on the board"""
        pass

    def receive_shot(self, x, y):
        """Process a shot at coordinates (x,y)"""
        pass

    def is_game_over(self):
        """Check if all ships are sunk"""
        pass
