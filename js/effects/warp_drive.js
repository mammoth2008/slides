(function () {
    // 1. Create Canvas
    const canvas = document.createElement('canvas');
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.zIndex = '-1';
    canvas.style.background = '#000000';
    canvas.style.pointerEvents = 'none';
    document.body.appendChild(canvas);

    const ctx = canvas.getContext('2d');
    let width, height, cx, cy;

    // 2. Star System
    const starCount = 1000;
    const stars = [];

    // Speed control
    let speed = 0.5;        // Current speed
    const baseSpeed = 0.5;  // Normal cruising speed
    const warpSpeed = 20.0; // Speed during transition

    function initStars() {
        stars.length = 0;
        for (let i = 0; i < starCount; i++) {
            stars.push({
                x: (Math.random() - 0.5) * width * 2, // Spread wider than screen
                y: (Math.random() - 0.5) * height * 2,
                z: Math.random() * width // Depth
            });
        }
    }

    function resize() {
        width = window.innerWidth;
        height = window.innerHeight;
        canvas.width = width;
        canvas.height = height;
        cx = width / 2;
        cy = height / 2;
        initStars();
    }

    // Initial setup
    resize();
    window.addEventListener('resize', resize);

    // 3. Animation Loop
    function animate() {
        // Clear with slight fade for trail effect (optional, but pure black is requested)
        // ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
        // ctx.fillRect(0, 0, width, height);

        // Or just clear for sharp dots
        ctx.fillStyle = '#000000';
        ctx.fillRect(0, 0, width, height);

        ctx.fillStyle = '#FFFFFF';

        for (let i = 0; i < starCount; i++) {
            const star = stars[i];

            // Move star towards viewer (decrease z)
            star.z -= speed;

            // Reset if passed viewer
            if (star.z <= 0) {
                star.z = width;
                star.x = (Math.random() - 0.5) * width * 2;
                star.y = (Math.random() - 0.5) * height * 2;
            }

            // Project 3D position to 2D
            // Perspective projection: x' = x / z * constant
            const k = 128.0 / star.z;
            const px = star.x * k + cx;
            const py = star.y * k + cy;

            // Draw star
            if (px >= 0 && px <= width && py >= 0 && py <= height) {
                // Size depends on closeness (k)
                const size = (1 - star.z / width) * 2.5;
                const alpha = (1 - star.z / width);

                ctx.globalAlpha = alpha;
                ctx.beginPath();
                ctx.arc(px, py, size < 0 ? 0 : size, 0, Math.PI * 2);
                ctx.fill();
            }
        }
        ctx.globalAlpha = 1.0;

        // Speed Decay Logic
        if (speed > baseSpeed) {
            speed *= 0.95;
            if (speed < baseSpeed) speed = baseSpeed;
        }

        requestAnimationFrame(animate);
    }

    animate();

    // 4. Impress.js Integration
    document.addEventListener('impress:stepleave', function () {
        speed = warpSpeed;
    });

})();
