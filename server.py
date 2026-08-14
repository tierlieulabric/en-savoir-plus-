import os
import json
import sys

try:
    from flask import Flask, render_template_string, request, jsonify
except ImportError as exc:
    print("Le paquet 'flask' est absent. Installez-le avec : pip install flask")
    sys.exit(1)

app = Flask(__name__)

FICHIER_SAVE = "sauvegarde.json"

# Structure par défaut avec ID, Nom et Valeur
STRUCTURE_DEFAUT = {
    "c1": {"nom": "Compteur 1", "valeur": 0},
    "c2": {"nom": "Compteur 2", "valeur": 0},
    "c3": {"nom": "Compteur 3", "valeur": 0}
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
<!doctype html>
<html lang="fr">
<head>
    <meta charset="utf-8">
    <title>Compteurs</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .counter { margin-bottom: 20px; padding: 12px; border: 1px solid #ddd; border-radius: 8px; }
        .counter h3 { margin: 0 0 8px; }
        .actions { margin-top: 8px; }
        button { margin-right: 6px; }
    </style>
</head>
<body>
    {% for cid, info in compteurs.items() %}
    <div class="counter" data-id="{{ cid }}">
        <h3>{{ info.nom }}</h3>
        <div>{{ info.valeur }}</div>
        <div class="actions">
            <button onclick="send('add', '{{ cid }}', 1)">+1</button>
            <button onclick="send('add', '{{ cid }}', -1)">-1</button>
            <button onclick="send('reset', '{{ cid }}')">Réinitialiser</button>
        </div>
    </div>
    {% endfor %}

    <script>
        function send(action, id, val = 0) {
            fetch('/update', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ action: action, id: id, val: val })
            })
            .then(response => response.json())
            .then(() => location.reload());
        }
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