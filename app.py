from flask import Flask, render_template, session
from config import Config
from blueprints.auth import auth_bp
from blueprints.data_owner import data_owner_bp
from blueprints.analyst import analyst_bp  # Importation du module Analyste

app = Flask(__name__)
app.config.from_object(Config)

# Enregistrement de tous les Blueprints applicatifs
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(data_owner_bp, url_prefix='/data-owner')
app.register_blueprint(analyst_bp, url_prefix='/analyst')

@app.route('/')
def index():
    # Détection de l'état de la session pour la page d'accueil globale
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)