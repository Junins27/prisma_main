(() => {
  "use strict";
  const seed = window.PRISMA_DATA;
  const escape = (value = "") => String(value).replace(/[&<>"']/g, (char) => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#039;"}[char]));
  const api = async (path, options) => {
    const response = await fetch(path, {headers: {"Content-Type":"application/json", ...(options?.headers || {})}, ...options});
    if (!response.ok) throw new Error("API indisponível");
    return response.json();
  };
  const card = (item) => `<article class="project-card${item.featured ? " project-card--featured" : ""}" data-reveal>
    <a class="project-visual" href="/case.html?slug=${encodeURIComponent(item.slug)}" aria-label="Ver case ${escape(item.title)}">${item.images?.[0] ? `<img src="${escape(item.images[0].url)}" alt="">` : '<div class="project-art" aria-hidden="true"><span></span><span></span><i></i></div>'}<span class="project-arrow" aria-hidden="true">↗</span></a>
    <div class="project-meta"><span>${escape(item.frontTitle || item.front)} · ${escape(item.category)}</span><span>Case autorizado</span></div>
    <h3><a href="/case.html?slug=${encodeURIComponent(item.slug)}">${escape(item.title)}</a></h3><p>${escape(item.summary)}</p></article>`;
  const placeholder = (front) => `<article class="project-card project-placeholder" data-reveal><div class="project-visual project-visual--placeholder project-visual--${front.slug}"><div class="project-art" aria-hidden="true"><span></span><span></span><i></i></div><span class="placeholder-badge">Espaço reservado</span></div><div class="project-meta"><span>${front.title}</span><span>Case em preparação</span></div><h3>Case de ${front.title}</h3><p>Este espaço receberá um case real e autorizado desta frente quando estiver pronto para publicação.</p></article>`;
  const reveal = (root = document) => root.querySelectorAll("[data-reveal]").forEach((element) => element.classList.add("is-visible"));
  async function loadCases() {
    let state = seed;
    try { state = await api("/api/site"); } catch (_) { /* O conteúdo inicial mantém o site disponível sem D1. */ }
    const cases = (state.cases || []).filter((item) => item.status === "published").map((item) => ({...item, frontTitle: seed.fronts.find((front) => front.slug === item.front)?.title || item.front}));
    document.querySelectorAll("[data-project-list]").forEach((container) => {
      const front = container.dataset.projectList;
      const filtered = front ? cases.filter((item) => item.front === front) : cases;
      container.innerHTML = filtered.length ? filtered.map(card).join("") : (front ? placeholder(seed.fronts.find((item) => item.slug === front)) : seed.fronts.map(placeholder).join(""));
      reveal(container);
    });
    applyContact(state.contact);
    return {state, cases};
  }
  function applyContact(contact = {}) {
    document.querySelector(".contact-copy")?.querySelectorAll(".contact-detail").forEach((element) => element.remove());
    const footer = document.querySelector(".footer-grid");
    footer?.querySelector("[data-footer-contact]")?.remove();
    if (!footer || !contact.email && !contact.phone && !contact.whatsapp && !contact.availability && !contact.location && !contact.instagram_url && !contact.linkedin_url) return;
    const icon = (name) => ({
      email: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18v12H3zM3 7l9 6 9-6"/></svg>',
      phone: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3h4l2 5-2.5 1.7a15 15 0 0 0 4.8 4.8L16 12l5 2v4c-10 1-16-5-15-15Z"/></svg>',
      whatsapp: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 11.5a8 8 0 0 1-11.8 7L4 20l1.5-4.2A8 8 0 1 1 20 11.5ZM9 8.2c.2 2 1.8 3.6 3.8 3.8l1-1.2 2 1c-1.2 2.2-5.5.8-7.2-1S5.3 4.8 7.5 3.7l1 2Z"/></svg>',
      pin: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s7-6.1 7-12a7 7 0 1 0-14 0c0 5.9 7 12 7 12Zm0-9.5a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5Z"/></svg>',
      clock: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8"/><path d="M12 7v5l3 2"/></svg>',
      link: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 15 15 9M8 18H6a4 4 0 0 1 0-8h3m7 4h2a4 4 0 0 0 0-8h-3"/></svg>'
    }[name]);
    const item = (type, label, value, href = "") => `<${href ? "a" : "span"} class="footer-contact__item" ${href ? `href="${escape(href)}" ${href.startsWith("http") ? 'target="_blank" rel="noopener"' : ""}` : ""}><i class="footer-contact__icon">${icon(type)}</i><span><small>${label}</small><strong>${escape(value)}</strong></span></${href ? "a" : "span"}>`;
    const whatsappDigits = String(contact.whatsapp || "").replace(/\D/g, "");
    const rows = [contact.email ? item("email", "E-mail", contact.email, `mailto:${contact.email}`) : "", contact.phone ? item("phone", "Telefone", contact.phone, `tel:${contact.phone.replace(/\D/g, "")}`) : "", contact.whatsapp ? item("whatsapp", "WhatsApp", contact.whatsapp, whatsappDigits ? `https://wa.me/${whatsappDigits}` : "") : "", contact.availability ? item("clock", "Atendimento", contact.availability) : "", contact.location ? item("pin", "Localização", contact.location) : "", contact.instagram_url ? item("link", "Instagram", "Acessar perfil", contact.instagram_url) : "", contact.linkedin_url ? item("link", "LinkedIn", "Acessar perfil", contact.linkedin_url) : ""].filter(Boolean).join("");
    footer.insertAdjacentHTML("beforeend", `<div class="footer-links footer-contact" data-footer-contact><p class="footer-label">Contato</p>${rows}</div>`);
  }
  function setCaseDetail(cases) {
    const target = document.querySelector("[data-case-detail]");
    if (!target) return;
    const slug = new URLSearchParams(location.search).get("slug");
    const item = cases.find((entry) => entry.slug === slug);
    if (!item) { target.innerHTML = '<section class="section"><div class="container"><h1>Case não encontrado</h1><p>Este case pode ainda não estar publicado.</p><a class="button" href="/">Voltar para a Prisma</a></div></section>'; return; }
    const front = seed.fronts.find((entry) => entry.slug === item.front);
    document.title = `${item.title} — Prisma`;
    const gallery = (item.images || []).length ? `<section class="section project-gallery-section"><div class="container"><div class="project-gallery-heading"><p class="detail-label">Galeria do projeto</p><p>${item.images.length} imagem(ns)</p></div><div class="project-gallery" tabindex="0">${item.images.map((image, index) => `<figure class="project-gallery__item"><img src="${escape(image.url)}" alt="${escape(image.alt || `${item.title} — imagem ${index + 1}`)}" loading="lazy"></figure>`).join("")}</div></div></section>` : "";
    target.innerHTML = `<article class="project-detail"><header class="project-detail-hero section"><div class="container"><a class="back-link" href="/frentes/${item.front}/#cases"><span aria-hidden="true">←</span> Voltar para ${escape(front?.title || item.front)}</a><div class="project-detail-heading"><div><p class="eyebrow"><span></span>${escape(front?.title || item.front)} · ${escape(item.category)}</p><h1>${escape(item.title)}</h1></div><p>${escape(item.summary)}</p></div><div class="project-detail-visual">${item.images?.[0] ? `<img src="${escape(item.images[0].url)}" alt="">` : '<div class="project-art project-art--large" aria-hidden="true"><span></span><span></span><i></i></div>'}</div></div></header>${gallery}<section class="section project-story"><div class="container project-story-grid"><aside><p class="detail-label">Entregáveis</p><ul>${String(item.deliverables || "").split(",").filter(Boolean).map((entry) => `<li>${escape(entry.trim())}</li>`).join("")}</ul>${item.external_url ? `<a class="button button--small" href="${escape(item.external_url)}" target="_blank" rel="noopener">Acessar <span>↗</span></a>` : ""}</aside><div class="project-story-copy"><section><p class="detail-label">O desafio</p><div class="rich-text"><p>${escape(item.challenge).replace(/\n/g,"<br>")}</p></div></section><section><p class="detail-label">A solução</p><div class="rich-text"><p>${escape(item.solution).replace(/\n/g,"<br>")}</p></div></section></div></div></section></article>`;
  }
  function wireContact() {
    const form = document.querySelector("[data-contact-form]");
    if (!form) return;
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const status = form.querySelector("[data-form-status]");
      const data = Object.fromEntries(new FormData(form));
      if (!data.privacy_consent) { status.textContent = "Confirme o consentimento para enviar."; return; }
      status.textContent = "Enviando…";
      try { await api("/api/contact", {method:"POST", body:JSON.stringify(data)}); form.reset(); status.textContent = "Mensagem recebida. Obrigado por compartilhar o contexto."; }
      catch (_) { status.textContent = "O envio ainda não está configurado. Tente novamente em breve."; }
    });
  }
  document.addEventListener("DOMContentLoaded", async () => { const {cases} = await loadCases(); setCaseDetail(cases); wireContact(); });
})();
