import discord
import asyncio
import aiohttp
import datetime

from http import HTTPStatus

class Session:
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def exists(self, site):
        try:
            async with self.session.get(site) as res:
                return res.status
        except aiohttp.errors.ClientOSError:
            return 404

async def main(client):
    session = Session()

    @client.event
    async def on_ready():
        print('------')
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

    @client.event
    async def on_message(message):
        if message.content.startswith('+ping'):
            site = message.content.split(' ')[1]  # Assume url is second
            status = await session.exists(site)

            if status == HTTPStatus.OK:
                embed = discord.Embed(
                    title="Website Status",
                    description=":white_check_mark:",
                    color=0x35EE1F
                )
                embed.set_author(
                    name=message.author.name,
                    icon_url=message.author.avatar_url)
                embed.set_footer(
                    text='Website Pinger | Powered by @AnotherCop', 
                    icon_url='https://pbs.twimg.com/profile_images/1068858813263024128/X1vXvUbT_400x400.jpg')
                embed.timestamp = datetime.datetime.utcnow()
                
                await client.send_message(message.channel, embed=embed)
            else:
                embed = discord.Embed(
                    title="Website Status",
                    description=":x:",
                    color=0xF52C2C
                )
                embed.set_author(
                    name=message.author.name,
                    icon_url=message.author.avatar_url)
                embed.set_footer(
                    text='Website Pinger Bot | Powered by: @AnotherCop', 
                    icon_url='https://pbs.twimg.com/profile_images/1068858813263024128/X1vXvUbT_400x400.jpg')
                embed.timestamp = datetime.datetime.utcnow()
                
                await client.send_message(message.channel, embed=embed)
                
    await client.start('NTM4NDM0MjI5ODc3MzQyMjYx.DyzvpQ.TTOy5jIdYpXIBdKNTTEdF0GQG2s')

def init():
    client = discord.Client()
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main(client))
    except KeyboardInterrupt:
        loop.run_until_complete(client.close())
    finally:
        if not client.is_closed:
            loop.run_until_complete(client.close())
        loop.close()

init()
