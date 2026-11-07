import {createSession, failure, json} from "./_lib.js";

export async function onRequestPost(context) {
  try {
    if (!context.env.ADMIN_PASSWORD || !context.env.ADMIN_SESSION_SECRET) return json({error: "A área administrativa ainda não foi configurada."}, 503);
    const {password} = await context.request.json();
    if (typeof password !== "string" || password !== context.env.ADMIN_PASSWORD) return json({error: "Senha inválida."}, 401);
    return json({token: await createSession(context.env)});
  } catch (error) { return failure(error); }
}
