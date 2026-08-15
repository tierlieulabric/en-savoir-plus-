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
            <h4 id="site_nom_c1">Chargement...</h4>
            <h2><span id="site_val_c1">0</span></h2>
            <button onclick="modifierSite('c1', 1)">+1</button>
            <button onclick="modifierSite('c1', -1)">-1</button>
        </div>

        <div style="margin: 15px; padding: 10px; border: 1px solid #ddd; border-radius: 8px;">
            <h4 id="site_nom_c2">Chargement...</h4>
            <h2><span id="site_val_c2">0</span></h2>
            <button onclick="modifierSite('c2', 1)">+1</button>
            <button onclick="modifierSite('c2', -1)">-1</button>
        </div>

        <div style="margin: 15px; padding: 10px; border: 1px solid #ddd; border-radius: 8px;">
            <h4 id="site_nom_c3">Chargement...</h4>
            <h2><span id="site_val_c3">0</span></h2>
            <button onclick="modifierSite('c3', 1)">+1</button>
            <button onclick="modifierSite('c3', -1)">-1</button>
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


@app.route("/update", methods=["POST"])
def update():
  data = request.json
  cid = data.get("id")
  if cid in compteurs:
    compteurs[cid] += data.get("val", 0)
  return jsonify(compteurs)


@app.route("/data")
def data():
  return jsonify(compteurs)  # Pour récupérer les données en JSON


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)


