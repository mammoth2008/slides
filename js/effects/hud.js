(function () {
    // Mouse Parallax & HUD Data
    document.addEventListener('mousemove', function (e) {
        const x = e.clientX;
        const y = e.clientY;
        const w = window.innerWidth;
        const h = window.innerHeight;

        // Calculate normalized coordinates (-1 to 1)
        const mx = (x / w) * 2 - 1;
        const my = (y / h) * 2 - 1;

        // Update CSS variables
        document.body.style.setProperty('--mx', mx.toFixed(4));
        document.body.style.setProperty('--my', my.toFixed(4));
    });
})();
