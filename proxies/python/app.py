from flask import Flask, request, Response
import requests

# Hardcoded upstream Context Broker (adjust if needed)
UPSTREAM = "http://example.com:1026"

app = Flask(__name__)

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, PATCH, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Origin, Content-Type, Accept, Authorization, Link",
    "Access-Control-Expose-Headers": "Location, Link, Content-Location",
    "Access-Control-Max-Age": "86400",
}

@app.after_request
def add_cors(resp):
    for k, v in CORS_HEADERS.items():
        resp.headers[k] = v
    return resp

@app.route("/", defaults={"path": ""}, methods=["GET","POST","PUT","PATCH","DELETE","OPTIONS"])  # noqa: E231
@app.route("/<path:path>", methods=["GET","POST","PUT","PATCH","DELETE","OPTIONS"])              # noqa: E231
def proxy(path: str):
    # Preflight
    if request.method == "OPTIONS":
        return Response(status=204)

    # Build upstream URL (preserve path and query)
    url = f"{UPSTREAM}/{path}"
    if request.query_string:
        url = f"{url}?{request.query_string.decode('utf-8', errors='ignore')}"

    # Pass-through headers (drop Host)
    headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}

    try:
        upstream_resp = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            data=request.get_data(),
            allow_redirects=False,
            timeout=60,
        )
    except requests.RequestException as e:
        return Response(f"Upstream error: {e}", status=502)

    # Filter hop-by-hop and length headers
    excluded = {"content-encoding", "transfer-encoding", "content-length", "connection"}
    out_headers = [(k, v) for k, v in upstream_resp.headers.items() if k.lower() not in excluded]

    return Response(
        upstream_resp.content,
        status=upstream_resp.status_code,
        headers=out_headers,
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1027)
