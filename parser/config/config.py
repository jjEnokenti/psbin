import os

from dotenv import load_dotenv

load_dotenv()


class BaseConfig:

    API_KEY = os.environ.get('API_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY')

    URL = 'wss://stream.binance.com:9443/stream?streams=xrpusdt@miniTicker'


if __name__ == '__main__':
    print(BaseConfig.__dict__)
