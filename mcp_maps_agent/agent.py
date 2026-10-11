import os
from dotenv import load_dotenv

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

load_dotenv()

MAPS_API_KEY = os.getenv("MAPS_API_KEY")

MAPS_MCP_URL = "https://mapstools.googleapis.com/mcp" # google-hosted maps MCP endpoint

maps_toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=MAPS_MCP_URL,
        headers={
            "X-Goog-Api-Key": MAPS_API_KEY,
                 },
    )
)

root_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="maps_mcp_agent",
    instruction="You are a helpful assistant that can answer questions about Google Maps data. You have access to the Maps MCP toolset, which allows you to retrieve information about places, routes, and other map-related data.",
    tools=[maps_toolset]
)




