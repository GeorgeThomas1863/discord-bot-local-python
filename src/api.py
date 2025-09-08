"""
API module for communicating with the local LLM.
Replaces the OpenAI API calls with local LLM requests.
"""

import aiohttp
from ..config.config import LLM_ENDPOINT, SYSTEM_PROMPT


async def send_to_llm(input_array):

    # Prepare the request payload (OpenAI-compatible format)
    payload = {
        "messages": input_array,
        "temperature": 0.7,  # Adjust for more/less creative responses
        "max_tokens": 1000,  # Maximum response length
        "stream": False,  # Get complete response at once
    }

    try:
        # Create an async HTTP session
        async with aiohttp.ClientSession() as session:
            # Send POST request to local LLM
            async with session.post(
                LLM_ENDPOINT, json=payload, headers={"Content-Type": "application/json"}
            ) as response:

                # Check if request was successful
                if response.status == 200:
                    # Parse JSON response
                    data = await response.json()

                    # Extract the message content (OpenAI format)
                    # The response structure should be similar to OpenAI's
                    ai_message = data["choices"][0]["message"]["content"]

                    print(f"LLM Response received: {len(ai_message)} characters")
                    return ai_message
                else:
                    # Handle error responses
                    error_text = await response.text()
                    print(f"LLM Error {response.status}: {error_text}")
                    return f"Error: LLM returned status {response.status}"

    except aiohttp.ClientError as e:
        # Handle connection errors
        print(f"Connection error to local LLM: {e}")
        return "The connection is fucked, double check the LLM is running and try again"
    except Exception as e:
        # Handle any other errors
        print(f"Unexpected error: {e}")
        return "Something went wrong, no idea what the problem is, please make George fix it."


def define_system_prompt():

    return [{"role": "system", "content": SYSTEM_PROMPT}]
