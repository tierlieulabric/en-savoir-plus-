import os
import json
from flask import Flask, render_template_string, request, jsonify  # type: ignore[import-not-found]

app = Flask(__name__)

FICHIER_SAVE = "sauvegarde.json"

# Structure par défaut avec ID, Nom et Valeur
STRUCTURE_DEFAUT = {
    "c1": {"nom": "Mon Compteur 1", "valeur": 0},
    "c2": {"nom": "Mon Compteur 2", "valeur": 0},
    "c3": {"nom": "Mon Compteur 3", "valeur": 0}
}

def charger_donnees():
    if os.path.exists(FICHIER_SAVE):
        try:
            with open(FICHIER_SAVE, "r") as f:
                data = json.load(f)
                # Vérification que le fichier a le nouveau format
                if "c1" in data and "nom" in data["c1"]:
                    return data
        except Exception:
            pass
    return STRUCTURE_DEFAUT

def sauvegarder_donnees():
    with open(FICHIER_SAVE, "w") as f:
        json.dump(compteurs, f)

compteurs = charger_donnees()

page_html = """
<!DOCTYPE html>
<html>

<head>
    <title>Mes Compteurs</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>

<body style="font-family: Arial; text-align: center; margin-top: 30px; background-color: #f4f4f9;">

    <!-- 1. L'affichage des compteurs sur votre site -->
    <div style="font-family: Arial; text-align: center; max-width: 400px; margin: auto;">
        <h3>Tableau de Bord</h3>

        <div style="margin: 15px; padding: 10px; border: 1px solid #ddd; border-radius: 8px;">
            <h4 id="site_nom_c1">J'adore</h4>
            <h2><span id="site_val_c1">0</span></h2>
            <button onclick="modifierSite('Jadore', 1)">+1</button>
            <button onclick="modifierSite('Jadore', -1)">-1</button>
        </div>

        <div style="margin: 15px; padding: 10px; border: 1px solid #ddd; border-radius: 8px;">
            <h4 id="site_nom_c2">J'aime</h4>
            <h2><span id="site_val_c2">0</span></h2>
            <button onclick="modifierSite('Jaime', 1)">+1</button>
            <button onclick="modifierSite('Jaime', -1)">-1</button>
        </div>

        <div style="margin: 15px; padding: 10px; border: 1px solid #ddd; border-radius: 8px;">
            <h4 id="site_nom_c3">J'aime pas</h4>
            <h2><span id="site_val_c3">0</span></h2>
            <button onclick="modifierSite('Jaime pas', 1)">+1</button>
            <button onclick="modifierSite('Jaime pas', -1)">-1</button>
        </div>
    </div>

    <!-- 2. Le script qui communique avec votre Python -->
    <script>
        // URL de votre serveur Python hébergé (sans le slash à la fin)
        const API_URL = "https://en-savoir-plus-2.onrender.com";

        // Charger les données dès l'ouverture de la page du site
        function chargerDonneesDuSite() {
            fetch(API_URL + "/data")
                .then(res => res.json())
                .then(data => actualiserDesign(data));
        }

        // Envoyer un +1 ou -1 depuis le site
        function modifierSite(id, val) {
            fetch(API_URL + "/update", {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id: id, action: 'add', val: val })
            })
                .then(res => res.json())
                .then(data => actualiserDesign(data));
        }

        // Mettre à jour le texte et les chiffres sur votre page
        function actualiserDesign(data) {
            for (let id in data) {
                let elVal = document.getElementById('site_val_' + id);
                let elNom = document.getElementById('site_nom_' + id);
                if (elVal) elVal.innerText = data[id].valeur;
                if (elNom) elNom.innerText = data[id].nom;
            }
        }

        // Lancement automatique au chargement de la page
        chargerDonneesDuSite();
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(page_html, compteurs=compteurs)

@app.route('/update', methods=['POST'])
def update():
    data = request.json
    action = data.get('action')
    cid = data.get('id')
    
    if action == 'reset_all':
        for key in compteurs:
            compteurs[key]["valeur"] = 0
    elif action == 'reset' and cid in compteurs:
        compteurs[cid]["valeur"] = 0
    elif action == 'add' and cid in compteurs:
        compteurs[cid]["valeur"] += data.get('val', 0)
    elif action == 'rename' and cid in compteurs:
        compteurs[cid]["nom"] = data.get('nouveau_nom')
        
    sauvegarder_donnees()
    return jsonify(compteurs)

@app.route("/data")
def data():
    return jsonify(compteurs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)