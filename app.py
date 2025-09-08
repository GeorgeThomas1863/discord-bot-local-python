from discord import Client, Intents, LoginFailure
from config.bot import DISCORD_TOKEN
from config.config import PREFIX
from src.discord_msg import handle_message
import traceback


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

    print(f"{client.user} has connected to Discord!")
    print(f"Bot is ready to receive messages.")
    print(f"Prefix: {PREFIX}")


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

    traceback.print_exc()


def main():
    """
    Main function to start the bot.
    """
    if not DISCORD_TOKEN:
        print("ERROR: DISCORD_TOKEN NOT FOUND")
        return

    print("Starting Discord bot...")

    try:
        # Start the bot (this blocks until the bot shuts down)
        client.run(DISCORD_TOKEN)
    except LoginFailure:
        print("ERROR: Invalid Discord token!")
    except Exception as e:
        print(f"ERROR: Failed to start bot: {e}")


if __name__ == "__main__":
    # Run the bot when this file is executed directly
    main()
