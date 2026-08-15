from flask import Flask, jsonify, request
try:
    from flask_cors import CORS  # type: ignore  # <-- OBLIGATOIRE POUR AUTORISER LA SAUVEGARDE VIA INTERNET
except ImportError:
    CORS = None

app = Flask(__name__)
if CORS:
    CORS(app) # <-- CETTE LIGNE OUVRE LA PORTE DU SERVEUR À VOTRE HTML

compteurs_data = {
    "c1": {"nom": "J'adore", "valeur": 0},
    "c2": {"nom": "J'aime", "valeur": 0},
    "c3": {"nom": "J'aime pas", "valeur": 0}
}

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(compteurs_data)

@app.route('/update', methods=['POST'])
def update_data():
    req = request.get_json()
    id_compteur = req.get('id') # Reçoit 'Jadore', 'Jaime' ou 'Jaime pas'
    valeur_a_ajouter = req.get('val') # Reçoit 1 ou -1
    
    # Faire le lien avec les cases de sauvegarde (c1, c2, c3)
    if id_compteur == 'Jadore':
        compteurs_data['c1']['valeur'] += valeur_a_ajouter
    elif id_compteur == 'Jaime':
        compteurs_data['c2']['valeur'] += valeur_a_ajouter
    elif id_compteur == 'Jaime pas':
        compteurs_data['c3']['valeur'] += valeur_a_ajouter
        
    return jsonify(compteurs_data)