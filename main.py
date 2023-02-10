import asyncio

from parser.app import create_app

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        asyncio.run(create_app())
    except KeyboardInterrupt:
        exit()
