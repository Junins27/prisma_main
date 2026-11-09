import {failure, initialise, isAuthorised, json, saveState} from "./_lib.js";

const clean = (value, length) => typeof value === "string" ? value.trim().slice(0, length) : "";
const slugify = (value) => clean(value, 120).normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 120) || "case";
const mediaUrl = (key) => `/api/media/${key.split("/").map(encodeURIComponent).join("/")}`;
const numberInRange = (value, fallback, min, max) => {
  const number = Number(value);
  return Number.isFinite(number) ? Math.min(max, Math.max(min, Math.round(number))) : fallback;
};
const normaliseImages = (images) => {
  if (!Array.isArray(images)) return [];
  return images.slice(0, 5).map((image) => {
    const key = clean(image?.key, 300);
    if (!key || !/^cases\/[a-z0-9-]+\.(?:avif|jpe?g|png|webp)$/i.test(key)) return null;
    return {key, url: mediaUrl(key), alt: clean(image?.alt, 180), fit: image?.fit === "cover" ? "cover" : "contain", position_x: numberInRange(image?.position_x, 50, 0, 100), position_y: numberInRange(image?.position_y, 50, 0, 100), zoom: numberInRange(image?.zoom, 100, 100, 200)};
  }).filter(Boolean);
};
const normalise = (source, existing = {}) => {
  const item = {
    ...existing,
    front: ["marketing", "tecnologia"].includes(source.front) ? source.front : "",
    title: clean(source.title, 120), category: clean(source.category, 80), summary: clean(source.summary, 240),
    challenge: clean(source.challenge, 5000), solution: clean(source.solution, 5000), deliverables: clean(source.deliverables, 220),
    external_url: clean(source.external_url, 500), status: source.status === "published" ? "published" : "draft",
    featured: Boolean(source.featured), images: normaliseImages(source.images), updated_at: new Date().toISOString()
  };
  if (!item.front || !item.title || !item.category || !item.summary || !item.challenge || !item.solution || !item.deliverables) throw new Error("Preencha todos os campos obrigatórios do case.");
  if (item.external_url && !/^https:\/\//i.test(item.external_url)) throw new Error("O link externo precisa começar com https://.");
  return item;
};

export async function onRequest(context) {
  try {
    if (!(await isAuthorised(context.request, context.env))) return json({error: "Sessão expirada."}, 401);
    const state = await initialise(context.env);
    if (context.request.method === "GET") return json({cases: state.cases || []});
    const input = await context.request.json();
    if (context.request.method === "POST") {
      const item = normalise(input);
      let slug = slugify(item.title), suffix = 2;
      while ((state.cases || []).some((entry) => entry.slug === slug)) slug = `${slugify(item.title)}-${suffix++}`;
      item.slug = slug; item.created_at = new Date().toISOString();
      state.cases = [...(state.cases || []), item]; await saveState(context.env, state); return json({case: item}, 201);
    }
    if (context.request.method === "PUT") {
      const index = (state.cases || []).findIndex((entry) => entry.slug === input.slug);
      if (index < 0) return json({error: "Case não encontrado."}, 404);
      const item = normalise(input, state.cases[index]); state.cases[index] = item; await saveState(context.env, state); return json({case: item});
    }
    return json({error: "Método não permitido."}, 405);
  } catch (error) { return failure(error); }
}
