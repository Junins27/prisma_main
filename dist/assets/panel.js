(() => {
    "use strict";

    const root = document.documentElement;
    const body = document.body;
    const themeMeta = document.querySelector("#theme-color-meta");
    const themeStatus = document.querySelector("[data-theme-status]");
    const themes = {
        golden: { color: "#13171B", label: "Golden Hour" },
        solar: { color: "#FFF6E0", label: "Solar Editorial" },
    };

    const setTheme = (theme, announce = false) => {
        if (!themes[theme]) return;
        root.dataset.theme = theme;
        document.querySelectorAll("[data-theme-choice]").forEach((button) => {
            button.setAttribute("aria-pressed", String(button.dataset.themeChoice === theme));
        });
        if (themeMeta) themeMeta.content = themes[theme].color;
        try { localStorage.setItem("prisma-theme", theme); } catch (error) { /* Cookie preserves the server preference. */ }
        document.cookie = `prisma_theme=${theme}; max-age=31536000; path=/; SameSite=Lax`;
        if (announce && themeStatus) themeStatus.textContent = `Versão ${themes[theme].label} ativada.`;
    };
    document.querySelectorAll("[data-theme-choice]").forEach((button) => button.addEventListener("click", () => setTheme(button.dataset.themeChoice, true)));
    setTheme(root.dataset.theme || "golden");

    const menuToggle = document.querySelector("[data-panel-menu-toggle]");
    const overlay = document.querySelector("[data-panel-overlay]");
    const closeMenu = () => {
        body.classList.remove("panel-menu-open");
        if (menuToggle) {
            menuToggle.setAttribute("aria-expanded", "false");
            menuToggle.querySelector(".visually-hidden").textContent = "Abrir menu do painel";
        }
    };
    if (menuToggle) menuToggle.addEventListener("click", () => {
        const opening = !body.classList.contains("panel-menu-open");
        body.classList.toggle("panel-menu-open", opening);
        menuToggle.setAttribute("aria-expanded", String(opening));
        menuToggle.querySelector(".visually-hidden").textContent = opening ? "Fechar menu do painel" : "Abrir menu do painel";
    });
    if (overlay) overlay.addEventListener("click", closeMenu);
    document.addEventListener("keydown", (event) => { if (event.key === "Escape") closeMenu(); });
    document.querySelectorAll(".panel-nav a").forEach((link) => link.addEventListener("click", closeMenu));

    const imageInput = document.querySelector("#id_image");
    const imageOutput = document.querySelector("[data-image-preview-output]");
    const imageEmpty = document.querySelector("[data-image-preview-empty]");
    if (imageInput && imageOutput && imageEmpty) imageInput.addEventListener("change", () => {
        const [file] = imageInput.files;
        if (!file) return;
        const reader = new FileReader();
        reader.addEventListener("load", () => {
            imageOutput.src = String(reader.result);
            imageOutput.hidden = false;
            imageEmpty.classList.add("is-hidden");
        });
        reader.readAsDataURL(file);
    });

    document.querySelectorAll("[data-count-for]").forEach((counter) => {
        const field = document.getElementById(counter.dataset.countFor);
        if (!field) return;
        const update = () => { counter.textContent = `${field.value.length} / ${field.maxLength}`; };
        field.addEventListener("input", update);
        update();
    });

    const titleField = document.querySelector("#id_title");
    const frontField = document.querySelector("#id_front");
    const statusField = document.querySelector("#id_status");
    const summaryTitle = document.querySelector("[data-summary-title]");
    const summaryFront = document.querySelector("[data-summary-front]");
    const summaryStatus = document.querySelector("[data-summary-status]");
    if (titleField && summaryTitle) {
        const updateTitle = () => { summaryTitle.textContent = titleField.value.trim() || "Case sem título"; };
        titleField.addEventListener("input", updateTitle); updateTitle();
    }
    if (frontField && summaryFront) {
        const updateFront = () => { summaryFront.textContent = frontField.selectedOptions[0]?.text || "Frente do case"; };
        frontField.addEventListener("change", updateFront); updateFront();
    }
    if (statusField && summaryStatus) {
        const updateStatus = () => { summaryStatus.textContent = statusField.selectedOptions[0]?.text || "Rascunho"; };
        statusField.addEventListener("change", updateStatus); updateStatus();
    }
    document.querySelectorAll("[data-dismiss-message]").forEach((button) => button.addEventListener("click", () => button.closest(".panel-message")?.remove()));
})();
