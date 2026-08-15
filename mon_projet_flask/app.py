from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
# Configuration pour le temps réel
socketio = SocketIO(app, cors_allowed_origins="*")

# Notre compteur global
compteur = 0

@app.route('/')
def index():
    # Flask va chercher automatiquement le fichier index.html dans le dossier templates
    return render_template('index.html', initial_val=compteur)

@socketio.on('clic_bouton')
def handle_click():
    global compteur
    compteur += 1
    # On renvoie la mise à jour en direct à tout le monde
    emit('mise_a_jour', {'valeur': compteur}, broadcast=True)

if __name__ == '__main__':
    # Lancement sur le réseau local
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)