import os
import mysql.connector
from config import Config

def get_db_connection():
    """Retourne une connexion active à la base de données (MySQL ou PostgreSQL)"""
    if Config.DATABASE_URL:
        # Configuration pour PostgreSQL sur Render
        import psycopg2
        from psycopg2.extras import RealDictCursor
        conn = psycopg2.connect(Config.DATABASE_URL)
        return conn
    else:
        # Configuration locale avec XAMPP (MySQL)
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        return conn

def execute_query(query, params=(), fetch=False, commit=False):
    """Fonction générique pour exécuter proprement les requêtes SQL"""
    conn = get_db_connection()
    # Utilisation de dictionary=True pour MySQL et RealDictCursor pour Postgres
    if Config.DATABASE_URL:
        import psycopg2.extras
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    else:
        cursor = conn.cursor(dictionary=True)
        
    try:
        cursor.execute(query, params)
        result = None
        if fetch:
            result = cursor.fetchall()
        if commit:
            conn.commit()
        return result
    except Exception as e:
        print(f" Erreur SQL : {e}")
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()