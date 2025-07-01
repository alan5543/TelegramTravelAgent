# main.py
import asyncio
import sys
import os

from fastapi import FastAPI, Request, HTTPException # New imports
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from config import TELEGRAM_BOT_TOKEN, logger # Ensure logger is imported
from mcp_server_config import mcp_server_configs # Make sure this file exists and contains configs
from mcp_client import MCPClient
from gemini_client import GeminiChatClient
from telegram_bot import (
    start_command,
    new_chat_command,
    help_command,
    handle_message,
    error_handler,
)

# --- FastAPI Application Setup ---
app = FastAPI()

# Initialize clients and Telegram Application globally or on startup
# This ensures they are ready before any webhook calls come in
mcp_client = MCPClient()
chat_client = GeminiChatClient()
telegram_application = None # Initialize as None, set in startup

@app.on_event("startup")
async def startup_event():
    """
    Runs when the FastAPI application starts.
    Initializes MCP client and Telegram bot application.
    """
    global telegram_application # Use global to modify the outer variable

    logger.info("Application starting up...")

    try:
        # Connect to MCP servers
        logger.info("Connecting to MCP servers...")
        # Make sure mcp_server_configs is correctly defined in mcp_server_config.py
        await mcp_client.connect(mcp_server_configs)
        logger.info("MCP Client connected.")

        # Build the Telegram application
        telegram_application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

        # Store clients in bot_data for access in handlers
        telegram_application.bot_data["mcp_client"] = mcp_client
        telegram_application.bot_data["chat_client"] = chat_client

        # Register handlers
        telegram_application.add_handler(CommandHandler("start", start_command))
        telegram_application.add_handler(CommandHandler("new", new_chat_command))
        telegram_application.add_handler(CommandHandler("help", help_command))
        telegram_application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        telegram_application.add_error_handler(error_handler)

        # Initialize the Telegram Application (important for webhooks)
        await telegram_application.initialize()

        logger.info("Telegram Bot Application initialized for webhooks!")

    except Exception as e:
        logger.critical("A critical error occurred during startup: %s", e, exc_info=True)
        # Depending on your deployment, you might want to exit or raise here
        raise # Re-raise to prevent server from starting if critical error

@app.on_event("shutdown")
async def shutdown_event():
    """
    Runs when the FastAPI application is shutting down.
    Performs graceful cleanup.
    """
    logger.info("Application shutting down...")
    if telegram_application:
        await telegram_application.shutdown() # Properly shut down the PTB application
        logger.info("Telegram Application shut down.")
    await mcp_client.cleanup()
    logger.info("MCP Client cleaned up.")

@app.post(f"/webhook/{TELEGRAM_BOT_TOKEN}") # Use the bot token in the path for security
async def telegram_webhook(request: Request):
    """
    Endpoint to receive Telegram webhook updates.
    """
    if not telegram_application:
        logger.error("Telegram Application not initialized when webhook received.")
        raise HTTPException(status_code=503, detail="Service Unavailable: Bot not initialized.")

    try:
        # Get the JSON payload from the request
        update_json = await request.json()
        # Create a Telegram Update object from the JSON
        update = Update.de_json(update_json, telegram_application.bot)

        # Process the update using the PTB application
        await telegram_application.process_update(update)

        return {"status": "ok"} # Telegram expects a 200 OK response
    except Exception as e:
        logger.error(f"Error processing webhook update: {e}", exc_info=True)
        # Return 500 status code for internal errors
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/")
async def read_root():
    """
    A simple health check endpoint.
    """
    return {"message": "Telegram Bot Webhook is running."}

# --- This block is for local development using `python main.py` ---
# When deployed with Uvicorn, this __name__ == "__main__" block won't execute.
# Uvicorn directly imports `app` from this file.
if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Uvicorn server for local testing...")
    # Use a port like 8000 or 7860 (Hugging Face default)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    # reload=True is useful for local development, automatically restarts server on code changes