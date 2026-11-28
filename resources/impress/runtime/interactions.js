(function () {
  "use strict";

  function initializeImageZoom() {
    const images = Array.from(document.querySelectorAll("img.zoomable-image[data-full-src]"));
    if (!images.length) return;

    const overlay = document.createElement("dialog");
    overlay.className = "image-zoom-overlay";
    overlay.setAttribute("aria-label", "图片预览");
    overlay.innerHTML = '<img alt="">';
    document.body.appendChild(overlay);

    const overlayImage = overlay.querySelector("img");
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    const duration = () => reducedMotion.matches ? 0 : 420;
    let activeSource = null;
    let isAnimating = false;
    let loadToken = 0;

    const frame = (rect) => ({
      left: `${rect.left}px`,
      top: `${rect.top}px`,
      width: `${rect.width}px`,
      height: `${rect.height}px`,
    });

    const setFrame = (rect) => Object.assign(overlayImage.style, frame(rect));

    const targetRect = (source, sourceRect) => {
      const padding = 54;
      const maxWidth = Math.max(240, window.innerWidth - padding * 2);
      const maxHeight = Math.max(180, window.innerHeight - padding * 2);
      const fullWidth = Number(source.dataset.fullWidth) || source.naturalWidth || sourceRect.width;
      const fullHeight = Number(source.dataset.fullHeight) || source.naturalHeight || sourceRect.height;
      const ratio = fullWidth > 0 && fullHeight > 0 ? fullWidth / fullHeight : 4 / 3;
      let width = maxWidth;
      let height = width / ratio;
      if (height > maxHeight) {
        height = maxHeight;
        width = height * ratio;
      }
      return {
        left: (window.innerWidth - width) / 2,
        top: (window.innerHeight - height) / 2,
        width,
        height,
      };
    };

    const animateFrame = (from, to, done) => {
      const milliseconds = duration();
      if (!milliseconds) {
        setFrame(to);
        done();
        return;
      }
      const animation = overlayImage.animate(
        [frame(from), frame(to)],
        { duration: milliseconds, easing: "cubic-bezier(0.22, 1, 0.36, 1)", fill: "forwards" }
      );
      animation.onfinish = () => {
        setFrame(to);
        done();
      };
      animation.oncancel = done;
    };

    const loadFullImage = async (source, token) => {
      const fullImage = new Image();
      fullImage.src = source.dataset.fullSrc;
      try {
        await fullImage.decode();
      } catch (_error) {
        return;
      }
      if (token === loadToken && activeSource === source && overlay.open) {
        overlayImage.src = fullImage.currentSrc || fullImage.src;
      }
    };

    const open = (source) => {
      if (isAnimating || overlay.open) return;
      const from = source.getBoundingClientRect();
      if (!from.width || !from.height) return;

      isAnimating = true;
      activeSource = source;
      loadToken += 1;
      overlayImage.src = source.currentSrc || source.src;
      overlayImage.alt = source.alt || "";
      document.body.classList.add("image-zoom-active");
      overlay.showModal();
      setFrame(from);
      requestAnimationFrame(() => {
        overlay.classList.add("is-visible");
        animateFrame(from, targetRect(source, from), () => {
          isAnimating = false;
        });
      });
      loadFullImage(source, loadToken);
    };

    const close = () => {
      if (isAnimating || !overlay.open || !activeSource) return;
      const source = activeSource;
      const from = overlayImage.getBoundingClientRect();
      const to = source.getBoundingClientRect();
      isAnimating = true;
      loadToken += 1;
      overlay.classList.remove("is-visible");
      animateFrame(from, to.width && to.height ? to : from, () => {
        overlay.close();
        overlayImage.removeAttribute("src");
        overlayImage.removeAttribute("style");
        overlayImage.alt = "";
        activeSource = null;
        document.body.classList.remove("image-zoom-active");
        isAnimating = false;
        source.focus({ preventScroll: true });
      });
    };

    images.forEach((image) => {
      image.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();
        open(image);
      });
      image.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          event.stopPropagation();
          open(image);
        }
      });
    });

    overlayImage.addEventListener("click", (event) => {
      event.preventDefault();
      event.stopPropagation();
      close();
    });
    overlay.addEventListener("click", (event) => {
      if (event.target === overlay) close();
    });
    overlay.addEventListener("cancel", (event) => {
      event.preventDefault();
      close();
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && overlay.open) close();
    });
  }

  function initializeCodeLineFocus() {
    const blocks = Array.from(document.querySelectorAll(".code-frame pre"));
    if (!blocks.length) return;

    let activeBlock = null;

    const clear = (block) => {
      if (!block) return;
      block.classList.remove("code-line-active");
      block.style.removeProperty("--active-line-top");
      block.style.removeProperty("--active-line-left");
      block.style.removeProperty("--active-line-height");
      block.style.removeProperty("--active-line-width");
      block.style.removeProperty("--active-line-number");
      delete block.dataset.activeLine;
      if (activeBlock === block) activeBlock = null;
    };

    blocks.forEach((block) => {
      block.addEventListener("click", (event) => {
        const code = block.querySelector("code");
        if (!code) return;

        const blockStyle = window.getComputedStyle(block);
        const codeStyle = window.getComputedStyle(code);
        const lineHeight = Number.parseFloat(codeStyle.lineHeight);
        const paddingTop = Number.parseFloat(blockStyle.paddingTop);
        const borderTop = Number.parseFloat(blockStyle.borderTopWidth);
        const rect = block.getBoundingClientRect();
        const scaleY = block.offsetHeight > 0 ? rect.height / block.offsetHeight : 1;
        const screenY = event.clientY - rect.top;
        const relativeY = screenY / scaleY + block.scrollTop - borderTop - paddingTop;
        const lineIndex = Math.floor(relativeY / lineHeight);
        const lineCount = code.textContent.split("\n").length;
        if (!Number.isFinite(lineHeight) || lineHeight <= 0 || lineIndex < 0 || lineIndex >= lineCount) return;

        event.stopPropagation();
        if (block.dataset.activeLine === String(lineIndex)) {
          clear(block);
          return;
        }
        clear(activeBlock);
        activeBlock = block;
        block.dataset.activeLine = String(lineIndex);
        block.style.setProperty("--active-line-top", `${paddingTop + lineIndex * lineHeight}px`);
        block.style.setProperty("--active-line-left", `${block.scrollLeft}px`);
        block.style.setProperty("--active-line-height", `${lineHeight}px`);
        block.style.setProperty("--active-line-width", `${block.scrollWidth}px`);
        block.style.setProperty("--active-line-number", `"${String(lineIndex + 1).padStart(2, "0")}"`);
        block.classList.add("code-line-active");
      });
      block.addEventListener("scroll", () => {
        if (block.classList.contains("code-line-active")) {
          block.style.setProperty("--active-line-left", `${block.scrollLeft}px`);
        }
      });
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") clear(activeBlock);
    });
  }

  function initializeMathFit() {
    const blocks = Array.from(document.querySelectorAll(".math-block"));
    if (!blocks.length) return;

    const baseSize = 40;
    const minimumSize = 30;
    let ready = false;

    const fitAll = () => {
      ready = true;
      blocks.forEach((block) => {
        block.style.setProperty("--math-fit-size", `${baseSize}px`);
        block.classList.remove("math-overflow");
      });
      requestAnimationFrame(() => {
        blocks.forEach((block) => {
          const math = block.querySelector("mjx-math");
          if (!math) return;
          const style = window.getComputedStyle(block);
          const padding = Number.parseFloat(style.paddingLeft) + Number.parseFloat(style.paddingRight);
          const availableWidth = Math.max(1, block.clientWidth - padding);
          const naturalWidth = Math.max(1, math.scrollWidth || math.offsetWidth);
          const fittedSize = Math.max(minimumSize, Math.min(baseSize, baseSize * availableWidth / naturalWidth));
          block.style.setProperty("--math-fit-size", `${fittedSize.toFixed(2)}px`);
          block.classList.toggle(
            "math-overflow",
            fittedSize === minimumSize && naturalWidth * minimumSize / baseSize > availableWidth
          );
        });
      });
    };

    const whenMathJaxIsReady = () => {
      if (window.MathJax && window.MathJax.startup && window.MathJax.startup.promise) {
        window.MathJax.startup.promise.then(fitAll);
      } else {
        fitAll();
      }
    };

    if (document.readyState === "complete") whenMathJaxIsReady();
    else window.addEventListener("load", whenMathJaxIsReady, { once: true });
    window.addEventListener("resize", () => {
      if (ready) fitAll();
    });
  }

  function initializeProgressiveReveal() {
    const items = Array.from(document.querySelectorAll(".substep"));
    if (!items.length) return;

    const sync = (root) => {
      const candidates = root && root.matches && root.matches(".substep")
        ? [root]
        : Array.from((root || document).querySelectorAll(".substep"));
      candidates.forEach((item) => {
        const hidden = !item.classList.contains("substep-visible");
        item.toggleAttribute("inert", hidden);
        if (hidden) item.setAttribute("aria-hidden", "true");
        else item.removeAttribute("aria-hidden");
      });
    };

    sync(document);
    ["impress:stepenter", "impress:substep:enter", "impress:substep:leave"].forEach((name) => {
      document.addEventListener(name, (event) => sync(event.target));
    });
  }


  if (window.hljs) {
    window.hljs.highlightAll();
  }

  function initializeSpatialNavigation(root) {
    const toolbar = document.getElementById("spatial-tools");
    const back = document.getElementById("spatial-return");
    if (!toolbar || !back) return;

    const overviewId = "spatial-overview";
    let focusDestination = "";
    let resume = null;
    root.addEventListener("click", (event) => {
      const entry = event.target.closest(".spatial-entry");
      if (!entry) return;
      back.setAttribute("href", `#${entry.closest(".step").id}`);
      focusDestination = overviewId;
    });
    toolbar.addEventListener("click", (event) => {
      const link = event.target.closest('a[href^="#"]');
      if (link) focusDestination = link.getAttribute("href").slice(1);
    });
    root.addEventListener("impress:stepleave", (event) => {
      if (event.detail.next.id === overviewId) {
        back.setAttribute("href", `#${event.target.id}`);
        resume = {
          step: event.target,
          revealed: Array.from(event.target.querySelectorAll(".substep-visible")),
          active: event.target.querySelector(".substep-active"),
        };
      }
    });
    document.addEventListener("impress:stepenter", (event) => {
      if (!resume || event.target.id === overviewId) return;
      if (event.target === resume.step) {
        resume.revealed.forEach((element) => element.classList.add("substep-visible"));
        resume.active?.classList.add("substep-active");
      }
      resume = null;
    });
    root.addEventListener("impress:stepenter", (event) => {
      const step = event.target;
      const moveFocus = step.id === focusDestination;
      focusDestination = "";
      if (!moveFocus) return;
      if (step.id === overviewId) {
        back.focus({ preventScroll: true });
      } else {
        step.tabIndex = -1;
        step.focus({ preventScroll: true });
      }
    });
  }

  function initializePresentation() {
    const root = document.getElementById("impress");
    if (!window.impress || !root) return;

    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    window.impress.addPreStepLeavePlugin((event) => {
      if (reducedMotion.matches) event.detail.transitionDuration = 0;
    });

    const syncFocus = (active) => {
      if (!active) return;
      root.querySelectorAll(".step").forEach((step) => {
        const inactive = step !== active;
        if (inactive && step.contains(document.activeElement)) document.activeElement.blur();
        step.toggleAttribute("inert", inactive);
        if (inactive) step.setAttribute("aria-hidden", "true");
        else step.removeAttribute("aria-hidden");
      });
    };
    root.addEventListener("impress:init", () => syncFocus(root.querySelector(".step.active")));
    root.addEventListener("impress:stepleave", (event) => syncFocus(event.detail.next));
    root.addEventListener("impress:stepenter", (event) => syncFocus(event.target));
    initializeSpatialNavigation(root);
    window.impress().init();
  }

  initializePresentation();
  initializeImageZoom();
  initializeCodeLineFocus();
  initializeMathFit();
  initializeProgressiveReveal();
})();
