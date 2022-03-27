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
    
    @tasks.loop(seconds=int(os.getenv('INTERVAL') or 15))
    async def fetch_price(self):
        await self.wait_until_ready()

        r = requests.get(f"http://quotation-api.dunamu.com/v1/recent/securities?shortCodes={self.short_code}")
        try:
            data = r.json()[0]

            stock_name = data['name']
            display_name = f"{stock_name}"
            trade_price = data['tradePrice']
            price_detail = f"({round(data['signedChangeRate'] * 100, 2)}%)"

            if self.user.display_name != display_name:
                await self.user.edit(username=display_name)

            if self.last_price != trade_price:
                await self.change_presence(activity=disnake.Game(name=f"💰 {trade_price:,} {price_detail}"))
                self.last_price = trade_price

        except Exception as e:
            print(e)
            pass

scheduler = Scheduler()
scheduler.run(os.environ.get('DISCORD_BOT_TOKEN'))
