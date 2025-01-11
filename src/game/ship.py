class Ship:
    def __init__(self, length, name):
        self.length = length
        self.name = name
        self.hits = 0
        self.position = []  # Liste des coordonnées occupées par le navire

    def is_sunk(self):
        """Return True if the ship is sunk"""
        return self.hits >= self.length

    def hit(self):
        """Register a hit on the ship"""
        self.hits += 1
        return self.is_sunk()
