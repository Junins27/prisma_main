(() => {
    "use strict";

    const root = document.documentElement;
    const body = document.body;
    const themeMeta = document.querySelector("#theme-color-meta");
    const themeStatus = document.querySelector("[data-theme-status]");
    const themeMap = {
        golden: {
            slug: "golden-hour",
            label: "Golden Hour",
            color: "#13171B",
        },
        solar: {
            slug: "solar-editorial",
            label: "Solar Editorial",
            color: "#FFF6E0",
        },
    };

    const persistTheme = (theme) => {
        try {
            localStorage.setItem("prisma-theme", theme);
        } catch (error) {
            // Cookies ainda mantêm a preferência quando o armazenamento é bloqueado.
        }
        document.cookie = `prisma_theme=${theme}; max-age=31536000; path=/; SameSite=Lax`;
    };

    const updateThemeUrl = (theme) => {
        const config = themeMap[theme];
        const url = new URL(window.location.href);

        if (body.dataset.page === "home") {
            url.pathname = config.url || `/tema/${config.slug}/`;
            url.searchParams.delete("tema");
        } else {
            url.searchParams.set("tema", config.slug);
        }
        window.history.replaceState({ theme }, "", `${url.pathname}${url.search}${url.hash}`);
    };

    const applyTheme = (theme, { announce = false, updateUrl = false } = {}) => {
        if (!themeMap[theme]) return;
        root.dataset.theme = theme;
        document.querySelectorAll("[data-theme-choice]").forEach((button) => {
            button.setAttribute("aria-pressed", String(button.dataset.themeChoice === theme));
        });
        if (themeMeta) themeMeta.setAttribute("content", themeMap[theme].color);
        persistTheme(theme);
        if (updateUrl) updateThemeUrl(theme);
        if (announce && themeStatus) {
            themeStatus.textContent = `Versão visual ${themeMap[theme].label} ativada.`;
        }
    };

    document.querySelectorAll("[data-theme-choice]").forEach((button) => {
        themeMap[button.dataset.themeChoice].url = button.dataset.themeUrl;
        button.addEventListener("click", () => {
            applyTheme(button.dataset.themeChoice, { announce: true, updateUrl: true });
        });
    });
    applyTheme(root.dataset.theme);

    const header = document.querySelector("[data-site-header]");
    const navToggle = document.querySelector("[data-nav-toggle]");
    const nav = document.querySelector("[data-nav]");

    const closeNav = () => {
        if (!header || !navToggle) return;
        header.classList.remove("nav-open");
        navToggle.setAttribute("aria-expanded", "false");
        const label = navToggle.querySelector(".visually-hidden");
        if (label) label.textContent = "Abrir menu";
    };

    if (navToggle && header) {
        navToggle.addEventListener("click", () => {
            const open = !header.classList.contains("nav-open");
            header.classList.toggle("nav-open", open);
            navToggle.setAttribute("aria-expanded", String(open));
            const label = navToggle.querySelector(".visually-hidden");
            if (label) label.textContent = open ? "Fechar menu" : "Abrir menu";
        });
    }

    if (nav) {
        nav.querySelectorAll("a").forEach((link) => link.addEventListener("click", closeNav));
    }

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") closeNav();
    });

    const syncHeader = () => {
        if (header) header.classList.toggle("is-scrolled", window.scrollY > 16);
    };
    syncHeader();
    window.addEventListener("scroll", syncHeader, { passive: true });

    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const revealItems = document.querySelectorAll("[data-reveal]");
    if (reduceMotion || !("IntersectionObserver" in window)) {
        revealItems.forEach((item) => item.classList.add("is-visible"));
    } else {
        body.classList.add("reveal-ready");
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (!entry.isIntersecting) return;
                    entry.target.classList.add("is-visible");
                    observer.unobserve(entry.target);
                });
            },
            { rootMargin: "0px 0px -7%", threshold: 0.08 },
        );
        revealItems.forEach((item) => observer.observe(item));
    }

    const messageField = document.querySelector("#id_message");
    const characterCount = document.querySelector("[data-character-count]");
    const syncCharacterCount = () => {
        if (messageField && characterCount) {
            characterCount.textContent = `${messageField.value.length} / 3000`;
        }
    };
    if (messageField) messageField.addEventListener("input", syncCharacterCount);
    syncCharacterCount();

    document.querySelectorAll(".field--error").forEach((field, index) => {
        const control = field.querySelector("input, select, textarea");
        const error = field.querySelector(".field-error");
        if (!control || !error) return;
        if (!error.id) error.id = `field-error-${index + 1}`;
        control.setAttribute("aria-invalid", "true");
        control.setAttribute("aria-describedby", error.id);
    });

    document.querySelectorAll("[data-dismiss-message]").forEach((button) => {
        button.addEventListener("click", () => button.closest(".message")?.remove());
    });
})();
