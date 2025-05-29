document.addEventListener('scroll', function() {
    const elements = document.querySelectorAll('#plot-container .fade-in:not(.animated)');
    const windowHeight = window.innerHeight || document.documentElement.clientHeight;
    elements.forEach(element => {
        const rect = element.getBoundingClientRect();
        if (rect.top <= windowHeight * 0.8 && rect.bottom >= 0) {
            console.log('Animating element:', element.textContent.substring(0, 20) + '...');
            element.classList.add('animated');
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const elements = document.querySelectorAll('#plot-container .fade-in:not(.animated)');
    const windowHeight = window.innerHeight || document.documentElement.clientHeight;
    elements.forEach(element => {
        const rect = element.getBoundingClientRect();
        if (rect.top <= windowHeight * 0.8 && rect.bottom >= 0) {
            console.log('Initial animating element:', element.textContent.substring(0, 20) + '...');
            element.classList.add('animated');
        }
    });
});