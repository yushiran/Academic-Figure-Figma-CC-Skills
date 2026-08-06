# Figma MCP connection, seats and quota

## Install and authenticate

```bash
claude plugin install figma@claude-plugins-official
```

The plugin bundles the remote MCP server (`https://mcp.figma.com/mcp`) plus the
figma-use / figma-generate-diagram / figma-create-new-file skills. After install the
server tools appear as deferred tools; load them via ToolSearch.

OAuth flow (remote/SSH session):
1. Call `authenticate` → it prints a `figma.com/oauth/mcp?...` URL.
2. User opens it in a browser and approves.
3. Browser redirects to `http://localhost:3118/callback?...` and shows a connection
   error — **this is expected** on a remote session. The user copies the FULL callback
   URL from the address bar and pastes it into chat.
4. Call `complete_authentication` with that `callback_url`.

Verify with `whoami` — it returns handle, email, and per-plan **seat + tier**.
`whoami` is quota-exempt: use it freely to re-check after any plan/seat change.

## Quota table (per Figma docs, 2026)

| Seat | Starter | Professional | Organization | Enterprise |
|---|---|---|---|---|
| View, Collab | 6/month | 6/month | 6/month | 6/month |
| Full, Dev | 6/month (Starter) | 200/day, 15/min | 200/day | 600/day, 20/min |

Quota-exempt tools: `whoami`, `generate_figma_design`, `add_code_connect_map`.
Everything else (use_figma, get_metadata, get_screenshot, ...) counts.

## The traps, in the order they actually bite

1. **Seat type beats plan tier.** Professional plan + View seat is still 6 calls/month.
   You need a **Full (or Dev) seat**; Dev seats cannot edit design files, so for this
   skill it must be Full.
2. **Being team owner does not mean holding a Full seat.** Check the Members page:
   team page → Members → your row → seat dropdown → Full/Editor.
3. **Re-authenticate after changing seat.** Seat info is baked into the OAuth token;
   `whoami` keeps reporting the old seat until the OAuth flow is redone.
4. **Students: Figma Education is free** (figma.com/education, verify with university
   email). Grants the full Professional plan for one year, renewable while enrolled —
   i.e. 200 calls/day at zero cost. Files may need to live under the education team.
5. Do not begin a drawing session on 6/month quota — a single figure takes 15-30 write
   calls. Fix the seat first.

## Working style under quota

- Batch related mutations into one use_figma call (≤10 logical operations).
- Screenshot inside the same call (`await node.screenshot()`) instead of a separate
  get_screenshot call.
- Failed scripts are atomic (nothing applied) and still consume a call — on error,
  STOP, read the message, fix, one retry.
