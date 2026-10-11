# MCP Google Maps Agent (Google ADK)

A minimal Google ADK (Agent Development Kit) agent that connects to Google's
hosted Maps MCP server over Streamable HTTP, exposing Maps tools (places,
routes, etc.) to an `LlmAgent` running Gemini 2.0 Flash. The entire agent
definition lives in `mcp_maps_agent/agent.py`.

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

- `mcp_maps_agent/agent.py` wires together three ADK pieces:
  - `StreamableHTTPConnnectionParams` — connection config pointing at the
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
