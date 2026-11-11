import {failure, initialise, isAuthorised, json} from "./_lib.js";

export async function onRequestGet(context) {
  try {
    const state = await initialise(context.env);
    const authenticated = await isAuthorised(context.request, context.env);
    const content = state.content || {};
    return json({cases: authenticated ? (state.cases || []) : (state.cases || []).filter((item) => item.status === "published"), contact: state.contact, team: (state.team || []).filter((member) => member.name), content: {testimonials: (content.testimonials || []).filter((item) => item.visible && item.quote && item.author), partners: (content.partners || []).filter((item) => item.authorised && item.name), insights: (content.insights || []).filter((item) => item.visible && item.title)}});
  } catch (error) { return failure(error); }
}
