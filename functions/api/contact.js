import {database, failure, json} from "./_lib.js";

const validTypes = new Set(["website", "system", "data", "automation", "brand", "other"]);
const clean = (value, length) => typeof value === "string" ? value.trim().slice(0, length) : "";
export async function onRequestPost(context) {
  try {
    const input = await context.request.json();
    const message = {name: clean(input.name, 120), email: clean(input.email, 254), company: clean(input.company, 120), project_type: clean(input.project_type, 20), message: clean(input.message, 3000), created_at: new Date().toISOString()};
    if (!message.name || !/^\S+@\S+\.\S+$/.test(message.email) || !validTypes.has(message.project_type) || !message.message || input.privacy_consent !== "true") return json({error: "Revise os campos obrigatórios e o consentimento."}, 400);
    const db = database(context.env);
    await db.prepare("CREATE TABLE IF NOT EXISTS contact_messages (id INTEGER PRIMARY KEY AUTOINCREMENT, payload TEXT NOT NULL, created_at TEXT NOT NULL)").run();
    await db.prepare("INSERT INTO contact_messages (payload, created_at) VALUES (?, ?)").bind(JSON.stringify(message), message.created_at).run();
    return json({ok: true}, 201);
  } catch (error) { return failure(error); }
}
