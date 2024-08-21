document.addEventListener('DOMContentLoaded', function() {
    const slider = document.querySelector('.slider-container');
    const slides = document.querySelectorAll('.slide');
    let currentSlide = 0;

    function nextSlide() {
        currentSlide = (currentSlide + 1) % slides.length;
        slider.scrollTo({
            left: slides[currentSlide].offsetLeft,
            behavior: 'smooth'
        });
    }

    // Automatic sliding every 5 seconds
    setInterval(nextSlide, 3000);

    // Optional: Add manual navigation buttons
    const prevButton = document.createElement('button');
    prevButton.textContent = 'Previous';
    const nextButton = document.createElement('button');
    nextButton.textContent = 'Next';

    prevButton.addEventListener('click', () => {
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        slider.scrollTo({
            left: slides[currentSlide].offsetLeft,
            behavior: 'smooth'
        });
    });

    nextButton.addEventListener('click', nextSlide);

    slider.parentNode.insertBefore(prevButton, slider);
    slider.parentNode.insertBefore(nextButton, slider.nextSibling);
});
