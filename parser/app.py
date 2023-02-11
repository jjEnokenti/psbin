import json

import websockets

from parser.config.config import BaseConfig


async def app():
    """ Парсер биржи """

    # url для подключения к бирже
    url = BaseConfig.URL

    async with websockets.connect(url) as connect:
        print('Processing...')
        while True:

            data = json.loads(await connect.recv())['data']['k']  # данные свечи

            current_price = float(data['c'])  # текущая цена xrp
            current_max_price = float(data['h'])  # максимальная цена в данном часовом периоде

            if current_price < current_max_price:  # если текущая цена меньше максимальной
                # вычисление процента падения текущей цены к максимальной
                percent = (current_max_price - current_price) / current_price * 100  # noqa 501
                if percent >= 1:
                    # если процент больше или равен 1 вывести сообщение в консоль
                    print(f'Цена XRP к USDT упала на {round(percent, 4)}%')
