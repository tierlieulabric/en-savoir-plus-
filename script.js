// 1. On sélectionne TOUS les boutons qui ont la classe "btn-action"
const boutons = document.querySelectorAll('.btn-action');

// 2. On parcourt la liste de ces boutons
boutons.forEach(bouton => {
    // 3. On écoute le clic sur CHAQUE bouton individuellement
    bouton.addEventListener('click', (e) => {
        // e.target représente le bouton précis qui vient d'être cliqué
        const boutonClique = e.target;

        // 4. On vérifie son texte actuel pour faire la bascule
        if (boutonClique.textContent.trim() === "Enregistrer") {
            boutonClique.textContent = "Réserver";

            // --- CODE DE LA NOTIFICATION ---
            // Remplacez 'mes-reservations-xyz' par le nom choisi dans votre application
            fetch('https://ntfy.sh/topolite42400', {
                method: 'POST',
                body: 'Quelqu\'un a cliqué sur Enregistrer !', // Le message de la notification
                headers: {
                    'Title': 'Nouvelle Réservation 🎉' // Le titre de la notification
                }
            })
                .then(response => console.log('Notification envoyée !'))
                .catch(error => console.error('Erreur:', error));
            // --------------------------------

        } else {
            // Optionnel : permet d'annuler et de revenir à "Enregistrer" si on re-clique
            boutonClique.textContent = "Enregistrer";
        }
    });
});
