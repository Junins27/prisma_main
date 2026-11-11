import {failure, initialise, isAuthorised, json} from "./_lib.js";

export async function onRequestGet(context) {
  try {
    const state = await initialise(context.env);
    const authenticated = await isAuthorised(context.request, context.env);
    return json({cases: authenticated ? (state.cases || []) : (state.cases || []).filter((item) => item.status === "published"), contact: state.contact, team: (state.team || []).filter((member) => member.name)});
  } catch (error) { return failure(error); }
}
