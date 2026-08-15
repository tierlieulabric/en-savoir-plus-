from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit

app = Flask(__name__)
# On active SocketIO pour connecter l'ordi et le téléphone en temps réel
socketio = SocketIO(app, cors_allowed_origins="*")

# Le compteur magique qui commence à 0
compteur = 0

# Le design et le bouton de votre site web
HTML_PAGE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mon Compteur Partagé</title>
    <!-- On charge l'outil Socket.IO pour le navigateur -->
    <script src="https://cloudflare.com"></script>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            text-align: center; 
            background-color: #f4f7f6;
            margin: 0;
            padding-top: 100px;
        }
        .container {
            background-color: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            display: inline-block;
        }
        h1 { color: #333; margin-bottom: 10px; }
        #chiffre { 
            font-size: 90px; 
            font-weight: bold; 
            color: #007BFF; 
            margin: 20px 0; 
        }
        button { 
            font-size: 22px; 
            padding: 15px 40px; 
            background-color: #28a745; 
            color: white; 
            border: none; 
            border-radius: 8px; 
            cursor: pointer;
            font-weight: bold;
            transition: 0.2s;
        }
        button:hover { background-color: #218838; }
        button:active { transform: scale(0.98); }
    </style>
</head>
<body>
    <div class="container">
        <h1>Compteur de mon site</h1>
        <div id="chiffre">{{ initial_val }}</div>
        <button onclick="clicBouton()">Ajouter +1</button>
    </div>

    <script>
        // Connexion magique en direct avec Flask
        var socket = io(http://10.0.0.6:5000);

        // Quand un appareil clique, tout le monde reçoit le nouveau chiffre ici
        socket.on('mise_a_jour', function(data) {
            document.getElementById('chiffre').innerText = data.valeur;
        });

        // Quand on clique sur le bouton, on envoie le signal à Flask
        function clicBouton() {
            socket.emit('clic_bouton');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    # Affiche la page web avec la valeur actuelle du compteur
    return render_template_string(HTML_PAGE, initial_val=compteur)

@socketio.on('clic_bouton')
def handle_click():
    global compteur
    compteur += 1 # On ajoute 1 au compteur général
    # On envoie le nouveau chiffre à TOUS les appareils connectés en même temps !
    emit('mise_a_jour', {'valeur': compteur}, broadcast=True)

if __name__ == '__main__':
    # host='0.0.0.0' permet à votre téléphone d'entrer sur le site de votre PC
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
