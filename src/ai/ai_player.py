import random

class AIPlayer:
    def __init__(self):
        self.shots = set()  # Ensemble des tirs déjà effectués
        self.last_hit = None
        self.hunt_mode = False

    def get_shot(self, board_size=10):
        """Détermine les coordonnées du prochain tir"""
        if self.hunt_mode:
            # Mode chasse : cibler autour du dernier hit
            return self._hunt_target(board_size)
        else:
            # Mode recherche : tir aléatoire
            return self._random_shot(board_size)

    def _random_shot(self, board_size):
        """Génère un tir aléatoire sur une case non ciblée"""
        while True:
            x = random.randint(0, board_size - 1)
            y = random.randint(0, board_size - 1)
            if (x, y) not in self.shots:
                self.shots.add((x, y))
                return x, y

    def _hunt_target(self, board_size):
        """Cible les cases autour du dernier hit"""
        # À implémenter : logique de ciblage intelligent
        return self._random_shot(board_size)
