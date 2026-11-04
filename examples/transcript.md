# Example run: ledger-sync

Full Mattermost transcript of one run with the sample system. Ada is leaving, Maya is the manager, Ben takes over.

## ledger-sync-handover

**Switch (template kickoff)**

> @ledger-sync-interviewer @ada is leaving and hands ledger-sync over to
> @ben. Read the system folder, then greet @ada in one line
> and ask your first question.

**ledger-sync-interviewer**

> @ada Hi Ada. You own ledger-sync — who downstream depends on it running each night, and is there anything else you maintain?

**ada**

> @ledger-sync-interviewer Finance is the big one: the controllers team reconciles from the ledger every morning at 8, so if the sync hasn't landed by then they're blind. Treasury also reads the month-end report. Apart from ledger-sync I don't maintain anything else on my own.

**ledger-sync-interviewer**

> @ledger-sync-scribe Ada owns ledger-sync; Finance controllers reconcile from it at 8am daily, and Treasury reads the month-end report. Nothing else owned solo.

**ledger-sync-interviewer**

> @ada I see the nightly sync at 02:15 and month-end report at 06:00 on the 1st in the crontab. Are there any other recurring deadlines or check-ins I should know about?

**ledger-sync-scribe**

> @ledger-sync-interviewer ops/RUNBOOK.md line 8 has a TODO for the month-end report section — not yet covered.

**ledger-sync-scribe**

> @ledger-sync-interviewer src/sync.js line 4 has a `TODO(ada): remove once the FX feed is stable` around a hard-coded `FX_FALLBACK_RATE = 1.0` — not yet covered.

**ledger-sync-scribe**

> @ledger-sync-interviewer src/sync.js line 10 throws a rate-limit error with a fixed retry-after of 02:30 UTC — not yet covered.

**ledger-sync-scribe**

> @ledger-sync-interviewer src/sync.js line 16 hard-codes a ledger batch size limit of 500 entries — not yet covered.

**ada**

> @ledger-sync-interviewer The month-end report is the one that bites. Finance reads it at 9 on the 1st, but it needs the last day's settlements, so if the 02:15 sync fails on the last night of the month you have to re-run the sync first and then the report by hand. Also each quarter-end I send Treasury the FX fallback count by email, that's not automated at all.

**ledger-sync-interviewer**

> @ledger-sync-scribe Recurring deadlines: nightly sync at 02:15, month-end report at 06:00 on 1st (Finance reads at 9am, depends on last night’s settlements), and quarterly FX fallback count email to Treasury by hand.

**ledger-sync-interviewer**

> @ada Got it. Speaking of failures: when the sync breaks, what symptom shows up first, and what was the last real incident you had to fix?

**ada**

> @ledger-sync-interviewer First symptom is usually Finance pinging that the ledger is empty for yesterday; the job log on batch-01 shows a 429 from the processor. Last real one was in September: the processor rate-limits us until about 02:30 UTC, so the 02:15 run died. Fix was to wait until after 02:30 and re-run with --date for the missed day. I keep meaning to move the cron to 02:45 but never did.

**ledger-sync-interviewer**

> @ledger-sync-scribe Failure symptom: Finance notices ledger empty for yesterday; batch-01 log shows 429 from processor. Last incident: Sep, rate-limit at 02:15, fixed by waiting until after 02:30 and re-running --date. Ada intended to move cron to 02:45 but hasn't.

**ledger-sync-interviewer**

> @ada On access and vendors: what secrets or credentials does this system rely on, and who should Ben call if the processor or ledger API is down?

**ada**

> @ledger-sync-interviewer Three secrets, all in the team vault under ledger-sync: PROCESSOR_TOKEN, LEDGER_URL creds and the batch-01 SSH key. Processor outages go to their support desk, our account manager is in the vault note. For the ledger, page the Finance Systems on-call. Heads up: the processor token expires every 90 days and the next rotation is due on 15 December. I always did it by hand.

**ledger-sync-interviewer**

> @ledger-sync-scribe Access and vendors: three secrets in team vault (PROCESSOR_TOKEN, LEDGER_URL creds, batch-01 SSH key). Processor outages → support desk (account manager in vault note). Ledger outages → Finance Systems on-call. Processor token rotates every 90 days, next due 15 Dec, done manually.

**ledger-sync-interviewer**

> @ada What work is currently in progress, and have you made any promises to Finance, Treasury or anyone else that Ben needs to keep?

**ada**

> @ledger-sync-interviewer In progress: a half-done branch to drop the FX fallback once Treasury's new FX feed is live, it's blocked on them. Promise: I told the controllers lead the month-end report would include refunds starting with the December close. That's not started.

**ledger-sync-interviewer**

> @ledger-sync-scribe Work in progress: half-done branch to drop FX fallback, blocked on Treasury's new FX feed. Promise to controllers lead: month-end report will include refunds starting December close — not started yet.

**ledger-sync-interviewer**

> @ada Last question: what quirks or workarounds should Ben know? I noticed the ledger batch size is capped at 500 entries — is that a real hard limit — and are there any "never do X" rules?

**ada**

> @ledger-sync-interviewer Yes, 500 is a hard limit, the ledger returns 413 above it. Never re-run a day without --date: it defaults to yesterday and will double-post if yesterday already landed. And never run the month-end report before the last day's sync is confirmed in the ledger.

**ledger-sync-interviewer**

> @ledger-sync-scribe Quirks: ledger batch size of 500 is a hard limit — returns 413 if exceeded. Never re-run a day without `--date` or it defaults to yesterday and double-posts. Never run month-end report before last day's sync is confirmed landed.

**ledger-sync-interviewer**

> @ledger-sync-scribe Interview complete

**ledger-sync-interviewer**

> @ada Thanks Ada — that's everything. Good luck!

**ledger-sync-scribe**

> Handover guide is ready. Summary: Ada owns ledger-sync only; Finance reconciles daily at 8am, Treasury reads month-end on 1st. Failure mode is 429 from processor (fixed by waiting until after 02:30). Secrets in team vault (PROCESSOR_TOKEN rot due 15 Dec). Open work: FX fallback branch blocked on Treasury, and a promise to add refunds to month-end report by December close. Full guide written.
>
> @maya please reply "approve" or tell me what to change.

**maya**

> @ledger-sync-scribe Looks good. Two changes: under When it breaks, add the month-end recovery Ada described (if the last night of the month fails, re-run that day's sync first, then the report by hand). And make Ben the owner of the 15 December token rotation and the quarter-end FX email.

**ledger-sync-scribe**

> Changes applied:
> 1. Added month-end recovery steps under "When it breaks" (re-run last-day sync first, then report by hand).
> 2. Assigned the 15 December token rotation and quarterly FX fallback email to Ben.
>
> @maya please reply "approve" or tell me what else to change.

**maya**

> @ledger-sync-scribe approve

**ledger-sync-buddy**

> @ada @ada — Ben (your successor) has two questions that weren't captured in the handover document:
>
> 1. **How do you re-run the nightly sync safely when it fails?** (I can infer: re-run with `--date <missed-day>`, but want confirmation from you.)
>
> 2. **Who is the controllers lead you promised the refunds-in-month-end-report change to, and what exactly do they expect in the report?**
>
> Could you answer both? I'll forward them to Ben in the onboarding room.

**ada**

> @ledger-sync-buddy 1) Yes, re-run with --date for the missed day, after 02:30 UTC. 2) The controllers lead is Priya Shah. She wants refunds as a separate section in the month-end report, netted per merchant, starting with the December close on 1 January.

**ledger-sync-buddy**

> Thanks Ada — passing both answers to Ben and updating the guide.

## ledger-sync-onboarding

**Switch (template kickoff)**

> @ledger-sync-buddy greet @ben in two lines: the guide arrives here
> once @maya approves it, and they can ask you anything meanwhile.

**ledger-sync-buddy**

> Hi @ben! The handover guide will arrive here once @maya has approved it.
>
> Feel free to ask me anything in the meantime — I'm here to help.

**ledger-sync-scribe**

> 📄 created room document “Handover guide”.

**ledger-sync-scribe**

> @ben @ben the handover guide for ledger-sync is ready in this room as a document called "Handover guide". It covers what you own, the daily and monthly schedule, how to fix failures, access and contacts, open work, and gotchas. Welcome aboard — tag me if you have questions.

**ben**

> @ledger-sync-buddy Two questions. 1) The sync failed last night, how do I re-run it safely? 2) Who is the controllers lead I made the refunds promise to, and what exactly do they expect in the report?

**ledger-sync-buddy**

> Hi @ben — here are the answers I have from the handover guide and files.
>
> **1) Re-running the sync safely after a failure**
> Check the job log on `batch-01`. The usual cause is a processor `429` rate-limit (which lifts after ~02:30 UTC). 
> - **Safe re-run:** `node /srv/ledger-sync/src/run.js --date <missed-day>`
> - ⚠️ **Never omit `--date`.** Without it the job defaults to `yesterday`; if yesterday already landed, it will double-post. (ops/crontab:2; HANDOVER.md:28,57–58)
>
> **2) Controllers lead & refunds-in-report promise**
> The guide records Ada's promise — "month-end report will include refunds starting with the December close" — but it **does not name the controllers lead or detail the expected format**. (HANDOVER.md:52; Open questions:63)
>
> I've just asked Ada directly in the handover room to get you the exact contact and expectations. I'll relay it here the moment she replies.

**ledger-sync-buddy**

> Hi @ben — Ada replied in the handover room. Here are the answers:
>
> 1) **Re-running the sync safely after a failure**
> Re-run with `--date <missed-day>` after **02:30 UTC**. Never omit `--date` or the job defaults to yesterday and will double-post. (Ada, handover room context)
>
> 2) **Controllers lead & refunds promise**
> The controllers lead is **Priya Shah**. She wants refunds as a **separate section in the month-end report, netted per merchant**, starting with the **December close on 1 January**. (Ada, handover room context)
>
> That's everything — let me know if you need anything else!

**ledger-sync-buddy**

> @ledger-sync-scribe New facts from Ada's reply in the handover room to update the "Handover guide":
>
> 1. **Re-running the sync safely after a failure:** Re-run with `--date <missed-day>` after **02:30 UTC**. Never omit `--date` or the job defaults to yesterday and will double-post.
>
> 2. **Controllers lead & refunds promise:** The controllers lead is **Priya Shah**. She wants refunds as a **separate section in the month-end report, netted per merchant**, starting with the **December close on 1 January**.
>
> These are the exact answers relayed to @ben. Please update the guide accordingly.

**ledger-sync-scribe**

> 📄 updated room document “Handover guide”.

