import {failure, initialise, isAuthorised, json, saveState} from "./_lib.js";

const clean = (value, length) => typeof value === "string" ? value.trim().slice(0, length) : "";
const mediaUrl = (key) => `/api/media/${key.split("/").map(encodeURIComponent).join("/")}`;

const photo = (source) => {
  const key = clean(source?.key, 300);
  if (!key || !/^team\/[a-z0-9-]+\.(?:avif|jpe?g|png|webp)$/i.test(key)) return null;
  return {key, url: mediaUrl(key)};
};

const normaliseTeam = (input, previous) => [0, 1, 2].map((index) => {
  const source = Array.isArray(input) ? input[index] || {} : {};
  return {id: `member-${index + 1}`, name: clean(source.name, 100), role: clean(source.role, 100), bio: clean(source.bio, 700), photo: photo(source.photo)};
});

export async function onRequest(context) {
  try {
    if (!(await isAuthorised(context.request, context.env))) return json({error: "Sessão expirada."}, 401);
    const state = await initialise(context.env);
    if (context.request.method === "GET") return json({team: state.team});
    if (context.request.method !== "PUT") return json({error: "Método não permitido."}, 405);
    state.team = normaliseTeam(await context.request.json(), state.team);
    await saveState(context.env, state);
    return json({team: state.team});
  } catch (error) { return failure(error); }
}
