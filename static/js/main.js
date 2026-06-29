document.addEventListener('DOMContentLoaded', function() {
    
    // 1. GESTION DE LA DISPARITION DES ALERTES FLASH
    // Sélectionne toutes les alertes affichées à l'écran
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(function(alert) {
        // Après 5 secondes (5000 millisecondes), on applique une transition fluide
        setTimeout(function() {
            alert.style.transition = "opacity 0.6s ease, transform 0.6s ease";
            alert.style.opacity = "0";
            alert.style.transform = "translateY(-10px)";
            
            // On supprime définitivement l'élément du DOM une fois l'animation finie
            setTimeout(function() {
                alert.remove();
            }, 600);
        }, 5000);
    });

    // 2. DYNAMISME DU CURSEUR EPSILON (PANNEAU ANALYSTE)
    const epsilonSlider = document.getElementById('epsilon');
    const epsilonValueLabel = document.getElementById('epsilon-val');
    
    if (epsilonSlider && epsilonValueLabel) {
        epsilonSlider.addEventListener('input', function() {
            const val = parseFloat(this.value);
            epsilonValueLabel.innerText = val.toFixed(1);
            
            // Changement de couleur dynamique du texte selon le niveau de risque/bruit
            if (val <= 0.5) {
                epsilonValueLabel.style.color = "var(--success-color)"; // Vert : Protection forte
            } else if (val > 0.5 && val <= 1.2) {
                epsilonValueLabel.style.color = "var(--warning-color)"; // Orange : Équilibré
            } else {
                epsilonValueLabel.style.color = "var(--danger-color)";  // Rouge : Moins de bruit, risque accru
            }
        });
    }
});