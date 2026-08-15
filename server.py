import os
import json
from flask import Flask, render_template_string, request, jsonify  # type: ignore[import-not-found]

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
<!DOCTYPE html>
<html>
<head>
    <title>Mes Compteurs</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: Arial; text-align: center; margin-top: 30px; background-color: #f4f4f9;">
    <h1>Suivi des Compteurs</h1>
    
    {% for id, info in compteurs.items() %}
        <div style="margin: 20px; padding: 15px; border: 1px solid #ccc; background: white; border-radius: 8px; display: inline-block; min-width: 250px;">
            <!-- Zone du nom modifiable -->
            <div style="margin-bottom: 10px;">
                <span id="nom_{{ id }}" style="font-size: 20px; font-weight: bold; cursor: pointer; border-bottom: 1px dashed #666;" onclick="renommer('{{ id }}')">
                    {{ info.nom }}
                </span>
            </div>
            
            <h2><span id="val_{{ id }}">{{ info.valeur }}</span></h2>
            
            <button onclick="modifier('{{ id }}', 1)" style="padding: 8px 12px; font-size: 16px;">+1</button>
            <button onclick="modifier('{{ id }}', -1)" style="padding: 8px 12px; font-size: 16px;">-1</button>
            <button onclick="raz('{{ id }}')" style="padding: 8px 12px; font-size: 14px; background-color: #ffcccc; border-radius: 4px;">RAZ</button>
        </div>
    {% endfor %}
    
    <div style="margin-top: 40px;">
        <button onclick="razTout()" style="padding: 10px 20px; font-size: 16px; background-color: #ff4d4d; color: white; border: none; border-radius: 5px; cursor: pointer;">
            Tout remettre à zéro
        </button>
    </div>

    <script>
        function modifier(id, val) {
            envoyerRequete({id: id, action: 'add', val: val});
        }

        function raz(id) {
            let nom = document.getElementById('nom_' + id).innerText;
            if(confirm("Confirmer la remise à zéro de '" + nom + "' ?")) {
                envoyerRequete({id: id, action: 'reset'});
            }
        }

        function razTout() {
            if(confirm("Voulez-vous vraiment TOUT remettre à zéro ?")) {
                envoyerRequete({action: 'reset_all'});
            }
        }

        function renommer(id) {
            let elementNom = document.getElementById('nom_' + id);
            let ancienNom = elementNom.innerText;
            let nouveauNom = prompt("Entrez le nouveau nom :", b64DecodeUnicode(elementNom.dataset.raw || b64EncodeUnicode(ancienNom)));
            
            if (nouveauNom && nouveauNom.trim() !== "") {
                envoyerRequete({id: id, action: 'rename', nouveau_nom: nouveauNom.trim()});
            }
        }

        function envoyerRequete(data) {
            fetch('/update', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            })
            .then(res => res.json())
            .then(data => updateAffichage(data));
        }

        function updateAffichage(data) {
            for (let id in data) {
                let elVal = document.getElementById('val_' + id);
                let elNom = document.getElementById('nom_' + id);
                if(elVal) elVal.innerText = data[id].valeur;
                if(elNom) {
                    elNom.innerText = data[id].nom;
                    elNom.dataset.raw = b64EncodeUnicode(data[id].nom);
                }
            }
        }
        
        function b64EncodeUnicode(str) {
            return btoa(encodeURIComponent(str).replace(/%([0-9A-F]{2})/g, function(match, p1) {
                return String.fromCharCode('0x' + p1);
            }));
        }

        function b64DecodeUnicode(str) {
            return decodeURIComponent(atob(str).split('').map(function(c) {
                return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
            }).join(''));
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