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

    def connect(self):
        """Se connecte au serveur"""
        try:
            self.client.connect((self.host, self.port))
            return True
        except:
            return False

    def send_data(self, data):
        """Envoie des données au serveur"""
        try:
            self.client.send(json.dumps(data).encode())
            return True
        except:
            return False

    def receive_data(self):
        """Reçoit les données du serveur"""
        while True:
            try:
                data = self.client.recv(2048).decode()
                if not data:
                    break
                
                # Décoder les données JSON reçues
                message = json.loads(data)
                
                # Si un callback est défini, l'appeler avec les données reçues
                if self.callback:
                    self.callback(message)
                    
            except:
                break
        
        self.client.close()

    def start_receiving(self):
        """Démarre un thread pour recevoir les données"""
        receive_thread = threading.Thread(target=self.receive_data)
        receive_thread.start()

    def set_callback(self, callback):
        """Définit la fonction de callback pour les données reçues"""
        self.callback = callback
