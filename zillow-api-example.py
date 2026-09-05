"""
Zillow API: A Quick Start Example
See more at: https://apify.com/johnvc/zillow-api?fpr=9n7kx3
Input schema: https://apify.com/johnvc/zillow-api/input-schema?fpr=9n7kx3

This script shows how to call the Zillow API on Apify from Python and read its
structured JSON output. The default run searches one city for sale while staying
cheap. The --example recipes mirror common use cases: rentals in a ZIP, homes
with recent price cuts, and recently sold homes.

Get your free Apify API key at: https://apify.com?fpr=9n7kx3

Examples:
  uv run python zillow-api-example.py
  uv run python zillow-api-example.py --example rentals
  uv run python zillow-api-example.py --example price_cuts
  uv run python zillow-api-example.py --example sold
"""

from __future__ import annotations

import argparse
import os
from typing import Any

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

ACTOR_ID = "johnvc/zillow-api"


def _print_items(items: list[dict[str, Any]]) -> None:
    """Print a short summary of the listings returned."""
    print(f"Returned {len(items)} listing(s).\n")
    for item in items:
        kind = item.get("resultType", "listing")
        if kind == "rental":
            name = item.get("buildingName") or item.get("title")
            rent = item.get("minBaseRent")
            rent_str = f"${rent}+/mo" if rent else "rent n/a"
            print(f"- [rental] {name} | {rent_str} | {item.get('city')}, {item.get('state')} | {item.get('url')}")
        elif kind == "sold":
            print(f"- [sold]   {item.get('title')} | sold {item.get('soldDate')} | "
                  f"Zestimate {item.get('zestimate')} | {item.get('url')}")
        elif kind == "error":
            print(f"- [error]  {item.get('errorMessage')}")
        else:
            change = item.get("priceChange")
            change_str = f" (changed {change})" if change else ""
            print(f"- [sale]   {item.get('title')} | {item.get('price')}{change_str} | "
                  f"{item.get('beds')}bd/{item.get('baths')}ba | {item.get('url')}")


def _run(client: ApifyClient, run_input: dict[str, Any]) -> None:
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    if run is None:
        raise SystemExit("The Actor run did not return a result.")
    items = list(client.dataset(run.default_dataset_id).iterate_items())
    _print_items(items)


def run_default(client: ApifyClient) -> None:
    """Cheap general quick-start: homes for sale in one city.

    Inputs are kept small (one city, maxResults 10, the billed minimum) so this
    first run stays inexpensive. Raise maxResults once you know your budget.
    """
    _run(client, {
        "locations": ["Austin, TX"],
        "statusType": "sale",
        "bedsMin": 3,
        "priceMax": 600000,
        "maxResults": 10,
    })


def run_rentals(client: ApifyClient) -> None:
    """Rentals in a single ZIP code.

    See the task page:
    https://apify.com/johnvc/zillow-api?fpr=9n7kx3
    """
    _run(client, {
        "locations": ["78704"],
        "statusType": "rent",
        "maxResults": 10,
    })


def run_price_cuts(client: ApifyClient) -> None:
    """Homes with a recent price cut: the motivated-seller / stale-inventory feed."""
    _run(client, {
        "locations": ["Phoenix, AZ"],
        "statusType": "sale",
        "priceReduction": True,
        "maxResults": 10,
    })


def run_sold(client: ApifyClient) -> None:
    """Recently sold homes (sold date, Zestimate, and tax-assessed value)."""
    _run(client, {
        "locations": ["Austin, TX"],
        "statusType": "sold",
        "maxResults": 10,
    })


def main() -> None:
    """Dispatch a quick-start or a use-case recipe."""
    parser = argparse.ArgumentParser(description="Zillow API examples")
    parser.add_argument(
        "--example",
        default="default",
        choices=["default", "rentals", "price_cuts", "sold"],
        help="Which recipe to run (see the README Recipes section).",
    )
    args = parser.parse_args()

    token = os.getenv("APIFY_API_TOKEN")
    if not token:
        raise SystemExit("Set APIFY_API_TOKEN in .env or the environment.")

    client = ApifyClient(token)
    dispatch = {
        "default": run_default,
        "rentals": run_rentals,
        "price_cuts": run_price_cuts,
        "sold": run_sold,
    }
    dispatch[args.example](client)


if __name__ == "__main__":
    main()
