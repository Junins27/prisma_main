import {failure, initialise, isAuthorised, json, saveState} from "./_lib.js";

const clean = (value, length) => typeof value === "string" ? value.trim().slice(0, length) : "";
const fronts = new Set(["marketing", "tecnologia", "integrado"]);
const normalise = (items) => (Array.isArray(items) ? items : []).slice(0, 24).map((item, index) => ({
  id: `service-${index + 1}`,
  front: fronts.has(item?.front) ? item.front : "tecnologia",
  title: clean(item?.title, 120),
  summary: clean(item?.summary, 500),
  starting_price: clean(item?.starting_price, 80),
  support_summary: clean(item?.support_summary, 280),
  support_price: clean(item?.support_price, 80),
  visible: Boolean(item?.visible)
})).filter((item) => item.title);

export async function onRequest(context) {
  try {
    if (!(await isAuthorised(context.request, context.env))) return json({error: "Sessão expirada."}, 401);
    const state = await initialise(context.env);
    if (context.request.method === "GET") return json({services: state.services || []});
    if (context.request.method !== "PUT") return json({error: "Método não permitido."}, 405);
    const services = normalise(await context.request.json());
    if (services.some((service) => !service.summary)) throw new Error("Todo serviço cadastrado precisa de uma descrição breve.");
    state.services = services;
    await saveState(context.env, state);
    return json({services});
  } catch (error) { return failure(error); }
}
