const carousel = document.getElementById('carousel');
const dots = document.querySelectorAll('.dot');

// 1. Détecter le clic sur un bouton rond
dots.forEach(dot => {
    dot.addEventListener('click', (e) => {
        const targetIndex = e.target.getAttribute('data-index');
        const width = carousel.offsetWidth;

        // Fait défiler le carrousel jusqu'à la bonne image
        carousel.scrollTo({
            left: targetIndex * width,
            behavior: 'smooth'
        });
    });
});

// 2. Mettre à jour le bouton actif quand le carrousel défile
carousel.addEventListener('scroll', () => {
    const width = carousel.offsetWidth;
    // Calcule l'index de l'image actuellement visible
    const currentIndex = Math.round(carousel.scrollLeft / width);

    // Aligne la classe "active" sur le bon bouton rond
    dots.forEach((dot, index) => {
        if (index === currentIndex) {
            dot.classList.add('active');
        } else {
            dot.classList.remove('active');
        }
    });
});
