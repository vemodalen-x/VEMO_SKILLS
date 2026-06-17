#!/usr/bin/env python3
"""
viz_report.py — Self-contained HTML report builder for multi-step pipelines.

Pipeline-agnostic core for the `pipeline-viz-report` skill. Feed it per-step
images, annotations, timings and metrics; it emits a SINGLE .html file with
every image embedded as base64 (no sidecar files — email it, host it, done).

Dependencies: numpy + opencv-python (cv2) only. No project-specific imports.
Images are expected as BGR uint8 (cv2 convention). See encode helpers for
grayscale / float-heatmap handling.

Typical use:

    from viz_report import PipelineReport

    rep = PipelineReport("My Pipeline", "subtitle / one-liner")
    rep.add_step(
        1, "Denoise", time_ms=12,
        algo_html="Median filter removes salt-and-pepper noise ...",
        why_html="Median beats Gaussian here because it preserves edges ...",
        formula_html="out = median(in, k=3)",
        compare=(noisy_bgr, clean_bgr, "Noisy", "Denoised"),
        diff=(noisy_bgr, clean_bgr),            # auto |after-before| heatmap
    )
    rep.add_metrics({"PSNR": ("31.4 dB", True), "Time": ("0.4s", None)})
    rep.export("report.html")

The interactive-server variant (parameter sliders + live re-run) is documented
in references/design-patterns.md — the encode/HTML helpers here are reused as-is.
"""

import base64
import html as _html
from typing import Dict, List, Optional, Sequence, Tuple, Union

import cv2
import numpy as np

ArrayLike = np.ndarray
CompareSpec = Union[Tuple[ArrayLike, ArrayLike, str, str],
                    Tuple[ArrayLike, ArrayLike, str, str, str]]


# ── Encoding: numpy array → base64 data-URI payload ───────────────────────────

def encode(img: ArrayLike, *, kind: str = "color", quality: int = 88,
           png: bool = False) -> str:
    """Encode an image to a base64 string for inline <img src="data:...">.

    kind:
      "color" — BGR uint8 (cv2 default), encoded directly.
      "gray"  — single channel; uint8 passed through, float [0,1] scaled to 255.
      "heat"  — float array (any range) min-max normalised then JET colormapped.
                Use for difference maps / weight maps / attention — the human
                eye reads a colormap far faster than a dim grayscale ramp.
      "mask"  — grayscale forced to lossless PNG. Use for binary masks / trimaps
                / label maps / line-art, where JPEG ringing would lie about hard
                edges (PNG costs ~3-5x bytes but tells the truth).
    png: force lossless PNG instead of JPEG for any kind.
    """
    if kind == "mask":
        kind, png = "gray", True
    if kind == "gray":
        if img.dtype in (np.float32, np.float64):
            vis = np.clip(img * 255.0, 0, 255).astype(np.uint8)
        else:
            vis = img
        img = cv2.cvtColor(vis, cv2.COLOR_GRAY2BGR)
    elif kind == "heat":
        f = img.astype(np.float32)
        lo, hi = float(f.min()), float(f.max())
        norm = (f - lo) / (hi - lo + 1e-6)
        vis = np.clip(norm * 255.0, 0, 255).astype(np.uint8)
        img = cv2.applyColorMap(vis, cv2.COLORMAP_JET)
    elif kind != "color":
        raise ValueError(f"unknown kind={kind!r} (color|gray|heat)")

    if png:
        ok, buf = cv2.imencode(".png", img)
    else:
        ok, buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, quality])
    if not ok:
        raise RuntimeError("cv2.imencode failed")
    mime = "png" if png else "jpeg"
    return f"data:image/{mime};base64," + base64.b64encode(buf).decode("ascii")


def diff_heat(before: ArrayLike, after: ArrayLike) -> ArrayLike:
    """|after - before| collapsed to a single float channel, for kind='heat'.

    Self-normalising (encode() does the min-max), so it answers the one question
    a reviewer always asks of a pipeline step: *what exactly did this change?*
    """
    if before.shape[:2] != after.shape[:2]:
        raise ValueError(
            f"diff_heat: before {before.shape[:2]} vs after {after.shape[:2]} "
            "differ in size — a crop/scale step changed geometry; resize or "
            "crop both to a common size before comparing")
    d = np.abs(after.astype(np.float32) - before.astype(np.float32))
    if d.ndim == 3:
        d = d.mean(axis=2)
    return d


def resize_for_display(img: ArrayLike, max_w: int = 1024) -> ArrayLike:
    """Downscale wide images before encoding. The report is for *seeing the
    difference*, not pixel-peeping originals — full-res 4K frames bloat the
    file to tens of MB and slow the browser. INTER_AREA = clean downscale."""
    h, w = img.shape[:2]
    if w <= max_w:
        return img
    scale = max_w / w
    return cv2.resize(img, (max_w, int(h * scale)), interpolation=cv2.INTER_AREA)


# ── Report builder ────────────────────────────────────────────────────────────

class PipelineReport:
    """Accumulates pipeline steps and renders one self-contained HTML file."""

    def __init__(self, title: str, subtitle: str = "", *,
                 display_width: int = 1024, jpeg_quality: int = 88,
                 lang: str = "en"):
        self.title = title
        self.subtitle = subtitle
        self.display_width = display_width
        self.jpeg_quality = jpeg_quality
        self.lang = lang
        self._sections: List[str] = []
        self._timings: Dict[str, float] = {}
        self._cmp_id = 0

    # -- internal encode honouring display width + quality --
    # kind "mask" = grayscale + lossless PNG (hard edges must not get JPEG ringing)
    def _enc(self, img: ArrayLike, kind: str = "color") -> str:
        png = kind == "mask"
        enc_kind = "gray" if kind == "mask" else kind
        small = resize_for_display(img, self.display_width)
        return encode(small, kind=enc_kind, quality=self.jpeg_quality, png=png)

    def _img_card(self, img: ArrayLike, caption: str, kind: str = "color") -> str:
        src = self._enc(img, kind=kind)
        cap = _html.escape(caption)
        return (f'<div class="img-card"><img src="{src}" alt="{cap}" '
                f'onclick="lb(this.src)"><div class="caption">{cap}</div></div>')

    def _compare(self, spec: CompareSpec) -> str:
        left, right, ll, rl = spec[0], spec[1], spec[2], spec[3]
        if left.shape[:2] != right.shape[:2]:
            raise ValueError(
                f"compare: left {left.shape[:2]} vs right {right.shape[:2]} "
                "differ in size — the slider overlays both in the same pixels, "
                "so resize or crop to a common size first")
        kind = spec[4] if len(spec) > 4 else "color"
        self._cmp_id += 1
        cid = f"cmp{self._cmp_id}"
        ls, rs = self._enc(left, kind=kind), self._enc(right, kind=kind)
        ll, rl = _html.escape(ll), _html.escape(rl)
        return (
            f'<div class="cmp" id="{cid}" tabindex="0" role="slider" '
            f'aria-label="{ll} / {rl} comparison" aria-valuenow="50">'
            f'<img src="{rs}" alt="{rl}">'
            f'<div class="cmp-ov" style="width:50%"><img src="{ls}" alt="{ll}"></div>'
            f'<div class="cmp-dv" style="left:50%"></div>'
            f'<div class="cmp-lab l">{ll}</div><div class="cmp-lab r">{rl}</div>'
            f'</div>')

    def add_step(self, num: Union[int, str], title: str, *,
                 time_ms: Optional[float] = None,
                 algo_html: str = "", why_html: str = "", formula_html: str = "",
                 images: Optional[Sequence[Tuple[str, ArrayLike, str]]] = None,
                 compare: Optional[CompareSpec] = None,
                 diff: Optional[Union[ArrayLike, Tuple[ArrayLike, ArrayLike]]] = None,
                 diff_caption: str = "Difference") -> "PipelineReport":
        """Append one pipeline stage.

        algo_html  : WHAT the step does (1-3 sentences). HTML allowed.
        why_html   : WHY it is done this way / why this method over the obvious
                     alternative. Rendered as a highlighted call-out box.
        formula_html: the actual math / pseudocode, monospace block. <br> for lines.
        images     : list of (caption, array, kind) static panels.
        compare    : (before, after, left_label, right_label[, kind]) draggable slider.
        diff       : float heatmap array, OR (before, after) to auto-compute it.
        """
        parts = [f'<div class="step"><div class="step-h">'
                 f'<div class="step-n">{_html.escape(str(num))}</div>'
                 f'<div class="step-t">{_html.escape(title)}</div>']
        if time_ms is not None:
            parts.append(f'<div class="step-ms">{int(round(time_ms))}ms</div>')
        parts.append('</div><div class="step-b">')

        if algo_html:
            parts.append(f'<div class="algo">{algo_html}</div>')
        if formula_html:
            parts.append(f'<div class="formula">{formula_html}</div>')
        if why_html:
            parts.append(f'<div class="why"><b>Why:</b> {why_html}</div>')

        if compare is not None:
            parts.append('<div class="hint">drag the divider to compare</div>')
            parts.append(self._compare(compare))
        if images:
            cards = "".join(self._img_card(a, c, k) for c, a, k in images)
            parts.append(f'<div class="imgs">{cards}</div>')
        if diff is not None:
            arr = diff_heat(diff[0], diff[1]) if isinstance(diff, tuple) else diff
            parts.append(f'<div class="imgs">'
                         f'{self._img_card(arr, diff_caption, kind="heat")}</div>')

        parts.append('</div></div><div class="arrow">&#8595;</div>')
        self._sections.append("".join(parts))
        return self

    def add_metrics(self, metrics: dict, title: str = "Metrics") -> "PipelineReport":
        """metrics: {label: value} or {label: (value, ok)} where ok in
        {True, False, None}. True→green, False→red, None→neutral. A verdict row
        at a glance beats forcing the reader to interpret raw numbers."""
        cells = []
        for label, v in metrics.items():
            if isinstance(v, tuple):
                value, ok = v
            else:
                value, ok = v, None
            cls = "pass" if ok is True else "fail" if ok is False else ""
            cells.append(f'<div class="metric"><div class="m-l">'
                         f'{_html.escape(str(label))}</div>'
                         f'<div class="m-v {cls}">{_html.escape(str(value))}</div></div>')
        self._sections.append(
            f'<div class="step"><div class="step-h">'
            f'<div class="step-n" style="background:var(--ok)">&#10003;</div>'
            f'<div class="step-t">{_html.escape(title)}</div></div>'
            f'<div class="metrics">{"".join(cells)}</div></div>')
        return self

    def add_timings(self, timings: dict) -> "PipelineReport":
        """timings: {step_name: seconds}. Rendered as proportional bars so the
        bottleneck is obvious without mental arithmetic."""
        self._timings = dict(timings)
        return self

    def _timings_html(self) -> str:
        if not self._timings:
            return ""
        total = sum(self._timings.values()) or 1e-9
        rows = []
        for k, v in self._timings.items():
            pct = max(2.0, v / total * 100.0)
            rows.append(
                f'<div class="tm"><div class="tm-r">'
                f'<span>{_html.escape(k)}</span><span>{v*1000:.0f}ms</span></div>'
                f'<div class="tm-bar"><div style="width:{pct:.0f}%"></div></div></div>')
        return (f'<div class="step"><div class="step-h">'
                f'<div class="step-n" style="background:var(--muted)">T</div>'
                f'<div class="step-t">Timing breakdown</div>'
                f'<div class="step-ms">{total*1000:.0f}ms total</div></div>'
                f'<div class="step-b">{"".join(rows)}</div></div>'
                f'<div class="arrow">&#8595;</div>')

    def render(self) -> str:
        body = self._timings_html() + "".join(self._sections)
        return _PAGE.format(
            lang=_html.escape(self.lang),
            title=_html.escape(self.title),
            subtitle=_html.escape(self.subtitle),
            css=_CSS, js=_JS, body=body)

    def export(self, out_path: str) -> str:
        import os
        html_str = self.render()
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_str)
        mb = os.path.getsize(out_path) / (1024 * 1024)
        print(f"Wrote {out_path} ({mb:.1f} MB, {len(self._sections)} sections)")
        return out_path


# ── Static assets (dark theme; tweak the :root vars to rebrand) ───────────────

_CSS = """
:root{--bg:#0f1117;--card:#1a1d27;--border:#2a2d3a;--text:#e4e6eb;
--muted:#8b8fa3;--accent:#6366f1;--ok:#22c55e;--fail:#ef4444;--warn:#f59e0b}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter',-apple-system,BlinkMacSystemFont,'Noto Sans SC',sans-serif;
background:var(--bg);color:var(--text);line-height:1.7}
.header{background:linear-gradient(135deg,#1e1b4b,#312e81);padding:28px 36px;
border-bottom:1px solid var(--border)}
.header h1{font-size:24px;font-weight:700;letter-spacing:-.5px}
.header p{color:var(--muted);font-size:13px;margin-top:5px}
.main{max-width:1400px;margin:0 auto;padding:28px}
.step{background:var(--card);border-radius:14px;border:1px solid var(--border);
overflow:hidden;margin-bottom:8px}
.step-h{display:flex;align-items:center;gap:14px;padding:16px 22px;
border-bottom:1px solid var(--border);background:rgba(99,102,241,.05)}
.step-n{width:30px;height:30px;border-radius:50%;background:var(--accent);
color:#fff;display:flex;align-items:center;justify-content:center;
font-size:14px;font-weight:700;flex-shrink:0}
.step-t{font-size:16px;font-weight:600}
.step-ms{font-size:11px;color:var(--accent);font-family:monospace;
background:rgba(99,102,241,.12);padding:3px 10px;border-radius:4px;margin-left:auto}
.step-b{padding:20px 22px}
.algo{font-size:14px;margin-bottom:14px}
.algo strong{color:var(--accent)}
.algo code,.formula{font-family:'JetBrains Mono',monospace}
.algo code{background:rgba(99,102,241,.12);color:var(--accent);
padding:1px 6px;border-radius:4px;font-size:13px}
.formula{background:var(--bg);border:1px solid var(--border);padding:10px 16px;
border-radius:8px;margin:10px 0;font-size:13px;color:var(--accent);overflow-x:auto}
.why{background:rgba(245,158,11,.08);border-left:3px solid var(--warn);
padding:12px 16px;border-radius:0 8px 8px 0;margin:14px 0;font-size:13px;color:#fbbf24}
.why b{color:var(--warn)}
.hint{font-size:11px;color:var(--muted);margin:4px 0 8px;text-transform:uppercase;
letter-spacing:.5px}
.imgs{display:flex;flex-wrap:wrap;gap:14px;margin:14px 0}
.img-card{flex:1;min-width:200px;max-width:50%}
.img-card img{width:100%;border-radius:8px;display:block;background:#000;cursor:zoom-in}
.img-card .caption{text-align:center;font-size:12px;color:var(--muted);
margin-top:6px;font-weight:500}
.cmp{position:relative;overflow:hidden;border-radius:8px;cursor:ew-resize;
user-select:none;width:100%;margin:8px 0}
.cmp:focus{outline:2px solid var(--accent);outline-offset:2px}
.cmp img{display:block;width:100%}
.cmp-ov{position:absolute;top:0;left:0;height:100%;overflow:hidden}
.cmp-ov img{display:block;height:100%;width:auto;min-width:100%}
.cmp-dv{position:absolute;top:0;width:3px;height:100%;background:var(--accent);z-index:10}
.cmp-lab{position:absolute;top:8px;padding:2px 8px;font-size:11px;
background:rgba(0,0,0,.75);color:#fff;border-radius:4px;z-index:11}
.cmp-lab.l{left:8px}.cmp-lab.r{right:8px}
.metrics{display:flex;gap:14px;flex-wrap:wrap;padding:18px 22px;
background:rgba(99,102,241,.03)}
.metric{background:var(--bg);padding:12px 18px;border-radius:8px;
border:1px solid var(--border);min-width:130px}
.m-l{font-size:11px;color:var(--muted);text-transform:uppercase}
.m-v{font-size:20px;font-weight:700;font-family:monospace}
.m-v.pass{color:var(--ok)}.m-v.fail{color:var(--fail)}
.tm{margin-bottom:8px;font-size:12px}
.tm-r{display:flex;justify-content:space-between;color:var(--muted)}
.tm-bar{height:4px;background:var(--border);border-radius:2px;margin-top:3px}
.tm-bar>div{height:100%;background:var(--accent);border-radius:2px}
.arrow{text-align:center;color:var(--border);font-size:24px;margin:2px 0}
.lb{display:none;position:fixed;inset:0;background:rgba(0,0,0,.92);z-index:2000;
align-items:center;justify-content:center;cursor:zoom-out}
.lb.on{display:flex}.lb img{max-width:95vw;max-height:95vh;object-fit:contain}
@media(max-width:900px){.img-card{max-width:100%}}
"""

_JS = """
function lb(src){var b=document.getElementById('lb');
document.getElementById('lbimg').src=src;b.classList.add('on');}
document.addEventListener('DOMContentLoaded',function(){
 var lbx=document.getElementById('lb');
 lbx.onclick=function(){this.classList.remove('on');};
 document.addEventListener('keydown',function(e){
  if(e.key==='Escape')lbx.classList.remove('on');});
 document.querySelectorAll('.cmp').forEach(function(c){
  var ov=c.querySelector('.cmp-ov'),dv=c.querySelector('.cmp-dv'),drag=false;
  function setP(p){p=Math.max(0,Math.min(100,p));
   ov.style.width=p+'%';dv.style.left=p+'%';
   c.setAttribute('aria-valuenow',Math.round(p));}
  function set(x){var r=c.getBoundingClientRect();
   if(r.width>0)setP((x-r.left)/r.width*100);}
  c.addEventListener('mousedown',function(e){drag=true;set(e.clientX);});
  document.addEventListener('mousemove',function(e){if(drag)set(e.clientX);});
  document.addEventListener('mouseup',function(){drag=false;});
  c.addEventListener('touchstart',function(e){drag=true;set(e.touches[0].clientX);});
  c.addEventListener('touchmove',function(e){if(drag){e.preventDefault();
   set(e.touches[0].clientX);}});
  c.addEventListener('touchend',function(){drag=false;});
  c.addEventListener('keydown',function(e){
   if(e.key!=='ArrowLeft'&&e.key!=='ArrowRight')return;
   e.preventDefault();
   var cur=parseFloat(ov.style.width)||50;
   setP(cur+(e.key==='ArrowRight'?2:-2));});
 });
});
"""

_PAGE = """<!DOCTYPE html>
<html lang="{lang}"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title}</title><style>{css}</style></head>
<body>
<div class="header"><h1>{title}</h1><p>{subtitle}</p></div>
<div class="main">{body}</div>
<div class="lb" id="lb"><img id="lbimg" src=""></div>
<script>{js}</script>
</body></html>"""
