import asyncio

from kasa import SmartPlug

plug_host = '192.168.0.104'

plug = SmartPlug(plug_host)


async def run():
    while True:
        await plug.update()
        if plug.is_off:
            await plug.turn_on()
        else:
            await plug.turn_off()
        await asyncio.sleep(1)


asyncio.run(run())
