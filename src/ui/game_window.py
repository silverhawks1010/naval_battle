import pygame
import PIL.Image

class GameWindow:
    def __init__(self, width=800, height=600):
        pygame.init()
        pygame.mixer.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        pygame.display.set_caption("Bataille Navale - SilverHawks")
        
        # Couleurs
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 0, 255)
        self.RED = (255, 0, 0)
        self.GRAY = (128, 128, 128)
        self.GREEN = (34, 139, 34)
        self.BROWN = (119, 65, 39)

        # État du jeu
        self.is_host = False
        self.is_connected = False
        self.opponent_ready = False
        self.my_turn = False
        self.player_name = "Joueur 1"  # Par défaut
        
        # Configuration des boutons du menu principal
        self.buttons = {
            'host': {
                'text': 'Héberger',
                'color': self.BLUE,
                'action': None,
                'width': 200,
                'height': 50
            },
            'join': {
                'text': 'Rejoindre',
                'color': self.GREEN,
                'action': None,
                'width': 200,
                'height': 50
            },
            'quit': {
                'text': 'Quitter',
                'color': self.RED,
                'action': None,
                'width': 200,
                'height': 50
            }
        }

        pygame.mixer.music.load("assets/sound/background_sound.mp3")
        pygame.mixer.music.play(-1)  # Play the music in a loop

        # Charger les sons des boutons
        self.button_hover_sound = pygame.mixer.Sound("assets/sound/button_hover.wav")
        self.button_click_sound = pygame.mixer.Sound("assets/sound/button_click.wav")
        
        # Initialiser le dictionnaire des rectangles de boutons
        self.button_rects = {}
        self.current_hovered_button = None  # Pour suivre quel bouton est survolé

    def create_button(self, text, color, width, height, y_offset):
        """Crée un bouton centré horizontalement avec un décalage vertical"""
        x = (self.width - width) // 2
        y = (self.height // 2) + y_offset
        button_rect = pygame.Rect(x, y, width, height)
        
        # Dessiner le bouton
        pygame.draw.rect(self.screen, color, button_rect)
        pygame.draw.rect(self.screen, self.WHITE, button_rect, 2)
        
        # Ajouter le texte
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)
        
        return button_rect

    def draw_main_menu(self):
        """Dessine le menu principal"""
        # Charger et redimensionner le fond
        background = pygame.image.load("assets/images/main_menu.png")
        background = pygame.transform.scale(background, (self.width, self.height))

        # Charger et redimensionner le logo
        logo = pygame.image.load("assets/images/logo.png")
        logo_width = int(self.width * 0.13)  # 30% de la largeur de l'écran
        logo_height = int(logo_width * (logo.get_height() / logo.get_width()))
        logo = pygame.transform.scale(logo, (logo_width, logo_height))

        # Afficher le fond
        self.screen.blit(background, (0, 0))

        # Centrer le logo en haut
        logo_x = (self.width - logo_width) // 2
        logo_y = int(self.height * 0.16)  # 10% depuis le haut
        self.screen.blit(logo, (logo_x, logo_y))

        # Créer les boutons avec espacement
        button_spacing = 125  # Espacement vertical entre les boutons
        buttons_start_y = -50  # Position Y du premier bouton par rapport au centre

        # Créer et stocker les rectangles des boutons
        self.button_rects = {}
        for i, (key, button) in enumerate(self.buttons.items()):
            y_offset = buttons_start_y + (i * button_spacing)
            button_width, button_height = 442, 86  # Dimensions du bouton
            button_x = (self.width - button_width) // 2
            button_y = (self.height // 2) + y_offset
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

            # Charger et redimensionner l'image du bouton
            button_image = pygame.image.load("assets/images/button.png")
            button_image = pygame.transform.scale(button_image, (button_width, button_height))

            # Afficher le bouton
            self.screen.blit(button_image, (button_x, button_y))

            # Ajouter le texte sur le bouton
            font = pygame.font.Font("assets/fonts/PirataOne-Regular.ttf", 55)
            text_surface = font.render(button['text'], True, self.BROWN)
            text_rect = text_surface.get_rect(center=button_rect.center)
            text_rect.y -= 5
            self.screen.blit(text_surface, text_rect)

            # Stocker le rectangle du bouton pour la gestion des clics
            self.button_rects[key] = button_rect


    def draw_options_menu(self):
        """Dessine le menu des options"""
        # Charger et redimensionner le fond popup
        background = pygame.image.load("assets/images/popup.png")
        background = pygame.transform.scale(background, (self.width, self.height))
        
        # Afficher le fond
        self.screen.blit(background, (0, 0))
        
        # Réinitialiser les boutons pour le menu des options
        self.button_rects = {}
        
        # Position du bouton retour en bas
        button_width, button_height = 442, 86
        button_x = (self.width - button_width) // 2
        button_y = self.height*0.9  # Position en bas avec une marge
        return_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        
        # Charger et redimensionner l'image du bouton
        button_image = pygame.image.load("assets/images/button.png")
        button_image = pygame.transform.scale(button_image, (button_width, button_height))
        
        # Afficher le bouton
        self.screen.blit(button_image, (button_x, button_y))
        
        # Ajouter le texte sur le bouton
        font = pygame.font.Font("assets/fonts/PirataOne-Regular.ttf", 55)
        text_surface = font.render("Retour", True, self.BROWN)
        text_rect = text_surface.get_rect(center=return_rect.center)
        text_rect.y -= 5
        self.screen.blit(text_surface, text_rect)
        
        # Stocker le rectangle du bouton pour la gestion des clics
        self.button_rects['return'] = return_rect

    def draw_game_board(self):
        """Dessine le plateau de jeu"""
        # Charger et redimensionner le fond
        background = pygame.image.load("assets/images/gamebord.png")
        background = pygame.transform.scale(background, (self.width, self.height))
        
        # Afficher le fond
        self.screen.blit(background, (0, 0))
        
        # Afficher le nom du joueur
        font = pygame.font.Font("assets/fonts/PirataOne-Regular.ttf", 55)
        player_text = font.render(self.player_name, True, self.WHITE)
        text_rect = player_text.get_rect(center=(self.width/2, self.height*0.1))
        self.screen.blit(player_text, text_rect)
        
        # Réinitialiser les boutons pour le jeu
        self.button_rects = {}
        
        # Configuration de la grille
        grid_size = 10  # 10x10 cases
        cell_size = 75  # Taille de chaque case en pixels
        margin_left = self.width * 0.5 - grid_size * cell_size // 2  # Marge à gauche
        margin_top = self.height * 0.5 - grid_size * cell_size // 2   # Marge en haut
        grid_width = cell_size * grid_size
        grid_height = cell_size * grid_size
        
        # Police pour les coordonnées
        font = pygame.font.Font(None, 36)
        
        # Dessiner les lettres (A-J)
        letters = 'ABCDEFGHIJ'
        for i, letter in enumerate(letters):
            text = font.render(letter, True, self.WHITE)
            text_rect = text.get_rect()
            text_rect.center = (margin_left - 20, margin_top + i * cell_size + cell_size // 2)
            self.screen.blit(text, text_rect)
        
        # Dessiner les chiffres (1-10)
        for i in range(10):
            text = font.render(str(i + 1), True, self.WHITE)
            text_rect = text.get_rect()
            text_rect.center = (margin_left + i * cell_size + cell_size // 2, margin_top - 20)
            self.screen.blit(text, text_rect)
        
        # Dessiner la grille
        for i in range(grid_size + 1):
            # Lignes horizontales
            start_pos = (margin_left, margin_top + i * cell_size)
            end_pos = (margin_left + grid_width, margin_top + i * cell_size)
            pygame.draw.line(self.screen, self.WHITE, start_pos, end_pos, 1)
            
            # Lignes verticales
            start_pos = (margin_left + i * cell_size, margin_top)
            end_pos = (margin_left + i * cell_size, margin_top + grid_height)
            pygame.draw.line(self.screen, self.WHITE, start_pos, end_pos, 1)

    def draw_waiting_screen(self, server_ip):
        """Dessine l'écran d'attente avec l'IP du serveur"""
        # Charger et redimensionner le fond
        background = pygame.image.load("assets/images/gamebord.png")
        background = pygame.transform.scale(background, (self.width, self.height))
        self.screen.blit(background, (0, 0))
        
        # Afficher le message d'attente
        font = pygame.font.Font("assets/fonts/PirataOne-Regular.ttf", 55)
        text = font.render("En attente d'un autre joueur...", True, self.WHITE)
        text_rect = text.get_rect(center=(self.width/2, self.height*0.4))
        self.screen.blit(text, text_rect)
        
        # Afficher l'IP du serveur
        font_ip = pygame.font.Font("assets/fonts/PirataOne-Regular.ttf", 36)
        ip_text = font_ip.render(f"IP du serveur: {server_ip}", True, self.WHITE)
        ip_rect = ip_text.get_rect(center=(self.width/2, self.height*0.5))
        self.screen.blit(ip_text, ip_rect)

    def draw_join_screen(self):
        """Dessine l'écran de saisie d'IP"""
        # Charger et redimensionner le fond
        background = pygame.image.load("assets/images/gamebord.png")
        background = pygame.transform.scale(background, (self.width, self.height))
        self.screen.blit(background, (0, 0))
        
        # Réinitialiser les boutons
        self.button_rects = {}
        
        # Afficher le titre
        font = pygame.font.Font("assets/fonts/PirataOne-Regular.ttf", 55)
        text = font.render("Entrez l'IP du serveur", True, self.WHITE)
        text_rect = text.get_rect(center=(self.width/2, self.height*0.3))
        self.screen.blit(text, text_rect)
        
        # Afficher l'IP en cours de saisie
        if not hasattr(self, 'input_ip'):
            self.input_ip = ""
        
        input_font = pygame.font.Font("assets/fonts/PirataOne-Regular.ttf", 36)
        input_text = input_font.render(self.input_ip + "_", True, self.WHITE)
        input_rect = input_text.get_rect(center=(self.width/2, self.height*0.4))
        self.screen.blit(input_text, input_rect)
        
        # Dessiner le bouton de connexion
        button_width, button_height = 442, 86
        button_x = (self.width - button_width) // 2
        button_y = self.height * 0.6
        connect_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        
        # Charger et redimensionner l'image du bouton
        button_image = pygame.image.load("assets/images/button.png")
        button_image = pygame.transform.scale(button_image, (button_width, button_height))
        self.screen.blit(button_image, (button_x, button_y))
        
        # Ajouter le texte sur le bouton
        button_text = font.render("Connexion", True, self.BROWN)
        text_rect = button_text.get_rect(center=connect_rect.center)
        text_rect.y -= 5
        self.screen.blit(button_text, text_rect)
        
        self.button_rects['connect'] = connect_rect
        
        # Dessiner le bouton retour
        return_y = self.height * 0.8
        return_rect = pygame.Rect(button_x, return_y, button_width, button_height)
        self.screen.blit(button_image, (button_x, return_y))
        
        return_text = font.render("Retour", True, self.BROWN)
        text_rect = return_text.get_rect(center=return_rect.center)
        text_rect.y = return_y + button_height//2 - 5
        self.screen.blit(return_text, text_rect)
        
        self.button_rects['return'] = return_rect

    def handle_events(self):
        """Gère les événements du menu principal"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            # Gestion des clics
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    for key, rect in self.button_rects.items():
                        if rect.collidepoint(event.pos):
                            self.button_click_sound.play()
                            if key == 'quit':
                                return False
                            elif key == 'host':
                                return 'host'
                            elif key == 'join':
                                return 'join'
                            elif key == 'return':
                                return 'return'
        
        # Gestion du survol des boutons
        mouse_pos = pygame.mouse.get_pos()
        hovered_button = None
        
        # Vérifier quel bouton est survolé
        for key, button_rect in self.button_rects.items():
            if button_rect.collidepoint(mouse_pos):
                hovered_button = key
                break
        
        # Si on survole un nouveau bouton
        if hovered_button != self.current_hovered_button:
            if hovered_button is not None:  # Si on entre dans un bouton
                self.button_hover_sound.play()
            self.current_hovered_button = hovered_button
            
        return True

    def handle_click(self, pos):
        """Gère les clics sur les boutons du menu"""
        for key, rect in self.button_rects.items():
            if rect.collidepoint(pos) and self.buttons[key]['action']:
                self.buttons[key]['action']()

    def set_button_action(self, button_name, action):
        """Définit l'action à exécuter lorsqu'un bouton est cliqué"""
        if button_name in self.buttons:
            self.buttons[button_name]['action'] = action

    def draw_grid(self, x, y, cell_size, grid):
        """Dessine une grille de jeu"""
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                rect = pygame.Rect(
                    x + i * cell_size,
                    y + j * cell_size,
                    cell_size,
                    cell_size
                )
                pygame.draw.rect(self.screen, self.WHITE, rect, 1)

    def update(self):
        """Met à jour l'affichage"""
        pygame.display.flip()

    def clear(self):
        """Efface l'écran"""
        self.screen.fill((0, 0, 0))

    def handle_join_events(self):
        """Gère les événements de l'écran de saisie d'IP"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return ('connect', self.input_ip)
                elif event.key == pygame.K_BACKSPACE:
                    self.input_ip = self.input_ip[:-1]
                elif event.unicode.isprintable():
                    self.input_ip += event.unicode
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    for key, rect in self.button_rects.items():
                        if rect.collidepoint(event.pos):
                            self.button_click_sound.play()
                            if key == 'connect':
                                return ('connect', self.input_ip)
                            elif key == 'return':
                                self.input_ip = ""
                                return ('return', None)
        
        return ('continue', None)
