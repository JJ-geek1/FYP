import numpy as np
from decimal import Decimal

def add_laplacian_noise(true_value, epsilon, sensitivity):
    """
    Applique le mécanisme de Laplace pour garantir la Confidentialité Différentielle.
    """
    if true_value is None:
        return None
        
    # Sécurité : Éviter une division par zéro si un epsilon incorrect est fourni
    if epsilon <= 0:
        epsilon = 0.1
        
    # --- MODIFICATION ICI ---
    # Conversion explicite de true_value en float au cas où ce serait un Decimal
    # Cela évite le TypeError: unsupported operand type(s) for +: 'decimal.Decimal' and 'float'
    clean_value = float(true_value) if isinstance(true_value, Decimal) else float(true_value)
    
    # Calcul de l'échelle (scale) du bruit de Laplace : b = Sensibilité / Epsilon
    scale = float(sensitivity) / float(epsilon)
    
    # Génération du bruit basé sur la distribution de Laplace
    noise = np.random.laplace(0, scale)
    
    # Retourne la valeur modifiée par le bruit (arrondie pour rester réaliste)
    return round(clean_value + noise, 2)

def calculate_protected_average(sum_value, count_value, epsilon):
    """
    Calcule une moyenne de manière sécurisée en appliquant la confidentialité différentielle.
    """
    # Conversion des valeurs en float pour éviter les erreurs de type en amont
    sum_f = float(sum_value) if sum_value is not None else 0.0
    count_f = float(count_value) if count_value is not None else 0.0
    
    if count_f == 0:
        return 0.0
        
    real_avg = sum_f / count_f
    
    computed_sensitivity = 10.0 
    
    return add_laplacian_noise(real_avg, epsilon, computed_sensitivity)