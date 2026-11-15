(function () {
  "use strict";

  const modules = JSON.parse(document.getElementById("course-modules").textContent);
  const tabs = Array.from(document.querySelectorAll(".module-tab"));
  const panel = document.getElementById("module-panel");
  const lessons = document.getElementById("module-lessons");

  function selectModule(index) {
    const selected = modules[index];
    tabs.forEach((tab, tabIndex) => {
      tab.setAttribute("aria-selected", String(tabIndex === index));
      tab.tabIndex = tabIndex === index ? 0 : -1;
    });
    panel.setAttribute("aria-labelledby", tabs[index].id);
    const status = selected.lessons.length ? `${selected.lessons.length} 节课件` : "课件准备中";
    document.getElementById("module-label").textContent = `${selected.id} · ${status}`;
    document.getElementById("module-heading").textContent = selected.title;
    document.getElementById("module-purpose").textContent = selected.purpose;
    document.getElementById("module-evidence").textContent = selected.evidence;
    lessons.replaceChildren();

    selected.lessons.forEach((lesson) => {
      const link = document.createElement("a");
      link.className = "lesson-link";
      link.href = lesson.href;
      const number = document.createElement("span");
      number.textContent = lesson.number;
      const title = document.createElement("strong");
      title.textContent = lesson.title;
      const arrow = document.createElement("span");
      arrow.textContent = "→";
      arrow.setAttribute("aria-hidden", "true");
      link.append(number, title, arrow);
      lessons.append(link);
    });
    if (!selected.lessons.length) {
      const note = document.createElement("p");
      note.className = "empty";
      note.textContent = "本模块课件正在准备中。";
      lessons.append(note);
    }
  }

  tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => {
      selectModule(index);
      if (window.matchMedia("(max-width: 700px)").matches) {
        const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
        panel.scrollIntoView({ block: "start", behavior: reducedMotion ? "instant" : "smooth" });
      }
    });
    tab.addEventListener("keydown", (event) => {
      const movement = { ArrowRight: 1, ArrowLeft: -1, ArrowDown: 2, ArrowUp: -2 };
      let nextIndex;
      if (event.key === "Home") nextIndex = 0;
      else if (event.key === "End") nextIndex = tabs.length - 1;
      else if (event.key in movement) nextIndex = (index + movement[event.key] + tabs.length) % tabs.length;
      else return;
      event.preventDefault();
      selectModule(nextIndex);
      tabs[nextIndex].focus();
    });
  });
})();
