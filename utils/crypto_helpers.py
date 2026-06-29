import hmac
import hashlib
from config import Config

def anonymize_identifier(raw_data):
    """
    Transforme une donnée identifiable (Nom, CNI, Téléphone) en un jeton unique et irréversible.
    Si l'entrée est vide ou invalide, retourne None.
    """
    if not raw_data:
        return None
        
    # Nettoyage de base (enlever les espaces inutiles au début et à la fin et passage en minuscules)
    clean_data = str(raw_data).strip().lower()
    
    # Génération du hachage sécurisé à l'aide du sel de l'application
    secure_hash = hmac.new(
        Config.CRYPTO_SALT, 
        clean_data.encode('utf-8'), 
        hashlib.sha256
    ).hexdigest()
    
    return secure_hash

def mask_text_fallback(text, visible_chars=3):
    """
    Alternative visuelle pour l'affichage (ex: Masquer un email : elv***@domain.com)
    Utile pour les interfaces d'administration sans exposer la donnée brute.
    """
    if not text or len(text) <= visible_chars:
        return "***"
    return text[:visible_chars] + "***" + text[-visible_chars:]