const encoder = new TextEncoder();
const json = (data, status = 200) => new Response(JSON.stringify(data), {status, headers: {"Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store"}});
const base64url = (bytes) => btoa(String.fromCharCode(...bytes)).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/g, "");
const decode64url = (value) => Uint8Array.from(atob(value.replace(/-/g, "+").replace(/_/g, "/")), (char) => char.charCodeAt(0));

export function database(env) {
  if (!env.PRISMA_DB) throw new Error("O binding PRISMA_DB não está configurado.");
  return env.PRISMA_DB;
}

export async function initialise(env) {
  const db = database(env);
  await db.batch([
    db.prepare("CREATE TABLE IF NOT EXISTS prisma_state (id INTEGER PRIMARY KEY CHECK (id = 1), payload TEXT NOT NULL, updated_at TEXT NOT NULL)"),
    db.prepare("CREATE TABLE IF NOT EXISTS contact_messages (id INTEGER PRIMARY KEY AUTOINCREMENT, payload TEXT NOT NULL, created_at TEXT NOT NULL)")
  ]);
  const stored = await db.prepare("SELECT payload FROM prisma_state WHERE id = 1").first();
  if (!stored) {
    const state = JSON.stringify({cases: []});
    await db.prepare("INSERT INTO prisma_state (id, payload, updated_at) VALUES (1, ?, ?)").bind(state, new Date().toISOString()).run();
    return {cases: []};
  }
  try { return JSON.parse(stored.payload); } catch (_) { return {cases: []}; }
}

export async function saveState(env, state) {
  await database(env).prepare("UPDATE prisma_state SET payload = ?, updated_at = ? WHERE id = 1").bind(JSON.stringify(state), new Date().toISOString()).run();
}

async function hmac(secret, value) {
  const key = await crypto.subtle.importKey("raw", encoder.encode(secret), {name: "HMAC", hash: "SHA-256"}, false, ["sign", "verify"]);
  return new Uint8Array(await crypto.subtle.sign("HMAC", key, encoder.encode(value)));
}

export async function createSession(env) {
  if (!env.ADMIN_SESSION_SECRET) throw new Error("O segredo ADMIN_SESSION_SECRET não está configurado.");
  const payload = base64url(encoder.encode(JSON.stringify({exp: Date.now() + 1000 * 60 * 60 * 12})));
  return `${payload}.${base64url(await hmac(env.ADMIN_SESSION_SECRET, payload))}`;
}

export async function isAuthorised(request, env) {
  if (!env.ADMIN_SESSION_SECRET) return false;
  const token = request.headers.get("Authorization")?.replace(/^Bearer\s+/i, "");
  if (!token || !token.includes(".")) return false;
  const [payload, signature] = token.split(".");
  try {
    const expected = base64url(await hmac(env.ADMIN_SESSION_SECRET, payload));
    if (signature.length !== expected.length || !crypto.subtle.timingSafeEqual) {
      if (signature !== expected) return false;
    } else if (!crypto.subtle.timingSafeEqual(encoder.encode(signature), encoder.encode(expected))) return false;
    const claims = JSON.parse(new TextDecoder().decode(decode64url(payload)));
    return Number.isFinite(claims.exp) && claims.exp > Date.now();
  } catch (_) { return false; }
}

export function failure(error, fallback = "Não foi possível concluir esta operação.") {
  console.error(error);
  return json({error: error?.message || fallback}, 503);
}

export {json};
