import pygame
import sys
from src.game.game import Game
from src.ui.game_window import GameWindow
from src.network.server import GameServer
from src.network.client import GameClient
import threading

def main():
    game_window = GameWindow()
    game = Game()
    client = None
    server = None
    
    running = True
    current_screen = 'main'
    
    while running:
        if current_screen == 'main':
            result = game_window.handle_events()
            if result == 'host':
                # Démarrer le serveur
                server = GameServer()
                server_thread = threading.Thread(target=server.start)
                server_thread.start()
                
                # Se connecter en tant qu'hôte
                client = GameClient()
                if client.connect():
                    game_window.is_host = True
                    game_window.is_connected = True
                    game_window.player_name = "Joueur 1"
                    current_screen = 'waiting'
                
            elif result == 'join':
                # Se connecter au serveur
                client = GameClient()
                if client.connect():
                    game_window.is_connected = True
                    game_window.player_name = "Joueur 2"
                    current_screen = 'game'
                
            elif not result:  # Si False, quitter le jeu
                running = False
            
            game_window.clear()
            game_window.draw_main_menu()
            
        elif current_screen == 'waiting':
            result = game_window.handle_events()
            if not result:  # Si False, quitter le jeu
                running = False
            
            game_window.clear()
            # Afficher un message d'attente
            font = pygame.font.Font(None, 74)
            text = font.render("En attente d'un autre joueur...", True, game_window.WHITE)
            text_rect = text.get_rect(center=(game_window.width/2, game_window.height/2))
            game_window.screen.blit(text, text_rect)
            
            # Si un deuxième joueur se connecte, passer à l'écran de jeu
            if server and len(server.clients) == 2:
                current_screen = 'game'
            
        elif current_screen == 'game':
            result = game_window.handle_events()
            if not result:  # Si False, quitter le jeu
                running = False
            
            game_window.clear()
            game_window.draw_game_board()
        
        game_window.update()

    # Nettoyage
    if client:
        client.client.close()
    if server:
        server.server.close()
    pygame.quit()

if __name__ == '__main__':
    main()
