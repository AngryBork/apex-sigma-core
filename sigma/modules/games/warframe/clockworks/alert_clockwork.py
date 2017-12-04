import asyncio

from sigma.modules.games.warframe.commons.cycles.generic import send_to_channels
from sigma.modules.games.warframe.commons.parsers.alert_parser import get_alert_data, generate_alert_embed


async def alert_clockwork(ev):
    ev.bot.loop.create_task(cycler(ev))


async def cycler(ev):
    while True:
        try:
            alerts, triggers = await get_alert_data(ev.db)
            if alerts:
                response = await generate_alert_embed(alerts)
                await send_to_channels(ev, response, 'WarframeAlertChannel', triggers)
        except Exception as err:
            pass
        await asyncio.sleep(2)
