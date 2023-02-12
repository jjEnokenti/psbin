import asyncio

from parser.app import app
from parser.config.config import BaseConfig

pare = BaseConfig.PARE

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        asyncio.run(app(pare=pare))
    except KeyboardInterrupt:
        exit()
