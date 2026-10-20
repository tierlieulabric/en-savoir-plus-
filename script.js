// 1. Sélectionner tous les carrousels de la page
const allCarousels = document.querySelectorAll('.custom-carousel');

allCarousels.forEach((carousel) => {
    let currentIndex = 0;
    const slides = carousel.querySelectorAll('.carousel-slide');
    const dotsContainer = carousel.querySelector('.carousel-dots');

    // 2. Générer dynamiquement les points ronds selon le nombre d'images
    slides.forEach((_, index) => {
        const dot = document.createElement('span');
        dot.classList.add('dot');
        if (index === 0) dot.classList.add('active'); // Le premier point est actif au départ
        
        // Clic sur un point -> affiche l'image correspondante
        dot.addEventListener('click', () => {
            showSlide(index);
        });
        
        dotsContainer.appendChild(dot);
    });

    // Récupérer la liste des points fraîchement créés pour ce carrousel
    const dots = dotsContainer.querySelectorAll('.dot');

    // 3. Fonction pour changer de slide et mettre à jour le point actif
    function showSlide(index) {
        // Retirer la classe active de la slide et du point actuels
        slides[currentIndex].classList.remove('active');
        dots[currentIndex].classList.remove('active');
        
        // Mettre à jour l'index
        currentIndex = index;
        
        // Ajouter la classe active sur la nouvelle slide et le nouveau point
        slides[currentIndex].classList.add('active');
        dots[currentIndex].classList.add('active');
    }
});

