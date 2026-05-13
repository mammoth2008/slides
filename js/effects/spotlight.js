(function () {
    // 1. Create Overlay Element
    const overlay = document.createElement('div');
    overlay.id = 'spotlight-overlay';
    Object.assign(overlay.style, {
        position: 'fixed',
        top: '0',
        left: '0',
        width: '100%',
        height: '100%',
        zIndex: '9999',
        pointerEvents: 'none', // Allow clicking through
        background: 'radial-gradient(circle 200px at var(--x, 50%) var(--y, 50%), transparent 0%, rgba(0,0,0,0.98) 20%)',
        opacity: '0',
        transition: 'opacity 0.5s',
        visibility: 'hidden' // Hide when opacity is 0 to avoid any interference
    });
    document.body.appendChild(overlay);

    // 2. Mouse Tracking
    document.addEventListener('mousemove', function (e) {
        if (!document.body.classList.contains('global-spotlight')) return;

        const x = e.clientX + 'px';
        const y = e.clientY + 'px';
        overlay.style.setProperty('--x', x);
        overlay.style.setProperty('--y', y);
    });

    // 3. Impress Integration
    document.addEventListener('impress:stepenter', function (e) {
        const step = e.target;

        if (step.classList.contains('spotlight-mode')) {
            document.body.classList.add('global-spotlight');
            overlay.style.visibility = 'visible';
            overlay.style.opacity = '1';
        } else {
            document.body.classList.remove('global-spotlight');
            overlay.style.opacity = '0';
            setTimeout(() => {
                if (!document.body.classList.contains('global-spotlight')) {
                    overlay.style.visibility = 'hidden';
                }
            }, 500);
        }
    });

})();
