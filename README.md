# Canadian carrier referral programs — a verified, dated dataset

Every major Canadian mobile carrier's refer-a-friend programme, read from the
carrier's own website and published with the date it was checked.

**Last verified: 2026-09-01 · 8 carriers · 4 live, 4 discontinued**

Maintained alongside the human-readable version at
**<https://mobilereferrals.ca/carrier-referral-programs/>**

---

## Why this exists

Referral-code aggregators routinely publish programmes that no longer exist. At
the time of writing, several still advertise Virgin Plus and Fido referral
offers — **both ended in 2024–2025**. Nobody maintains a dated, sourced record,
so this is one.

The interesting finding is that **half the industry has left**. Bell closed both
of its flanker programmes on the same day. Rogers closed both of its own,
earlier and separately. Every surviving programme belongs to TELUS or Quebecor.

## The data

| Carrier | Parent | Status | New customer | Referrer |
|---|---|---|---|---|
| Fizz | Quebecor | live | $40 outside Quebec, $25 in Quebec | $25 |
| Koodo | TELUS | live | $25 as $5/mo × 5 months | same |
| Public Mobile | TELUS | live | $10 | 1 point per 30 days, uncapped |
| Freedom Mobile | Quebecor | live | $25 | $25, capped at $250/yr |
| chatr | Rogers | **ended 31 May 2023** | — | — |
| Fido | Rogers | **ended 2 July 2024** | — | — |
| Lucky Mobile | Bell | **ended 9 June 2025** | — | — |
| Virgin Plus | Bell | **ended 9 June 2025** | — | — |

Full detail — payout timing, plan minimums, caps, and whether a forgotten code
can be recovered — is in the JSON and CSV.

## Files

- [`carrier-referral-programs.json`](carrier-referral-programs.json) — full records with source URLs
- [`carrier-referral-programs.csv`](carrier-referral-programs.csv) — same data, flat

## Method

1. Amounts are read from **the carrier's own** website or support documentation.
   Never from a coupon site or a referral aggregator.
2. Every record carries the `source` URL it was read from.
3. Where a carrier's own pages contradict each other, that is recorded rather
   than resolved. Fizz is the live example: its programme page says $25 in every
   region while its plan pages say $40 outside Quebec.
4. Anything that could not be confirmed is left blank. **A blank cell is
   publishable; a plausible guess is not.**

Every figure here was adversarially re-checked before publication — three of the
original records were rejected and re-verified rather than shipped.

## Known limits

- **Amounts change without notice.** Check the carrier's own page before acting.
- Public Mobile's referrer reward is 1 Public Point per 30 days. The commonly
  quoted "1 point = $1" appears on **no current Public Mobile page** — its only
  source is a staff forum post from January 2022, so the dollar value is
  deliberately not asserted here.
- Freedom Mobile has **no shareable referral code**. Its programme is invite-only
  and its terms permit referring only "individuals with whom you have a personal
  relationship", so it cannot be used the way the others can.

## Corrections

Open an issue, or email hello@mobilereferrals.ca. Corrections get fixed and
logged with a date rather than quietly edited.

## Licence

[CC BY 4.0](LICENSE) — use it freely, credit
[MobileReferrals.ca](https://mobilereferrals.ca/carrier-referral-programs/).

## Disclosure

Maintained by [MobileReferrals.ca](https://mobilereferrals.ca/), an independent
site that publishes guides to these programmes and shares referral codes for two
of them. Not affiliated with, endorsed by, or sponsored by any carrier. The
dataset states what each carrier publishes, including for programmes we earn
nothing from.
