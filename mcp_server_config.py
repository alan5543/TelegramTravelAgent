import os

# --- MCP Server Configuration ---
mcp_server_configs = [
       {
            # MCP tool to calculate the budget of the trip
            "name": "calculator-mcp",
            "command": "npx",
            "args": [
                "-y", 
                "@smithery/cli@latest", 
                "run", 
                "@alan5543/calculator-mcp", 
            ],
            "env": None
        },
        {
            # MCP tool to search for airbnbs in the destination
            "name": "airbnb-mcp-server",
            "command": "npx",
            "args": [
                "-y", 
                "@smithery/cli@latest", 
                "run", 
                "@alan5543/airbnb-mcp-server", 
            ],
            "env": None
        },
        {
            # MCP tool to search for flights to the destination
            "name": "flight-search-mcp",
            "command": "npx",
            "args": [
                "-y", 
                "@smithery/cli@latest", 
                "run", 
                "@alan5543/flight-search-mcp", 
            ],
            "env": None
        },
        {
            # MCP tool to plan, discover and book the trip and hotel
            "name": "travel-agent-mcp-server",
            "command": "npx",
            "args": [
                 "-y",
                "@smithery/cli@latest",
                "run",
                "@alan5543/travel-agent-mcp-server",
            ],
            "env": {
                "SERP_API_KEY": os.getenv("SERP_API_KEY"),
                "CURRENCYFREAKS_API_KEY": os.getenv("CURRENCYFREAKS_API_KEY")
            }
        },
        {
            # MCP tool to fetch the information from the web
            "name": "fetch_server",
            "command": "uvx",
            "args": [
                "mcp-server-fetch", 
                "--user-agent=TravelBuddyBot/1.0"
            ],
            "env": None,
        },
        {
            # MCP tool to fetch the information from the wikipedia, for finding the information of the tourist spots
            "name": "wikipedia-mcp",
            "command": "uvx",
            "args": [
                "wikipedia-mcp"
            ],
            "env": None,
        },
        {
            # MCP tool to think sequentially as a travel agent
            "name": "sequential_thinking",
            "command": "npx",
            "args": [
                "-y", 
                "@modelcontextprotocol/server-sequential-thinking"
            ],
            "env": None
        }
    ]