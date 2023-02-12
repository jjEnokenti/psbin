import os

from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    API_KEY = os.environ.get('API_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    PARE = os.environ.get('PARE')
    URL = 'wss://fstream.binance.com/stream?streams=xrpusdt@kline_1h'
