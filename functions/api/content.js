import {failure, initialise, isAuthorised, json, saveState} from "./_lib.js";

const clean = (value, length) => typeof value === "string" ? value.trim().slice(0, length) : "";
const isUrl = (value) => !value || /^https:\/\//i.test(value);
const mediaUrl = (key) => `/api/media/${key.split("/").map(encodeURIComponent).join("/")}`;
const logo = (source) => {
  const key = clean(source?.key, 300);
  if (!key || !/^partners\/[a-z0-9-]+\.(?:avif|jpe?g|png|webp)$/i.test(key)) return null;
  return {key, url: mediaUrl(key)};
};
const testimonials = (items) => (Array.isArray(items) ? items : []).slice(0, 6).map((item, index) => ({id: `testimonial-${index + 1}`, quote: clean(item?.quote, 700), author: clean(item?.author, 100), role: clean(item?.role, 140), visible: Boolean(item?.visible)}));
const partners = (items) => (Array.isArray(items) ? items : []).slice(0, 12).map((item, index) => ({id: `partner-${index + 1}`, name: clean(item?.name, 100), url: clean(item?.url, 500), logo: logo(item?.logo), authorised: Boolean(item?.authorised)}));
const insights = (items) => (Array.isArray(items) ? items : []).slice(0, 6).map((item, index) => ({id: `insight-${index + 1}`, title: clean(item?.title, 140), category: clean(item?.category, 70), summary: clean(item?.summary, 400), url: clean(item?.url, 500), published_at: clean(item?.published_at, 10), visible: Boolean(item?.visible)}));

export async function onRequest(context) {
  try {
    if (!(await isAuthorised(context.request, context.env))) return json({error: "Sessão expirada."}, 401);
    const state = await initialise(context.env);
    if (context.request.method === "GET") return json({content: state.content});
    if (context.request.method !== "PUT") return json({error: "Método não permitido."}, 405);
    const input = await context.request.json();
    const content = {testimonials: testimonials(input.testimonials), partners: partners(input.partners), insights: insights(input.insights)};
    if ([...content.partners, ...content.insights].some((item) => !isUrl(item.url))) throw new Error("Links externos precisam começar com https://.");
    state.content = content;
    await saveState(context.env, state);
    return json({content});
  } catch (error) { return failure(error); }
}
