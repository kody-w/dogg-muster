# dogg-muster — a federated node of the global tick network

**A TEMPLATE rendezvous (muster) plan: where to gather, who holds which role, when to check in, and what to fall back to — with every real value replaced by a PLACEHOLDER.**

This repo keeps its own append-only chain of rapp/1 frames in `muster/`. Once a day a
GitHub Action reads the current tick anchor from the spine at
[kody-w/dogg](https://github.com/kody-w/dogg) and appends one frame carrying this
node's muster template, referencing that tick — so this chain joins every other node's
data on the same clock.

## What this actually carries

Every frame's `payload.plan` has the same shape:

- `version` — the template's revision number.
- `muster_points[]` — `{name, what3words_or_coords, order}`, an ordered list of
  gathering points (primary, secondary, fallback).
- `roles[]` — `{role, holder}`, who is responsible for what.
- `check_in_windows_hours[]` — the hours (0–23, UTC) a check-in is expected.
- `comms_fallback[]` — an ordered list of communication channels to try in order.

**Every `what3words_or_coords`, every `holder`, and every entry in `comms_fallback` is
the literal string `PLACEHOLDER`.** This repo is public. A real muster plan — real
coordinates, real names, real family members, real radio channels — is exactly the
kind of data that should never sit in a public GitHub repo tied to a real identity.
**Real plans belong in a private kit** (a printed card, an encrypted local file, a
device that never leaves your control) — never here.

## Why it matters offline / for heirlooms

A rendezvous plan is only useful if it has a known-good *shape* everyone agreed on
*before* the day it's needed — and if that shape can be checked, versioned, and handed
down without depending on any app staying online. This chain is the versioned,
tick-anchored, cryptographically self-verifying *shape*: an heirloom kit can fork this
repo, swap every `PLACEHOLDER` for a real value in a private copy, print it, and still
be able to prove — offline, years later — that the shape it printed matches a specific
tick on a specific day, using nothing but `tools/rapp.py` and arithmetic. The public
chain proves the template never silently drifted; it proves nothing about, and holds
nothing of, anyone's actual plan.

## Precision and limits

- **Precision:** exact. There is no live data source here to be noisy or stale — the
  template is either present and byte-identical to what was hashed, or the frame fails
  to verify.
- **Limits:** this is a *shape*, not a plan. It carries zero real coordinates, zero
  real names, zero real schedules. It cannot be used to find anyone or coordinate a
  real rendezvous as-is — by design. Turning it into something usable requires a
  private step this repo deliberately does not take.
- **Cadence:** one frame per day (if the spine tick has advanced since the last one),
  not one per tick — a template doesn't need the density a live-data node does.

**Verify it yourself:** `python3 tools/verify_thread.py` re-checks every frame with the
reference implementation from [kody-w/rapp-1](https://github.com/kody-w/rapp-1). CI runs
the same oracle on every push.

**Start your own node:** fork this repo, edit `THEME` / `STREAM` / the template
function at the top of `tools/collect.py`, and enable the scheduled workflow. Your
chain, your outlook, same clock — announce it on the spine's registry
([kody-w/dogg](https://github.com/kody-w/dogg) issues) so agents can find it.

## Trust

<!--trust-->
No ratings yet — used this chain? [Rate it](../../issues/new?template=rate.yml): valid ratings publish automatically as verifiable frames.
<!--/trust-->
