const MAX_UPLOAD_BYTES = 5 * 1024 * 1024;

function constantTimeEqual(left, right) {
  const encoder = new TextEncoder();
  const a = encoder.encode(left || "");
  const b = encoder.encode(right || "");
  const length = Math.max(a.length, b.length);
  let mismatch = a.length ^ b.length;

  for (let index = 0; index < length; index += 1) {
    mismatch |= (a[index % Math.max(a.length, 1)] || 0) ^
      (b[index % Math.max(b.length, 1)] || 0);
  }
  return mismatch === 0;
}

function objectKey(request) {
  const pathname = new URL(request.url).pathname;
  const key = decodeURIComponent(pathname.replace(/^\/+/, ""));
  if (!key.startsWith("media/") || key.includes("..") || key.endsWith("/")) {
    return null;
  }
  return key;
}

function authorized(request, env) {
  if (!env.MEDIA_UPLOAD_KEY) return false;

  const authorization = request.headers.get("Authorization") || "";
  const bearerToken = authorization.startsWith("Bearer ")
    ? authorization.slice("Bearer ".length)
    : "";
  const cookieToken = (request.headers.get("Cookie") || "")
    .split(";")
    .map((item) => item.trim())
    .find((item) => item.startsWith("media_upload_key="))
    ?.slice("media_upload_key=".length);
  return constantTimeEqual(
    bearerToken || request.headers.get("X-Media-Upload-Key") || cookieToken,
    env.MEDIA_UPLOAD_KEY,
  );
}

export default {
  async fetch(request, env) {
    const key = objectKey(request);
    if (!key) {
      return new Response("Invalid object key", { status: 400 });
    }

    if (request.method === "HEAD") {
      const object = await env.MEDIA_BUCKET.head(key);
      if (!object) return new Response(null, { status: 404 });
      const headers = new Headers({
        "Content-Length": String(object.size),
        ETag: object.httpEtag,
        "Last-Modified": object.uploaded.toUTCString(),
      });
      object.writeHttpMetadata(headers);
      return new Response(null, { status: 200, headers });
    }

    if (!authorized(request, env)) {
      return new Response("Forbidden", { status: 403 });
    }

    if (request.method === "PUT") {
      const contentLength = Number(request.headers.get("Content-Length") || 0);
      if (contentLength > MAX_UPLOAD_BYTES) {
        return new Response("File too large", { status: 413 });
      }

      const object = await env.MEDIA_BUCKET.put(key, request.body, {
        httpMetadata: {
          contentType: request.headers.get("Content-Type") || "application/octet-stream",
          cacheControl: "public, max-age=31536000, immutable",
        },
      });
      return Response.json({ key, etag: object.httpEtag }, { status: 201 });
    }

    if (request.method === "DELETE") {
      await env.MEDIA_BUCKET.delete(key);
      return new Response(null, { status: 204 });
    }

    return new Response("Method not allowed", {
      status: 405,
      headers: { Allow: "HEAD, PUT, DELETE" },
    });
  },
};
