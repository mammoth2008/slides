(function () {
    // Check dependencies
    if (typeof html2canvas === 'undefined') {
        console.warn('html2canvas not loaded, Particles effect disabled.');
        return;
    }

    const DISINTEGRATION_DURATION = 1500; // ms

    // Helper: Random range
    const random = (min, max) => Math.random() * (max - min) + min;

    // Core Disintegrate Function
    window.disintegrate = function (element, callback) {
        html2canvas(element, {
            backgroundColor: null, // Transparent background
            scale: 1 // Use 1:1 scale for performance
        }).then(originalCanvas => {
            // 1. Hide original element
            const originalVisibility = element.style.visibility;
            element.style.visibility = 'hidden';

            // 2. Create container for particles
            const container = document.createElement('div');
            container.style.position = 'absolute';
            container.style.top = element.offsetTop + 'px';
            container.style.left = element.offsetLeft + 'px';
            container.style.width = element.offsetWidth + 'px';
            container.style.height = element.offsetHeight + 'px';
            container.style.pointerEvents = 'none';
            container.style.zIndex = '1000';
            // Transform should match the element's transform if possible, 
            // but impress.js handles transforms on the step. 
            // Since we are inside the step (or replacing it visually), we might need to be careful.
            // Actually, if we append to the parent of the step (the canvas), we need to match transforms.
            // Easier: Append to the step itself? No, step is hidden.
            // Append to the step's parent (#impress) but position might be tricky due to 3D transforms.
            // Alternative: Append to the element's parent, but since element is hidden, it's fine.
            // Wait, impress steps have 3D transforms. If we create a div at offsetTop/Left, it is relative to the step's local space?
            // Yes, if we append to element.parentNode (the #impress div), it shares the same coordinate space *if* the step wasn't transformed?
            // No, each step has its own transform.
            // Best bet: Create the particle canvas inside the step element, then hide the *content* of the step, not the step itself.
            // But the user said "Hide original DOM element".
            // Let's try appending to the step element and hiding all other children.

            // Actually, html2canvas takes a snapshot.
            // Let's create a canvas that replaces the element visually.

            const ctx = originalCanvas.getContext('2d');
            const { width, height } = originalCanvas;

            // Create a new canvas for rendering particles
            const particleCanvas = document.createElement('canvas');
            particleCanvas.width = width;
            particleCanvas.height = height;
            particleCanvas.style.position = 'absolute';
            particleCanvas.style.top = '0';
            particleCanvas.style.left = '0';
            particleCanvas.style.width = '100%';
            particleCanvas.style.height = '100%';

            // If we append to 'element', and 'element' is hidden, this won't show.
            // So we should NOT hide 'element' completely, but maybe opacity=0?
            // But we want to show the particles.
            // Strategy: Append particleCanvas to element. Hide all other children of element.

            // Save original children display states
            const childrenStates = [];
            Array.from(element.children).forEach(child => {
                childrenStates.push({ node: child, display: child.style.display });
                child.style.display = 'none';
            });

            element.style.visibility = 'visible'; // Ensure container is visible
            element.appendChild(particleCanvas);

            const pCtx = particleCanvas.getContext('2d');

            // 3. Generate Particles
            // We'll divide the image into 32x32 chunks (or smaller for performance)
            // 32x32 might be too blocky. Let's try density based.
            const particleSize = 4; // 4x4 pixels
            const cols = Math.ceil(width / particleSize);
            const rows = Math.ceil(height / particleSize);
            const particles = [];

            for (let i = 0; i < cols; i++) {
                for (let j = 0; j < rows; j++) {
                    // Randomly skip some to create "dust" feel? No, keep all for full image.
                    // But maybe only create particles for non-transparent pixels.
                    const x = i * particleSize;
                    const y = j * particleSize;

                    // Get pixel data (expensive loop, optimize if needed)
                    // Better: Draw full image, then clear parts? No.
                    // Let's just create objects.

                    particles.push({
                        x: x,
                        y: y,
                        vx: random(-2, 2) - 10, // Move left/up mostly? User said "Top Left"
                        vy: random(-2, 2) - 10,
                        r: 0, // rotation
                        vr: random(-0.2, 0.2),
                        alpha: 1,
                        decay: random(0.01, 0.03)
                    });
                }
            }

            // Optimization: Draw the image chunks once?
            // Actually, drawing thousands of small rects from a source canvas is okay.

            let startTime = null;

            function animate(timestamp) {
                if (!startTime) startTime = timestamp;
                const progress = timestamp - startTime;

                pCtx.clearRect(0, 0, width, height);

                let activeParticles = 0;

                particles.forEach(p => {
                    if (p.alpha <= 0) return;
                    activeParticles++;

                    // Update
                    // "Left Top" drift: vx < 0, vy < 0
                    // Add some randomness
                    p.x += (Math.random() - 0.5) * 2 - 1; // Drift left
                    p.y += (Math.random() - 0.5) * 2 - 1; // Drift up

                    // User said "Random rotation and displacement (mostly top-left)"
                    p.x -= Math.random() * 2;
                    p.y -= Math.random() * 2;

                    p.r += p.vr;
                    p.alpha -= p.decay;

                    // Draw
                    pCtx.save();
                    pCtx.globalAlpha = p.alpha;
                    pCtx.translate(p.x + particleSize / 2, p.y + particleSize / 2);
                    pCtx.rotate(p.r);
                    // Draw chunk from original canvas
                    pCtx.drawImage(originalCanvas,
                        p.x, p.y, particleSize, particleSize,
                        -particleSize / 2, -particleSize / 2, particleSize, particleSize
                    );
                    pCtx.restore();
                });

                if (activeParticles > 0 && progress < DISINTEGRATION_DURATION) {
                    requestAnimationFrame(animate);
                } else {
                    // Done
                    if (callback) callback();
                    // Restore?
                    // element.removeChild(particleCanvas);
                    // Array.from(element.children).forEach((child, idx) => {
                    //     if (childrenStates[idx]) child.style.display = childrenStates[idx].display;
                    // });
                }
            }

            requestAnimationFrame(animate);
        });
    };

    // 4. Impress Integration
    let isDisintegrating = false;

    document.addEventListener('impress:stepleave', function (event) {
        const step = event.target;

        // Check for data-effect="snap"
        if (step.dataset.effect !== 'snap') return;

        // Avoid loop
        if (isDisintegrating) return;

        // Prevent default transition
        event.preventDefault();
        isDisintegrating = true;

        // Run Disintegration
        window.disintegrate(step, () => {
            // Animation Complete
            isDisintegrating = false;

            // Proceed to next step
            // We need to know where we were going. 
            // impress:stepleave event details might have 'next' step.
            // But impress.js API: api.next() triggers it.
            // If we just call api.next(), it will trigger stepleave again.
            // We need to bypass the check or temporarily remove the effect.

            // Hack: Remove the effect attribute temporarily?
            step.dataset.effect = 'snapped'; // Mark as done

            const api = impress();
            // Try to go to the next step that was intended.
            // event.detail.next is the next step element.
            if (event.detail && event.detail.next) {
                api.goto(event.detail.next);
            } else {
                api.next();
            }

            // Restore effect attribute after a delay (if we want to replay it later)
            setTimeout(() => {
                step.dataset.effect = 'snap';
                // Restore visibility? The step is now "left", so it's fine if it looks broken.
                // But if we go back, we might want it restored.
                // Ideally, we should restore DOM state when step is re-entered.
            }, 2000);
        });
    });

    // Restore step visibility on enter
    document.addEventListener('impress:stepenter', function (event) {
        const step = event.target;
        // If we messed up the DOM, restore it.
        // This requires saving state properly or just reloading content.
        // For now, let's assume simple restoration:
        const canvas = step.querySelector('canvas');
        if (canvas) {
            canvas.remove();
            Array.from(step.children).forEach(child => {
                child.style.display = ''; // Reset display
            });
        }
    });

})();
