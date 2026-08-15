from flask import Flask, jsonify, request, render_template_string  # type: ignore
from flask_cors import CORS  # type: ignore

app = Flask(__name__)
CORS(app)

# Valeurs de départ pour les trois compteurs
compteurs = {"c1": 0, "c2": 0, "c3": 0}

# Page web pour voir et modifier les compteurs
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


# Structure exacte que votre JavaScript attend
compteurs_data = {
    "c1": {"nom": "J'adore", "valeur": 0},
    "c2": {"nom": "J'aime", "valeur": 0},
    "c3": {"nom": "J'aime pas", "valeur": 0}
}


@app.route("/")
def index():
    return render_template_string(page_html)


@app.route("/data", methods=["GET"])
def data():
    return jsonify(compteurs_data)


@app.route("/update", methods=["POST"])
def update():
    req = request.get_json()
    id_compteur = req.get('id')
    valeur_a_ajouter = req.get('val', 0)
    
    # Correspondance entre le bouton HTML et la clé (c1, c2, c3)
    cle_map = {'Jadore': 'c1', 'Jaime': 'c2', 'Jaime pas': 'c3'}
    cle = cle_map.get(id_compteur)
    
    if cle in compteurs_data:
        compteurs_data[cle]['valeur'] += valeur_a_ajouter
    
    return jsonify(compteurs_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)