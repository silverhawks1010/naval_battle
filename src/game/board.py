class Board:
    def __init__(self, size=10):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]  # 0: vide, 1: bateau, 2: tir manqué, 3: tir touché
        self.ships = []
        self.shots = set()  # Ensemble des tirs reçus (x, y)

    def is_valid_position(self, ship, x, y, horizontal=True):
        """Vérifie si le placement du bateau est valide"""
        # Vérifier si le bateau sort de la grille
        if horizontal:
            if x < 0 or x + ship.length > self.size or y < 0 or y >= self.size:
                return False
        else:
            if x < 0 or x >= self.size or y < 0 or y + ship.length > self.size:
                return False

        # Vérifier s'il y a collision avec d'autres bateaux
        for i in range(ship.length):
            check_x = x + (i if horizontal else 0)
            check_y = y + (0 if horizontal else i)
            if self.grid[check_y][check_x] == 1:  # Case déjà occupée
                return False

        return True

    def place_ship(self, ship, x, y, horizontal=True):
        """Place un bateau sur la grille"""
        if not self.is_valid_position(ship, x, y, horizontal):
            return False

        # Placer le bateau
        ship.position = []
        for i in range(ship.length):
            pos_x = x + (i if horizontal else 0)
            pos_y = y + (0 if horizontal else i)
            self.grid[pos_y][pos_x] = 1
            ship.position.append((pos_x, pos_y))

        self.ships.append(ship)
        return True

    def receive_shot(self, x, y):
        """Traite un tir aux coordonnées (x,y)"""
        if not (0 <= x < self.size and 0 <= y < self.size) or (x, y) in self.shots:
            return False, None

        self.shots.add((x, y))
        
        # Vérifier si un bateau est touché
        if self.grid[y][x] == 1:
            self.grid[y][x] = 3  # Marquer comme touché
            # Trouver le bateau touché
            for ship in self.ships:
                if (x, y) in ship.position:
                    ship.hit()
                    return True, ship.is_sunk()
        else:
            self.grid[y][x] = 2  # Marquer comme tir manqué
            return False, None

    def is_game_over(self):
        """Vérifie si tous les bateaux sont coulés"""
        return all(ship.is_sunk() for ship in self.ships)

    def get_ship_at(self, x, y):
        """Retourne le bateau à la position donnée, ou None"""
        for ship in self.ships:
            if (x, y) in ship.position:
                return ship
        return None
