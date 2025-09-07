"""
Utility functions for the Discord bot.
Helper functions for username formatting and typing indicators.
"""

import asyncio
import re


def fix_username(username):
    """
    Clean up Discord username for use in API calls.
    Removes spaces and special characters.
    
    Args:
        username (str): Raw Discord username
    
    Returns:
        str: Cleaned username with only alphanumeric characters and underscores
    """
    # Replace spaces with underscores
    username = username.replace(' ', '_')
    
    # Remove all non-alphanumeric characters except underscores
    username = re.sub(r'[^\w]', '', username)
    
    return username


async def typing_loop(channel):
    """
    Continuously send typing indicators to show the bot is processing.
    This runs as a background task until cancelled.
    
    Args:
        channel: Discord channel object to send typing indicators to
    """
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