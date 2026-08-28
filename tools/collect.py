#!/usr/bin/env python3
"""A federated tick-network node: this repo's own append-only chain, keyed to the
global tick spine at kody-w/dogg.

Unlike a live-data node (spot prices, FX, fees), this node's "source" is a TEMPLATE:
a rendezvous (muster) plan whose real values — where to gather, who holds which role,
when to check in — are never public. Every value here is a PLACEHOLDER string. What
this chain proves is the SHAPE of a muster plan and its cadence, keyed to the same
global clock every other node uses, so an heirloom kit (paper or offline) can be built
from a known-good, versioned template instead of improvised under stress.

Every run reads the spine's current tick anchor and, if this node hasn't already
recorded that tick, appends one frame carrying the template. Frames verify with the
reference implementation (tools/rapp.py, from kody-w/rapp-1); CI re-verifies the whole
chain on every push.
"""
import json, sys, pathlib, datetime, urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import rapp as R
import chainio

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPINE_HEAD = "https://raw.githubusercontent.com/kody-w/dogg/main/ticks/HEAD.json"
TIMEOUT = 8

# ---- edit these three for your node -------------------------------------------------
THEME = "muster"                      # also the data directory name
STREAM = "muster:@kody-w/dogg-muster"                    # your stream id (your repo, your name)
# This node has no external SOURCES — the payload is a static template, not fetched
# data. rapp/1 canonical hashing forbids floats: numeric facts ride as strings or ints.
# -------------------------------------------------------------------------------------

def utc():
    n = datetime.datetime.now(datetime.timezone.utc)
    return n.strftime("%Y-%m-%dT%H:%M:%S.") + f"{n.microsecond // 1000:03d}Z"

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": f"tick-node-{THEME}"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode())

def muster_plan():
    """The TEMPLATE. Every personal value is a PLACEHOLDER string — see README.
    A real plan (real coordinates, real names, real channels) belongs in a private
    kit, never in this public repo."""
    return {
        "version": 1,
        "muster_points": [
            {"name": "PLACEHOLDER_POINT_PRIMARY", "what3words_or_coords": "PLACEHOLDER", "order": 1},
            {"name": "PLACEHOLDER_POINT_SECONDARY", "what3words_or_coords": "PLACEHOLDER", "order": 2},
            {"name": "PLACEHOLDER_POINT_FALLBACK", "what3words_or_coords": "PLACEHOLDER", "order": 3},
        ],
        "roles": [
            {"role": "PLACEHOLDER_ROLE_LEAD", "holder": "PLACEHOLDER"},
            {"role": "PLACEHOLDER_ROLE_NAVIGATOR", "holder": "PLACEHOLDER"},
            {"role": "PLACEHOLDER_ROLE_COMMS", "holder": "PLACEHOLDER"},
            {"role": "PLACEHOLDER_ROLE_MEDICAL", "holder": "PLACEHOLDER"},
        ],
        "check_in_windows_hours": [0, 6, 12, 18],
        "comms_fallback": [
            "PLACEHOLDER_CHANNEL_PRIMARY",
            "PLACEHOLDER_CHANNEL_SECONDARY",
            "PLACEHOLDER_CHANNEL_LAST_RESORT",
        ],
    }

def load_chain(d):
    return chainio.load_chain(d)

def main():
    spine = get(SPINE_HEAD)
    tick_n, tick_hash = spine["count"] - 1, spine["head_frame"]
    d = ROOT / THEME
    d.mkdir(exist_ok=True)
    chain = load_chain(d)
    head = chain[-1] if chain else None
    if head is not None and head["payload"].get("tick") == tick_n:
        print(f"{THEME}: tick {tick_n} already recorded — nothing to do")
        return
    plan = muster_plan()
    payload = {"tick": tick_n, "tick_frame": tick_hash, "spine": "kody-w/dogg",
               "fetched_utc": utc(), "plan": plan}
    if head is None:
        payload["about"] = (f"A federated node of the global tick network: a TEMPLATE "
                            f"{THEME} (rendezvous) plan, one frame per observed tick, "
                            "keyed to the spine's tick anchors so it joins every other "
                            "node's data on the same clock. Every value is a "
                            "PLACEHOLDER — see README.")
    f = R.build_frame(f"{THEME}.snapshot", STREAM, (head["seq"] + 1) if head else 0,
                      utc(), payload, prev=(head["payload_hash"] if head else None))
    ok, step, why = R.verify_frame(f, head=head, stream_id_of_record=STREAM)
    if not ok:
        raise ValueError(f"refusing invalid frame: {step}: {why}")
    chainio.append_frame(d, f, STREAM)
    print(f"{THEME} frame {f['seq']} @ spine tick {tick_n}: "
          f"{len(plan['muster_points'])} points, {len(plan['roles'])} roles")

if __name__ == "__main__":
    main()
