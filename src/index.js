// Domain ohne www -> www (Pfad und Query bleiben erhalten), sonst statische Assets.
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname === "die-unternehmensimmobilie.de") {
      url.hostname = "www.die-unternehmensimmobilie.de";
      url.protocol = "https:";
      return Response.redirect(url.toString(), 301);
    }
    return env.ASSETS.fetch(request);
  },
};
