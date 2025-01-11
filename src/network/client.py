import socket
import json
import threading

class GameClient:
    def __init__(self, host='localhost', port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.game_state = {}
        self.callback = None
        self.receive_thread = None

    def connect(self):
        """Se connecte au serveur"""
        try:
            self.client.settimeout(5)  # Timeout de 5 secondes pour la connexion
            self.client.connect((self.host, self.port))
            self.client.settimeout(None)  # Remettre le timeout par défaut
            
            # Démarrer le thread de réception
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.daemon = True
            self.receive_thread.start()
            
            return True
        except:
            return False

    def send_shot(self, x, y):
        """Envoie un tir au serveur"""
        message = {
            'type': 'shot',
            'x': x,
            'y': y
        }
        try:
            self.client.send(json.dumps(message).encode())
            return True
        except:
            return False

    def send_shot_result(self, x, y, hit, sunk):
        """Envoie le résultat d'un tir au serveur"""
        message = {
            'type': 'shot_result',
            'x': x,
            'y': y,
            'hit': hit,
            'sunk': sunk
        }
        try:
            self.client.send(json.dumps(message).encode())
            return True
        except:
            return False

    def set_callback(self, callback):
        """Définit la fonction de callback pour les messages reçus"""
        self.callback = callback

    def receive_messages(self):
        """Reçoit les messages du serveur"""
        while True:
            try:
                message = self.client.recv(1024).decode()
                if not message:
                    break

                data = json.loads(message)
                if self.callback:
                    self.callback(data)

            except:
                break

        self.client.close()
