"""
Static TFLite runtime-envelope gate — flatbuffer op-dump.

Given a candidate model and one or more TARGET RUNTIME ENVELOPES, decide PASS / REJECT
**statically**, without loading the model in any TFLite runtime. An envelope is a target
runtime version V: the model PASSES that envelope iff it uses NO custom ops AND its declared
`min_runtime_version` is <= V. The model's overall verdict is the AND over all envelopes asked
for (e.g. a host runtime and a device runtime).

WHY STATIC (not interpreter `_get_ops_details()`): a custom op is exactly what can stop an
interpreter from loading (unresolved-custom-op at allocate) — so an interpreter-based detector
can choke on the very case the gate exists to catch. We parse the TFLite flatbuffer directly:
OperatorCode table -> custom ops; Model.metadata -> min_runtime_version. This works whether or
not a kernel is registered, and needs no TensorFlow runtime installed.

A `.task` (MediaPipe Tasks bundle) is a ZIP of inner .tflite(s) + metadata — we unzip and parse
each inner model; the candidate's verdict is the AND over inner models.

Usage:
    python envelope_gate.py <model.tflite | bundle.task> \
        --envelope <name>=<version> [--envelope <name>=<version> ...] [--json]

    # examples (version strings are caller values, not baked in):
    #   --envelope host=2.1.0                  one envelope
    #   --envelope host=2.1.0 --envelope device=2.10.0   two envelopes, AND'd

Output: per-model op list + min_runtime_version + per-envelope verdict, and an overall verdict
(PASS / REJECTED-envelope) with the offending ops/version listed.

Exit codes: 0 = PASS · 1 = REJECTED-envelope · 2 = parse-suspect (refused to stamp a verdict).

Requirements (no tensorflow): pip install tflite flatbuffers
"""

import argparse
import json
import os
import sys
import zipfile

from tflite.Model import Model


def _parse_version(s):
    """'2.1.0' -> (2,1,0); tolerant of missing/extra components. None if unparseable."""
    if not s:
        return None
    parts = []
    for tok in str(s).strip().split("."):
        digits = "".join(ch for ch in tok if ch.isdigit())
        if digits == "":
            break
        parts.append(int(digits))
    return tuple(parts) if parts else None


def _version_le(a, b):
    """a <= b with component-wise comparison; missing components treated as 0."""
    n = max(len(a), len(b))
    a = a + (0,) * (n - len(a))
    b = b + (0,) * (n - len(b))
    return a <= b


def parse_envelopes(specs):
    """['host=2.1.0', 'device=2.10'] -> [('host',(2,1,0)), ('device',(2,10))]."""
    out = []
    for spec in specs:
        if "=" not in spec:
            raise ValueError("envelope must be name=version, got: {!r}".format(spec))
        name, ver = spec.split("=", 1)
        parsed = _parse_version(ver)
        if parsed is None:
            raise ValueError("unparseable envelope version: {!r}".format(spec))
        out.append((name.strip(), parsed, ver.strip()))
    return out


def dump_tflite_bytes(buf, name, envelopes):
    """Static parse of one .tflite flatbuffer against each envelope. Returns a record dict."""
    model = Model.GetRootAsModel(bytearray(buf), 0)

    # --- OperatorCodes: collect builtin ids + any custom op names ---
    builtin_ops = set()
    custom_ops = []
    n_codes = model.OperatorCodesLength()
    for i in range(n_codes):
        oc = model.OperatorCodes(i)
        # A non-empty custom_code string is the definitive custom-op signal (robust across
        # schema versions). CUSTOM is enum 32 in the TFLite schema.
        custom_code = oc.CustomCode()
        if custom_code is not None and len(custom_code) > 0:
            custom_ops.append(custom_code.decode("utf-8", "replace"))
        else:
            # DeprecatedBuiltinCode for older models; BuiltinCode for newer.
            bc = oc.BuiltinCode()
            if bc == 32:  # BuiltinOperator.CUSTOM
                custom_ops.append("<custom:unnamed>")
            else:
                builtin_ops.add(int(bc))

    # --- min_runtime_version from Model.metadata (key -> buffer holding the string) ---
    min_rt_raw = None
    n_meta = model.MetadataLength()
    for i in range(n_meta):
        md = model.Metadata(i)
        key = md.Name()
        if key is not None and key.decode("utf-8", "replace") == "min_runtime_version":
            buf_idx = md.Buffer()
            b = model.Buffers(buf_idx)
            data = b.DataAsNumpy() if b.DataLength() > 0 else None
            if data is not None:
                # stored as a null-terminated ascii string in the buffer
                min_rt_raw = bytes(data).split(b"\x00", 1)[0].decode("ascii", "replace")
            break

    min_rt = _parse_version(min_rt_raw)
    has_custom = len(custom_ops) > 0

    # one verdict per requested envelope: PASS iff no custom op AND min_rt <= target.
    # An unknown (missing/unparseable) min_runtime_version CANNOT certify PASS — fail closed.
    env_results = {}
    for env_name, env_ver, env_raw in envelopes:
        version_ok = (min_rt is not None) and _version_le(min_rt, env_ver)
        env_pass = (not has_custom) and version_ok
        reasons = []
        if has_custom:
            reasons.append("custom op(s): " + ", ".join(custom_ops))
        if not version_ok:
            reasons.append("min_runtime_version={} > {}".format(
                min_rt_raw if min_rt_raw else "MISSING", env_raw))
        env_results[env_name] = {
            "target_version": env_raw,
            "verdict": "PASS" if env_pass else "FAIL",
            "fail_reasons": reasons,
        }

    return {
        "inner_model": name,
        "n_operator_codes": n_codes,
        "builtin_op_count": len(builtin_ops),
        "custom_ops": custom_ops,
        "min_runtime_version": min_rt_raw,
        "envelopes": env_results,
    }


def dump_candidate(path, envelopes):
    """Dispatch on extension: .task is a zip of inner .tflite(s); .tflite is parsed directly."""
    records = []
    if path.lower().endswith(".task"):
        with zipfile.ZipFile(path, "r") as zf:
            inner = [n for n in zf.namelist() if n.lower().endswith(".tflite")]
            if not inner:
                raise ValueError(".task bundle has no inner .tflite: {}".format(path))
            for n in inner:
                records.append(dump_tflite_bytes(zf.read(n), n, envelopes))
    else:
        with open(path, "rb") as f:
            records.append(dump_tflite_bytes(f.read(), os.path.basename(path), envelopes))
    return records


def main():
    ap = argparse.ArgumentParser(
        description="Static TFLite runtime-envelope gate (op-dump).")
    ap.add_argument("model", help="path to .tflite or .task")
    ap.add_argument("--envelope", "-e", action="append", default=[], metavar="NAME=VERSION",
                    help="target runtime envelope, repeatable (e.g. host=2.1.0 device=2.10.0)")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = ap.parse_args()

    if not args.envelope:
        ap.error("at least one --envelope NAME=VERSION is required")
    envelopes = parse_envelopes(args.envelope)
    env_names = [e[0] for e in envelopes]

    records = dump_candidate(args.model, envelopes)

    # candidate verdict per envelope = AND over inner models; overall = AND over envelopes.
    per_env = {}
    for name in env_names:
        per_env[name] = "PASS" if all(
            r["envelopes"][name]["verdict"] == "PASS" for r in records) else "FAIL"
    verdict = "PASS" if all(v == "PASS" for v in per_env.values()) else "REJECTED-envelope"

    # self-test guard: a parse that found zero operator-codes is suspect (wrong table / corrupt
    # read) — refuse to stamp a verdict on it (avoids a false PASS).
    suspect = [r["inner_model"] for r in records if r["n_operator_codes"] == 0]

    result = {
        "candidate": os.path.basename(args.model),
        "verdict": verdict,
        "envelopes": per_env,
        "inner_models": records,
        "parse_suspect": suspect,
    }

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("candidate : {}".format(result["candidate"]))
        print("verdict   : {}".format(verdict))
        print("envelopes : {}".format(
            "  ".join("{}={}".format(k, v) for k, v in per_env.items())))
        for r in records:
            print("  - {}".format(r["inner_model"]))
            print("      operator_codes={} builtins={} custom={}".format(
                r["n_operator_codes"], r["builtin_op_count"], r["custom_ops"] or "none"))
            print("      min_runtime_version={}".format(r["min_runtime_version"]))
            for name in env_names:
                er = r["envelopes"][name]
                line = "      {} (<= {}): {}".format(name, er["target_version"], er["verdict"])
                if er["fail_reasons"]:
                    line += "  [" + "; ".join(er["fail_reasons"]) + "]"
                print(line)
        if suspect:
            print("WARNING parse-suspect (0 operator codes): {} — DO NOT stamp verdict".format(
                suspect))

    if suspect:
        sys.exit(2)
    sys.exit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
