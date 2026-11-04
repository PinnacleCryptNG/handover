# ledger-sync handover

## Summary

ledger-sync moves settled card payments from the processor into the finance ledger every night. (README.md:3). Owner: Ada Okafor. Successor: Ben.

## What you own

- **ledger-sync** (this repo). No other solo-owned systems. (Ada, interview)
- Downstream consumers:
  - **Finance controllers** reconcile from the ledger every morning at 8am. (Ada, interview)
  - **Treasury** reads the month-end report. (Ada, interview)

## Schedule

| Job | Cron | Source |
|-----|------|--------|
| Nightly sync | 02:15 UTC (`15 2 * * *`) | (ops/crontab:2) |
| Month-end report | 06:00 UTC on the 1st (`0 6 1 * *`) | (ops/crontab:3) |

- Finance reads the month-end report at 9am on the 1st. (Ada, interview)
- **Quarterly:** email Treasury the FX fallback count by hand. Not automated. (Ada, interview)

## When it breaks

**Symptom:** Finance pings that the ledger is empty for yesterday. Check the job log on `batch-01` — usually shows a 429 from the processor. (Ada, interview; ops/RUNBOOK.md:3)

**Last incident:** September — processor rate-limited until ~02:30 UTC, so the 02:15 run failed. Fix: wait until after 02:30, then re-run with `--date <missed-day>`. Never omit `--date` or the job defaults to yesterday and will double-post. (Ada, interview)

**Planned mitigation:** Ada intended to move the cron from 02:15 to 02:45 but never did. (Ada, interview)

**Month-end recovery:** If the sync fails on the last night of the month, re-run that day's sync first (`--date <last-day>`), then run the month-end report by hand. (Ada, interview)

## Access and contacts

**Secrets** (all in team vault under `ledger-sync`): (Ada, interview)
- `PROCESSOR_TOKEN`
- `LEDGER_URL` credentials
- `batch-01` SSH key

**Escalation:**
- Processor outages → support desk (account manager contact in vault note). (Ada, interview)
- Ledger API outages → Finance Systems on-call. (Ada, interview)

**Credential rotation:** Processor token expires every 90 days; next rotation is **15 December** — assigned to Ben, done by hand. (Ada, interview; manager edit)
- **Quarterly FX fallback email** to Treasury also assigned to Ben. (manager edit)

## Open work

1. **Half-done branch** to remove the FX fallback (`FX_FALLBACK_RATE = 1.0`) once Treasury's new FX feed is live. Blocked on Treasury. (Ada, interview; src/sync.js:4)
2. **Promise to controllers lead (Priya Shah):** month-end report will include a **separate refunds section, netted per merchant**, starting with the **December close on 1 January**. Not started. (Ada, interview)
3. **RUNBOOK.md line 8** has a TODO for the month-end report section. (ops/RUNBOOK.md:8)

## Gotchas

- **Ledger batch size** is hard-coded at 500 entries; the ledger returns HTTP 413 if exceeded. (Ada, interview; src/sync.js:16)
- **Never re-run without `--date`**: the job defaults to `yesterday`, and if yesterday already landed it will double-post. (Ada, interview)
- **Never run the month-end report** before confirming the last day's sync has landed in the ledger. (Ada, interview)
- **Rate-limit retry window:** the source code assumes processor rate limits lift after 02:30 UTC. (src/sync.js:10)

## Open questions

- Where is Treasury's new FX feed tracked / who is the contact for unblocking the FX fallback removal branch?
