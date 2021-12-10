import disnake
from disnake.ext import tasks

import os
import requests

class Scheduler(disnake.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_price = None
        self.interval = os.getenv('INTERVAL') or 15
        self.short_code = os.getenv('SHORT_CODE')

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print(f"SHORT_CODE: {self.short_code}")
        print(f"INTERVAL: {self.interval}")
        print("------")

    async def on_connect(self):
        self.fetch_price.start()
    
    @tasks.loop(seconds=3)
    async def fetch_price(self):
        await self.wait_until_ready()

        r = requests.get(f"http://quotation-api.dunamu.com/v1/recent/securities?shortCodes={self.short_code}")
        try:
            data = r.json()[0]
            if self.user.display_name != data['name']:
                await self.user.edit(username=data['name'])

            if self.last_price != data['tradePrice']:
                activity = disnake.Game(name=data['tradePrice'])
                await self.change_presence(activity=activity)
                self.last_price = data['tradePrice']

        except Exception as e:
            print(e)
            pass

scheduler = Scheduler()
scheduler.run(os.environ.get('DISCORD_BOT_TOKEN'))
