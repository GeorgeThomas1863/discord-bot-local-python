import asyncio
import re


def fix_username(username):

    # Replace spaces with underscores
    username = username.replace(" ", "_")

    # Remove all non-alphanumeric characters except underscores
    username = re.sub(r"[^\w]", "", username)

    return username


async def typing_loop(channel):

    try:
        while True:
            # Send typing indicator
            await channel.typing()

            # Wait 10 seconds before sending again
            # Discord typing indicators last about 10 seconds
            await asyncio.sleep(10)
    except asyncio.CancelledError:
        # Task was cancelled, stop the loop gracefully
        pass
