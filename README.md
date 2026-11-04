# Handover

When someone leaves a team, what they know usually leaves with them. Handover turns that
exit into a short, checked conversation in your team chat:

1. An **Interviewer** agent reads the system being handed over, then interviews the
   departing teammate one question at a time.
2. A **Scribe** agent checks every answer against the code, cron files and runbooks, and
   flags what the interview missed ("`ops/RUNBOOK.md` line 8 is a TODO").
3. The Scribe writes `HANDOVER.md`, with a source for every fact, and asks the **manager**
   to approve it in chat.
4. Once approved, the guide is published to the successor's room, where a **Buddy** agent
   answers their questions from it. When the guide has no answer, the Buddy asks the
   departing teammate in the other room and brings the answer back.

Built for the [Flip the Switch hackathon](https://www.wemakedevs.org/hackathons/switch)
(Best Business Workflow) on [Switch](https://github.com/sandbox-quantum/switch).

## Who is in which room

| Room | People | Agents |
| --- | --- | --- |
| `{slug}-handover` | departing teammate, manager | Interviewer, Scribe, Buddy |
| `{slug}-onboarding` | successor, manager | Buddy, Scribe |

The two rooms are linked, so the Buddy and the Scribe can carry questions and answers
between them. Everything is one Switch template:
[`templates/handover.template.yaml`](templates/handover.template.yaml).

## What Switch does here

- **Template** creates three agents, two rooms, a room group, the links and the kickoff
  messages in one go.
- **Rooms and addressing**: humans and agents talk by `@mention` in normal Mattermost
  channels (Slack, Teams, Discord and Telegram work the same way).
- **Linked rooms** let the Buddy route a question from the successor to the leaver.
- **Room documents**: the approved guide becomes the "Handover guide" document of the
  onboarding room, so every agent and person there reads the same text.
- **Shared working directory**: all three agents run in the folder being handed over, so
  the Scribe can cite file and line.

## Run it

You need [Switch Console](https://github.com/sandbox-quantum/switch/releases) and Docker.

1. Open Switch Console, choose **Run a local server**. It starts Switch and a Mattermost
   instance on your machine.
2. Set up an agent provider. This repo was built with
   [OpenCode](https://opencode.ai) on Nebius Token Factory; copy
   [`config/opencode.json`](config/opencode.json) to `~/.config/opencode/opencode.json`
   and export your Nebius key as `OPENAI_API_KEY` before starting Console. Claude Code or
   Codex also work (pick them under *Advanced* when you use the template).
3. Create three Mattermost users for the demo (or use real teammates):
   ```bash
   C=$(docker ps --format '{{.Names}}' | grep mattermost)
   for u in ada ben maya; do
     docker exec $C mmctl --local user create --username $u --email $u@example.com --password "<choose one>"
     docker exec $C mmctl --local team users add switch $u
   done
   ```
4. In Console: **Templates → Import template**, pick `templates/handover.template.yaml`,
   then **Use template**. Set *System folder* to the absolute path of
   [`workspace/ledger-sync`](workspace/ledger-sync) (or your own system) and **Create all**.
5. Sign in to Mattermost as `ada` and answer the Interviewer. Sign in as `maya` to approve
   the guide, and as `ben` to ask the Buddy questions.

[`scripts/mm.py`](scripts/mm.py) posts and reads messages as a given user through the
Mattermost API, which is handy for replaying the demo.

## Sample system

[`workspace/ledger-sync`](workspace/ledger-sync) is a small, made-up nightly payments sync
with the kind of gaps real systems have: a month-end cron job the runbook marks TODO, a
hard-coded FX fallback, a rate-limit workaround nobody wrote down.

## Notes

- Agents never ask for or repeat secret values; the guide names where secrets live.
- Every fact in the guide cites its source; anything unconfirmed goes under
  *Open questions* instead of being guessed.
