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
<body style="font-family: Arial; text-align: center; margin-top: 50px;">
    <h1>Suivi des Compteurs</h1>
    {% for id, val in compteurs.items() %}
        <div style="margin: 20px;">
            <h2>{{ id.upper() }} : <span id="{{ id }}">{{ val }}</span></h2>
            <button onclick="modifier('{{ id }}', 1)">Ajouter 1</button>
        </div>
    {% endfor %}
    <script>
        function modifier(id, val) {
            fetch('/update', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({id: id, val: val})
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById(id).innerText = data[id];
            });
        }
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


