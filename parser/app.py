from binance import BinanceSocketManager, AsyncClient

from parser.config.config import BaseConfig


def get_percent(current_price, current_max_price):
    # вычисление процента падения текущей цены к максимальной
    percent = (current_max_price - current_price) / current_price * 100  # noqa 501
    if percent >= 1:
        # если процент больше или равен 1 вернуть процент
        return percent

    return False


async def app(pare: str):
    """ Парсер биржи """

    # клиент
    client = await AsyncClient.create(
        api_key=BaseConfig.API_KEY,
        api_secret=BaseConfig.SECRET_KEY
    )
    bm = BinanceSocketManager(client)  # настройка подключения к веб-сокету бинанс
    await client.close_connection()  # закрытие соединение клиента
    ts = bm.kline_futures_socket(
        pare,
        interval='1h'
    )  # запрос на получения текущей свечи переданной пары (pare)

    cache = {}  # кэш для хранения значений текущей цены и максимальной цены за последний час
    async with ts as tscm:  # сессия с запросом к веб-сокету
        print('Processing...')
        while True:  # бесконечный цикл запросов
            res = await tscm.recv()  # актуальные данные свечи
            data = res['k']  # словарь с информацией цен

            current_price = float(data['c'])  # текущая цена
            current_max_price = float(data['h'])  # максимальная цена в данном часовом периоде
            if res['ps'] not in cache:  # если пары нет в кеше
                # создать ключи с именем пары и добавить значение текущей и максимальной цен в словарь
                cache.setdefault(res['ps'], {'current': float(data['c']), 'high': float(data['h'])})
                if current_price < current_max_price:  # если текущая цена меньше максимальной
                    # вычисление процента падения текущей цены к максимальной
                    percent = get_percent(current_price, current_max_price)
                    if percent:
                        # если процент больше или равен 1 вывести сообщение в консоль
                        print(f'Цена XRP к USDT упала на {round(percent, 4)}%')
            else:  # если пара есть в кеше
                # сравнить значения текущей цены и текущей цены сохраненной в кеше
                # и аналогично для максимальной
                #  если есть между ними разница
                if current_price != cache[res['ps']]['current'] and current_max_price != cache[res['ps']]['high']:
                    if current_price < cache[res['ps']]['current']:  # если текущая цена меньше текущей в кеше
                        if current_price < current_max_price:  # если текущая цена меньше максимальной
                            # вычисление процента падения текущей цены к максимальной
                            percent = get_percent(current_price, current_max_price)
                            if percent:
                                # если процент больше или равен 1 вывести сообщение в консоль
                                print(f'Цена XRP к USDT упала на {round(percent, 4)}%')
                    # обновить значения в кеше
                    cache[res['ps']]['current'] = current_price
                    cache[res['ps']]['high'] = current_max_price
