import decimal
import json

import websockets

from parser.config.config import BaseConfig


async def create_app():
    url = BaseConfig.URL

    async with websockets.connect(url) as connect:
        max_value_per_hour = decimal.Decimal(
            json.loads(
                await connect.recv()
            )['data']['c']
        )

        while True:
            data = json.loads(await connect.recv())['data']
            current_value = decimal.Decimal(data['c'])

            if current_value > max_value_per_hour:
                max_value_per_hour = current_value
            elif current_value < max_value_per_hour:
                percent = (max_value_per_hour - current_value) / current_value * 100
                if percent >= 1:
                    print(f'Цена XRP к USDT упала на {round(percent, 5)}%')
