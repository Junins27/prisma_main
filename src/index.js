import * as cases from "../functions/api/cases.js";
import * as contact from "../functions/api/contact.js";
import * as media from "../functions/api/media.js";
import * as session from "../functions/api/session.js";
import * as settings from "../functions/api/settings.js";
import * as site from "../functions/api/site.js";

const withPath = (request, pathname, search = "") => {
  const url = new URL(request.url);
  url.pathname = pathname;
  url.search = search;
  return new Request(url, request);
};

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const context = {request, env, ctx};
    if (url.pathname === "/api/site" && request.method === "GET") return site.onRequestGet(context);
    if (url.pathname === "/api/session" && request.method === "POST") return session.onRequestPost(context);
    if (url.pathname === "/api/cases") return cases.onRequest(context);
    if (url.pathname === "/api/settings") return settings.onRequest(context);
    if (url.pathname === "/api/media" || url.pathname.startsWith("/api/media/")) return media.onRequest(context);
    if (url.pathname === "/api/contact" && request.method === "POST") return contact.onRequestPost(context);
    if (url.pathname === "/tema/golden-hour/" || url.pathname === "/tema/solar-editorial/") return env.ASSETS.fetch(withPath(request, "/"));
    if (url.pathname.startsWith("/projetos/")) return env.ASSETS.fetch(withPath(request, "/case.html", `?slug=${encodeURIComponent(url.pathname.split("/").filter(Boolean).pop() || "")}`));
    return env.ASSETS.fetch(request);
  }
};
