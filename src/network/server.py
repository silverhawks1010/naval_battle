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
        print(f"Joueur {player_id + 1} connecté depuis {addr}")

        while True:
            try:
                data = client.recv(2048).decode()
                if not data:
                    break

                # Décoder les données JSON reçues
                message = json.loads(data)
                
                # Envoyer les données à l'autre joueur
                other_client = self.clients[1 - player_id] if len(self.clients) > 1 else None
                if other_client:
                    other_client.send(json.dumps(message).encode())

            except:
                break

        print(f"Joueur {player_id + 1} déconnecté")
        if client in self.clients:
            self.clients.remove(client)
        client.close()

    def start(self):
        """Démarre le serveur et attend les connexions"""
        while len(self.clients) < 2:
            client, addr = self.server.accept()
            self.clients.append(client)
            thread = threading.Thread(target=self.handle_client, args=(client, addr))
            thread.start()

        print("Deux joueurs connectés, la partie peut commencer!")
