import {failure, initialise, isAuthorised, json, saveState} from "./_lib.js";

const clean = (value, length) => typeof value === "string" ? value.trim().slice(0, length) : "";
const isUrl = (value) => !value || /^https:\/\//i.test(value);

const normaliseContact = (source) => ({
  email: clean(source.email, 254),
  phone: clean(source.phone, 80),
  whatsapp: clean(source.whatsapp, 80),
  availability: clean(source.availability, 160),
  location: clean(source.location, 120),
  instagram_url: clean(source.instagram_url, 500),
  linkedin_url: clean(source.linkedin_url, 500)
});

export async function onRequest(context) {
  try {
    if (!(await isAuthorised(context.request, context.env))) return json({error: "Sessão expirada."}, 401);
    const state = await initialise(context.env);
    if (context.request.method === "GET") return json({contact: state.contact});
    if (context.request.method !== "PUT") return json({error: "Método não permitido."}, 405);
    const contact = normaliseContact(await context.request.json());
    if (contact.email && !/^\S+@\S+\.\S+$/.test(contact.email)) throw new Error("Informe um e-mail válido ou deixe o campo vazio.");
    if (!isUrl(contact.instagram_url) || !isUrl(contact.linkedin_url)) throw new Error("Os links sociais precisam começar com https://.");
    state.contact = contact;
    await saveState(context.env, state);
    return json({contact});
  } catch (error) { return failure(error); }
}
