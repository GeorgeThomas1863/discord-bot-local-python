"""
Main entry point for the Discord bot.
Equivalent to app.js in the JavaScript version.
"""

from discord import Client, Intents
from discord.ext import commands
import asyncio
from config.bot import DISCORD_TOKEN
from config.config import PREFIX
from discord_msg import handle_message


# Create the bot client
client = Client(
    intents=Intents(
        guilds=True,  # Allows accessing guild (server) info
        members=True,  # Allows accessing member info
        messages=True,
        message_content=True,  # Allows reading message content
    )
)


@client.event
async def on_ready():
    """
    Event handler for when the bot successfully connects to Discord.
    This runs once when the bot starts up.
    """
    print(f"{client.user} has connected to Discord!")
    print(f"Bot is ready to receive messages.")
    print(f"Prefix: {PREFIX}")

    # Optional: Set bot status
    await client.change_presence(activity=discord.Game(name=f"Chatting with {PREFIX}"))


@client.event
async def on_message(message):
    """
    Event handler for new messages.
    This runs every time a message is sent in any channel the bot can see.

    Args:
        message: Discord message object containing all message data
    """
    # Pass the message to our handler
    await handle_message(message, client)


@client.event
async def on_error(event, *args, **kwargs):
    """
    Global error handler for the bot.
    Logs any errors that occur during event processing.
    """
    print(f"Error in {event}:")
    import traceback

    traceback.print_exc()


def main():
    """
    Main function to start the bot.
    """
    if not DISCORD_TOKEN:
        print("ERROR: DISCORD_TOKEN not found in environment variables!")
        print("Please add your bot token to the .env file")
        return

    print("Starting Discord bot...")

    try:
        # Start the bot (this blocks until the bot shuts down)
        client.run(DISCORD_TOKEN)
    except discord.LoginFailure:
        print("ERROR: Invalid Discord token!")
    except Exception as e:
        print(f"ERROR: Failed to start bot: {e}")


if __name__ == "__main__":
    # Run the bot when this file is executed directly
    main()
