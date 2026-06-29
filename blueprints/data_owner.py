from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database.db_manager import execute_query
from utils.crypto_helpers import anonymize_identifier

data_owner_bp = Blueprint('data_owner', __name__, template_folder='../templates/data_owner')

@data_owner_bp.route('/rules')
def view_rules():
    if 'user_id' not in session or session.get('user_role') != 'data_owner':
        flash("Accès refusé.", "danger")
        return redirect(url_for('auth.login'))
    return render_template('rules.html')

@data_owner_bp.route('/upload', methods=['GET', 'POST'])
def upload_record():
    # Sécurité : Vérifier si l'utilisateur est connecté et est bien un Data Owner
    if 'user_id' not in session or session.get('user_role') != 'data_owner':
        flash("Accès refusé. Cette zone est réservée aux propriétaires de données.", "danger")
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        # 1. Récupération des données brutes du formulaire
        nom_patient = request.form.get('nom_patient')
        cni_numero = request.form.get('cni')
        age = request.form.get('age')
        revenu_annuel = request.form.get('revenu')
        categorie_medicale = request.form.get('categorie')
        
        if not cni_numero or not age or not revenu_annuel:
            flash("Veuillez remplir les champs obligatoires (CNI, Âge, Revenu).", "warning")
            return redirect(url_for('data_owner.upload_record'))
            
        # 2. PRIVACY-PRESERVING : Anonymisation immédiate des identifiants (PII)
        # On ne stockera JAMAIS le vrai nom ni la vraie CNI en clair.
        cni_anonymisee = anonymize_identifier(cni_numero)
        nom_anonymise = anonymize_identifier(nom_patient) if nom_patient else None
        
        # 3. Insertion sécurisée dans la base de données
        query = """
            INSERT INTO shared_records (identifiant_anonyme, nom_masque, age, revenu, categorie)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (cni_anonymisee, nom_anonymise, int(age), float(revenu_annuel), categorie_medicale)
        
        try:
            execute_query(query, params, commit=True)
            flash("Données sécurisées, anonymisées et enregistrées avec succès !", "success")
            return redirect(url_for('data_owner.upload_record'))
        except Exception as e:
            flash("Une erreur est survenue lors de la protection des données.", "danger")
            return redirect(url_for('data_owner.upload_record'))

    # Si c'est un GET, on affiche le formulaire et l'historique des dépôts de l'organisation
    # (Pour l'affichage, on ne récupère que des données déjà anonymes)
    records = execute_query("SELECT id, identifiant_anonyme, age, categorie FROM shared_records ORDER BY id DESC LIMIT 10", fetch=True)
    
    return render_template('upload.html', records=records)