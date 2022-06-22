import asyncio

async def main():
    print('Hello ...')
    await asyncio.sleep(1)
    print('... World!')

asyncio.get_event_loop().run_until_complete(main())

#It could not be:
#main()