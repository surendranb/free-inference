// Content negotiation: markdown clients get the catalog as text/markdown.
export async function onRequest(context) {
  const req = context.request;
  const accept = req.headers.get("accept") || "";
  if (new URL(req.url).pathname === "/" && accept.includes("text/markdown")) {
    const res = await context.env.ASSETS.fetch(new URL("/index.md", req.url));
    if (res.ok) {
      return new Response(res.body, {
        status: 200,
        headers: { "content-type": "text/markdown; charset=utf-8", vary: "Accept" },
      });
    }
  }
  const res = await context.next();
  res.headers.set("Vary", "Accept");
  return res;
}
