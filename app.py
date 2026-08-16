import os
import json
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_compteur_123!'

# Configuration stable pour Render avec Eventlet
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

FICHIER_SAUVEGARDE = "/tmp/sauvegarde.json"

def donnees_par_defaut():
    return {
        'compteur1': {'nom': 'Compteur A', 'valeur': 0},
        'compteur2': {'nom': 'Compteur B', 'valeur': 0},
        'compteur3': {'nom': 'Compteur C', 'valeur': 0}
    }

def charger_donnees():
    if os.path.exists(FICHIER_SAUVEGARDE):
        try:
            with open(FICHIER_SAUVEGARDE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return donnees_par_defaut()
    return donnees_par_defaut()

def sauvegarder_donnees():
    try:
        with open(FICHIER_SAUVEGARDE, "w", encoding="utf-8") as f:
            json.dump(compteurs, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print("Erreur de sauvegarde:", e)

compteurs = charger_donnees()

@app.route('/')
def index():
    return render_template('index.html', compteurs_initiaux=compteurs)

@socketio.on('connect')
def au_connecter():
    emit('mise_a_jour', compteurs)

@socketio.on('incrementer')
def au_incrementer(id_compteur):
    if id_compteur in compteurs:
        compteurs[id_compteur]['valeur'] += 1
        sauvegarder_donnees()
        emit('mise_a_jour', compteurs, broadcast=True)

@socketio.on('changer_nom')
def au_changer_nom(donnees):
    id_compteur = donnees.get('id')
    nouveau_nom = donnees.get('nom')
    if id_compteur in compteurs and nouveau_nom:
        compteurs[id_compteur]['nom'] = nouveau_nom
        sauvegarder_donnees()
        emit('mise_a_jour', compteurs, broadcast=True)

@socketio.on('remettre_a_zero')
def au_remettre_a_zero():
    for cle in compteurs:
        compteurs[cle]['valeur'] = 0
    sauvegarder_donnees()
    emit('mise_a_jour', compteurs, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
