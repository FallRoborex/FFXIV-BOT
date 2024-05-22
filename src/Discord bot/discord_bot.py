import os
from discord import Intents, Client, Message
from dotenv import load_dotenv
from response import get_response

# Load the Token 
load_dotenv()
TOKEN = str(os.getenv("DISCORD_TOKEN"))


# Bot Setup
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)


# Message Functionality
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print("(Message was empty)")
        return

    is_private = user_message[0] == "?"
    if is_private:
        user_message = user_message[1:]

    try:
        response = str(get_response(user_message))
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


@client.event
async def on_ready() -> None:
    print(f"{client.user} is now running!")


@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    if message.content.startswith("%%") or message.content.startswith("?"):
        user_message = str(message.content)
        print(f"[{message.channel}] {message.author}: \"{user_message}\"")
        await send_message(message, user_message)


def main() -> None:
    client.run(token=TOKEN)


if __name__ == "__main__":
    main()
