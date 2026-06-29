from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db_manager import execute_query

auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nom_complet = request.form.get('nom_complet')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role') # 'data_owner' ou 'analyst'
        
        if not nom_complet or not email or not password or not role:
            flash("Veuillez remplir tous les champs obligatoires.", "danger")
            return redirect(url_for('auth.register'))
            
        # Vérifier si l'adresse email existe déjà dans le système
        user_check = execute_query("SELECT id FROM users WHERE email = %s", (email,), fetch=True)
        if user_check:
            flash("Cette adresse email est déjà enregistrée.", "warning")
            return redirect(url_for('auth.register'))
            
        # Hachage sécurisé du mot de passe
        password_hashed = generate_password_hash(password, method='scrypt')
        
        # Insertion du nouvel utilisateur en base de données
        query = """
            INSERT INTO users (nom_complet, email, password_hash, role) 
            VALUES (%s, %s, %s, %s)
        """
        try:
            execute_query(query, (nom_complet, email, password_hashed, role), commit=True)
            flash("Votre compte a été créé avec succès ! Vous pouvez vous connecter.", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash("Une erreur est survenue lors de l'enregistrement.", "danger")
            return redirect(url_for('auth.register'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Récupération de l'utilisateur
        query = "SELECT id, nom_complet, password_hash, role FROM users WHERE email = %s"
        user = execute_query(query, (email,), fetch=True)
        
        if user and check_password_hash(user[0]['password_hash'], password):
            # Stockage des variables essentielles dans la session Flask
            session['user_id'] = user[0]['id']
            session['user_name'] = user[0]['nom_complet']
            session['user_role'] = user[0]['role']
            
            flash(f"Ravi de vous revoir, {user[0]['nom_complet']} !", "success")
            return redirect(url_for('index'))
        else:
            flash("Identifiants incorrects. Veuillez réessayer.", "danger")
            return redirect(url_for('auth.login'))
            
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    # Nettoyage complet de la session
    session.clear()
    flash("Vous avez été déconnecté avec succès.", "info")
    return redirect(url_for('auth.login'))