#!/usr/bin/env python3

import argparse
import csv
import json
import sys
import urllib.error
import urllib.request


DEFAULT_RPC_URL = "https://api.mainnet-beta.solana.com"
LAMPORTS_PER_SOL = 1_000_000_000

WALLETS = [
    {
        "rank": 1,
        "address": "MJKqp326RZCHnAAbew9MDdui3iCKWco7fsK9sVuZTX2",
        "category": "Treasury",
        "holder_type": "Top holder",
    },
    {
        "rank": 2,
        "address": "52C9T2T7JRojtxumYnYZhyUmrN7kqzvCLc4Ksvjk7TxD",
        "category": "Exchange",
        "holder_type": "Top holder",
    },
    {
        "rank": 3,
        "address": "8BseXT9EtoEhBTKFFYkwTnjKSUZwhtmdKY2Jrj8j45Rt",
        "category": "Whale",
        "holder_type": "Top holder",
    },
    {
        "rank": 4,
        "address": "GitYucwpNcg6Dx1Y15UQ9TQn8LZMX1uuqQNn8rXxEWNC",
        "category": "Validator",
        "holder_type": "Top holder",
    },
    {
        "rank": 5,
        "address": "9QgXqrgdbVU8KcpfskqJpAXKzbaYQJecgMAruSWoXDkM",
        "category": "Vault",
        "holder_type": "Top holder",
    },
    {
        "rank": 6,
        "address": "9uRJ5aGgeu2i3J98hsC5FDxd2PmRjVy9fQwNAy7fzLG3",
        "category": "Fund",
        "holder_type": "Top holder",
    },
    {
        "rank": 7,
        "address": "EJRJswH9LyjhAfBWwPBvat1LQtrJYK4sVUzsea889cQt",
        "category": "Bot cluster",
        "holder_type": "Bot holder",
    },
    {
        "rank": 8,
        "address": "53nHsQXkzZUp5MF1BK6Qoa48ud3aXfDFJBbe1oECPucC",
        "category": "MM desk",
        "holder_type": "Bot holder",
    },
    {
        "rank": 9,
        "address": "8PjJTv657aeN9p5R2WoM6pPSz385chvTTytUWaEjSjkq",
        "category": "Arb desk",
        "holder_type": "Bot holder",
    },
    {
        "rank": 10,
        "address": "AHB94zKUASftTdqgdfiDSdnPJHkEFp7zX3yMrcSxABsv",
        "category": "Custody",
        "holder_type": "Top holder",
    },
    {
        "rank": 11,
        "address": "9idsurpeyaXMygRmmnKuwauuB1zEjarj2r6Bjdji4SoK",
        "category": "Custom",
        "holder_type": "Watchlist",
    },
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Fetch tracked Solana wallet balances from a Solana RPC endpoint."
    )
    parser.add_argument(
        "--rpc-url",
        default=DEFAULT_RPC_URL,
        help="Solana RPC URL. Default: %(default)s",
    )
    parser.add_argument(
        "--format",
        choices=("json", "csv"),
        default="json",
        help="Output format. Default: %(default)s",
    )
    parser.add_argument(
        "--output",
        help="Write output to a file instead of stdout.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=20,
        help="HTTP timeout in seconds. Default: %(default)s",
    )
    return parser.parse_args()


def rpc_request(rpc_url, payload, timeout):
    request = urllib.request.Request(
        rpc_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"RPC HTTP error {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"RPC connection failed: {exc}") from exc


def fetch_wallets(rpc_url, timeout):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getMultipleAccounts",
        "params": [
            [item["address"] for item in WALLETS],
            {"encoding": "base64", "commitment": "confirmed"},
        ],
    }
    data = rpc_request(rpc_url, payload, timeout)
    if "error" in data:
        raise RuntimeError(f"RPC returned error: {data['error']}")

    result = data.get("result", {})
    value = result.get("value", [])
    if len(value) != len(WALLETS):
        raise RuntimeError("RPC result length did not match wallet list length.")

    rows = []
    for wallet, account in zip(WALLETS, value):
        lamports = account["lamports"] if account else None
        rows.append(
            {
                "rank": wallet["rank"],
                "address": wallet["address"],
                "category": wallet["category"],
                "holder_type": wallet["holder_type"],
                "lamports": lamports,
                "balance_sol": None if lamports is None else lamports / LAMPORTS_PER_SOL,
                "exists": account is not None,
            }
        )

    return {
        "rpc_url": rpc_url,
        "slot": result.get("context", {}).get("slot"),
        "wallet_count": len(rows),
        "wallets": rows,
    }


def write_json(payload, output_path):
    text = json.dumps(payload, indent=2)
    if output_path:
        with open(output_path, "w", encoding="utf-8") as handle:
            handle.write(text + "\n")
    else:
        print(text)


def write_csv(payload, output_path):
    fieldnames = [
        "rank",
        "address",
        "category",
        "holder_type",
        "lamports",
        "balance_sol",
        "exists",
    ]
    if output_path:
        handle = open(output_path, "w", encoding="utf-8", newline="")
    else:
        handle = sys.stdout
    try:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for wallet in payload["wallets"]:
            writer.writerow(wallet)
    finally:
        if output_path:
            handle.close()


def main():
    args = parse_args()
    payload = fetch_wallets(args.rpc_url, args.timeout)
    if args.format == "json":
        write_json(payload, args.output)
    else:
        write_csv(payload, args.output)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
