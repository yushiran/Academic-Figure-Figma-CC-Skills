# Figma MCP setup — guided tutorial + reference

## Tutorial: from zero to drawing-ready (Claude leads)

Run this as a state machine, top to bottom. **Verify each step before advancing**;
report progress to the user in plain language at every step. Division of labour:
Claude runs tools and verifies; the user does browser actions (authorise, change
seat) with exact click-paths supplied.

### Step 1 — Detect the MCP server

ToolSearch for "figma". Tools like `use_figma` / `whoami` present → Step 2.

Absent → have the user (or run via Bash) install the plugin:
```bash
claude plugin install figma@claude-plugins-official
```
The MCP server connects at session start, so after a fresh install the user must
**restart the session** ("/exit and reopen, then say: continue Figma setup").
Already installed but tools missing → same restart advice.

### Step 2 — OAuth

Call `authenticate` → it returns a `figma.com/oauth/mcp?...` URL. Tell the user:
open it in a browser and approve.

**Remote/SSH sessions (cluster, devbox):** after approving, the browser lands on
`http://localhost:3118/callback?...` and shows a connection error — **this is
expected, not a failure**. The user copies the FULL callback URL from the address
bar and pastes it into chat; call `complete_authentication` with it.

Local sessions complete automatically. Either way, verify: Step 3.

### Step 3 — Verify seat and plan (`whoami`, quota-exempt, use freely)

`whoami` returns handle, email, and per-plan `seat` + `tier`. Decision:

| whoami says | Action |
|---|---|
| seat **Full**/Dev, tier professional/organization/enterprise/**student** | ✅ 200/day — go to Step 4 |
| seat **View**/Collab (ANY tier) | ❌ 6 calls/MONTH — fix the seat, below |
| tier starter + seat Full | ❌ still 6/month — plan upgrade needed, below |

**Fix the seat** (user does, give this path): Figma team page → `Members` → own row
→ seat dropdown → **Full/Editor**. Being team owner does NOT imply a Full seat —
check the dropdown, not the role.

**Free plan for students**: figma.com/education → verify with university email →
full Professional plan, one year, renewable while enrolled.

**CRITICAL after any seat/plan change:** the seat is baked into the OAuth token.
Re-run Step 2 (re-authenticate), then `whoami` again until it shows the new seat.
This is the step people miss — whoami will keep reporting the old seat until
re-auth.

### Step 4 — Write smoke test (costs 1 call; skip on 6/month quota and warn instead)

One `use_figma` call on the target file: create a frame named `__probe__` at
(-500,-500), capture its id, remove it, `return {writeAccess:"OK"}`. Error mentioning
permissions → the file belongs to a different plan/team than the whoami account;
move the file into the entitled team or share it with edit rights.

### Step 5 — Report ready

Summarise: handle, plan/seat, daily quota, target file confirmed writable. Then
enter the drawing workflow at Step 0 (SKILL.md).

## Quota reference (per Figma docs, 2026)

| Seat | Starter | Professional | Organization | Enterprise |
|---|---|---|---|---|
| View, Collab | 6/month | 6/month | 6/month | 6/month |
| Full, Dev | 6/month | 200/day, 15/min | 200/day | 600/day, 20/min |

Quota-exempt tools: `whoami`, `generate_figma_design`, `add_code_connect_map`.
Everything else (use_figma, get_metadata, get_screenshot, ...) counts. Dev seats
cannot edit design files — for this skill the seat must be **Full**.

## Working style under quota

- Batch related mutations into one use_figma call; screenshot inside the same call.
- Failed scripts are atomic (nothing applied) but still consume a call — on error,
  STOP, read the message, fix, one retry.
- Never start a drawing session on 6/month quota: one figure takes 15-30 write calls.

## Stuck-points table

| Symptom | Cause → fix |
|---|---|
| Tools absent after plugin install | MCP connects at session start → restart session |
| Browser error page after authorising | Remote session — expected; paste the full callback URL |
| whoami shows old seat after upgrade | Token bakes the seat → re-run OAuth |
| "resources can't be accessed" / 403 on file | File owned by another team/plan than the whoami account — check file location, move it under the entitled team |
| Rate-limit error mid-drawing | Per-minute cap (10-15/min) — halve fan-out width, continue; do not tight-loop retry |
| Tool calls suddenly unavailable mid-session | MCP server reconnecting — retry via ToolSearch once, else restart session |
