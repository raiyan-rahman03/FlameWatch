window.addEventListener('load', () => {
    const loader = document.getElementById('loader');
    const content = document.getElementById('main');

    setTimeout(() => {
        loader.style.display = 'none';
        // content.style.display = 'block';
    }, 10000);
});
