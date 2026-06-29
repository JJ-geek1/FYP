-- 1. Table des Utilisateurs (Gestion des Comptes et des Rôles)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom_complet VARCHAR(150) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(30) NOT NULL, -- 'data_owner' ou 'analyst'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Note pour Render (PostgreSQL) : Lors de l'exécution sur Render, 
-- le mot-clé 'AUTO_INCREMENT' sera automatiquement adapté en 'SERIAL' si tu utilises un outil de migration,
-- ou tu pourras remplacer 'INT AUTO_INCREMENT' par 'SERIAL' directement dans leur console.


-- 2. Table des Données Partagées (Stockage Anonymisé)
-- Aucun nom en clair, aucune CNI visible. Tout est haché avant l'insertion.
CREATE TABLE IF NOT EXISTS shared_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    identifiant_anonyme VARCHAR(64) NOT NULL, -- Contient le HMAC-SHA256 de la CNI
    nom_masque VARCHAR(64),                   -- Contient le HMAC-SHA256 du nom
    age INT NOT NULL,
    revenu DECIMAL(12, 2) NOT NULL,           -- Utilisé pour les calculs de moyennes
    categorie VARCHAR(100) NOT NULL,          -- Ex: 'Santé', 'Finance', 'Ressources Humaines'
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- 3. Table de Log d'Audit (Immutable Audit Trail)
-- Historique obligatoire pour surveiller les actions des analystes
CREATE TABLE IF NOT EXISTS data_access_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_user INT NOT NULL,
    requete_executee TEXT NOT NULL,           -- Description de la statistique demandée
    motif_acces TEXT NOT NULL,                -- Pourquoi l'analyste fait cette recherche
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE
);