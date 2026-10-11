# MCP Google Maps Agent (Google ADK)

A minimal Google ADK (Agent Development Kit) agent that connects to Google's
hosted Maps MCP server over Streamable HTTP, exposing Maps tools (places,
routes, etc.) to an `LlmAgent` running Gemini 3.1 Flash Lite. The entire agent
definition lives in `mcp_maps_agent/agent.py`.

- **Entry point:** `mcp_maps_agent/agent.py` — the whole agent is defined here.
- **How it works:** it wraps a `StreamableHTTPConnectionParams` connection to
  `https://mapstools.googleapis.com/mcp` (authenticated via `X-Goog-Api-Key`)
  in an `McpToolset`, then hands that toolset to an `LlmAgent` (`root_agent`)
  running on Gemini.
- **No local tools:** all Maps functionality lives on Google's remote MCP
  server — nothing to maintain locally beyond the connection wiring.
- **Run it:** `adk web` (browser chat UI) or `adk run mcp_maps_agent`
  (terminal), after setting `MAPS_API_KEY` in a `.env` file.

It's essentially a reference example showing how little code is needed to
bolt a hosted MCP toolset onto an ADK agent.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file (gitignored) in the repo root with:

```
MAPS_API_KEY=<your Google Maps API key>
```

`agent.py` loads this via `python-dotenv` and sends it as the
`X-Goog-Api-Key` header when connecting to the MCP endpoint.

## Running the agent

This follows the standard ADK project layout (an agent package directory
containing `agent.py` with a module-level `root_agent`), so the ADK CLI can
discover and run it from the repo root:

```bash
adk web          # launch the ADK dev UI and chat with the agent in a browser
adk run mcp_maps_agent   # run the agent directly in the terminal
```

There is no custom entrypoint script, test suite, or lint config in this
project — `adk web`/`adk run` and manual inspection are the only ways to
exercise it.

## Architecture notes

```
 User                LlmAgent                  McpToolset               Google Maps
 input      ────▶   (Gemini 3.1       ────▶   (MCP client,     ────▶   MCP server
 "find a             Flash Lite)               Streamable HTTP)         (places,
  route to                │                         │                   routes API)
  the park"              │                         │                         │
                         │  decides it needs        │                         │
                         │  a Maps tool,            │                         │
                         │  calls it     ───────────▶                         │
                         │                          │  forwards call +        │
                         │                          │  X-Goog-Api-Key  ───────▶
                         │                          │                         │
                         │                          │  ◀────── route/place ───┘
                         │  ◀── tool result ─────────┘           data
                         │
 reply     ◀───── natural-language answer
 to user           grounded in the tool result
```

- `mcp_maps_agent/agent.py` wires together three ADK pieces:
  - `StreamableHTTPConnectionParams` — connection config pointing at the
    Google-hosted Maps MCP endpoint (`https://mapstools.googleapis.com/mcp`),
    authenticated via the `X-Goog-Api-Key` header.
  - `McpToolset` — wraps that MCP connection so its tools can be handed to an
    agent.
  - `LlmAgent` — the Gemini-backed agent (`root_agent`) that receives the
    `maps_toolset` as its `tools`.
- ADK discovers agents by convention: it looks for a `root_agent` variable in
  an `agent.py` inside a package directory (here, `mcp_maps_agent/`). Keep
  that name and location if extending this agent, or add sibling package
  directories for additional agents.
- All Maps functionality comes from Google's remote MCP server — there is no
  local tool implementation to maintain; changes to tool behavior happen on
  Google's side, not in this repo.
