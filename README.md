# Crypto Native

Comic-style Solana wallet watchboard with a loud mobile-first layout, randomized activity stats, clickable address copy effects, and rare-dispatch interactions.

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
- Category labels, holder types, rates, ETAs, and dispatch states are UI effects unless backed by a real data source.

## Next Ideas

- wire the board to live Solana RPC data
- add a real repo link to the GitHub badge in the page header
- replace placeholder dispatch behavior with a real workflow
- add a small README screenshot or animated preview
