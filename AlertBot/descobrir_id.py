import asyncio
from telethon import TelegramClient

api_id = 32214311  # coloque seu API ID
api_hash = "8ea019885c2814bdd30e186180499e01"

async def main():
    async with TelegramClient("alertbot", api_id, api_hash) as client:
        result = await client.get_entity("https://t.me/+IBzrC3cDJmczZjAx")
        print("ID do canal:", result.id)

# cria loop manualmente — necessário no Python 3.14
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(main())