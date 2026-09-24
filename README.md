# 🏠 Zillow API: US Real Estate Listings for Sale, Rent & Sold

> A **Zillow API** on Apify that returns US real estate listings as clean, structured JSON. Search by plain city or ZIP, filter for price cuts, and export homes for sale, for rent, and sold.

**Actor page:** [apify.com/johnvc/zillow-api](https://apify.com/johnvc/zillow-api?fpr=9n7kx3)
**Input schema:** [apify.com/johnvc/zillow-api/input-schema](https://apify.com/johnvc/zillow-api/input-schema?fpr=9n7kx3)

This Zillow API turns [Zillow](https://www.zillow.com) into a structured data feed. Send a location and a few filters and get back typed rows for each listing: price, beds, baths, square footage, address, coordinates, broker, Zestimate, days on market, and the amount and date of any recent price cut. It covers homes for sale, rentals, and recently sold homes, and it resolves a plain city or ZIP to the right Zillow region for you.

## Video Walkthrough

[![Watch the walkthrough](https://img.youtube.com/vi/jREWahDGhJM/maxresdefault.jpg)](https://www.youtube.com/watch?v=jREWahDGhJM)

### Text walkthrough

The **Zillow API** takes plain locations, so you never build a search URL or look up a region id: pass `"Austin, TX"` or `"78704"` in `locations`, pick a `statusType` of `sale`, `rent`, or `sold`, and add filters like `priceReduction` or `bedsMin`. Each row comes back with `price`, `priceValue`, `priceChange`, `beds`, `baths`, `squareFeet`, `address`, `latitude`, `longitude`, and `url`, plus `zestimate` and `daysOnZillow`. A single Zillow search is capped at 820 results, so turn on `autoShard` to sweep a whole metro by splitting the map into tiles. One common use case is a weekly price-cut feed: set `priceReduction` to true for a city, save it as a Task, and schedule it so your dataset always shows the freshest motivated-seller listings. Rentals return building-level data (per-floorplan rents, available units, leasing phone), and sold results return the sold date with the Zestimate and tax-assessed value.

## Quick Start

### Prerequisites
- Python 3.11 or higher
- An Apify account and API key ([get a free key here](https://apify.com?fpr=9n7kx3))

1. **Clone the repository**
   ```bash
   git clone https://github.com/johnisanerd/Apify-Zillow-API.git
   cd Apify-Zillow-API
   ```

2. **Install dependencies with UV**
   ```bash
   # Install UV if you do not have it:
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Install project dependencies:
   uv sync
   ```

3. **Configure your API key**
   ```bash
   cp .env.example .env
   # Edit .env and add your Apify API key
   # Get your free API key at: https://apify.com?fpr=9n7kx3
   ```

4. **Run the example**
   ```bash
   uv run python zillow-api-example.py
   # Optional recipes:
   # uv run python zillow-api-example.py --example rentals
   # uv run python zillow-api-example.py --example price_cuts
   # uv run python zillow-api-example.py --example sold
   ```

### Alternative: set the API key directly
```bash
export APIFY_API_TOKEN="your_api_key_here"
uv run python zillow-api-example.py
```

## Why Use This Zillow API?

Zillow's own developer access runs through an invite-only partner program, so most people cannot self-serve. This Zillow API is the practical alternative: no application, no region ids, no hand-built search URLs. You send plain inputs and get structured JSON.

It is correct where raw scrapers are silently wrong. Hand most tools a ZIP code and they return a different city's listings; this Actor resolves the ZIP to the right Zillow region first, so `78704` gives you Austin, not a same-numbered town in another state.

It covers the full market in one place: for sale, for rent, and sold, each with the fields that match. It is built to run on a schedule, so a saved search becomes a standing feed you can diff week over week.

And it is MCP-ready, so an AI assistant can call it as a tool and ask for listings in plain language.

## Features

### Core Capabilities
- Search homes for sale, for rent, and recently sold across the US.
- Plain-name location input: city, ZIP, county, neighborhood, or state.
- Price-cut filter with the change amount and date for motivated-seller and stale-inventory work.
- Map sharding to sweep a whole metro past the 820-result cap.

### Data Quality
- Typed fields, not scraped strings: numeric prices, coordinates, and dates.
- Deduplicated results across map tiles.
- Photo URLs are passed through, never re-hosted.

## Recipes

### Homes for sale in a city

[Run this on Apify](https://apify.com/johnvc/zillow-api?fpr=9n7kx3): search a city or ZIP for sale with beds and price filters, get back typed listing rows.

Local: `uv run python zillow-api-example.py`

### Rentals in a ZIP code

[Run this on Apify](https://apify.com/johnvc/zillow-api?fpr=9n7kx3): building-level rentals with per-floorplan rents, available units, and leasing phone.

Local: `uv run python zillow-api-example.py --example rentals`

### Homes with recent price cuts

[Run this on Apify](https://apify.com/johnvc/zillow-api?fpr=9n7kx3): set `priceReduction` and read `priceChange` and `priceChangeDate` for a motivated-seller feed.

Local: `uv run python zillow-api-example.py --example price_cuts`

### Recently sold homes

[Run this on Apify](https://apify.com/johnvc/zillow-api?fpr=9n7kx3): recently sold homes with sold date, Zestimate, and tax-assessed value.

Local: `uv run python zillow-api-example.py --example sold`

**Schedule tip:** Save any of these inputs as an Apify Task and [schedule it](https://apify.com/johnvc/zillow-api?fpr=9n7kx3) to run daily or weekly so your dataset stays fresh without manual runs.

## Usage Examples

### Basic Example
```json
{
  "locations": ["Austin, TX"],
  "statusType": "sale",
  "maxResults": 10
}
```

### Advanced Example
```json
{
  "locations": ["Phoenix, AZ"],
  "statusType": "sale",
  "priceReduction": true,
  "bedsMin": 3,
  "priceMax": 600000,
  "autoShard": true,
  "maxResults": 2000,
  "maxUpstreamCalls": 80
}
```

## Input Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `locations` | `list[str]` | one location source | `["Austin, TX"]` | Plain place names: city, ZIP, county, neighborhood, or state. Up to 25 per run. |
| `statusType` | `str` | YES | `sale` | `sale`, `rent`, or `sold`. |
| `priceMin` / `priceMax` | `int` | no | - | Price range (list price for sale/sold, monthly rent for rent). |
| `bedsMin` / `bedsMax` | `int` | no | - | Bedroom range. |
| `priceReduction` | `bool` | no | `false` | Only listings with a recent price cut. |
| `listingType` | `list[str]` | no | - | For sale: owner (FSBO), agent, new construction, foreclosure, and more. |
| `homeType` | `list[str]` | no | - | House, condo, townhome, multi-family, lot/land, apartment, manufactured. |
| `autoShard` | `bool` | no | `false` | Sweep past the 820-result cap by splitting the map into tiles. |
| `maxUpstreamCalls` | `int` | no | `40` | Hard ceiling on requests for a sharded run. |
| `maxResults` | `int` | no | `200` | Main cost control. Minimum 10 per search. |

## Output Format

```json
{
  "resultType": "forSale",
  "zpid": "29444234",
  "title": "1200 Barton Hills Dr, Austin, TX 78704",
  "price": "$425,000",
  "priceValue": 425000,
  "priceChange": -15000,
  "priceChangeDate": "2026-08-12",
  "beds": 3,
  "baths": 2,
  "squareFeet": 1842,
  "city": "Austin",
  "state": "TX",
  "zipcode": "78704",
  "latitude": 30.2489,
  "longitude": -97.7791,
  "url": "https://www.zillow.com/homedetails/29444234_zpid/",
  "regionId": "10221",
  "scrapedAt": "2026-08-25T14:22:07Z"
}
```

<!-- ask-ai:start -->
## 🤖 Ask an AI assistant about this Actor

Open a ready-to-send prompt about the Zillow API in the AI of your choice:

- 💬 [ChatGPT](https://chatgpt.com/?q=Using%20the%20Zillow%20API%20on%20Apify%20%28https://apify.com/johnvc/zillow-api?fpr=9n7kx3%29%2C%20walk%20me%20through%20this%20use%20case:%20%22Zillow%20Open%20Houses%20API:%20Homes%20with%20Open%20Houses%22.%20Show%20me%20the%20input%20JSON%2C%20the%20output%20fields%2C%20and%20how%20to%20automate%20it%20with%20the%20API%20or%20MCP.)
- 🧠 [Claude](https://claude.ai/new?q=Using%20the%20Zillow%20API%20on%20Apify%20%28https://apify.com/johnvc/zillow-api?fpr=9n7kx3%29%2C%20walk%20me%20through%20this%20use%20case:%20%22Zillow%20Open%20Houses%20API:%20Homes%20with%20Open%20Houses%22.%20Show%20me%20the%20input%20JSON%2C%20the%20output%20fields%2C%20and%20how%20to%20automate%20it%20with%20the%20API%20or%20MCP.)
- 🔍 [Perplexity](https://www.perplexity.ai/search?q=Using%20the%20Zillow%20API%20on%20Apify%20%28https://apify.com/johnvc/zillow-api?fpr=9n7kx3%29%2C%20walk%20me%20through%20this%20use%20case:%20%22Zillow%20Open%20Houses%20API:%20Homes%20with%20Open%20Houses%22.%20Show%20me%20the%20input%20JSON%2C%20the%20output%20fields%2C%20and%20how%20to%20automate%20it%20with%20the%20API%20or%20MCP.)
- 🅒 [Copilot](https://copilot.microsoft.com/?q=Using%20the%20Zillow%20API%20on%20Apify%20%28https://apify.com/johnvc/zillow-api?fpr=9n7kx3%29%2C%20walk%20me%20through%20this%20use%20case:%20%22Zillow%20Open%20Houses%20API:%20Homes%20with%20Open%20Houses%22.%20Show%20me%20the%20input%20JSON%2C%20the%20output%20fields%2C%20and%20how%20to%20automate%20it%20with%20the%20API%20or%20MCP.)
<!-- ask-ai:end -->

## People also search for

### Is this a Zillow scraper or an API?

This repo teaches the **Zillow API** on Apify. People often search for a "zillow scraper"; the same Actor covers that need and returns structured JSON you can call from Python or MCP, without building or maintaining a scraper yourself.

### How do I get Zillow data from Python?

Clone this repo, set `APIFY_API_TOKEN`, and run `uv run python zillow-api-example.py`. See Quick Start and Recipes above.

### How do I search Zillow by ZIP code or city?

Put the ZIP or city in `locations`, for example `"78704"` or `"Austin, TX"`. The Actor resolves it to the correct [Zillow](https://www.zillow.com) region automatically, so you do not get another city's listings by mistake.

### Can I use this Zillow API with MCP or Claude?

Yes. Use the install sections below to add the Actor as an MCP tool in [Claude Code](https://claude.ai/referral/uIlpa7nPLg) (free trial), [Claude Cowork](https://claude.ai/referral/uIlpa7nPLg) (free trial), Claude.ai, Cursor, or ChatGPT.

### How do I get more than 800 Zillow results for one city?

Turn on `autoShard`. A single Zillow search returns at most 820 results, so the Actor splits the map into tiles and merges them, deduplicated, to cover a full metro. Use `maxUpstreamCalls` to cap the cost.

---

## Install in Claude Cowork Desktop

![Install in Claude Cowork Desktop](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_desktop.png)

Cowork is the desktop app's automation mode. To give it the Zillow API as a tool, add the Apify MCP server as a connector.

1. Open the Claude desktop app and go to **Settings → Connectors** (or **Settings → Developer → Edit Config** to edit `claude_desktop_config.json` directly).
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
2. Add the Apify MCP server, preloaded with only this Actor:

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=actors,docs,johnvc/zillow-api"
      ]
    }
  }
}
```

3. Restart the app. When Cowork first calls the tool, complete the OAuth prompt in your browser, or add your Apify API token in the connector settings to skip OAuth.
4. In a Cowork chat, confirm the tool is available and ask it to run the Zillow API.

Download the desktop app and start a free trial: https://claude.ai/referral/uIlpa7nPLg
More help: https://docs.apify.com/platform/integrations/claude-desktop

## Install in Claude Code

![Install in Claude Code](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_code.png)

Claude Code is the command-line tool. Add the Actor's MCP server with one command:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/zillow-api"
```

To use a token instead of browser OAuth:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/zillow-api" \
  --header "Authorization: Bearer YOUR_APIFY_TOKEN"
```

Then verify with `claude mcp list`, or run `/mcp` inside a session. Ask Claude Code to call the Zillow API.

Try Claude Code free: https://claude.ai/referral/uIlpa7nPLg
Claude Code MCP docs: https://code.claude.com/docs/en/mcp

## Install in Claude (website)

![Install in Claude (website)](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_ai.png)

On claude.ai you add Apify as a connector, then enable just this Actor's tool.

1. Go to **Settings → Connectors → Browse connectors** and search for **Apify MCP server**. Install it (enable or update if prompted).
2. When connecting, authenticate with your Apify API token, and enable the tool `johnvc/zillow-api`.
3. In any chat, open **+ → Connectors** and turn on **Apify**.
4. Alternatively, choose **Add custom connector** and paste the full MCP URL `https://mcp.apify.com/?tools=actors,docs,johnvc/zillow-api`, using OAuth when prompted.
5. Ask Claude to run the Zillow API.

Open Claude on the web: https://claude.ai

## Install in Cursor

![Install in Cursor](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_cursor.png)

Cursor reads MCP servers from a project file at `.cursor/mcp.json`.

1. In your project, create `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/zillow-api"
    }
  }
}
```

2. If you prefer token auth over browser OAuth, add a header:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/zillow-api",
      "headers": { "Authorization": "Bearer YOUR_APIFY_TOKEN" }
    }
  }
}
```

3. Open **Cursor → Settings → MCP** and confirm the **apify** server is connected (green dot).
4. In Composer or Chat, ask Cursor to call the Zillow API.

New to Cursor? Get it here: https://cursor.com/referral?code=XQP4VBLI3NNX

## Install in ChatGPT

![Install in ChatGPT](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_ChatGPT.png)

ChatGPT connects to the Apify MCP server through Developer mode (available on ChatGPT Pro, Plus, Business, Enterprise, and Education plans).

1. Click your profile icon, then go to **Settings > Apps**. If you do not see a **Create app** button, open **Advanced settings** and enable **Developer mode**.
2. Click **Create app** and fill out the form:
   - **Name:** Apify
   - **MCP Server URL:** `https://mcp.apify.com/?tools=actors,docs,johnvc/zillow-api`
   - **Authentication:** OAuth
3. Click **Create** and authorize the connection with Apify.
4. To use the app in a conversation, click **+** in the chat, choose **Developer mode**, and select **Apify**.

More help: https://docs.apify.com/platform/integrations/mcp

---

[**Made with care**](https://apify.com/johnvc?fpr=9n7kx3)

*Use the Zillow API to power your data workflows with reliable, structured results.*

Last Updated: 2026.09.22
