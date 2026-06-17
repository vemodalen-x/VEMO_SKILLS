# Design patterns & the interactive-server recipe

Read this when you are (a) building the **interactive server** mode, (b)
**rebranding/theming** the report, or (c) want to understand *why* the builder
is shaped the way it is so you can adapt it confidently.

## Why these design choices

### Self-contained = base64-embedded, one file
Images are inlined as `data:image/...;base64,` URIs instead of `<img src="step1.png">`.
A pipeline report is a thing you *send* — to a reviewer, a client, your future
self. Sidecar image folders break the moment the file is moved or emailed. One
file always survives. The cost is size (base64 is ~33% larger than the bytes,
and everything lives in one document), which is why display-downscaling and
JPEG quality matter (below).

### Downscale before encoding, don't pixel-peep
A report exists to show *what changed between steps*, not to audit native 4K
pixels. Encoding full-res frames bloats the file to tens of MB and janks the
browser. Downscale the long edge to ~1024px with `INTER_AREA` (the correct
filter for shrinking — it area-averages, avoiding aliasing). Thresholds and
ratios are unaffected because they live in value space, not pixel space.

### JPEG q≈88 for photos, PNG for masks
Photographic intermediates compress beautifully as JPEG at quality 85–90 — near
invisible loss, a fraction of the bytes. But hard-edged content (binary masks,
trimaps, label maps, line art) gets JPEG **ringing**: ghost halos along edges
that *lie* about what the algorithm produced. Use lossless PNG there
(`encode(..., png=True)`). Rule: lossy for continuous tone, lossless for
anything with a hard edge that carries meaning.

### Compare slider beats side-by-side
Two images side by side force the eye to saccade and hold one in memory. A
slider puts before/after in the **same pixels** — change pops out because only
the changed region differs as you drag. This is the single highest-leverage UI
choice in the report. Pair it with a diff heatmap for the "what exactly?"
follow-up.

### Diff heatmap = the reviewer's first question, answered
Every reviewer of a pipeline step asks "what did this actually change?"
`|after - before|`, mean-collapsed to one channel and JET-colormapped, answers
it at a glance: bright = changed a lot, dark = untouched. It instantly reveals
both *intended* effects and *accidental* ones (a step that was supposed to touch
only hair edges but lit up the whole frame is a bug you can now see).

### what / why / formula — the explanatory triad
Code shows *what*. Comments rot. The durable, hard-to-reconstruct knowledge is
*why this method over the obvious one* and *what artifact it prevents*. The
builder gives `why_html` its own highlighted call-out precisely because it is
the most valuable and the most often omitted. Always fill it for any
non-trivial step.

### Theme via CSS variables
All colors live in `:root { --bg / --card / --accent / --ok / --fail / --warn }`
in `_CSS`. Rebrand by editing those few lines — every component inherits. The
default is a dark "engineering report" palette; swap to light by inverting
`--bg`/`--text` and softening `--border`.

## Interactive server recipe (parameter sliders + live re-run)

When the user wants to *tune* parameters rather than read a fixed report, serve
the pipeline over HTTP: sliders in a sidebar POST params to `/api/run`, the
server re-runs the pipeline and returns the step images as JSON, the page
re-renders. It reuses `viz_report.encode` / `diff_heat` verbatim — only the
transport and layout differ.

Skeleton (stdlib `http.server`, no framework needed):

```python
import json, time
from http.server import HTTPServer, BaseHTTPRequestHandler
from viz_report import encode, diff_heat, resize_for_display

def run_pipeline(params: dict) -> dict:
    """Run all steps with the given params; return base64 images + metrics.
    Return shape: {"steps": {name: b64}, "timings": {name: sec}, "metrics": {...}}.
    """
    img = load_input()
    steps, timings = {}, {}
    t = time.time()
    out = step_one(img, k=params.get("k", 3))
    timings["step_one"] = time.time() - t
    steps["before"] = encode(resize_for_display(img))
    steps["after"]  = encode(resize_for_display(out))
    steps["diff"]   = encode(resize_for_display(diff_heat(img, out)), kind="heat")
    return {"steps": steps, "timings": timings, "metrics": {"verdict": "PASS"}}

PAGE = """<!DOCTYPE html><html><head><meta charset=utf-8>
<style>/* sidebar + .cmp styles — copy from viz_report._CSS */</style></head>
<body>
 <input type=range id=k min=1 max=15 step=2 value=3
        oninput="document.getElementById('kv').textContent=this.value">
 <span id=kv>3</span>
 <button onclick="run()">Run</button>
 <div id=out></div>
<script>
async function run(){
  const params = {k: +document.getElementById('k').value};
  const r = await fetch('/api/run', {method:'POST',
      headers:{'Content-Type':'application/json'}, body:JSON.stringify(params)});
  const d = await r.json();
  // render d.steps into #out: <img src="data:image/jpeg;base64,${d.steps.after}">
}
window.addEventListener('load', run);   // auto-run with defaults on load
</script></body></html>"""

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        body = PAGE.encode()
        self.send_response(200); self.send_header("Content-Type","text/html")
        self.send_header("Content-Length", str(len(body))); self.end_headers()
        self.wfile.write(body)
    def do_POST(self):
        if self.path != "/api/run":
            self.send_response(404); self.end_headers(); return
        n = int(self.headers.get("Content-Length", 0))
        params = json.loads(self.rfile.read(n) or b"{}")
        body = json.dumps(run_pipeline(params)).encode()
        self.send_response(200); self.send_header("Content-Type","application/json")
        self.send_header("Content-Length", str(len(body))); self.end_headers()
        self.wfile.write(body)

HTTPServer(("0.0.0.0", 8700), H).serve_forever()
```

Server-mode notes:
- **Auto-run on load** (`window.addEventListener('load', run)`) so the user sees
  output immediately with defaults, not a blank page.
- **Show a loading overlay** while `/api/run` is in flight — a multi-model
  pipeline can take seconds, and a frozen page looks broken.
- **One slider value label per input** updated on `oninput` — instant feedback
  even before re-running.
- **`encode()` returns the full `data:` URI** in `viz_report`; if you build the
  JSON payload yourself, strip the prefix or keep it consistent with the client.
- Bind to `0.0.0.0` only on trusted networks; `127.0.0.1` otherwise.

## Privacy: embedded ≠ hidden

Base64 is encoding, not encryption — anyone with the `.html` can decode every
frame back to pixels. A self-contained report is *easy to share*, which also
means it is *easy to over-share*. Before sending one, check that no
intermediate (a raw input photo, a customer image, an internal screenshot) is
something you would not paste into the recipient's inbox. When in doubt, redact
or crop the input before it enters the pipeline.

## Adapting to non-image pipelines

The builder is image-centric but the structure (steps → what/why/formula →
compare → diff → metrics → timing) fits any pipeline. For data/tabular steps,
render intermediate state to an image first: a matplotlib figure saved to a
numpy array, or a rendered table. `encode()` takes any BGR uint8 array, so
`fig.canvas` → array → `encode()` drops straight in.

## Provenance

Generalized from an internal hair-matting / bokeh pipeline visualizer
(`vis_pipeline_server.py`). That original is **not bundled** with this skill —
everything reusable from it has been folded into `references/scripts/viz_report.py` and
the server recipe above, which together cover both modes end-to-end.
