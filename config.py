import os

class Config:
    # Clé secrète Flask pour sécuriser les sessions
    SECRET_KEY = os.environ.get('SECRET_KEY', 'super_secret_key_royal_privacy_2026')
    
    # Sel cryptographique pour le hachage des données sensibles (Ex: CNI, Noms)
    CRYPTO_SALT = os.environ.get('CRYPTO_SALT', 'Cameroon_Cyber_Salt_2026_Secure_Token').encode('utf-8')
    
    # Détection automatique de la base de données (Render utilise DATABASE_URL)
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    # Configuration de repli si on est en local sur XAMPP
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_NAME = os.environ.get('DB_NAME', 'privacy_sharing_db')