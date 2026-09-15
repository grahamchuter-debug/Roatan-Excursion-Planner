/**
 * Roatan Excursion Planner — Workers Assets entry (Phase 38B).
 * Canonical: apex HTTPS + trailing-slash directory URLs.
 * www → apex; .html → /slug/; bare known /slug → /slug/; real 404 — never soft-home.
 */
const APEX_HOST = "roatanexcursionplanner.com";

const EDITORIAL_SLUGS = new Set([
  "about",
  "best-roatan-excursions",
  "contact",
  "glass-bottom-boat-tours-roatan",
  "mahogany-bay-vs-coxen-hole",
  "methodology",
  "one-day-in-roatan",
  "privacy",
  "roatan-beach-breaks",
  "roatan-cruise-port-guide",
  "roatan-excursions-for-first-time-visitors",
  "roatan-family-excursions",
  "roatan-faq",
  "roatan-private-tours",
  "roatan-reef-vs-beach",
  "roatan-sloth-and-monkey-tours",
  "roatan-snorkelling-tours",
  "roatan-wildlife-encounters",
  "roatan-zipline-excursions",
  "terms",
  "west-bay-beach-excursions",
]);

const BLOCKED_EXACT = new Set([
  "/package.json",
  "/package-lock.json",
  "/wrangler.jsonc",
  "/wrangler.toml",
  "/deploy.sh",
  "/.assetsignore",
  "/.gitignore",
  "/template.html",
  "/template",
  "/worker.js",
]);

function isBlockedPath(pathname) {
  const p = (pathname || "/").toLowerCase();
  if (BLOCKED_EXACT.has(p)) return true;
  if (
    p === "/content" ||
    p.startsWith("/content/") ||
    p === "/partials" ||
    p.startsWith("/partials/") ||
    p === "/scripts" ||
    p.startsWith("/scripts/") ||
    p === "/data" ||
    p.startsWith("/data/")
  ) {
    return true;
  }
  if (p.endsWith(".py") || p.endsWith(".mjs") || p.endsWith(".ts")) return true;
  if (p.includes("destination.config.json")) return true;
  if (p.startsWith("/wrangler")) return true;
  return false;
}

function isKnownBarePath(pathname) {
  const p = (pathname || "/").replace(/\/+$/, "") || "/";
  if (p === "/") return false;
  const parts = p.split("/").filter(Boolean);
  if (parts[0] === "ship-schedule") return true;
  if (parts.length === 1 && EDITORIAL_SLUGS.has(parts[0])) return true;
  return false;
}

function toCanonicalPath(pathname) {
  let path = pathname || "/";
  const lower = path.toLowerCase();

  if (lower === "/404.html" || lower === "/404") {
    return "/404.html";
  }

  if (lower.endsWith(".html")) {
    path = path.slice(0, -5);
    if (path.toLowerCase().endsWith("/index")) path = path.slice(0, -6);
    if (path === "" || path.toLowerCase() === "/index") return "/";
    if (!path.endsWith("/")) path += "/";
    return path;
  }

  if (path.length > 1 && !path.endsWith("/") && !path.includes(".") && isKnownBarePath(path)) {
    return path + "/";
  }

  return path || "/";
}

async function serve404(env, url) {
  const notFound = await env.ASSETS.fetch(new URL("/404.html", url.origin));
  return new Response(notFound.body, {
    status: 404,
    headers: {
      "content-type": "text/html; charset=utf-8",
      "cache-control": "no-store",
      "x-robots-tag": "noindex, follow",
    },
  });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const host = url.hostname.toLowerCase();
    const isWww = host === `www.${APEX_HOST}`;
    const isHttp = url.protocol === "http:";
    const rawPath = url.pathname || "/";
    const rawLower = rawPath.toLowerCase();
    const is404Doc = rawLower === "/404.html" || rawLower === "/404";

    if (isBlockedPath(rawPath) && !is404Doc) {
      return serve404(env, url);
    }

    const hasHtml = rawLower.endsWith(".html") && !is404Doc;
    const needsBareSlash =
      !is404Doc &&
      rawPath.length > 1 &&
      !rawPath.endsWith("/") &&
      !rawPath.includes(".") &&
      isKnownBarePath(rawPath);
    const needsHostFix = isWww || isHttp;

    if (needsHostFix || hasHtml || needsBareSlash) {
      const dest = new URL(url.toString());
      dest.hostname = APEX_HOST;
      dest.protocol = "https:";
      dest.pathname = toCanonicalPath(rawPath);
      if (dest.toString() !== url.toString()) {
        return Response.redirect(dest.toString(), 301);
      }
    }

    const assetResponse = await env.ASSETS.fetch(request);

    if (assetResponse.status === 404) {
      return serve404(env, url);
    }

    return assetResponse;
  },
};
