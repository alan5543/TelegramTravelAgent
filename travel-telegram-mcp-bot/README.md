# Telegram Travel Agent ✈️🤖

The Telegram Travel Agent is a sophisticated Telegram bot designed to streamline travel planning by integrating with the Gemini language model and leveraging the Model Context Protocol (MCP) client architecture. It connects to multiple MCP servers to provide real-time travel-related services, including flight searches, accommodation bookings, trip planning, local event discovery, and destination exploration. The bot supports multilingual communication in English, Chinese, and Cantonese, ensuring accessibility for a diverse user base.

This project is ideal for travelers seeking a seamless, interactive experience to plan their trips directly through Telegram, with structured, user-friendly responses and robust backend integrations.

## Features

- **Multilingual Support**: Communicates fluently in English, Chinese, and Cantonese, automatically translating responses to match the user's language preference for consistency.
- **Comprehensive Travel Services**:
  - Search for flights to various destinations.
  - Find Airbnb listings and hotels.
  - Plan trips with recommendations for restaurants, shops, and local attractions.
  - Discover local events and explore tourist spots.
- **MCP Integration**: Leverages the Model Context Protocol to connect with specialized MCP servers for real-time data retrieval and processing.
- **Customizable Configuration**: Allows users to configure the language model and set limits on tool iterations for tailored responses.
- **Structured Output**: Delivers results in a clear, emoji-based, plaintext format, sorted by price, ensuring readability and ease of use.
- **Scalable Design**: Modular architecture supports the addition of new MCP servers and tools for expanded functionality.

## Architecture

The Telegram Travel Agent operates as an MCP client, interfacing with the Gemini language model and multiple MCP servers to handle travel-related queries. The bot processes user inputs via Telegram, uses Gemini for natural language understanding, and delegates specific tasks (e.g., flight search, budget calculation) to dedicated MCP servers. The system prompt ensures consistent, user-friendly responses, while the MCP client orchestrates tool calls within defined limits.

### MCP Client

The **Model Context Protocol (MCP)** is a framework that enables the Telegram Travel Agent to act as an MCP client, communicating with external MCP servers to execute specialized tasks. Each MCP server is a standalone service designed for a specific function, such as searching for flights, calculating budgets, or fetching web data. The MCP client coordinates these interactions by:

1. **Receiving User Input**: The bot processes user queries via Telegram, interpreting them using the Gemini language model.
2. **Tool Selection**: Based on the query, the MCP client selects the appropriate MCP server(s) to handle the request (e.g., `flight-search-mcp` for flight queries).
3. **Task Execution**: The client sends requests to the selected MCP server, which processes the task and returns results (e.g., flight details, hotel listings).
4. **Iteration Control**: The `MAX_TOOL_ITERATIONS` setting limits the number of sequential tool calls in a single conversation, ensuring efficient and focused responses (e.g., searching for a hotel, calculating its cost, and finding flights in one session).
5. **Response Formatting**: The client formats the results according to the system prompt, presenting them in a structured, plaintext format with emojis for clarity.

This modular approach allows the bot to scale by integrating new MCP servers for additional functionalities, making it highly extensible and adaptable.

## Installation

### Prerequisites
- **Python**: Version 3.8 or higher.
- **uv**: A Python package manager for dependency management and execution.
- **Node.js**: Required for running MCP servers via `npx`.
- **API Keys**: Obtain keys for Telegram, Gemini, OpenRouter, and SerpAPI.

### Setup Instructions
1. **Clone the Repository**:
   ```
   git clone https://github.com/alan5543/telegram-travel-agent.git
   cd telegram-travel-agent
   ```

2. **Install uv**:
   - Follow the official [uv installation guide](https://github.com/astral-sh/uv#installation).
   - Example for macOS/Linux:
     ```
     curl -LsSf https://astral.sh/uv/install.sh | sh
     ```
   - For Windows, use PowerShell or download the installer.

3. **Install Dependencies**:
   Run the following command to install required Python packages:
   ```
   uv sync
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the project root and add the following:
   ```
   TELEGRAM_BOT_TOKEN="your_api_key_here"
   GEMINI_API_KEY="your_api_key_here"
   CURRENCYFREAKS_API_KEY="your_api_key_here"
   SERP_API_KEY="your_api_key_here"
   ```

### Running the Bot
To start the Telegram Travel Agent, execute:
```
uv run main.py
```
This command runs the bot using `uv`, ensuring all dependencies are correctly loaded.

## Configuration

### Model Configuration
Edit `config.py` to configure the language model and tool iteration limits:
```python
# --- Model Configuration ---
GEMINI_MODEL = "gemini-2.0-flash"
MAX_TOOL_ITERATIONS = 5
```
- `GEMINI_MODEL`: Specifies the Gemini model (e.g., `gemini-2.0-flash`).
- `MAX_TOOL_ITERATIONS`: Controls the maximum number of MCP tool calls in a single conversation (e.g., searching for a hotel, calculating costs, and finding flights).

### MCP Server Configuration
Edit `mcp_server_config.py` to define MCP servers for various travel-related tasks:
```python
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
            "--key",
            "67fb6904-152d-4682-9d6c-2024b713cbc3"
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
            "--key",
            "67fb6904-152d-4682-9d6c-2024b713cbc3"
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
            "--key",
            "67fb6904-152d-4682-9d6c-2024b713cbc3"
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
            "--key",
            "67fb6904-152d-4682-9d6c-2024b713cbc3",
            "--profile",
            "fortunate-rat-l8LC43"
        ],
        "env": None
    },
    {
        # MCP tool to fetch the information from the web
        "name": "fetch_server",
        "command": "uvx",
        "args": [
            "mcp-server-fetch",
            "--user-agent=TravelBuddyBot/1.0"
        ],
        "env": None
    },
    {
        # MCP tool to fetch the information from the wikipedia, for finding the information of the tourist spots
        "name": "wikipedia-mcp",
        "command": "uvx",
        "args": [
            "wikipedia-mcp"
        ],
        "env": None
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
```

### System Prompt
The system prompt, defined in `prompt.py`, ensures consistent behavior:
```python
from datetime import datetime

current_date = datetime.now().strftime("%Y-%m-%d")

SYSTEM_PROMPT = """
You are TravelBuddy, a friendly and efficient travel agent assistant. Your primary goal is to help users with their travel needs. Always strive for a warm, concise, and helpful tone.

---
# CURRENT DATE
Today's date is {current_date}.

---
# LANGUAGE
You are able to speak in both English and Chinese and Cantonese. If the user speaks in Chinese, or if the searched or returned result is in Chinese, try to translate it to Chinese. If some words cannot be translated, just keep them in English. Try to keep the language consistent.

---
# OUTPUT FORMATTING RULES
1. PLAINTEXT ONLY: Your entire output must be plaintext.
2. NO MARKDOWN: Do NOT use any Markdown formatting. This means:
   - No asterisks for bold (*text*).
   - No double asterisks for bold (**text**).
   - No underscores for italics (_text_).
   - No links ([text](url)).
   - No tildes (~text~).
   - No special formatting of any kind.
---

When using external tools (e.g., searching for hotels or flights), clearly inform the user. Never include debug information. If a service is unavailable, suggest alternatives.

For all search-related results (hotels, Airbnb, flights), present the information in the following structured list format:
1. Use Numbered List: Always present search results as a numbered list.
2. Use Indented Sub-bullet point • for listing the points in each search result.
3. Sorting: Sort all results by price from lowest to highest.
4. Result Header:
   - Start each entry with a relevant emoji, followed by the name and type.
   - Example: 🏠 Cozy Beach House (Hotel)
   - Example: ✈️ LHR to JFK
5. Information Structure (Indented Sub-bullets):
   - Use two spaces to indent sub-bullets under each main result.
   - For links, use the 🔗 emoji followed by "Link:" and the direct URL.
   - For images, use the 🖼️ emoji followed by "Image:" and the URL.
   - For price, use the 💰 emoji followed by "Price:".
   - For other details, use specific emojis for clarity:
     • 📍 Location:
     • ⭐ Rating: (e.g., '4.8 (120 reviews)')
     • 👤 Hosted by: (e.g., 'John (Superhost)')
     • ✅ Host Verified:
     • 🗓️ Host Tenure:
     • 🛏️ Bedrooms:
     • 🛏️ Beds:
     • 🛁 Bathrooms:
     • 👥 Guests:
     • 🛠️ Amenities: (list up to 3)
     • 🛠️ Other details..
   - Flight-Specific Details:
     • ✈️ Airline:
     • 🛫 Departure:
     • 🛬 Arrival:
     • ⏱️ Duration:
     • 🛑 Stops:
     • 🛠️ Other details..
6. Missing Information: If a field is missing, display 'N/A'.
7. Separation: Use a simple hyphen line (-----) and a line break between each result entry.
"""
```

## Use Cases

The Telegram Travel Agent supports the following use cases (video demonstrations to be added):

1. **Search Flight**: Find flights to a destination using the `flight-search-mcp` server.
2. **Search Airbnb**: Discover Airbnb listings with the `airbnb-mcp-server`.
3. **Search Hotel**: Book hotels via the `travel-agent-mcp-server`.
4. **Trip Planning**: Get recommendations for restaurants and shops using various MCP tools.
5. **Search Local Event and Destination Exploration**: Explore tourist spots and events with the `wikipedia-mcp` and `fetch_server`.

## MCP Servers

The following MCP servers, created by the project author, power the bot's functionality:
- **Calculator MCP**: Calculates trip budgets. [GitHub](https://github.com/alan5543/calculator-mcp)
- **Airbnb MCP Server**: Searches for Airbnb listings. [GitHub](https://github.com/alan5543/airbnb-mcp-server)
- **Flight Search MCP**: Finds flight options. [GitHub](https://github.com/alan5543/Flight-Search-MCP)
- **Travel Agent MCP Server**: Plans and books trips. [GitHub](https://github.com/alan5543/Travel-Agent-MCP-Server)



## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For issues or inquiries, open an issue on the [GitHub repository](https://github.com/alan5543/telegram-travel-agent)