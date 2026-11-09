import {failure, isAuthorised, json} from "./_lib.js";

const maxFilesize = 8 * 1024 * 1024;
const extensions = {"image/avif": "avif", "image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"};
const mediaUrl = (key) => `/api/media/${key.split("/").map(encodeURIComponent).join("/")}`;

const keyFromRequest = (request) => {
  const pathname = new URL(request.url).pathname;
  return decodeURIComponent(pathname.slice("/api/media/".length));
};

export async function onRequest(context) {
  try {
    const {request, env} = context;
    if (!env.PRISMA_MEDIA) throw new Error("O armazenamento de imagens PRISMA_MEDIA ainda não está configurado.");
    const requestedKey = keyFromRequest(request);

    if (request.method === "GET") {
      if (!requestedKey.startsWith("cases/")) return json({error: "Imagem não encontrada."}, 404);
      const object = await env.PRISMA_MEDIA.get(requestedKey);
      if (!object) return json({error: "Imagem não encontrada."}, 404);
      return new Response(object.body, {headers: {
        "Content-Type": object.httpMetadata?.contentType || "application/octet-stream",
        "Cache-Control": "public, max-age=31536000, immutable",
        "ETag": object.httpEtag
      }});
    }

    if (!(await isAuthorised(request, env))) return json({error: "Sessão expirada."}, 401);
    if (request.method !== "POST") return json({error: "Método não permitido."}, 405);

    const form = await request.formData();
    const file = form.get("image");
    if (!file || typeof file.arrayBuffer !== "function") throw new Error("Selecione uma imagem para enviar.");
    if (!extensions[file.type]) throw new Error("Envie uma imagem JPG, PNG, WebP ou AVIF.");
    if (file.size > maxFilesize) throw new Error("Cada imagem pode ter no máximo 8 MB.");

    const key = `cases/${crypto.randomUUID()}.${extensions[file.type]}`;
    await env.PRISMA_MEDIA.put(key, await file.arrayBuffer(), {httpMetadata: {contentType: file.type}});
    return json({image: {key, url: mediaUrl(key), alt: ""}}, 201);
  } catch (error) { return failure(error); }
}
