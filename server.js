import { join } from "path";  // Requires Bun >= 0.6.0
import { file } from "bun";

// Built-in HTTP server in Bun
Bun.serve({
  port: 8000,
  fetch(req) {
    // Parse the incoming URL
    const url = new URL(req.url);

    // If path is "/", serve index.html
    if (url.pathname === "/") {
      return new Response(file(join(process.cwd(), "index.html")), {
        headers: {
          "Content-Type": "text/html",
        },
      });
    }

    // Otherwise, try to serve the file from disk
    try {
      const filePath = join(process.cwd(), url.pathname);
      // Return the requested file with an inferred content type
      return new Response(file(filePath), {
        headers: {
          "Content-Type": getMimeType(url.pathname),
        },
      });
    } catch (e) {
      // File not found
      return new Response("404 Not Found", { status: 404 });
    }
  },
});

// Basic MIME type helper 
function getMimeType(pathname) {
  const ext = pathname.split(".").pop().toLowerCase();
  switch (ext) {
    case "html":
      return "text/html";
    case "js":
      return "text/javascript";
    case "css":
      return "text/css";
    case "json":
      return "application/json";
    case "png":
      return "image/png";
    case "jpg":
    case "jpeg":
      return "image/jpeg";
    case "gif":
      return "image/gif";
    case "svg":
      return "image/svg+xml";
    default:
      return "application/octet-stream";
  }
}

console.log("Server running on http://localhost:8000");
