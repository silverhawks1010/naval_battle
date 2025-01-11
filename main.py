import pygame
import threading
from src.ui.game_window import GameWindow
from src.game.game import Game
from src.network.server import GameServer
from src.network.client import GameClient

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
                    game_window.init_game()  # Initialiser les plateaux et les bateaux
                    current_screen = 'waiting'
                
            elif result == 'join':
                current_screen = 'join'
                game_window.input_ip = ""  # Réinitialiser l'IP
                
            elif not result:  # Si False, quitter le jeu
                running = False
            
            game_window.clear()
            game_window.draw_main_menu()
            
        elif current_screen == 'waiting':
            result = game_window.handle_events()
            if not result:  # Si False, quitter le jeu
                running = False
            
            game_window.clear()
            game_window.draw_waiting_screen(server.local_ip)
            
            # Si un deuxième joueur se connecte, passer à l'écran de placement
            if server and len(server.clients) == 2:
                current_screen = 'placement'
                
        elif current_screen == 'join':
            result, ip = game_window.handle_join_events()
            if result == 'connect' and ip:
                # Se connecter au serveur avec l'IP saisie
                client = GameClient(ip)
                if client.connect():
                    game_window.is_connected = True
                    game_window.player_name = "Joueur 2"
                    game_window.init_game()  # Initialiser les plateaux et les bateaux
                    current_screen = 'placement'
                else:
                    # Gérer l'échec de connexion ici si nécessaire
                    pass
            elif result == 'return':
                current_screen = 'main'
            elif not result:  # Si False, quitter le jeu
                running = False
            
            game_window.clear()
            game_window.draw_join_screen()
            
        elif current_screen == 'placement':
            result = game_window.handle_placement_events()
            if not result:  # Si False, quitter le jeu
                running = False
            
            game_window.clear()
            game_window.draw_placement_screen()
            
            # Si tous les bateaux sont placés
            if game_window.all_ships_placed():
                current_screen = 'game'
        
        elif current_screen == 'game':
            result = game_window.handle_game_events()
            if not result:  # Si False, quitter le jeu
                running = False
            
            game_window.clear()
            game_window.draw_game_board()
            
            # Si tous les bateaux sont coulés
            if game_window.all_ships_sunk():
                current_screen = 'end'
        
        elif current_screen == 'end':
            result = game_window.handle_end_events()
            if not result:  # Si False, quitter le jeu
                running = False
            
            game_window.clear()
            game_window.draw_end_screen()
        
        game_window.update()

    # Nettoyage
    if client:
        client.client.close()
    if server:
        server.server.close()
    pygame.quit()

if __name__ == "__main__":
    main()
