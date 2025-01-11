import socket
import threading
import json

def get_local_ip():
    """Obtient l'adresse IP locale de la machine"""
    try:
        # Crée une connexion temporaire pour obtenir l'IP locale
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

class GameServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(2)  # Maximum 2 joueurs
        self.clients = []
        self.game_state = {}
        self.local_ip = get_local_ip()
        print(f"Serveur démarré sur {self.local_ip}:{port}")

    def handle_client(self, client, addr):
        """Gère la connexion avec un client"""
        player_id = len(self.clients)
        self.clients.append(client)
        print(f"Joueur {player_id + 1} connecté depuis {addr}")

        while True:
            try:
                message = client.recv(1024).decode()
                if not message:
                    break

                data = json.loads(message)
                if data['type'] == 'shot':
                    # Transmettre le tir à l'autre joueur
                    target_player = 0 if player_id == 1 else 1
                    if target_player < len(self.clients):
                        shot_data = {
                            'type': 'shot',
                            'x': data['x'],
                            'y': data['y'],
                            'from_player': player_id
                        }
                        self.clients[target_player].send(json.dumps(shot_data).encode())

                elif data['type'] == 'shot_result':
                    # Transmettre le résultat du tir à l'autre joueur
                    target_player = 0 if player_id == 1 else 1
                    if target_player < len(self.clients):
                        result_data = {
                            'type': 'shot_result',
                            'hit': data['hit'],
                            'sunk': data['sunk'],
                            'x': data['x'],
                            'y': data['y']
                        }
                        self.clients[target_player].send(json.dumps(result_data).encode())

            except:
                break

        # Nettoyer la connexion
        print(f"Joueur {player_id + 1} déconnecté")
        if client in self.clients:
            self.clients.remove(client)
        client.close()

    def start(self):
        """Démarre le serveur et attend les connexions"""
        while len(self.clients) < 2:
            client, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(client, addr))
            thread.start()

        print("Deux joueurs connectés, la partie peut commencer!")
