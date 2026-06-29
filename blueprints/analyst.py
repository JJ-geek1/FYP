from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from database.db_manager import execute_query
from utils.privacy_engine import add_laplacian_noise

analyst_bp = Blueprint('analyst', __name__, template_folder='../templates/analyst')

@analyst_bp.route('/query', methods=['GET', 'POST'])
def query_dashboard():
    # Sécurité : Seuls les utilisateurs connectés avec le rôle 'analyst' ont accès
    if 'user_id' not in session or session.get('user_role') != 'analyst':
        flash("Accès refusé. Cette zone est réservée aux analystes autorisés.", "danger")
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        categorie = request.form.get('categorie')
        epsilon = float(request.form.get('epsilon', 0.5)) # Budget de confidentialité choisi sur le GUI
        motif_recherche = request.form.get('motif')
        
        if not categorie or not motif_recherche:
            flash("Veuillez sélectionner une catégorie et indiquer le motif de votre recherche.", "warning")
            return redirect(url_for('analyst.query_dashboard'))
            
        # 1. Requête SQL d'agrégation brute (Calcul interne caché)
        query_brute = """
            SELECT SUM(revenu) as total_revenu, COUNT(id) as total_count 
            FROM shared_records 
            WHERE categorie = %s
        """
        result = execute_query(query_brute, (categorie,), fetch=True)
        
        vrai_revenu_total = result[0]['total_revenu'] if result[0]['total_revenu'] else 0
        compte_reel = result[0]['total_count'] if result[0]['total_count'] else 0
        
        if compte_reel == 0:
            flash(f"Aucune donnée disponible pour la catégorie '{categorie}'.", "info")
            return redirect(url_for('analyst.query_dashboard'))
            
        # 2. Application du Bruit de Laplace (Sensibilité estimée pour le revenu = 50 000 XAF)
        # Plus l'epsilon est petit, plus le bruit ajouté est grand (protection maximale)
        revenu_total_protege = add_laplacian_noise(vrai_revenu_total, epsilon=epsilon, sensitivity=50000)
        compte_protege = add_laplacian_noise(compte_reel, epsilon=epsilon, sensitivity=1)
        
        # S'assurer que le compte ne devienne pas négatif à cause du bruit
        compte_protege = max(1, round(compte_protege))
        
        # Calcul de la moyenne finale bruitée
        moyenne_revenu_protegee = round(revenu_total_protege / compte_protege, 2)
        
        # 3. IMMUTABLE AUDIT TRAIL : Enregistrement de la requête pour contrôle de sécurité
        query_log = """
            INSERT INTO data_access_logs (id_user, requete_executee, motif_acces)
            VALUES (%s, %s, %s)
        """
        texte_log = f"Calcul Moyenne Revenu sur la catégorie '{categorie}' avec un Epsilon de {epsilon}."
        execute_query(query_log, (session['user_id'], texte_log, motif_recherche), commit=True)
        
        # Renvoyer les résultats protégés au template
        donnees_resultat = {
            "categorie": categorie,
            "epsilon_utilise": epsilon,
            "nombre_individus_floute": compte_protege,
            "moyenne_revenu_anonyme": moyenne_revenu_protegee
        }
        
        return render_template('results.html', res=donnees_resultat)
        
    return render_template('query.html')