# NGSI-LD Mini Editor

Tiny, no-deps GUI to view/edit NGSI-LD entities via the Context Broker REST API.

This repo includes **two CORS proxy options** (incase your broker has no cors support, if you have cors enabled just open the index.html file) so the browser can call a broker running at
**`http://example.com:1026`** (NGSI-LD on `/ngsi-ld/v1/...`):

- `proxies/nginx/` — NGINX reverse proxy with permissive CORS (Docker Compose), listens on **:1027**.
- `proxies/python/` — ultra-simple Python/Flask CORS proxy (no Docker), listens on **:1027**.

> Open **`index.html`** (the editor) from a browser.  
> In the editor’s Query URL, point to the proxy, e.g.:
>
> ```
> http://localhost:1027/ngsi-ld/v1/entities?idPattern=.*&limit=100
> ```

## Upstream assumption
Both proxies are hardcoded to forward to:
```
http://example.com:1026
```
So any browser request like `http://localhost:1027/ngsi-ld/v1/entities?...` becomes:
```
http://example.com:1026/ngsi-ld/v1/entities?...
```

---

## Option A — NGINX CORS proxy (Docker)
```bash
cd proxies/nginx
docker compose up -d
```
- Proxy: `http://localhost:1027/`
- Path is preserved and forwarded to `http://example.com:1026/…`
- Adds permissive CORS (incl. preflight).

Files:
- `proxies/nginx/nginx.conf`
- `proxies/nginx/docker-compose.yml`

---

## Option B — Python CORS proxy (no Docker)
```bash
cd proxies/python
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python app.py
```
- Proxy: `http://localhost:1027/`
- Path is preserved and forwarded to `http://example.com:1026/…`
- Adds permissive CORS (incl. preflight).

Files:
- `proxies/python/app.py`
- `proxies/python/requirements.txt`

---

## Security
CORS is **wide open** (`Access-Control-Allow-Origin: *`). Lock it down before exposing publicly.
