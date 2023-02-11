import asyncio

from parser.app import app

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        asyncio.run(app())
    except KeyboardInterrupt:
        exit()
