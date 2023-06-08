import aiohttp
from decimal import Decimal
from discord import Client, Intents, HTTPException
from discord import Activity, ActivityType
import asyncio
import datetime

TOKEN_SYMBOL = "ADA"
watching = "cardano"

intents = Intents(guilds=True)
client = Client(intents=intents)


async def fetchPrice():
    url = f"https://api.coingecko.com/api/v3/coins/{watching}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_json = await response.json()
            adausd = response_json["market_data"]["current_price"]["usd"]
            return Decimal(str(adausd)).quantize(Decimal("0.000"))


async def updateBot(client: Client, symbol: str):
    while True:
        for guild in client.guilds:
            member = guild.get_member(client.user.id)
            try:
                price = await fetchPrice()
                print(f"Price for {guild.name}: {price}, {guild.id}")
                await member.edit(nick=f"{symbol}: ${price} USD")
                print(f"Nickname updated for {guild.name}")
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            except HTTPException as e:
                print(f"Error updating nickname for {guild.name}: {str(e)}")
        await asyncio.sleep(600)


@client.event
async def on_ready():
    print("ready yay!")
    await updateBot(client=client, symbol=TOKEN_SYMBOL)
    await client.change_presence(
        activity=Activity(name="Cardano", type=ActivityType.watching)
    )
    client.loop.create_task(updateBot(client, TOKEN_SYMBOL))

token= "discord token"

client.run(token)
