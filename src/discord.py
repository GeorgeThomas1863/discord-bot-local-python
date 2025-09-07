"""
Discord message handling module.
Processes incoming messages and generates responses.
"""

import discord
import asyncio
from config import ALLOWED_CHANNELS, PREFIX, CHUNK_SIZE_LIMIT
from api import send_to_llm, define_system_prompt
from utils import fix_username, typing_loop


async def handle_message(message, client):
    """
    Process incoming Discord messages and generate responses.
    
    Args:
        message: Discord message object
        client: Discord client instance
    """
    
    # Early returns for filtering messages we don't want to process
    
    # Ignore messages from bots (including ourselves)
    if message.author.bot:
        return
    
    # Check if message is in an allowed channel
    if message.channel.id not in ALLOWED_CHANNELS:
        return
    
    # Check if message starts with prefix or mentions the bot
    first_char = message.content.strip()[:1] if message.content.strip() else ''
    bot_mentioned = client.user in message.mentions
    
    # If neither condition is met, ignore the message
    if first_char != PREFIX and not bot_mentioned:
        return
    
    print(f"Processing message from {message.author}: {message.content[:50]}...")
    
    # Start typing indicator (shows "Bot is typing..." in Discord)
    typing_task = asyncio.create_task(typing_loop(message.channel))
    
    try:
        # Build conversation array from channel history
        convo_array = await build_convo_array(message.channel, client)
        
        print(f"Sending {len(convo_array)} messages to LLM...")
        
        # Get response from local LLM
        ai_message = await send_to_llm(convo_array)
        
        # Send the response back to Discord
        await send_discord_message(ai_message, message)
        
    except Exception as error:
        print(f"Error handling message: {error}")
        await message.reply("Sorry, I encountered an error processing your request.")
    
    finally:
        # Stop the typing indicator
        typing_task.cancel()
        try:
            await typing_task
        except asyncio.CancelledError:
            pass


async def build_convo_array(channel, client):
    """
    Build an array of recent messages from the channel for context.
    
    Args:
        channel: Discord channel to fetch messages from
        client: Discord client instance
    
    Returns:
        list: Array of message dictionaries for the LLM
    """
    
    # Start with system prompt
    convo_array = define_system_prompt()
    
    # Fetch last 10 messages from the channel
    messages = []
    async for msg in channel.history(limit=10):
        messages.append(msg)
    
    # Reverse to get chronological order (oldest first)
    messages.reverse()
    
    # Process each message
    for msg in messages:
        # Skip messages that don't start with prefix (unless from bot)
        if msg.author.id != client.user.id and not msg.content.startswith(PREFIX):
            continue
        
        # Clean username for API
        username = fix_username(msg.author.name)
        
        # Determine role (assistant for bot, user for humans)
        role = "assistant" if msg.author.id == client.user.id else "user"
        
        # Create message object
        convo_obj = {
            "role": role,
            "name": username,  # Optional: include username for context
            "content": msg.content
        }
        
        convo_array.append(convo_obj)
    
    print(f"Built conversation with {len(convo_array)} messages")
    return convo_array


async def send_discord_message(ai_message, original_message):
    """
    Send the AI response back to Discord, splitting if necessary.
    Discord has a 2000 character limit per message.
    
    Args:
        ai_message (str): The response from the LLM
        original_message: The Discord message to reply to
    """
    
    # If message is short enough, send it directly
    if len(ai_message) <= CHUNK_SIZE_LIMIT:
        await original_message.reply(ai_message)
        return
    
    # Split long messages into chunks
    chunks = []
    for i in range(0, len(ai_message), CHUNK_SIZE_LIMIT):
        chunk = ai_message[i:i + CHUNK_SIZE_LIMIT]
        chunks.append(chunk)
    
    # Send each chunk as a reply
    for i, chunk in enumerate(chunks):
        if i == 0:
            # First chunk as a reply
            await original_message.reply(chunk)
        else:
            # Subsequent chunks as regular messages in the same channel
            await original_message.channel.send(chunk)