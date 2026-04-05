# Crypto Native

Comic-style Solana wallet watchboard with a loud mobile-first layout, randomized activity stats, clickable address copy effects, and rare-dispatch interactions.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/vipulchartal-star/crypto-native)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/vipulchartal-star/crypto-native)
[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/vipulchartal-star/crypto-native)
[![Deploy to DO](https://www.deploytodo.com/do-btn-blue.svg)](https://cloud.digitalocean.com/apps/new?repo=https://github.com/vipulchartal-star/crypto-native/tree/main)

This project is a single-page static dashboard built in plain HTML, CSS, and JavaScript. It is designed to feel exaggerated and visual rather than neutral: thick borders, comic overlays, animated dispatch blocks, and a fake-live watchlist presentation.

## Project Summary

The page currently includes:

- a ranked wallet board
- mobile card-style layout for small screens
- randomized send rate, receive rate, and ETA fields
- click-to-copy wallet addresses with an `Address Copied!` comic burst
- per-wallet `Priority Dispatch` controls
- dispatch animation with a `Waiting For Reply` sign
- a GitHub badge and end-page banner copy

This is a presentation project, not a real on-chain analytics terminal. Some displayed values are intentionally randomized for effect.

## Files

- `index.html` — main dashboard page
- `fetch_wallets.py` — fetch tracked wallet balances from Solana RPC and write JSON or CSV
- `.do/deploy.template.yaml` — DigitalOcean App Platform deploy template
- `netlify.toml` — Netlify publish config
- `render.yaml` — Render Blueprint config for one-click hosting

## Tracking Repo

Tracking source repo used for this project:

- `https://github.com/vipulchartal-star/crypto-scraper.git`

## Local Preview

From this directory:

```sh
python3 -m http.server 8000
```

Then open:

```text
http://127.0.0.1:8000/index.html
```

## One-Click Hosting

- Vercel: use the `Deploy with Vercel` button above to clone and host the repo.
- Render: use the `Deploy to Render` button above. The included `render.yaml` sets this project up as a static site.
- Netlify: use the `Deploy to Netlify` button above. The included `netlify.toml` publishes the project root as a static site.
- DigitalOcean: use the `Deploy to DO` button above. The included `.do/deploy.template.yaml` configures App Platform as a static site deployment.
- Railway: Railway supports template-based deploy flows, but it requires a published Railway template instead of a direct repo button for this setup.

## Fetch Wallet Data

The repo now includes a Python script that fetches balances for the tracked wallet set directly from Solana RPC.

Default JSON output to stdout:

```sh
python3 fetch_wallets.py
```

Write JSON to a file:

```sh
python3 fetch_wallets.py --output wallets.json
```

Write CSV to a file:

```sh
python3 fetch_wallets.py --format csv --output wallets.csv
```

Use a custom RPC endpoint:

```sh
python3 fetch_wallets.py --rpc-url https://api.mainnet-beta.solana.com
```

## Wallet List

Tracked wallet set currently shown in the page:

1. `MJKqp326RZCHnAAbew9MDdui3iCKWco7fsK9sVuZTX2`
2. `52C9T2T7JRojtxumYnYZhyUmrN7kqzvCLc4Ksvjk7TxD`
3. `8BseXT9EtoEhBTKFFYkwTnjKSUZwhtmdKY2Jrj8j45Rt`
4. `GitYucwpNcg6Dx1Y15UQ9TQn8LZMX1uuqQNn8rXxEWNC`
5. `9QgXqrgdbVU8KcpfskqJpAXKzbaYQJecgMAruSWoXDkM`
6. `9uRJ5aGgeu2i3J98hsC5FDxd2PmRjVy9fQwNAy7fzLG3`
7. `EJRJswH9LyjhAfBWwPBvat1LQtrJYK4sVUzsea889cQt`
8. `53nHsQXkzZUp5MF1BK6Qoa48ud3aXfDFJBbe1oECPucC`
9. `8PjJTv657aeN9p5R2WoM6pPSz385chvTTytUWaEjSjkq`
10. `AHB94zKUASftTdqgdfiDSdnPJHkEFp7zX3yMrcSxABsv`
11. `9idsurpeyaXMygRmmnKuwauuB1zEjarj2r6Bjdji4SoK`

## Notes

- The wallet list is based on the current page content in this repo.
- Tracking/reference repo: `https://github.com/vipulchartal-star/crypto-scraper.git`
- The custom wallet was added manually to the board.
- `fetch_wallets.py` uses `getMultipleAccounts` against Solana RPC to fetch current lamport balances.
- Category labels, holder types, rates, ETAs, and dispatch states are UI effects unless backed by a real data source.

## Next Ideas

- wire the board to live Solana RPC data
- add a real repo link to the GitHub badge in the page header
- replace placeholder dispatch behavior with a real workflow
- add a small README screenshot or animated preview
